import csv
import pandas as pd

path1 = "/Users/scottwang/Desktop/Personal/L/2.0/POM_HQIIS_May2019_Original.csv"
path2 = "/Users/scottwang/Desktop/Personal/L/2.0/Category_Finalized.csv"

# Define lists for data
# Raw facility data
assetConfig = []
# Category list
category = []
# facility results with category number
assetConfig_copy = []
# Facilities with unite SF
assetConfig_copy2 = []

# Input data
with open(path1, 'rt') as f1, open(path2,'rt') as f2:
    asset = csv.reader(f1)
    ctg = csv.reader(f2)
    for i in asset:
        assetConfig.append(i)
    for j in ctg:
        category.append(j)


    for item in assetConfig:
        # Copy header
        if item[0] == 'AssetConfigQry' or item[0] == 'Accountable Organization':
            assetConfig_copy.append(item)
            continue
        # Check "Active" and assign category number
        if item[10] == 'Active':
            for item2 in category:
                if item[17].startswith(item2[2]):
                    item[25] = item2[0]
                    break
            assetConfig_copy.append(item)

    for item in assetConfig:
        if item[0] == 'AssetConfigQry' or item[0] == 'Accountable Organization':
            assetConfig_copy2.append(item)
            continue
        # Check "SF"
        if item[10] == 'Active' and item[22] == 'SF':
            for item2 in category:
                if item[17].startswith(item2[2]):
                    item[25] = item2[0]
                    break
            assetConfig_copy2.append(item)

# Output Data
path3 = '/Users/scottwang/Desktop/Personal/L/2.0/result.csv'
path4 = '/Users/scottwang/Desktop/Personal/L/2.0/result_SF.csv'

config=pd.DataFrame(assetConfig_copy)
column=assetConfig_copy[0]
config.columns=column
config=config.drop(0)
config.to_csv(path3,index=False)

config2=pd.DataFrame(assetConfig_copy2)
column=assetConfig_copy2[0]
config2.columns=column
config2=config2.drop(0)
config2.to_csv(path4,index=False)


# Count Cat
data = pd.read_csv(path3)
data_SF = pd.read_csv(path4)

data_result = data['Category'].value_counts()
# Change data type to dataframe
data_result = pd.DataFrame(data_result)
# print (data_result)

data_SF_result = data_SF['Category'].value_counts()
data_SF_result = pd.DataFrame(data_SF_result)
# print (data_SF_result)

# Inner join data_result and data_SF_result
result = pd.concat([data_result, data_SF_result], axis=1)
# print (result)
result.to_csv('/Users/scottwang/Desktop/Personal/L/2.0/count_result.csv',header=None)