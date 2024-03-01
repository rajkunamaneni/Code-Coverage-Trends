import pandas as pd
import argparse
import json
import urllib.error
import urllib.request

# Replace 'YOUR_API_TOKEN' with your actual GitHub API token
API_TOKEN = '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'

def append_data_to_csv(data, csv_filename):
    try:
        # Load existing data from CSV file
        existing_data = pd.read_csv(csv_filename)

        if isinstance(data, list):
            # Convert list to DataFrame
            data = pd.DataFrame([data], columns=['Owner', 'SSH URL', 'Created At'])

        # Append the new data to the existing data
        combined_data = pd.concat([existing_data, data], ignore_index=True)

        # Save to CSV
        combined_data.to_csv(csv_filename, index=False)

        print(f"New data appended to '{csv_filename}' successfully.")
    except FileNotFoundError:
        print("CSV file not found. Creating a new CSV file...")
        if isinstance(data, list):
            data = pd.DataFrame([data], columns=['Owner', 'SSH URL', 'Created At'])

        data.to_csv(csv_filename, index=False)
        print(f"New CSV file '{csv_filename}' created with the new data.")


def find_forks_and_append(repo_owner, repo_name):
    """
    Query the GitHub API for all forks of a repository and append them to a CSV file.
    """
    page = 1
    headers_written = False

    GITHUB_FORK_URL = f"https://api.github.com/repos/{repo_owner}/{repo_name}/forks"
    headers = {'Authorization': f'token {API_TOKEN}'}

    while True:
        try:
            req = urllib.request.Request(f"{GITHUB_FORK_URL}?page={page}", headers=headers)
            resp = urllib.request.urlopen(req)
            forks_data = json.loads(resp.read())
        except urllib.error.HTTPError as e:
            if e.code == 404:
                break

        if not forks_data:
            break

        for fork in forks_data:
            append_data_to_csv([fork['owner']['login'], fork['ssh_url'], fork['created_at']], f'{repo_owner}_{repo_name}_forks.csv')

        page += 1

def main():
    print("Fetching forks...")
    repo_owner = "flutter"
    repo_name = "flutter"

    find_forks_and_append(repo_owner, repo_name)

    print("Fetching forks completed. Fork data saved to CSV file.")


if __name__ == "__main__":
    main()

