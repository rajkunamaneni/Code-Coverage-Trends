import json
import requests
import urllib
import urllib.request, json
import pandas as pd
import sys
import os

from collections import defaultdict
from GrabReleaseCommits import retrieve_commit_hashes
from StarHistory import get_star_data
from GetRepoFromDataset import filter_github_repos

# Helper class for turning print output off temporarily.
class disablePrintOutput:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

# Helper functions for codecov printing of each commit info and their resulting code coverage
def __print_codecov_commits(content, username, repo_name):
    commit = None

    for commit in content['results']:
        totals = commit['totals']

        if totals is None:
            continue

        coverage = totals.get('coverage', None)

        if coverage is not None:
            print(f"codecov, {username}/{repo_name}, {coverage}%, {commit['commitid']}, {commit['timestamp']}")
        else:
            print(f"codecov not used: {username}/{repo_name}, {commit['commitid']}, {commit['timestamp']}")

def __print_codecov_commit_build(content, sha_value, username, repo_name):
    commit = None

    for commit in content['results']:
        totals = commit['totals']

        if totals is None:
            continue

        coverage = totals.get('coverage', None)

        if coverage is not None and commit['commitid'] == sha_value:
            print(f"codecov, {username}/{repo_name}, {coverage}%, {commit['commitid']}, {commit['timestamp']}")
            return True
        elif coverage is None:
            print(f"codecov not used: {username}/{repo_name}, {commit['commitid']}, {commit['timestamp']}")
            return False
        else:
            continue

    return False

def _display_codecov_first_page(platform, username, repo_name, token_name):
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
    content = json.loads(response.content)

    if response.status_code == 200:
        if content['count'] == 0:
            print("Repo did implement codecov but did not use it to generate code coverage reports.")
            return False

        __print_codecov_commits(content, username, repo_name)
    else:
        print("codecov returned with error status:".format(response.status_code))
        return False

    return True

def _display_codecov_all_builds(platform, username, repo_name, token_name):
    if token_name is None or token_name == "" or token_name == " ":
        print("invalid token: {}".format(token_name))
        return False

    #https://api.codecov.io/api/v2/{service}/{owner_username}/repos/{repo_name}/commits/
    codecov_endpoint = "https://api.codecov.io/api/v2/{}/{}/repos/{}/commits/"

    codecov_headers = {
        'Authorization': 'bearer {}'.format(token_name)
    }
    endpoint = codecov_endpoint.format(platform, username, repo_name)
    print(endpoint)
    response = requests.get(
        endpoint,
        headers=codecov_headers,
    )
    content = json.loads(response.text)
    __print_codecov_commits(content, username, repo_name)

    if response.status_code == 200:
        commit = None
        if content['count'] == 0:
            print("Repo did implement codecov but did not use it to generate code coverage reports.")
            return False

        next_page_url = content['next']

        while next_page_url is not None:
            print(next_page_url)
            __print_codecov_commits(content, username, repo_name)

            response = requests.get(
                next_page_url,
                headers=codecov_headers,
            )
            content = json.loads(response.text)
            next_page_url = content['next']

        __print_codecov_commits(content, username, repo_name)

    else:
        print("codecov returned with error status:".format(response.status_code))
        return False

    return True

def _display_codecov_build(platform, username, repo_name, token_name, sha_value):
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
    content = json.loads(response.text)
    print(endpoint)
    if __print_codecov_commit_build(content, sha_value, username, repo_name):
        return True

    if response.status_code == 200:
        commit = None
        if content['count'] == 0:
            print("Repo did implement codecov but did not use it to generate code coverage reports.")
            return False

        next_page_url = content['next']

        while next_page_url is not None:
            print(next_page_url)
            if __print_codecov_commit_build(content, sha_value, username, repo_name):
                return True
            response = requests.get(
                next_page_url,
                headers=codecov_headers,
            )
            content = json.loads(response.text)
            next_page_url = content['next']

        if __print_codecov_commit_build(content, sha_value, username, repo_name):
            return True
        else:
            error_msg = "codecov, repo from sha value: {} not found"
            print(error_msg.format(sha_value))
            return False

    else:
        print("codecov returned with error status:".format(response.status_code))
        return False

def _display_coverall(platform, username, repo_name):
    coverall_endpoint = "https://coveralls.io/github/{}/{}.json"
    coverall_endpoint = coverall_endpoint.format(username, repo_name)

    try:
        with urllib.request.urlopen(coverall_endpoint) as url:
            data = json.load(url)

            if data is not None and data['covered_percent'] is not None:
                print(f"coverall: {username}/{repo_name}: {data['covered_percent']}%")
                return True
    except urllib.error.HTTPError as e:
        print(f"coverall not used: {username}/{repo_name}")
        return False

def _display_coverall_ten_builds(platform, username, repo_name):
    page_num = 1
    coverall_endpoint = "https://coveralls.io/github/{}/{}.json?page={}"
    coverall_endpoint = coverall_endpoint.format(username, repo_name, page_num)

    try:
        with urllib.request.urlopen(coverall_endpoint) as url:
            data = json.load(url)

            if data is not None:
                data_builds = data['builds']

                for build in data_builds:
                    if build['covered_percent'] is not None:
                        print(f"coverall, {username}/{repo_name}, {build['covered_percent']}%")
                        print(f"commit_sha: {build['commit_sha']}, created_at: {build['created_at']}")
                return True
    except urllib.error.HTTPError as e:
        print(f"coverall not used: {username}/{repo_name}")
        return False

