from pydriller import Repository

def retrieve_commit_hashes(username, repo_name):
    """
    Retrieve commit hashes for a given GitHub repository.

    Parameters:
        username (str): The username or organization name on GitHub.
        repo_name (str): The name of the repository on GitHub.

    Returns:
        list: A list of list containing the commit hash and commit date.
    """
    repo_url = f'https://github.com/{username}/{repo_name}'
    print(f'Repository URL: {repo_url}')

    commits_info = []
    for commit in Repository(repo_url, only_releases=True).traverse_commits():
        commits_info.append([commit.hash, commit.author_date.strftime("%Y-%m-%d %H:%M:%S %Z")])
        # print(commit.hash, commit.msg, commit.author.name, commit.author_date, commit.committer.name, commit.committer_date)

    print(f'Total Release Tags: {len(commits_info)}')

    return commits_info

if __name__ == "__main__":
    username = 'rajkunamaneni'
    repo_name = 'TrafficDetector'
    commit_hashes = retrieve_commit_hashes(username, repo_name)
    for i in commit_hashes:
        print(i)