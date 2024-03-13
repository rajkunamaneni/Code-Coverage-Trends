import pandas as pd
import os
import glob
from datetime import datetime as dt
import MergeCsvFiles

def get_comulative_pr_data(in_date, existing_data_prs_by_dates):
    total_pr_to_date = 0
    for idx, date_inst in enumerate(existing_data_prs_by_dates["created_at"]):
        pr_creation_date_obj = dt.strptime(date_inst, "%Y-%m-%d")
        in_date_obj = dt.strptime(in_date, "%Y-%m-%d")

        if pr_creation_date_obj <= in_date_obj:
            total_pr_to_date+=existing_data_prs_by_dates["pull_requests"][idx]
        else:
            return total_pr_to_date

def combine_pr_totals_with_pop_report(pr_history_csv_file_list, pr_file_prefix, pop_csv_dict_of_df):
    for pr_csv_file in pr_history_csv_file_list:
        try:
            if pr_file_prefix in pr_csv_file:
                pr_csv_df, username, repository = MergeCsvFiles.get_username_reponame_from_filename(pr_csv_file, pr_file_prefix)

                for idx, pop_date_commit_dict_inst in enumerate(pop_csv_dict_of_df):
                    if (pop_date_commit_dict_inst['Username'] == username) \
                            and (pop_date_commit_dict_inst['Repository'] == repository):

                        for created_at_pr_row in zip(pr_csv_df['created_at'].values):
                            created_at_pr_row_zero = created_at_pr_row[0]

                            timestamp = pop_date_commit_dict_inst['Timestamp']
                            if timestamp == created_at_pr_row_zero:
                                pop_csv_dict_of_df[idx]['Total Pull Requests Before Timestamp'] = \
                                    get_comulative_pr_data(timestamp, pr_csv_df)
                                break
        except ValueError:
            print(f'repo used invalid naming practices, skipping: {pr_csv_file}')
            pass

def merge_csv_pop_report(pop_report_csv_path, pr_history_csv_path, pop_file_prefix, pr_file_prefix, new_prefix):
    pop_report_csv_file_list = glob.glob(os.path.join(pop_report_csv_path, "*.csv"))
    pr_history_csv_file_list = glob.glob(os.path.join(pr_history_csv_path, "*.csv"))

    for pop_report_csv_file in pop_report_csv_file_list:
        if (pop_file_prefix in pop_report_csv_file) and (new_prefix not in pop_report_csv_file):
            pop_csv_df_original = pd.read_csv(pop_report_csv_file)
            pop_csv_df_original['Total Pull Requests Before Timestamp'] = 0
            pop_csv_dict_of_df = pop_csv_df_original.to_dict('records')

            combine_pr_totals_with_pop_report(pr_history_csv_file_list, pr_file_prefix, pop_csv_dict_of_df)
            MergeCsvFiles.write_to_csv(pop_report_csv_file, pop_csv_dict_of_df, pop_report_csv_path, new_prefix)

if __name__ == "__main__":
    pop_report_csv_path = r'C:\Users\lenovoi7\Documents\GitHub\GitHub-Testing-Trends\data\Popularity_Reports_Medium_Star'
    pr_history_csv_path = r'C:\Users\lenovoi7\Documents\GitHub\GitHub-Testing-Trends\data\Pull_Request_CSV\Pull_Request_History_Med_Star_Repo'
    pop_file_prefix = r'WithPrandContributions_'
    pr_file_prefix = r'prs_per_day_'
    new_prefix = 'PrTotals'

    merge_csv_pop_report(pop_report_csv_path, pr_history_csv_path, pop_file_prefix, pr_file_prefix, new_prefix)
