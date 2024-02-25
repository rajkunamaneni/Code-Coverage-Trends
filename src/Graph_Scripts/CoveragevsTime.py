
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

# # Define the repository list
# username  = "fossas"
# repo = "fossa-cli"

data = ["RocketChat", "date-fns", "metabase", "tqdm", "axios", "dzenbot", "halfrost", "beego", "go-kratos", "getsentry", "chartjs", "go-gorm", "grafana", "parcel-bundler", "swoole", "go-gitea", "valyala", "rapid7", "apache", "grpc", "vapor", "lsd-rs", "felangel", "nsqio", "alibaba", "brettwooldridge", "dromara", "k3s-io", "toeverything", "pingcap", "babel", "mojs", "openssl", "mybatis", "photoprism", "mislav", "AdguardTeam", "SDWebImage", "dandavison", "encode", "Moya", "dapr", "istio", "n8n-io", "typeorm", "forem", "jestjs", "ant-design", "freeCodeCamp", "charmbracelet", "Tencent", "RustPython", "fastlane", "certbot", "jedisct1", "videojs", "TryGhost", "urfave", "keepassxreboot", "goharbor", "jesseduffield", "xi-editor", "diem", "httpie"]
    


#2021-2024
fromcsv  = ['AdguardTeam', 'apache', 'JuliaCI', 'jump-dev', 'videojs', 'weymouth', 'grafana', 'JuliaSymbolics', 'ihub-pub', 'keepassxreboot', 'microsoft', 'Tencent', 'kickstarter', 'allegro']

newList = []
for i in fromcsv:
    if i in data:
        newList.append(i)

print(newList)
repositories_list = ['AdguardTeam', 'videojs', 'grafana', 'keepassxreboot', 'Tencent']

# Plot code coverage results for each repository in the list
plt.figure(figsize=(10, 6))
for repo_name in repositories_list:
    repository_df = df[df['Username'] == repo_name]
    plt.plot(repository_df['Timestamp'], repository_df['Percentage'], label=repo_name)

# Set labels and title
plt.xlabel('Time')
plt.ylabel('Code Percentage Change')
# plt.title(f'Popularity Results Over Time {username}/{repo} Repository')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

# Show plot
plt.show()
