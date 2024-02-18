import pandas as pd

def filter_github_repos(csv_file_path):
    """
    Filter GitHub repositories based on specified languages and return a list of repositories.

    Args:
    csv_file_path (str): The file path to the CSV file containing the GitHub repository data.

    Returns:
    list: A list of lists, where each inner list contains the username, repository name, and domain of a filtered repository.
    """
    # Read CSV data into a DataFrame
    data = pd.read_csv(csv_file_path)

    # Convert DataFrame to a list of dictionaries
    data_dict = data.to_dict(orient='records')

    # Filter out repositories with specified languages
    languages_to_exclude = ['CSS', 'HTML', 'R', 'PHP', 'PowerShell', 'MATLAB', 'Perl', 'Shell', 'TeX', 'Vim Script']
    data_dict = [item for item in data_dict if item['language'] and item['language'] not in languages_to_exclude]

    # Extract username and repository name, and store in a list
    list_of_repos = []
    for item in data_dict:
        username = item['username']
        repo_name = item['repo_name']
        domain = item['language']
        list_of_repos.append([username, repo_name, domain])

    additional_repos = [
        ['rmanguinho', 'clean-ts-api', 'TypeScript'],
        ['alexjoverm', 'typescript-library-starter', 'TypeScript'],
        ['nickmerwin', 'node-coveralls', 'JavaScript'],
        ['bsamseth', 'cpp-project', 'C++'],
        ['codecov', 'codecov-action', 'TypeScript'],
        ['Aeternalis-Ingenium', 'FastAPI-Backend-Template', 'Python'],
        ['codecov', 'codecov-node', 'JavaScript'],
        ['ryansonshine', 'typescript-npm-package-template', 'TypeScript']
    ]
    list_of_repos.extend(additional_repos)

    return list_of_repos

if __name__ == "__main__":
    # Example usage
    github_repos = filter_github_repos('../data/github-ranking-2024-02-15.csv')
    for repo in github_repos:
        print(f"{repo[0]}/{repo[1]}, {repo[2]}")
    # Example of output: pnpm/pnpm, TypeScript





