import pandas as pd
import math

# Read the CSV file into a DataFrame
df = pd.read_csv("../../data/AddOrRemoveReport.csv")

# Filter the DataFrame for the repository "grafana"
grafana_df = df[df["Username"] == "lsd-rs"]

# Select only the required columns for correlation
selected_columns = ["Percentage", "Star_Count", "Additions", "Deletions",]
selected_df = grafana_df[selected_columns]

# Calculate correlation matrix
correlation_matrix = selected_df.corr()

print(correlation_matrix)
