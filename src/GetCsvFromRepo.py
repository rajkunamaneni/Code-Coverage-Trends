from datetime import datetime
import os
import pandas as pd
from Graphql import get_graphql_data
import inspect

class ProcessorGQL(object):
    def __init__(self, bulk_count_in, bulk_size_in, languages, search_param, sort_param):
        self.search_param = search_param
        self.sort_param = sort_param
        self.gql_format = """query{
    search(query: "%s", type: REPOSITORY, first:%d %s) {
      pageInfo { endCursor }
                edges {
                    node {
                        ...on Repository {
                            id
                            name
                            url
                            forkCount
                            stargazers {
                                totalCount
                            }
                            owner {
                                login
                            }
                            description
                            pushedAt
                            primaryLanguage {
                                name
                            }
                            openIssues: issues(states: OPEN) {
                                totalCount
                            }
                        }
                    }
                }
            }
        }
        """
        self.bulk_count = bulk_count_in
        self.bulk_size = bulk_size_in
        string_val = f"language:%s {self.search_param} {self.sort_param}"
        self.gql_stars_lang = self.gql_format % (string_val, self.bulk_size, "%s")
        self.languages = languages

    @staticmethod
    def parse_gql_result(result):
        res = []
        for repo in result["data"]["search"]["edges"]:
            repo_data = repo['node']
            res.append({
                'name': repo_data['name'],
                'stargazers_count': repo_data['stargazers']['totalCount'],
                'forks_count': repo_data['forkCount'],
                'language': repo_data['primaryLanguage']['name'] if repo_data['primaryLanguage'] is not None else None,
                'html_url': repo_data['url'],
                'owner': {
                    'login': repo_data['owner']['login'],
                },
                'open_issues_count': repo_data['openIssues']['totalCount'],
                'pushed_at': repo_data['pushedAt'],
            })
        return res

    def get_repos(self, qql):
        cursor = ''
        repos = []
        for i in range(0, self.bulk_count):
            repos_gql = get_graphql_data(qql % cursor)
            pageInfoEndCursor = repos_gql["data"]["search"]["pageInfo"]["endCursor"]

            if pageInfoEndCursor is not None:
                cursor = ', after:"' + pageInfoEndCursor + '"'
                repos += self.parse_gql_result(repos_gql)
        return repos

    def get_all_repos(self):
        repos_languages = {}
        for lang in self.languages:
            print("Getting repos of {}...".format(lang))
            repos_languages[lang] = self.get_repos(self.gql_stars_lang % (lang, '%s'))
            print("Getting repos of {} success!".format(lang))
        return repos_languages

class WriteFile(object):
    def __init__(self, repos_languages, bulk_count, bulk_size, languages):
        self.col = ['rank', 'item', 'repo_name', 'stars', 'forks', 'language', 'repo_url', 'username', 'issues', 'last_commit']
        self.repo_list = []
        self.bulk_count = bulk_count
        self.bulk_size = bulk_size
        for i in range(len(languages)):
            lang = languages[i]
            self.repo_list.append({
                "data": repos_languages[lang],
                "item": lang,
            })

    def repo_to_df(self, repos, item):
        repos_list = []
        for idx, repo in enumerate(repos):
            repo_info = [idx + 1, item, repo['name'], repo['stargazers_count'], repo['forks_count'], repo['language'],
                         repo['html_url'], repo['owner']['login'], repo['open_issues_count'], repo['pushed_at']]
            repos_list.append(repo_info)
        return pd.DataFrame(repos_list, columns=self.col)

    def save_to_csv(self, processor):
        df_all = pd.DataFrame(columns=self.col)
        for repo in self.repo_list:
            df_repos = self.repo_to_df(repos=repo["data"], item=repo["item"])
            df_all = pd.concat([df_all, df_repos], ignore_index=True)

        save_date = datetime.utcnow().strftime("%Y-%m-%d")
        os.makedirs('../data/Data', exist_ok=True)

        num_of_repo_per_lang = self.bulk_count * self.bulk_size
        csv_path = '../data/Data/github-ranking-'
        search_param_filename = str(processor.search_param).translate({ord(c): None for c in '\/:*?<>|'})
        sort_param_filename = str(processor.sort_param).translate({ord(c): None for c in '\/:*?<>|'})

        csv_path_name = csv_path + save_date + '_' + str(num_of_repo_per_lang) + '_' \
                        + search_param_filename + '_' + sort_param_filename + '.csv'
        df_all.to_csv(csv_path_name, index=False, encoding='utf-8')
        print('Saved repository data to: ' + csv_path_name)

def run_by_gql(num_of_repo_per_lang, languages, search_param, sort_param):
    bulk_size = 50
    bulk_count = int(num_of_repo_per_lang / bulk_size)

    processor = ProcessorGQL(bulk_count, bulk_size, languages, search_param, sort_param)
    repos_languages = processor.get_all_repos()
    wt_obj = WriteFile(repos_languages, bulk_count, bulk_size, languages)
    wt_obj.save_to_csv(processor)

if __name__ == "__main__":
    languages = ["ActionScript", "C", "CSharp", "CPP", "CoffeeScript", "Dart", "Go", "Java", "JavaScript",
                 "Objective-C", "Python", "PHP", "R", "Swift", "TypeScript"]
    num_of_repo_per_lang = 50
    search_param = "stars:>10"
    sort_param = "sort:stars-asc"
    run_by_gql(num_of_repo_per_lang, languages, search_param, sort_param)