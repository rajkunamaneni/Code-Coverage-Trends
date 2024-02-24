
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('../../data/FinalReport.csv')

# Define the original format string with milliseconds
original_format_string = '%Y-%m-%dT%H:%M:%S.%fZ'

# Define the parse_date function
def parse_date(date_string, format_string):
    try:
        return datetime.strptime(date_string, format_string)
    except ValueError:
        # If parsing with milliseconds fails, try parsing without milliseconds
        format_string_without_ms = '%Y-%m-%dT%H:%M:%SZ'
        return datetime.strptime(date_string, format_string_without_ms)

# Convert the 'Timestamp' column to datetime type using parse_date
df['Timestamp'] = df['Timestamp'].apply(lambda x: parse_date(x, original_format_string))

# Sort the DataFrame by 'Timestamp'
df = df.sort_values(by='Timestamp')

# Define the repository list
repositories_list = ["grafana"]

# Plot code coverage results for each repository in the list
plt.figure(figsize=(10, 6))
for repo_name in repositories_list:
    repository_df = df[df['Username'] == repo_name]
    plt.plot(repository_df['Timestamp'], repository_df['Percentage'], label=repo_name)

# Set labels and title
plt.xlabel('Time')
plt.ylabel('Percentage Change')
plt.title('Popularity Results Over Time (Selected Repositories)')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

# Show plot
plt.show()
