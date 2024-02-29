import requests
import DateUtil

def get_star_data(username, repo_name, dates):
    """
    Fetches data for a given repository from the Daily Stars Explorer API.
    https://emanuelef.github.io/daily-stars-explorer/
    
    Args:
    - username (str): The username or organization name on GitHub.
    - repo_name (str): The name of the repository in the format "owner/repository".
    - dates (list): A list of dates in the format "dd-mm-yyyy" for which to fetch the star count.
    
    Returns:
    - list or None: A list containing data for the repository if the request was successful, 
      otherwise returns None.

    Example:
    >>> get_repo_data("flutter", "flutter", ["16-01-2024", "15-02-2024"])
    [['06-03-2015', 0], ['07-03-2015', 0], ['08-03-2015', 0], ...]
    """
    # Define the base URL
    base_url = "https://143.47.235.108:8090/allStars"

    # Set the User-Agent header to mimic a browser or any other client
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    # Define the parameters
    params = {"repo": f"{username}/{repo_name}"}

    # Make the GET request with certificate verification
    response = requests.get(base_url, params=params, headers=headers, verify=True, timeout=200)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract the JSON response
        if response.ok:
            data = response.json()
        else:
            print("Failed to fetch data. Issue occur.")
            return None
        # Initialize result with provided dates
        result = [[date, None] for date in dates]
        # Update star counts if available
        for item in data['stars']:
            if item[0] in dates:
                # Find the index of the date in result list and update its star count
                idx = dates.index(item[0])
                result[idx][1] = item[2]
        return result
        
    else:
        # Print an error message if the request was unsuccessful
        print(f"Error fetching data for repository {repo_name}: {response.status_code}")
        return None
    
def get_daily_star_data(username, repo_name, dates):
    """
    Fetches data for a given repository from the Daily Stars Explorer API.
    https://emanuelef.github.io/daily-stars-explorer/

    Args:
    - username (str): The username or organization name on GitHub.
    - repo_name (str): The name of the repository in the format "owner/repository".
    - dates (list): A list of dates in the format "dd-mm-yyyy" for which to fetch the star count.

    Returns:
    - list or None: A list containing data for the repository if the request was successful, 
        otherwise returns None.

    Example:
    >>> get_repo_data("flutter", "flutter", ["16-01-2024", "15-02-2024"])
    [['06-03-2015', 0], ['07-03-2015', 0], ['08-03-2015', 0], ...]
    """
    # Define the base URL
    base_url = "https://143.47.235.108:8090/allStars"

    # Set the User-Agent header to mimic a browser or any other client
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    # Define the parameters
    params = {"repo": f"{username}/{repo_name}"}

    # Make the GET request with certificate verification
    response = requests.get(base_url, params=params, headers=headers, verify=True, timeout=200)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract the JSON response
        if response.ok:
            data = response.json()
        else:
            print("Failed to fetch data. Issue occur.")
            return None
        # Initialize result with provided dates
        result = [[date, None] for date in dates]
        # Update star counts if available
        for item in data['stars']:
            if item[0] in dates:
                # Find the index of the date in result list and update its star count
                idx = dates.index(item[0])
                result[idx][1] = item[1]
        return result
        
    else:
        # Print an error message if the request was unsuccessful
        print(f"Error fetching data for repository {repo_name}: {response.status_code}")
        return None

if __name__ == "__main__":
    # Example usage
    repository_names = [["flutter", "flutter"], ["tensorflow", "tensorflow"], ["facebook", "react"]]
    dates = ["06-03-2015", "16-01-2024", "15-02-2024", "17-02-2024"]

    for repo_name in repository_names:
        repo = f"{repo_name[0]}/{repo_name[1]}" #username/repo_name path
        print(f"Fetching data for repository: {repo} (GitHub link: https://github.com/{repo})")
        data = get_star_data(repo_name[0], repo_name[1], dates)
        if data:
            print(data)
        print()

    # Example usage
    print(DateUtil.format_dates('2020-01-06T13:03:15.666470Z'))

    # output = get_star_data('rajkunamaneni', 'TrafficDetector', ["06-03-2015", "16-01-2024", "15-02-2024", "17-02-2024"])
    # print(output)
