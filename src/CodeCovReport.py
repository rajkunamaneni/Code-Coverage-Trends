import json
import requests
import urllib
import urllib.request, json
import pandas as pd
import sys
import os
import time

from collections import defaultdict
from GrabReleaseCommits import retrieve_commit_hashes
from StarHistory import get_star_data
from GetRepoFromDataset import filter_github_repos

# Helper class for turning print output off temporarily.
DEBUG = False
DEBUG_IMPORT_FUNC = False

class disablePrintOutput:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

# Helper functions for codecov printing of each commit info and their resulting code coverage
def __get_codecov_commit_list(content, username, repo_name, language):
    commit = None
    commit_list = []
    for commit in content['results']:
        totals = commit['totals']

        if totals is None:
            continue

        coverage = totals.get('coverage', None)

        if coverage is not None:
            commit_list.append([username, repo_name, coverage, commit['commitid'], commit['timestamp'], language])
        else:
            print(f"codecov not used: {username}/{repo_name}/{language}, {commit['commitid']}, {commit['timestamp']}")

    return commit_list

def __get_codecov_commit_from_sha(content, sha_value, username, repo_name, language):
    commit = None

    for commit in content['results']:
        totals = commit['totals']

        if totals is None:
            continue

        coverage = totals.get('coverage', None)

        if coverage is not None and commit['commitid'] == sha_value:
            return [username, repo_name, coverage, commit['commitid'], commit['timestamp'], language]
        elif coverage is None:
            print(f"codecov not used: {username}/{repo_name}/{language}, {commit['commitid']}, {commit['timestamp']}")
            return False
        else:
            continue

    return False

def get_codecov_first_page(platform, username, repo_name, token_name, language):
    if token_name is None or token_name == "" or token_name == " ":
        print("invalid token: {}".format(token_name))
        return False

    codecov_endpoint = "https://codecov.io/api/v2/{}/{}"

    codecov_headers = {
        'Authorization': 'bearer {}'.format(token_name)
    }
    endpoint = codecov_endpoint.format(platform, username)
    endpoint = endpoint + "/repos/" + repo_name + "/commits"
    response = requests.get(
        endpoint,
        headers=codecov_headers,
    )

    if response.status_code == 200:
        content = json.loads(response.content)
        final_list = []

        if content['count'] == 0:
            print("Repo did implement codecov but did not use it to generate code coverage reports.")
            return False

        codecov_commit_list = __get_codecov_commit_list(content, username, repo_name, language)
        for commit in codecov_commit_list:
            final_list.append(commit)
    else:
        print("codecov returned with error status:".format(response.status_code))
        return False

    return final_list

def get_codecov_total_pages(platform, username, repo_name, token_name):
    if token_name is None or token_name == "" or token_name == " ":
        print("invalid token: {}".format(token_name))
        return False

    #https://api.codecov.io/api/v2/{service}/{owner_username}/repos/{repo_name}/commits/
    codecov_endpoint = "https://api.codecov.io/api/v2/{}/{}/repos/{}/commits/"

    codecov_headers = {
        'Authorization': 'bearer {}'.format(token_name)
    }
    endpoint = codecov_endpoint.format(platform, username, repo_name)
    response = requests.get(
        endpoint,
        headers=codecov_headers,
    )

    if response.status_code == 200:
        content = json.loads(response.text)
        return content['total_pages']
    else:
        print("codecov returned with error status:".format(response.status_code))
        return False

def get_codecov_all_builds(platform, username, repo_name, token_name, language):
    if token_name is None or token_name == "" or token_name == " ":
        print("invalid token: {}".format(token_name))
        return False

    #https://api.codecov.io/api/v2/{service}/{owner_username}/repos/{repo_name}/commits/
    codecov_endpoint = "https://api.codecov.io/api/v2/{}/{}/repos/{}/commits/"

    codecov_headers = {
        'Authorization': 'bearer {}'.format(token_name)
    }
    endpoint = codecov_endpoint.format(platform, username, repo_name)
    response = requests.get(
        endpoint,
        headers=codecov_headers,
        timeout=30
    )

    if response.status_code == 200:
        content = response.json()
    else:
        print("Failed to fetch data from codecov endpoint.")
        return None
    codecov_commit_list = []

    if response.status_code == 200:
        commit = None
        page_num = 0

        if content['count'] == 0:
            print("Repo did implement codecov but did not use it to generate code coverage reports.")
            return False

        while page_num < content['total_pages']:
            if page_num == 167:
                break
            codecov_commit_list.append(__get_codecov_commit_list(content, username, repo_name, language))
            if DEBUG: print(page_num)
            codecov_endpoint = "https://api.codecov.io/api/v2/{}/{}/repos/{}/commits/?page={}"
            page_num+=1
            endpoint = codecov_endpoint.format(platform, username, repo_name, page_num)
            response = requests.get(
                endpoint,
                headers=codecov_headers,
                timeout=250
            )

            if response.status_code == 200:
                content = response.json()
            else:
                print("Failed to fetch data from codecov endpoint.")
                return None
        final_list = []
        for commit in codecov_commit_list:
            for detail_commit in commit:
                final_list.append(detail_commit)
    else:
        print("codecov returned with error status:".format(response.status_code))
        return False

    return final_list

