import requests
from datetime import datetime


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
    response = requests.get(base_url, params=params, headers=headers, verify=True)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract the JSON response
        data = response.json()
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


def format_dates(original_date_string):
    """
    Description:
    This function takes a list of date strings in the format '%Y-%m-%dT%H:%M:%SZ', converts them into datetime objects, and then formats them as strings in the format '%d-%m-%Y'. It returns a list of formatted date strings.

    Parameters:
    - dates (list): A list of date strings in the format '%Y-%m-%dT%H:%M:%SZ'.

    Returns:
    - date_list (list): A list of formatted date strings in the format '%d-%m-%Y'.
    """

    try:
        # Define format string for parsing with milliseconds as optional
        format_string = '%Y-%m-%dT%H:%M:%S.%fZ'
        
        # Try parsing with milliseconds
        try:
            original_date = datetime.strptime(original_date_string, format_string)
        except ValueError:
            # If parsing with milliseconds fails, try parsing without milliseconds
            format_string = '%Y-%m-%dT%H:%M:%SZ'
            original_date = datetime.strptime(original_date_string, format_string)
        
        # Format the date as 'day-month-year'
        formatted_date = original_date.strftime('%d-%m-%Y')
        
        return formatted_date
    except ValueError:
        return "Invalid Date Format"

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
    print(format_dates('2020-01-06T13:03:15.666470Z'))

    # output = get_star_data('rajkunamaneni', 'TrafficDetector', ["06-03-2015", "16-01-2024", "15-02-2024", "17-02-2024"])
    # print(output)
