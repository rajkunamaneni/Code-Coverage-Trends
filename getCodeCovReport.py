from collections import defaultdict
import json
import requests

CODECOV_ENDPOINT = "https://codecov.io/api/v2/github/codecov/{}"
TOKEN_NAME = "{{ ACCESS TOKEN }}"
CODECOV_HEADERS = {
    'Authorization': 'bearer {}'.format(TOKEN_NAME)
}

def _get_all_repos():
    print('Retrieving all repos...', end=" ")
    endpoint = CODECOV_ENDPOINT.format('repos?page_size=500')
    response = requests.get(
        endpoint,
        headers=CODECOV_HEADERS,
    )
    repos = json.loads(response.content)['results']
    print("Found {} repositories".format(len(repos)))
    return sorted(repo['name'] for repo in repos)

def _display_coverage(repo_name):
    endpoint = CODECOV_ENDPOINT.format("repos/{}/commits".format(repo_name))
    response = requests.get(
        endpoint,
        headers=CODECOV_HEADERS,
    )
    content = json.loads(response.content)
    commit = None
    if content['count'] == 0:
        return
    print(repo_name, end=" ")

    for commit in content['results']:
        totals = commit['totals']
        if totals is None:
            continue

        coverage = totals.get('coverage', None)
        if coverage is not None:
            print('{}%'.format(coverage))
            return

    print('No coverage found on any commit')

def display_coverage_dashboard():
    repos = _get_all_repos()
    for repo in repos:
        _display_coverage(repo)

if __name__=="__main__":
    display_coverage_dashboard()