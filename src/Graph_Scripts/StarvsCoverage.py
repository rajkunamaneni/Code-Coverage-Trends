import pandas as pd
import matplotlib.pyplot as plt
import re

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('../../data/FinalReport.csv')

# Define the list of repositories
repositories_list = ["nsqio"]

# Filter the DataFrame for the specified repositories
filtered_df = df[df['Username'].isin(repositories_list)]

# Plot star count vs percentages for the filtered DataFrame
plt.figure(figsize=(10, 6))
for repo_name in repositories_list:
    repo_data = filtered_df[filtered_df['Username'] == repo_name]
    plt.scatter(repo_data['Star_Count'], repo_data['Percentage'], label=repo_name, alpha=0.5)

plt.title('Star Count vs Percentages for Selected Repositories')
plt.xlabel('Star Count')
plt.ylabel('Percentage')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()