def get_codecov_build(platform, username, repo_name, token_name, sha_value, language):
    if token_name is None or token_name == "" or token_name == " ":
        print("invalid token: {}".format(token_name))
        return False

    #https://api.codecov.io/api/v2/{service}/{owner_username}/repos/{repo_name}/commits/
    codecov_endpoint = "https://api.codecov.io/api/v2/{}/{}/repos/{}/commits/"

    codecov_headers = {
        'Authorization': 'bearer {}'.format(token_name)
    }
    endpoint = codecov_endpoint.format(platform, username, repo_name)

    response = requests.get(
        endpoint,
        headers=codecov_headers,
    )

    if response.status_code == 200:
        content = json.loads(response.text)
        if commit_build := __get_codecov_commit_from_sha(content, sha_value, username, repo_name, language):
            return commit_build

        commit = None
        if content['count'] == 0:
            print("Repo did implement codecov but did not use it to generate code coverage reports.")
            return False

        next_page_url = content['next']

        while next_page_url is not None:
            if commit_build := __get_codecov_commit_from_sha(content, sha_value, username, repo_name, language):
                return commit_build

            response = requests.get(
                next_page_url,
                headers=codecov_headers,
            )

            if response.status_code == 200:
                content = json.loads(response.text)
                next_page_url = content['next']
            else:
                print("error with pagination:".format(response.status_code))
                return False

        if commit_build := __get_codecov_commit_from_sha(content, sha_value, username, repo_name, language):
            return commit_build
        else:
            error_msg = "codecov, repo from sha value: {} not found"
            print(error_msg.format(sha_value))
            return False

    else:
        print("codecov returned with error status:".format(response.status_code))
        return False

def get_coverall_oldest_build(platform, username, repo_name, language):
    coverall_endpoint = "https://coveralls.io/{}/{}/{}.json"
    coverall_endpoint = coverall_endpoint.format(platform, username, repo_name)

    try:
        with urllib.request.urlopen(coverall_endpoint) as url:
            data = json.load(url)

            if data is not None and data['covered_percent'] is not None:
                return [username, repo_name, data['covered_percent'], data['commit_sha'], data['created_at'], language]
            else:
                return False

    except urllib.error.HTTPError as e:
        print(f"coverall not used: {platform}/{username}/{repo_name}: {e}")
        return False

def get_coverall_ten_builds(platform, username, repo_name, language):
    page_num = 1
    coverall_endpoint = "https://coveralls.io/{}/{}/{}.json?page={}"
    coverall_endpoint = coverall_endpoint.format(platform, username, repo_name, page_num)
    report_info = []

    try:
        with urllib.request.urlopen(coverall_endpoint) as url:
            data = json.load(url)

            if data is not None:
                data_builds = data['builds']

                for build in data_builds:
                    if build['covered_percent'] is not None:
                        report_info.append([username, repo_name, build['covered_percent'], build['commit_sha'],
                                            build['created_at'], language])
                return report_info
            else:
                return False

    except urllib.error.HTTPError as e:
        print(f"coverall not used: {platform}/{username}/{repo_name}: {e}")
        return False

def get_coverall_build(platform, username, repo_name, sha_value, language):
    page_num = 1
    coverall_endpoint_first_page = "https://coveralls.io/{}/{}/{}.json?page={}"
    coverall_endpoint_first_page = coverall_endpoint_first_page.format(platform, username, repo_name, page_num)

    try:
        with urllib.request.urlopen(coverall_endpoint_first_page) as first_page_url:
            data = json.load(first_page_url)

            if data is not None:
                page_size = data['pages']

                while page_num <= page_size:
                    coverall_endpoint_pages = "https://coveralls.io/github/{}/{}.json?page={}"
                    coverall_endpoint_pages = coverall_endpoint_pages.format(username, repo_name, page_num)

                    with urllib.request.urlopen(coverall_endpoint_pages) as pages_url:
                        data_pages = json.load(pages_url)
                        data_builds = data_pages['builds']

                        for build in data_builds:
                            if DEBUG: print(f"{build['commit_sha']} == {sha_value}")

                            if build['covered_percent'] is not None and build['commit_sha'] == sha_value:
                                return [username, repo_name, build['covered_percent'],
                                        build['commit_sha'], build['created_at'], language]
                    page_num += 1

                error_msg = "coverall, repo from sha value: {} not found"
                print(error_msg.format(sha_value))
                return False
            else:
                return False

    except urllib.error.HTTPError as e:
        print(f"coverall not used: {platform}/{username}/{repo_name}: {e}")
        return False


