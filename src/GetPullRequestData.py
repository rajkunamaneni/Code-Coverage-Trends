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
import GetContributorData
MAX_RETRIES = 20
GITHUB_TOKEN = "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"
user_agent_desktop = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '\
'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 '\
'Safari/537.36'

GITHUB_AUTH_HEADER = {
    'authorization': "token {0}".format(GITHUB_TOKEN),
    'User-Agent': user_agent_desktop
}

def append_data_to_csv(pull_requests, csv_filename, columns_input):

    with open(csv_filename, 'a', encoding="utf-8", newline='') as f:
        w = csv.DictWriter(f, columns_input)
        if globalvar.write_header_flag is True:
            w.writeheader()
            globalvar.write_header_flag = False
        for row_pr in pull_requests:
            w.writerow(row_pr)
    return True

def _get_pull_request_history_data(username, repo_name):
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(max_retries=MAX_RETRIES)
    session.mount('https://', adapter)
    session.mount('http://', adapter)
    github_endpoint = "https://api.github.com/repos/{}/{}/pulls?state=all&per_page=100"
    endpoint = github_endpoint.format(username, repo_name)
    print(endpoint)

    first_page = session.get(endpoint, headers=GITHUB_AUTH_HEADER, timeout=30)
    yield first_page

    next_page = first_page

    while _get_next_page(next_page) is not None:
        time.sleep(1)
        try:
            next_page_url = next_page.links['next']['url']
            next_page = session.get(next_page_url, headers=GITHUB_AUTH_HEADER, timeout=30)
            yield next_page
            print(next_page_url)
        except KeyError:
            logging.info("No more Github pages")
            break

def _get_next_page(page):
    return page if page.headers.get('link') is not None else None

def get_pull_requests(csv_path, username, repository):
    columns_in = ['user', 'url', 'issue_url', 'state', 'created_at', 'updated_at', 'merged_at', 'merge_commit_sha']
    all_pr_dict = []
    try:
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
            page_pr_dict = [dict(zip(columns_in, item)) for item in zip(*page_pr)] # convert to dict from list of keys and values
            all_pr_dict.append(page_pr_dict)
        merged_all_pr_dict = list(itertools.chain.from_iterable(all_pr_dict)) # flatten the list of dictionaries
        #append_data_to_csv(merged_all_pr_dict, f'{csv_path}pr_history_{username}_{repository}.csv',columns_in)

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
        globalvar.write_header_flag = True
        #append_data_to_csv(merged_all_pr_dict, f'{csv_path}pr_history_time_rm_{username}_{repository}.csv', columns_in)
        append_data_to_csv(merged_all_pr_dict, f'{csv_path}pr_history_{username}_{repository}.csv', columns_in)

        df_prs = pd.DataFrame(merged_all_pr_dict)
        df_prs_per_day = df_prs.groupby(["created_at"]).size().reset_index(name="pull_requests")

        GetContributorData.append_data_to_csv(df_prs_per_day, f'{csv_path}prs_per_day_{username}_{repository}.csv')
        globalvar.write_header_flag = True
    except ValueError:
        print(f'Decoding JSON failed for repo, skipping: {username}/{repository}')

if __name__ == "__main__":
    username, repository = "EvanLi", "Github-Ranking"
    username, repository = "mozilla", "shumway"
    get_pull_requests('../data/', username, repository)
