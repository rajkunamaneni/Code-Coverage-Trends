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
from datetime import datetime as dt

def get_comulative_pr_data(csv_path, username, repository, date):
    try:
        # Load existing data from CSV file
        csv_filename = f'{csv_path}prs_per_day_{username}_{repository}.csv'
        existing_data = pd.read_csv(csv_filename)
        in_date = dt.strptime(date, "%Y-%m-%d")
        total_pr_to_date = 0
        for idx, date_inst in enumerate(existing_data["created_at"]):
            pr_creation_date = dt.strptime(date_inst, "%Y-%m-%d")
            if pr_creation_date <= in_date:
                total_pr_to_date+=existing_data["pull_requests"][idx]

            else:
                print(f'{username}, {repository}, {date}, {total_pr_to_date}')
                return total_pr_to_date
    except FileNotFoundError:
        print("CSV file not found...")

if __name__ == "__main__":
    username = "operator-framework"
    repository = "operator-sdk"
    date = "2018-02-18"
    path = '../data/Pull_Request_CSV/Pull_Request_History_Med_Star_Repo/'
    get_comulative_pr_data(path, username, repository, date)
