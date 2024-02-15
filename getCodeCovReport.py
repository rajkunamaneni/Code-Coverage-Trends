from collections import defaultdict
import json
import requests

CODECOV_ENDPOINT = "https://codecov.io/api/v2/{}/{}"
TOKEN_NAME = ""
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

def display_coverage_dashboard(platform, username, repo_name):
    global CODECOV_ENDPOINT
    endpoint = CODECOV_ENDPOINT.format(platform, username)
    endpoint = endpoint + "/repos/" + repo_name + "/commits"
    _display_coverage(endpoint)

if __name__=="__main__":
    platform = 'github'
    username = 'codecov'
    repo_name = 'codecov-ats'
    display_coverage_dashboard(platform, username, repo_name)