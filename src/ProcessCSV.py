import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('output.csv')

# Get all unique usernames
unique_usernames = df['Repository'].unique()

print(unique_usernames)