def _display_coverall_build(platform, username, repo_name, sha_value):
    page_num = 1
    coverall_endpoint_first_page = "https://coveralls.io/github/{}/{}.json?page={}"
    coverall_endpoint_first_page = coverall_endpoint_first_page.format(username, repo_name, page_num)

    try:
        with urllib.request.urlopen(coverall_endpoint_first_page) as first_page_url:
            data = json.load(first_page_url)

            if data is not None:
                page_size = data['pages']

                while page_num <= page_size:
                    coverall_endpoint_pages = "https://coveralls.io/github/{}/{}.json?page={}"
                    coverall_endpoint_pages = coverall_endpoint_pages.format(username, repo_name, page_num)
                    print(coverall_endpoint_pages)

                    with urllib.request.urlopen(coverall_endpoint_pages) as pages_url:
                        data_pages = json.load(pages_url)
                        data_builds = data_pages['builds']

                        for build in data_builds:
                            if build['covered_percent'] is not None and build['commit_sha'] == sha_value:
                                print(f"coverall, {username}/{repo_name}, {build['covered_percent']}%")
                                print(f"commit_sha: {build['commit_sha']}, created_at: {build['created_at']}")
                                return True
                    page_num += 1

                error_msg = "coverall, repo from sha value: {} not found"
                print(error_msg.format(sha_value))
                return False
            return False
    except urllib.error.HTTPError as e:
        print(f"coverall not used: {username}/{repo_name}")
        return False


def _display_coverall_all_builds(platform, username, repo_name):
    page_num = 1
    coverall_endpoint_first_page = "https://coveralls.io/github/{}/{}.json?page={}"
    coverall_endpoint_first_page = coverall_endpoint_first_page.format(username, repo_name, page_num)

    try:
        with urllib.request.urlopen(coverall_endpoint_first_page) as first_page_url:
            data = json.load(first_page_url)

            if data is not None:
                page_size = data['pages']

                while page_num <= page_size:
                    coverall_endpoint_pages = "https://coveralls.io/github/{}/{}.json?page={}"
                    coverall_endpoint_pages = coverall_endpoint_pages.format(username, repo_name, page_num)
                    print(coverall_endpoint_pages)

                    with urllib.request.urlopen(coverall_endpoint_pages) as pages_url:
                        data_pages = json.load(pages_url)
                        data_builds = data_pages['builds']

                        for build in data_builds:
                            if build['covered_percent'] is not None:
                                print(f"coverall, {username}/{repo_name}, {build['covered_percent']}%")
                                print(f"commit_sha: {build['commit_sha']}, created_at: {build['created_at']}")
                    page_num += 1
                return True
            return False
    except urllib.error.HTTPError as e:
        print(f"coverall not used: {username}/{repo_name}")
        return False

def detect_coverage_tool_usage(platform, username, repo_name, codecov_API_token):
    with disablePrintOutput():
        codecov_used = _display_codecov_first_page(platform, username, repo_name, codecov_API_token)
        coverall_used = _display_coverall(platform, username, repo_name)

    if codecov_used or coverall_used:
        return [platform, username, repo_name, codecov_used, coverall_used]
    else:
        return None

if __name__=="__main__":
    #print(retrieve_commit_hashes('expressjs', 'express'))
    #print(get_star_data('expressjs', 'express', ["06-03-2015", "16-01-2024", "15-02-2024", "17-02-2024"]))
    #print(filter_github_repos('../data/github-ranking-2024-02-15.csv'))
    try:
        codecov_API_token = sys.argv[1]
        platform = sys.argv[2]
        username = sys.argv[3]
        repo_name = sys.argv[4]
        sha_value = sys.argv[5]
        function_option = sys.argv[6]

        if function_option == "1":
            print("**********************************_display_codecov_first_page**********************************")
            _display_codecov_first_page(platform, username, repo_name, codecov_API_token)
        elif function_option == "2":
            print("**********************************_display_codecov_all_builds**********************************")
            _display_codecov_all_builds(platform, username, repo_name, codecov_API_token)
        elif function_option == "3":
            print("**********************************_display_codecov_build**********************************")
            _display_codecov_build(platform, username, repo_name, codecov_API_token, sha_value)
        elif function_option == "4":
            print("**********************************_display_coverall**********************************")
            _display_coverall(platform, username, repo_name)
        elif function_option == "5":
            print("**********************************_display_coverall_ten_builds**********************************")
            _display_coverall_ten_builds(platform, username, repo_name)
        elif function_option == "6":
            print("**********************************_display_coverall_all_builds**********************************")
            _display_coverall_all_builds(platform, username, repo_name)
        elif function_option == "7":
            print("**********************************_display_coverall_build**********************************")
            _display_coverall_build(platform, username, repo_name, sha_value)
        elif function_option == "8":
            print("**********************************_detect_coverage_tool_usage**********************************")
            detect_coverage_tool_usage(platform, username, repo_name, codecov_API_token)
        else:
            print(f"Invalid option: {repr(function_option)}")

    except IndexError:
        print("{} codecov_API_token platform username repo_name sha_value function_option".format(sys.argv[0]))
        print("Usage example: CodeCovReport.py 12345678-90ab-cdef-1234-567890abcdef github rajkunamaneni "
              "Code-Coverage-Trends bc5eef62d759fbfc8c2b55da75b4740703856c7c 6")

        sys.exit(1)