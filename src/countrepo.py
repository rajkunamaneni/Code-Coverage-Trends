import pandas as pd

# Assuming the data is stored in a CSV file named 'data.csv'
data = pd.read_csv('Mar3Report.csv')

# Count the number of unique repositories
unique_repositories = data['Repository'].nunique()

print("Number of unique repositories:", unique_repositories)
