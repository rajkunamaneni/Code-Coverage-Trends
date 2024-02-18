from collections import defaultdict
import json
import requests
import urllib
import urllib.request, json
import pandas as pd
import sys
from GrabReleaseCommits import retrieve_commit_hashes

# Helper functions for codecov printing of each commit info and their resulting code coverage
def __print_codecov_commits(content):
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

def __print_codecov_commit_build(content, sha_value):
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
            return False

def _display_codecov_first_page(platform, username, repo_name, token_name):
    if token_name is None or token_name == "" or token_name == " ":
        print("invalid token: {}".format(token_name))
        return False

    CODECOV_ENDPOINT = "https://codecov.io/api/v2/{}/{}"

    CODECOV_HEADERS = {
        'Authorization': 'bearer {}'.format(token_name)
    }
    endpoint = CODECOV_ENDPOINT.format(platform, username)
    endpoint = endpoint + "/repos/" + repo_name + "/commits"
    response = requests.get(
        endpoint,
        headers=CODECOV_HEADERS,
    )
    content = json.loads(response.content)

    if response.status_code == 200:
        if content['count'] == 0:
            print("Repo did implement codecov but did not use it to generate code coverage reports.")
            return False

        __print_codecov_commits(content)
    else:
        print("codecov returned with error status:".format(response.status_code))
        return False

    return True

def _display_codecov_all_builds(platform, username, repo_name, token_name):
    if token_name is None or token_name == "" or token_name == " ":
        print("invalid token: {}".format(token_name))
        return False

    #https://api.codecov.io/api/v2/{service}/{owner_username}/repos/{repo_name}/commits/
    CODECOV_ENDPOINT = "https://api.codecov.io/api/v2/{}/{}/repos/{}/commits/"

    CODECOV_HEADERS = {
        'Authorization': 'bearer {}'.format(token_name)
    }
    endpoint = CODECOV_ENDPOINT.format(platform, username, repo_name)
    response = requests.get(
        endpoint,
        headers=CODECOV_HEADERS,
    )
    print(response)
    content = json.loads(response.text)

    if response.status_code == 200:
        commit = None
        print(content)
        if content['count'] == 0:
            print("Repo did implement codecov but did not use it to generate code coverage reports.")
            return False

        next_page_url = content['next']

        while next_page_url is not None:
            __print_codecov_commits(content)

            response = requests.get(
                next_page_url,
                headers=CODECOV_HEADERS,
            )
            content = json.loads(response.text)
            next_page_url = content['next']

        __print_codecov_commits(content)

    else:
        print("codecov returned with error status:".format(response.status_code))
        return False

    return True

def _display_codecov_build(platform, username, repo_name, token_name, sha_value):
    if token_name is None or token_name == "" or token_name == " ":
        print("invalid token: {}".format(token_name))
        return False

    #https://api.codecov.io/api/v2/{service}/{owner_username}/repos/{repo_name}/commits/
    CODECOV_ENDPOINT = "https://api.codecov.io/api/v2/{}/{}/repos/{}/commits/"

    CODECOV_HEADERS = {
        'Authorization': 'bearer {}'.format(token_name)
    }
    endpoint = CODECOV_ENDPOINT.format(platform, username, repo_name)
    response = requests.get(
        endpoint,
        headers=CODECOV_HEADERS,
    )
    content = json.loads(response.text)

    if response.status_code == 200:
        commit = None
        if content['count'] == 0:
            print("Repo did implement codecov but did not use it to generate code coverage reports.")
            return False

        next_page_url = content['next']

        while next_page_url is not None:
            if __print_codecov_commit_build(content, sha_value):
                break
            response = requests.get(
                next_page_url,
                headers=CODECOV_HEADERS,
            )
            content = json.loads(response.text)
            next_page_url = content['next']

        if __print_codecov_commit_build(content, sha_value):
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


if __name__=="__main__":
    #print(retrieve_commit_hashes('expressjs', 'express'))
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
        else:
            print(f"Invalid option: {repr(function_option)}")

    except IndexError:
        print("{} codecov_API_token platform username repo_name sha_value function_option".format(sys.argv[0]))

        # print("For function_option:")
        # print("1 ---> _display_codecov() for most recent commit code coverage")
        # print("2 ---> _display_coverall() for most recent commit code coverage")
        # print("3 ---> _display_coverall_ten_builds() for latest 10 commits of a repo")
        # print("4 ---> _display_coverall_all_builds() for all commits of a repo. "
        #       "WARNING: This might take long time to run.")
        # print("5 ---> _display_coverall_build() for coverage report based on a commit's sha hash value")

        print("Usage example: CodeCovReport.py 12345678-90ab-cdef-1234-567890abcdef github rajkunamaneni "
              "Code-Coverage-Trends bc5eef62d759fbfc8c2b55da75b4740703856c7c 6")
        sys.exit(1)