from datetime import datetime, timedelta
import pandas as pd

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

def retrieve_date_range_by_day(start_date, end_date):
    date_obj_list = pd.date_range(start_date, end_date).to_pydatetime().tolist()
    date_list = []

    for date_obj in date_obj_list:
        date_list.append(date_obj.date().strftime('%Y-%m-%d'))

    return date_list

if __name__ == "__main__":
    print(retrieve_date_range_by_day("2018-09-09", "2020-02-02"))