def get_coverall_all_builds(platform, username, repo_name, language):
    page_num = 1
    coverall_endpoint_first_page = "https://coveralls.io/{}/{}/{}.json?page={}"
    coverall_endpoint_first_page = coverall_endpoint_first_page.format(platform, username, repo_name, page_num)
    report_info = []
    try:
        with urllib.request.urlopen(coverall_endpoint_first_page) as first_page_url:
            data = json.load(first_page_url)

            if data is not None:
                page_size = data['pages']

                while page_num <= page_size:
                    coverall_endpoint_pages = "https://coveralls.io/github/{}/{}.json?page={}"
                    coverall_endpoint_pages = coverall_endpoint_pages.format(username, repo_name, page_num)

                    if DEBUG: print(coverall_endpoint_pages)

                    with urllib.request.urlopen(coverall_endpoint_pages) as pages_url:
                        data_pages = json.load(pages_url)
                        data_builds = data_pages['builds']
                        #[username, repo_name, coverage, commit['commitid'], commit['timestamp']]
                        for build in data_builds:
                            if build['covered_percent'] is not None:
                                report_info.append([username, repo_name, build['covered_percent'],
                                                    build['commit_sha'], build['created_at'], language])

                                if DEBUG:
                                    print(f"coverall, {platform}/{username}/{repo_name}, {build['covered_percent']}%")
                                    print(f"commit_sha: {build['commit_sha']}, created_at: {build['created_at']}")
                    page_num += 1
                return report_info

    except urllib.error.HTTPError as e:
        print(f"coverall not used: {platform}/{username}/{repo_name}: {e}")
        return False

def detect_coverage_tool_usage(platform, username, repo_name, codecov_API_token, language):
    with disablePrintOutput():
        codecov_used = bool(get_codecov_first_page(platform, username, repo_name, codecov_API_token, language))
        coverall_used = bool(get_coverall_oldest_build(platform, username, repo_name, language))

    if codecov_used or coverall_used:
        return [platform, username, repo_name, codecov_used, coverall_used, language]
    else:
        return None

if __name__=="__main__":
    if DEBUG_IMPORT_FUNC:
        print(retrieve_commit_hashes('expressjs', 'express'))
        print(get_star_data('expressjs', 'express', ["06-03-2015", "16-01-2024", "15-02-2024", "17-02-2024"]))
        print(filter_github_repos('../data/github-ranking-2024-02-15.csv'))

    try:
        codecov_API_token = sys.argv[1]
        platform = sys.argv[2]
        username = sys.argv[3]
        repo_name = sys.argv[4]
        sha_value = sys.argv[5]
        function_option = sys.argv[6]
        language = sys.argv[7]

        if function_option == "1":
            get_codecov_first_page(platform, username, repo_name, codecov_API_token, language)
        elif function_option == "2":
            get_codecov_all_builds(platform, username, repo_name, codecov_API_token, language)
        elif function_option == "3":
            get_codecov_build(platform, username, repo_name, codecov_API_token, sha_value, language)
        elif function_option == "4":
            get_coverall_oldest_build(platform, username, repo_name, language)
        elif function_option == "5":
            get_coverall_ten_builds(platform, username, repo_name, language)
        elif function_option == "6":
            get_coverall_all_builds(platform, username, repo_name, language)
        elif function_option == "7":
            get_coverall_build(platform, username, repo_name, sha_value, language)
        elif function_option == "8":
            detect_coverage_tool_usage(platform, username, repo_name, codecov_API_token, language)
        elif function_option == "9":
            get_codecov_total_pages(platform, username, repo_name, codecov_API_token)
        else:
            print(f"Invalid option: {repr(function_option)}")

    except IndexError:
        print("{} codecov_API_token platform username repo_name sha_value function_option".format(sys.argv[0]))
        print("Usage example: CodeCovReport.py 12345678-90ab-cdef-1234-567890abcdef github rajkunamaneni "
              "Code-Coverage-Trends bc5eef62d759fbfc8c2b55da75b4740703856c7c 6")

        sys.exit(1)