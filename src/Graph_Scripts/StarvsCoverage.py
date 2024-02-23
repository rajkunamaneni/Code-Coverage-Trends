import pandas as pd
import matplotlib.pyplot as plt
import re

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('../../data/FinalReport.csv')

data = {
    "Very High Star Count Repositories": ["airbnb", "facebook"],
    "High Star Count Repositories": ["RocketChat", "date-fns", "metabase", "tqdm", "axios", "dzenbot", "halfrost", "beego", "go-kratos", "getsentry", "chartjs", "go-gorm", "grafana", "parcel-bundler", "swoole", "go-gitea", "valyala", "rapid7", "apache", "grpc", "vapor", "lsd-rs", "felangel", "nsqio", "alibaba", "brettwooldridge", "dromara", "k3s-io", "toeverything", "pingcap", "babel", "mojs", "openssl", "mybatis", "photoprism", "mislav", "AdguardTeam", "SDWebImage", "dandavison", "encode", "Moya", "dapr", "istio", "n8n-io", "typeorm", "forem", "jestjs", "ant-design", "freeCodeCamp", "charmbracelet", "Tencent", "RustPython", "fastlane", "certbot", "jedisct1", "videojs", "TryGhost", "urfave", "keepassxreboot", "goharbor", "jesseduffield", "xi-editor", "diem", "httpie"],
    "Medium Star Count Repositories": ["krzysztofzablocki", "JuliaPlots", "ueberauth", "zio", "monix", "jogboms", "react-hook-form", "DioxusLabs", "sksamuel", "spark-jobserver", "ThreeMammals", "circe", "mozilla-mobile", "reactiveui", "bitwalker", "timholy", "rrousselGit", "JuliaSymbolics", "brianegan", "Cocoanetics", "luarocks", "elixir-wallaby", "IFTTT", "roughike", "mojotech", "mockk", "twitter-archive", "JuliaPy", "lukepighetti", "thechangelog", "mesosphere", "ReSwift", "twitter", "esp8266", "salesforce", "github", "gnachman", "Hammerspoon", "chef", "pry", "whatyouhide", "firezone", "opf", "activeadmin", "finagle", "isar", "QuantConnect", "hiddentao", "ruby-grape", "fthomas", "cesanta", "tekartik", "tgstation", "whitfin", "node-cache", "calcom", "facebookarchive", "wireapp", "sparkle-project", "duplicati", "kickstarter", "mossr", "chocolatey", "rust-lang", "fzyzcjy", "omniauth", "colinhacks", "alexjoverm", "schollz", "zetbaitsu", "danielgtaylor", "ReactiveX", "jump-dev", "ankidroid", "microsoft"],
    "Low Star Count Repositories": ["dianping", "Transmode", "pledbrook", "fossas", "cstjean", "chengchingwen", "JuliaGraphics", "elixir-tesla", "JuliaStats", "ihub-pub", "FRBNY-DSGE", "joshday", "ryansonshine", "jonathan-laurent", "allegro", "JuliaParallel", "nebula-plugins", "AlgebraicJulia", "pluskid", "boennemann", "JuliaCI", "JuliaCN", "openbakery", "ash-project", "JuliaDynamics", "JuliaInterop", "reanimate", "PainterQubits", "mcabbott", "SciML", "JuliaIO", "JuliaApproximation", "JuliaMath", "weymouth", "JuliaCollections"]
}

# Define the list of repositories
# repositories_list = data["Medium Star Count Repositories"]
repositories_list = ["grafana", "videojs",  "keepassxreboot", "Tencent"]

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