import pandas as pd
import math
import matplotlib.pyplot as plt
import seaborn as sns

# Read the CSV file into a DataFrame
df = pd.read_csv("../data/AddOrRemoveReport.csv")

repo = "lsd-rs/lsd"

# Filter the DataFrame for the repository "grafana"
grafana_df = df[df["Username"] == "lsd-rs"]

# Select only the required columns for correlation
selected_columns = ["Percentage", "Star_Count", "Additions", "Deletions",]
selected_df = grafana_df[selected_columns]
sns.heatmap(selected_df.corr().round(2), annot=True, cmap="vlag", linewidths=0.5, vmin=-1, vmax=1, center=0)
plt.title(f"Correlation Matrix for {repo} Repository")
plt.show()
