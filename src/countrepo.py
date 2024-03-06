import pandas as pd

# Assuming the data is stored in a CSV file named 'data.csv'
data = pd.read_csv('MediumMar4Report.csv')
# refinedRepoHighStars_612.csv
data = pd.read_csv('../data/refinedRepoLowStars_119.csv')

# Count the number of unique repositories
unique_repositories = data['repo_name'].nunique()

print("Number of unique repositories:", unique_repositories)

# import pandas as pd

# # Read the CSV file
# data = pd.read_csv('../data/refinedRepoMedStars_1255.csv')

# # Select unique repository names along with other columns
# unique_repo_data = data.drop_duplicates(subset=['repo_name'])

# # Save the unique repository data to a new CSV file
# unique_repo_data.to_csv('../data/unique_repo_data.csv', index=False)

# print("New CSV file with unique repository data has been created.")