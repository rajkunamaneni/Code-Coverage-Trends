import json
import requests
import urllib
import urllib.request, json
import pandas as pd
import sys
import os

from collections import defaultdict
from GrabReleaseCommits import *
from StarHistory import *
from GetRepoFromDataset import *
from CodeCovReport import *

if __name__=="__main__":
    github_repos = filter_github_repos('../data/github-ranking-2024-02-15.csv')
    print(github_repos)
    list = []
    for repo in github_repos:
        username, repo_name = repo[0], repo[1]
        token = "7848dd6f-5308-43f6-a02f-e10e31118854"
        list.append(detect_coverage_tool_usage("github", username, repo_name, token))
        retrieve_commit_hashes()
