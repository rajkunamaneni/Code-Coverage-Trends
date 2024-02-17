from collections import defaultdict
import json
import requests
import urllib
import urllib.request, json
import pandas as pd
import argparse

def _display_codecov(platform, username, repo_name):
    CODECOV_ENDPOINT = "https://codecov.io/api/v2/{}/{}"
    parser = argparse.ArgumentParser("codecov_enpoint")
    parser.add_argument("token_name", help="Token for codecov API.", type=str)
    args = parser.parse_args()
    token_name = args.token_name
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

    #print(f"codecov not used: {username}/{repo_name}")
    return False

def _display_coverall(platform, username, repo_name):
    coverall_endpoint = "https://coveralls.io/github/{}/{}.json"
    coverall_endpoint = coverall_endpoint.format(username, repo_name)
    try:
        with urllib.request.urlopen(coverall_endpoint) as url:
            data = json.load(url)
            if data is not None:
                print(f"coverall: {username}/{repo_name}: {data['covered_percent']}%")
                return True
    except urllib.error.HTTPError as e:
        #print(f"coverall not used: {username}/{repo_name}")
        return False

def display_coverage_dashboard(platform, username, repo_name):
    _display_codecov(platform, username, repo_name)
    _display_coverall(platform, username, repo_name)


if __name__=="__main__":
    platform = 'github'
    data = pd.read_csv('../data/github-ranking-2024-02-15.csv')
    data_dict = data.to_dict(orient='records')
    data_dict = [item for item in data_dict if item['item'] == 'JavaScript' or item['item'] == 'TypeScript']

    for item in data_dict:
        username = item['username']
        repo_name = item['repo_name']
        display_coverage_dashboard(platform, username, repo_name)
