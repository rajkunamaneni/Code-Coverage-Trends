import requests

def get_repo_data(repo_name):
    """
    Fetches data for a given repository from the Daily Stars Explorer API.
    https://emanuelef.github.io/daily-stars-explorer/
    
    Args:
    - repo_name (str): The name of the repository in the format "owner/repository".

    Returns:
    - list or None: A list containing data for the repository if the request was successful, 
      otherwise returns None.

    Example:
    >>> get_repo_data("flutter/flutter")
    [['06-03-2015', 0, 0], ['07-03-2015', 0, 0], ['08-03-2015', 0, 0], ...]
    """
    # Define the base URL
    base_url = "https://143.47.235.108:8090/allStars"

    # Set the User-Agent header to mimic a browser or any other client
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    # Define the parameters
    params = {"repo": repo_name}

    # Make the GET request with certificate verification
    response = requests.get(base_url, params=params, headers=headers, verify=True)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract the JSON response
        return response.json()
    else:
        # Print an error message if the request was unsuccessful
        print(f"Error fetching data for repository {repo_name}: {response.status_code}")
        return None

if __name__ == "__main__":
    # Example usage
    repository_names = ["flutter/flutter", "tensorflow/tensorflow", "facebook/react"]
    dates = ["06-03-2015", "16-01-2024", "15-02-2024", "16-02-2024"]

    # Fetch data for all repositories
    repo_data = {repo_name: get_repo_data(repo_name) for repo_name in repository_names}

    # Filter data based on dates
    for repo_name, data in repo_data.items():
        filtered_data = [item for item in data if item[0] in dates]
        print(f"Data for repository {repo_name}:")
        print(filtered_data)
        print()