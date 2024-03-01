import json
import logging
import requests
import DateUtil
import time

GITHUB_TOKEN = "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"
GITHUB_AUTH_HEADER = {
    'authorization': "token {0}".format(GITHUB_TOKEN),
}

def _get_pull_request_history_data(username, repo_name):
    session = requests.Session()
    #github_endpoint = "https://api.github.com/search/issues?q=repo%3A{}%2F{}&type=pullrequests&page=1"
    github_endpoint = "https://api.github.com/repos/{}/{}/pulls?state=all&page=1"
    endpoint = github_endpoint.format(username, repo_name)
    print(endpoint)

    first_page = session.get(endpoint, headers=GITHUB_AUTH_HEADER)
    yield first_page

    next_page = first_page

    while _get_next_page(next_page) is not None:
        time.sleep(4)
        try:
            next_page_url = next_page.links['next']['url']
            next_page = session.get(next_page_url, headers=GITHUB_AUTH_HEADER)
            yield next_page

        except KeyError:
            logging.info("No more Github pages")
            break

def _get_next_page(page):
    return page if page.headers.get('link') is not None else None

def get_pull_requests(username, repository):
    pull_request_list = []

    for page in _get_pull_request_history_data(username, repository):
        content = json.loads(page.content)
        pull_request_list.append(content)

    pull_requests = []
    for pr_page in pull_request_list:

        for pr_instance in pr_page:
            pull_requests.append(pr_instance)
    [pr.pop('body') for pr in pull_requests]
    return pull_requests

if __name__ == "__main__":
    username, repository = "EvanLi", "Github-Ranking"
    pull_requests = get_pull_requests(username, repository)

    for pr in pull_requests:
        print(pr)
