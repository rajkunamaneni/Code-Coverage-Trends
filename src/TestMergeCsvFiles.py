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
import glob

def strip_timestamp(pop_csv_dict_of_df):
    for idx, pop_date_commit_dict_inst in enumerate(pop_csv_dict_of_df):
        timestamp = pop_date_commit_dict_inst['Timestamp']

        if timestamp is not None:
            pop_csv_dict_of_df[idx]['Timestamp'] = timestamp.split('T', 1)[0]

def combine_pr_with_pop_report(pr_history_csv_file_list, pr_file_prefix, pop_csv_dict_of_df):
    for pr_csv_file in pr_history_csv_file_list:
        try:
            if pr_file_prefix in pr_csv_file:
                pr_csv_df = pd.read_csv(pr_csv_file)
                pr_csv_filename = os.path.basename(pr_csv_file)
                pr_csv_filename_no_prefix = pr_csv_filename.removeprefix('prs_per_day_')
                pr_csv_filename_no_suffix = pr_csv_filename_no_prefix.removesuffix('.csv')
                [username, repository] = pr_csv_filename_no_suffix.split('_')

                pr_count_aligned_date_list = []
                for idx, pop_date_commit_dict_inst in enumerate(pop_csv_dict_of_df):
                    if (pop_date_commit_dict_inst['Username'] == username) \
                            and (pop_date_commit_dict_inst['Repository'] == repository):

                        for created_at_pr_row, pull_requests_pr_row in \
                                zip(pr_csv_df['created_at'].values, pr_csv_df['pull_requests'].values):
                            if pop_date_commit_dict_inst['Timestamp'] == created_at_pr_row:
                                pop_csv_dict_of_df[idx]['Pull Requests on Timestamp'] = pull_requests_pr_row
                                break
        except ValueError:
            print(f'repo used bad naming practices, skipping: {pr_csv_file}')
            pass


def write_to_csv(pop_report_csv_file, pop_csv_dict_of_df, pop_report_csv_path, new_prefix):
    original_csv_name = os.path.basename(pop_report_csv_file)
    new_pop_csv_dict_of_df_keys = pop_csv_dict_of_df[0].keys()

    csv_file_with_append_pr_count = f'{pop_report_csv_path}/{new_prefix}{original_csv_name}'
    new_path_csv_output = csv_file_with_append_pr_count.replace(os.sep, '/')

    with open(new_path_csv_output, 'w', newline='') as out_file:
        dict_writer = csv.DictWriter(out_file, new_pop_csv_dict_of_df_keys)
        dict_writer.writeheader()
        dict_writer.writerows(pop_csv_dict_of_df)

    print(f"Merged Pull Request Count CSV file done: {new_path_csv_output}")


def merge_csv_pop_report(pop_report_csv_path, pr_history_csv_path, pop_file_suffix, pr_file_prefix):
    pop_report_csv_file_list = glob.glob(os.path.join(pop_report_csv_path, "*.csv"))
    pr_history_csv_file_list = glob.glob(os.path.join(pr_history_csv_path, "*.csv"))
    new_prefix = 'WithPr_'

    for pop_report_csv_file in pop_report_csv_file_list:
        if (pop_file_suffix in pop_report_csv_file) and (new_prefix not in pop_report_csv_file):
            pop_csv_df_original = pd.read_csv(pop_report_csv_file)
            pop_csv_df_original['Pull Requests on Timestamp'] = 0
            pop_csv_dict_of_df = pop_csv_df_original.to_dict('records')

            strip_timestamp(pop_csv_dict_of_df)
            combine_pr_with_pop_report(pr_history_csv_file_list, pr_file_prefix, pop_csv_dict_of_df)
            write_to_csv(pop_report_csv_file, pop_csv_dict_of_df, pop_report_csv_path, new_prefix)

if __name__ == "__main__":
    pop_report_csv_path = r'C:\Users\lenovoi7\Documents\GitHub\GitHub-Testing-Trends\data\Popularity_Reports_High_Star'
    pr_history_csv_path = r'C:\Users\lenovoi7\Documents\GitHub\GitHub-Testing-Trends\data\Pull_Request_History_High_Star_Repo'
    pop_file_suffix = r'PopularityReport'
    pr_file_prefix = r'prs_per_day_'

    merge_csv_pop_report(pop_report_csv_path, pr_history_csv_path, pop_file_suffix, pr_file_prefix)