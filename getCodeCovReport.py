from collections import defaultdict
import json
import requests
import urllib
import urllib.request, json

CODECOV_ENDPOINT = "https://codecov.io/api/v2/{}/{}"
TOKEN_NAME = "7848dd6f-5308-43f6-a02f-e10e31118854"
CODECOV_HEADERS = {
    'Authorization': 'bearer {}'.format(TOKEN_NAME)
}

def _display_coverage(endpoint):
    response = requests.get(
        endpoint,
        headers=CODECOV_HEADERS,
    )
    content = json.loads(response.content)
    commit = None
    if content['count'] == 0:
        return

    for commit in content['results']:
        totals = commit['totals']
        if totals is None:
            continue

        coverage = totals.get('coverage', None)
        if coverage is not None:
            print('{}%'.format(coverage))
            return

    print('No coverage found on any commit')

def _display_coverall(endpoint):
    response = requests.get(
        endpoint
    )
    print(response)

def display_coverage_dashboard(platform, username, repo_name):
    global CODECOV_ENDPOINT
    endpoint = CODECOV_ENDPOINT.format(platform, username)
    endpoint = endpoint + "/repos/" + repo_name + "/commits"
    _display_coverage(endpoint)

    coverall_endpoint = "https://coveralls.io/github/{}/{}.json"

    coverall_endpoint = coverall_endpoint.format(username, repo_name)
    try:
        with urllib.request.urlopen(coverall_endpoint) as url:
            data = json.load(url)
            print(data['covered_percent'])
    except urllib.error.HTTPError as e:
        print("repo does not use coverall")


if __name__=="__main__":
    platform = 'github'
    username = 'codecov'
    repo_name = 'codecov-ats'
    display_coverage_dashboard(platform, username, repo_name)