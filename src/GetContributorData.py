from pydriller import Repository
from collections import defaultdict
from GrabReleaseCommits import *
from DateUtil import *
from StarHistory import get_star_data, get_daily_star_data
from GetRepoFromDataset import filter_github_repos
from CodeCovReport import get_codecov_all_builds, detect_coverage_tool_usage, get_coverall_all_builds
import numpy as np
from datetime import datetime
import pandas as pd
import requests
import csv
import matplotlib.pyplot as plt
import seaborn as sns
import GetPullRequestData
import os.path


def get_contributor_counts(repo_name,repo_owner,repo_link,filename):    
    authors = []
    dates = []
    for commit in Repository(repo_link).traverse_commits():
        authors.append(commit.author.name)
        dates.append(commit.author_date.strftime("%Y-%m-%d"))
    d = {'authors':authors,'dates':dates}
    df = pd.DataFrame(d)
    df["dates"] = pd.to_datetime(df["dates"])
    df1 = df.groupby(["dates","authors"]).size().reset_index(name = "contributions")
    df2 = df1.groupby(["dates"]).size().reset_index(name = "contributors")
    append_data_to_csv(df2, filename)
    print(df2)
    
def append_data_to_csv(dataframe, csv_filename):
    try:
        # Load existing data from CSV file
        existing_data = pd.read_csv(csv_filename)

        # Append the new data to the existing data
        combined_data = pd.concat([existing_data, dataframe], ignore_index=True)

        # Save to CSV
        combined_data.to_csv(csv_filename, index=False)

        print(f"New data appended to '{csv_filename}' successfully.")
    except FileNotFoundError:
        print("CSV file not found. Creating a new CSV file...")
        dataframe.to_csv(csv_filename, index=False)
        print(f"New CSV file '{csv_filename}' created with the new data.")
        
def run_contributor_code():
    dfhigh = pd.read_csv("../data/refinedRepoHighStars_612.csv")
    for i in dfhigh.index:
        platform = dfhigh['platform'][i]
        username = dfhigh['username'][i]
        repo_name = dfhigh['repo_name'][i]
        repo_link = f'https://{platform}.com/{username}/{repo_name}.git'
        print(repo_link)
        filename = f'../data/contributorshigh/{username}_{repo_name}_contributors.csv'
        get_contributor_counts(repo_name,username,repo_link,filename)
    dfmed = pd.read_csv("../data/Refined_Repo_CSV/refinedRepoMedStars_No_Dupl.csv")
    for i in dfmed.index:
        platform = dfmed['platform'][i]
        username = dfmed['username'][i]
        repo_name = dfmed['repo_name'][i]
        repo_link = f'https://{platform}.com/{username}/{repo_name}.git'
        print(repo_link)
        filename = f'../data/contributorsmed/{username}_{repo_name}_contributors.csv'
        get_contributor_counts(repo_name,username,repo_link,filename)
    dflow = pd.read_csv("../data/refinedRepoLowStars_119.csv")
    for i in dflow.index:
        platform = dflow['platform'][i]
        username = dflow['username'][i]
        repo_name = dflow['repo_name'][i]
        repo_link = f'https://{platform}.com/{username}/{repo_name}.git'
        print(repo_link)
        filename = f'../data/contributorslow/{username}_{repo_name}_contributors.csv'
        get_contributor_counts(repo_name,username,repo_link,filename)
        


if __name__ == "__main__":
    run_contributor_code()
