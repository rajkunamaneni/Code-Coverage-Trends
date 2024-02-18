from collections import defaultdict
import json
import requests
import urllib
import urllib.request, json
import pandas as pd
import sys

def _display_codecov(platform, username, repo_name, token_name):
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
        commit = None
        if content['count'] == 0:
            return False

        for commit in content['results']:
            totals = commit['totals']
            if totals is None:
                continue

            coverage = totals.get('coverage', None)
            if coverage is not None:
                print(f"codecov: {username}/{repo_name}: {coverage}%")
                return True
            else:
                print(f"codecov not used: {username}/{repo_name}")
                return False

    print(f"codecov not used: {username}/{repo_name}")
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
                        print(f"commit_sha: {build['commit_sha']}, commit_message: {build['commit_message']}")
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
                                print(f"commit_sha: {build['commit_sha']}, commit_message: {build['commit_message']}")
                                return True
                    page_num += 1

                error_msg = "repo from sha value: {} not found"
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
                                print(f"commit_sha: {build['commit_sha']}, commit_message: {build['commit_message']}")
                    page_num += 1

                return True
            return False
    except urllib.error.HTTPError as e:
        print(f"coverall not used: {username}/{repo_name}")
        return False


if __name__=="__main__":
    # platform = 'github'
    # data = pd.read_csv('../data/github-ranking-2024-02-15.csv')
    # data_dict = data.to_dict(orient='records')
    # data_dict = [item for item in data_dict if item['item'] == 'JavaScript' or item['item'] == 'TypeScript']
    # for item in data_dict:
    #     username = item['username']
    #     repo_name = item['repo_name']

    try:
        codecov_API_token = sys.argv[1]
        platform = sys.argv[2]
        username = sys.argv[3]
        repo_name = sys.argv[4]
        sha_value = sys.argv[5]
        function_option = sys.argv[6]

    except IndexError:
        print("{} codecov_API_token platform username repo_name sha_value function_option".format(sys.argv[0]))

        print("For function_option:")
        print("1 ---> _display_codecov() for most recent commit code coverage")
        print("2 ---> _display_coverall() for most recent commit code coverage")
        print("3 ---> _display_coverall_ten_builds() for latest 10 commits of a repo")
        print("4 ---> _display_coverall_all_builds() for all commits of a repo. WARNING: This might take long time to run.")
        print("5 ---> _display_coverall_build() for coverage report based on a commit's sha hash value")
        print("6 ---> run everything!")

        print("Usage example: CodeCovReport.py 12345678-90ab-cdef-1234-567890abcdef github rajkunamaneni "
              "Code-Coverage-Trends bc5eef62d759fbfc8c2b55da75b4740703856c7c 6")
        sys.exit(1)

    if function_option == 1:
        _display_codecov(platform, username, repo_name, codecov_API_token)
    elif function_option == 2:
        _display_coverall(platform, username, repo_name)
    elif function_option == 3:
        _display_coverall_ten_builds(platform, username, repo_name)
    elif function_option == 4:
        _display_coverall_all_builds(platform, username, repo_name)
    elif function_option == 5:
        _display_coverall_build(platform, username, repo_name, sha_value)
    else:
        print("**********************************_display_codecov**********************************")
        _display_codecov(platform, username, repo_name, codecov_API_token)

        print("**********************************_display_coverall**********************************")
        _display_coverall(platform, username, repo_name)

        print("**********************************_display_coverall_ten_builds**********************************")
        _display_coverall_ten_builds(platform, username, repo_name)

        print("**********************************_display_coverall_all_builds**********************************")
        _display_coverall_all_builds(platform, username, repo_name)

        print("**********************************_display_coverall_builds**********************************")
        _display_coverall_build(platform, username, repo_name, sha_value)
