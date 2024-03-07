import json
import logging
import requests
import DateUtil
import time
import pandas as pd
import csv
import os
import GlobalVarSetting as globalvar
import itertools
from urllib3.exceptions import NewConnectionError
from urllib3.util.retry import Retry

GITHUB_TOKEN = "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"
user_agent_desktop = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '\
'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 '\
'Safari/537.36'

GITHUB_AUTH_HEADER = {
    'authorization': "token {0}".format(GITHUB_TOKEN),
    'User-Agent': user_agent_desktop
}
ERR_WAIT_TIME = 30
TIMEOUT_AFTER = 10

def transpose_page(page_pr):
    return list(map(list, zip(*page_pr)))

def convert_to_dict_from_list(columns_in, page_pr):
    return [dict(zip(columns_in, item)) for item in
                    zip(*page_pr)]

def flatten_list_dict(all_pr_dict):
    return list(itertools.chain.from_iterable(all_pr_dict))

def write_data_to_csv(pull_requests, csv_filename, columns_input):
    with open(csv_filename, 'w', encoding="utf-8", newline='') as f:
        w = csv.DictWriter(f, columns_input)
        if globalvar.write_header_flag is True:
            w.writeheader()
            globalvar.write_header_flag = False
        for row_pr in pull_requests:
            w.writerow(row_pr)
    return True

def write_df_data_to_csv(dataframe, csv_filename):
    dataframe.to_csv(csv_filename, index=False)
    print(f"New CSV file '{csv_filename}' created with the new data.")

def _get_from_page(session, next_page_url):
    while True:
        try:
            next_page_hold = session.get(next_page_url, headers=GITHUB_AUTH_HEADER, timeout=TIMEOUT_AFTER)
            return next_page_hold
        except (requests.ConnectionError, NewConnectionError, requests.exceptions.ChunkedEncodingError,
                requests.exceptions.ContentDecodingError, requests.exceptions.ConnectionError,
                requests.exceptions.ReadTimeout, requests.ReadTimeout) as e:
            print(f"Waiting for connection, sleep: {ERR_WAIT_TIME}, error: {e}")
            time.sleep(ERR_WAIT_TIME)
            pass

def _get_next_page(page):
    while True:
        try:
            return page if page.headers.get('link') is not None else None
        except (requests.ConnectionError, NewConnectionError, requests.exceptions.ChunkedEncodingError,
                requests.exceptions.ContentDecodingError, requests.exceptions.ConnectionError,
                requests.exceptions.ReadTimeout, requests.ReadTimeout) as e:
            print(f"Waiting for connection, sleep: {ERR_WAIT_TIME}, error: {e}")
            time.sleep(ERR_WAIT_TIME)
            pass

def _get_pull_request_history_data(username, repo_name):
    session = requests.Session()
    retry = Retry(total=False, backoff_factor=10)
    adapter = requests.adapters.HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)
    session.mount('http://', adapter)
    github_endpoint = "https://api.github.com/repos/{}/{}/pulls?state=all&per_page=100"
    endpoint = github_endpoint.format(username, repo_name)
    print(endpoint)

    first_page = _get_from_page(session, endpoint)
    yield first_page

    next_page = first_page

    while _get_next_page(next_page) is not None:
        try:
            next_page_url = next_page.links['next']['url']
            next_page = _get_from_page(session, next_page_url)
            yield next_page
            print(next_page_url)
        except KeyError:
            logging.info("No more Github pages")
            break

def process_json_page_to_list_of_dict_per_page(columns_in, page):
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

    page_pr = transpose_page(page_pr)
    page_pr_dict = convert_to_dict_from_list(columns_in, page_pr)
    return page_pr_dict

def strip_time_from_pr_row_entry(merged_all_pr_dict):
    for idx, repo_dict_instance in enumerate(merged_all_pr_dict):
        created_at = repo_dict_instance['created_at']
        if created_at is not None:
            merged_all_pr_dict[idx]['created_at'] = created_at.split('T', 1)[0]

        updated_at = repo_dict_instance['updated_at']
        if updated_at is not None:
            merged_all_pr_dict[idx]['updated_at'] = updated_at.split('T', 1)[0]

        merged_at = repo_dict_instance['merged_at']
        if merged_at is not None:
            merged_all_pr_dict[idx]['merged_at'] = merged_at.split('T', 1)[0]

def get_pull_requests(csv_path, username, repository):
    columns_in = ['user', 'url', 'issue_url', 'state', 'created_at', 'updated_at', 'merged_at', 'merge_commit_sha']
    all_pr_dict = []
    try:
        for page in _get_pull_request_history_data(username, repository):
            processed_dict = process_json_page_to_list_of_dict_per_page(columns_in, page)
            all_pr_dict.append(processed_dict)
        merged_all_pr_dict = flatten_list_dict(all_pr_dict)

        strip_time_from_pr_row_entry(merged_all_pr_dict)

        globalvar.write_header_flag = True
        write_data_to_csv(merged_all_pr_dict, f'{csv_path}pr_history_{username}_{repository}.csv', columns_in)

        df_prs = pd.DataFrame(merged_all_pr_dict)
        df_prs_per_day = df_prs.groupby(["created_at"]).size().reset_index(name="pull_requests")
        write_df_data_to_csv(df_prs_per_day, f'{csv_path}prs_per_day_{username}_{repository}.csv')
        globalvar.write_header_flag = True
    except ValueError:
        print(f'Decoding JSON failed for repo, skipping: {username}/{repository}')

if __name__ == "__main__":
    username, repository = "EvanLi", "Github-Ranking"
    username, repository = "mozilla", "shumway"
    get_pull_requests('../data/', username, repository)
