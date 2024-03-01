import json
import logging
import requests
import DateUtil
import time
import pandas as pd
import csv
import os

GITHUB_TOKEN = "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"
GITHUB_AUTH_HEADER = {
    'authorization': "token {0}".format(GITHUB_TOKEN),
}

def save_to_csv(pull_requests, username, repository):
    key_list = list(pull_requests[0].keys())
    csv_path = '../data/pr_history_'
    csv_path_name = csv_path + username + '_' + repository + '.csv'
    with open(csv_path_name, 'w', encoding="utf-8", newline='') as f:  # You will need 'wb' mode in Python 2.x
        w = csv.DictWriter(f, key_list)
        w.writeheader()
        for row_pr in pull_requests:
            w.writerow(row_pr)
    return True

def _get_pull_request_history_data(username, repo_name):
    session = requests.Session()
    #github_endpoint = "https://api.github.com/search/issues?q=repo%3A{}%2F{}&type=pullrequests&page=1"
    github_endpoint = "https://api.github.com/repos/{}/{}/pulls?state=all&per_page=100"
    endpoint = github_endpoint.format(username, repo_name)
    print(endpoint)

    first_page = session.get(endpoint, headers=GITHUB_AUTH_HEADER)
    yield first_page

    next_page = first_page

    while _get_next_page(next_page) is not None:
        time.sleep(2)
        try:
            next_page_url = next_page.links['next']['url']
            next_page = session.get(next_page_url, headers=GITHUB_AUTH_HEADER)
            yield next_page
            print(next_page_url)
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

    save_to_csv(pull_requests, username, repository)

if __name__ == "__main__":
    username, repository = "mozilla", "shumway"
    # username, repository = "EvanLi", "Github-Ranking"
    get_pull_requests(username, repository)
