import pandas as pd
from pydriller import Repository

def get_contributor_counts(repo_name,repo_owner,repo_link):
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
    filename = f'{repo_owner}_{repo_name}_contributors.csv'
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

if __name__ == "__main__":
    get_contributor_counts("flutter","flutter",'https://github.com/flutter/flutter.git')
