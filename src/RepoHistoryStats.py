import json
import logging
import requests
import DateUtil
import time
import pandas as pd
import csv
import os
import GrabForkData

GITHUB_TOKEN = "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"
GITHUB_AUTH_HEADER = {
    'authorization': "token {0}".format(GITHUB_TOKEN),
}
CSV_PATH = '../data/'

def _get_pull_request_history_data(username, repo_name):
    session = requests.Session()
    github_endpoint = "https://api.github.com/repos/{}/{}/pulls?state=all&per_page=100"
    endpoint = github_endpoint.format(username, repo_name)
    print(endpoint)

    first_page = session.get(endpoint, headers=GITHUB_AUTH_HEADER)
    yield first_page

    next_page = first_page

    while _get_next_page(next_page) is not None:
        time.sleep(1)
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
    columns_in = ['user', 'url', 'issue_url', 'state', 'created_at', 'updated_at', 'merged_at', 'merge_commit_sha']

    for page in _get_pull_request_history_data(username, repository):
        pr_page = json.loads(page.content)
        page_pr = []
        for pr_instance in pr_page:
            pr_instance_data = []
            for col in columns_in:
                if col in pr_instance.keys():
                    if col == 'user':
                        pr_instance_data.append(pr_instance[col]['login'])
                        continue
                    pr_instance_data.append(pr_instance[col])
            page_pr.append(pr_instance_data)
        page_pr = list(map(list, zip(*page_pr))) # to transpose
        print(page_pr)
        GrabForkData.append_data_to_csv(page_pr,
                                            f'{CSV_PATH}pr_history_{username}_{repository}.csv',
                                            columns_in)

if __name__ == "__main__":
    username, repository = "mozilla", "shumway"
    #username, repository = "EvanLi", "Github-Ranking"
    get_pull_requests(username, repository)
