def append_data_to_csv(dataframe, csv_filename):
    try:
        # Load existing data from CSV file
        existing_data = pd.read_csv(csv_filename)

        # Append the new data to the existing data
        combined_data = pd.concat([existing_data, dataframe], ignore_index=True)

        # Save to CSV
        combined_data.to_csv(csv_filename, index=False)

        print(f"New data appended to '{csv_filename}' successfully.")
    except FileNotFoundError:
        print("CSV file not found. Creating a new CSV file...")
        dataframe.to_csv(csv_filename, index=False)
        print(f"New CSV file '{csv_filename}' created with the new data.")
        
def append_contributor_counts():
    dfpop = pd.read_csv("../data/Popularity_Reports_High_Star/WithPr_HighMar3Report.csv")
    dfpop['contributions'] = ''
    prevUser = ''
    prevRepo = ''
    dftemp = pd.DataFrame()
    for i in dfpop.index:
        username = dfpop['Username'][i]
        repo_name = dfpop['Repository'][i]
        filename = f'../data/contributorshigh/{username}_{repo_name}_contributors.csv'
        if not (os.path.isfile(filename)):
            continue
        if not (username == prevUser and repo_name == prevRepo):
            dftemp = pd.read_csv(filename)
            print(filename)
            print(dftemp['dates'])
            prevUser = username
            prevRepo = repo_name
        result = dftemp.loc[dftemp['dates'] == dfpop['Timestamp'][i], 'contributors']
        if not (result.size==0):
            print(result.values[0])
            dfpop.loc[i,'contributions'] = result.values[0]
    print(dfpop)
    filenamenew = "../data/Popularity_Reports_High_Star/WithPrandContributions_HighMar3Report.csv"
    append_data_to_csv(dfpop,filenamenew)
    dfpop = pd.read_csv("../data/Popularity_Reports_Low_Star/WithPr_LowMar5Report.csv")
    dfpop['contributions'] = ''
    prevUser = ''
    prevRepo = ''
    dftemp = pd.DataFrame()
    for i in dfpop.index:
        username = dfpop['Username'][i]
        repo_name = dfpop['Repository'][i]
        filename = f'../data/contributorslow/{username}_{repo_name}_contributors.csv'
        if not (os.path.isfile(filename)):
            continue
        if not (username == prevUser and repo_name == prevRepo):
            dftemp = pd.read_csv(filename)
            print(filename)
            print(dftemp['dates'])
            prevUser = username
            prevRepo = repo_name
        result = dftemp.loc[dftemp['dates'] == dfpop['Timestamp'][i], 'contributors']
        if not (result.size==0):
            print(result.values[0])
            dfpop.loc[i,'contributions'] = result.values[0]
    print(dfpop)
    filenamenew = "../data/Popularity_Reports_Low_Star/WithPrandContributions_LowMar5Report.csv"
    append_data_to_csv(dfpop,filenamenew)
    dfpop = pd.read_csv("../data/Popularity_Reports_Medium_Star/WithPr_MediumMar4Report.csv")
    dfpop['contributions'] = ''
    prevUser = ''
    prevRepo = ''
    dftemp = pd.DataFrame()
    for i in dfpop.index:
        username = dfpop['Username'][i]
        repo_name = dfpop['Repository'][i]
        filename = f'../data/contributorsmed/{username}_{repo_name}_contributors.csv'
        if not (os.path.isfile(filename)):
            continue
        if not (username == prevUser and repo_name == prevRepo):
            dftemp = pd.read_csv(filename)
            print(filename)
            print(dftemp['dates'])
            prevUser = username
            prevRepo = repo_name
        result = dftemp.loc[dftemp['dates'] == dfpop['Timestamp'][i], 'contributors']
        if not (result.size==0):
            print(result.values[0])
            dfpop.loc[i,'contributions'] = result.values[0]
    print(dfpop)
    filenamenew = "../data/Popularity_Reports_Medium_Star/WithPrandContributions_MediumMar4Report.csv"
    append_data_to_csv(dfpop,filenamenew)

if __name__ == "__main__":
    append_contributor_counts() 
    
