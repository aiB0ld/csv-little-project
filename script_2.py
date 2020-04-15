import csv
import pandas as pd

path1 = "/Users/scottwang/Desktop/Personal/L/3.0/POM_HQIIS_May2019_Original.csv"
path2 = "/Users/scottwang/Desktop/Personal/L/3.0/Category_Finalized.csv"

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
path3 = '/Users/scottwang/Desktop/Personal/L/3.0/result.csv'
path4 = '/Users/scottwang/Desktop/Personal/L/3.0/result_SF.csv'

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


# --------------------------------------------------------
assetConfig_result = []
with open(path3, 'rt') as f:
    asset = csv.reader(f)
    for i in asset:
        assetConfig_result.append(i)

count_map1 = {}
for i in range(1, 22):
    if (i in range(13,18) or i in range(19,20)):
        continue
    count = 0
    for item in assetConfig_result:
        if (item[25] == "Category" or item[25] == ''):
            continue
        if (float(item[25]) == i):
            count = count + 1
    count_map1[i] = count
count_df1 = pd.DataFrame(list(count_map1.items()), columns=['Facility group', 'count facility group'])
count_df1.set_index('Facility group',inplace=True)

assetConfig_SF_result = []
with open(path4, 'rt') as f:
    asset = csv.reader(f)
    for i in asset:
        assetConfig_SF_result.append(i)

sum_map = {}
min_map = {}
max_map = {}
count_map = {}
ave_map = {}
for i in range(1, 22):
    if (i in range(13,18) or i in range(19,20)):
        continue
    sum = 0.0
    min = 1000000000.0
    max = 0.0
    count = 0
    for item in assetConfig_SF_result:
        if (item[25] == "Category" or item[25] == ''):
            continue
        if (float(item[25]) == i):
            sum += float(item[21])
            count = count + 1
            if (float(item[21]) < min):
                min = float(item[21])
            if (float(item[21]) > max):
                max = float(item[21])
    if (count == 0):
        ave_map[i] = 0.0
        min_map[i] = 0.0
    if (count != 0):
        ave_map[i] = round(float(sum) / count, 1)
        min_map[i] = min
    sum_map[i] = sum
    max_map[i] = max
    count_map[i] = count

count_df = pd.DataFrame(list(count_map.items()), columns=['Facility group', 'count facility group with SF'])
min_df = pd.DataFrame(list(min_map.items()), columns=['Facility group', 'Min SF with SF'])
max_df = pd.DataFrame(list(max_map.items()), columns=['Facility group', 'Max SF with SF'])
ave_df = pd.DataFrame(list(ave_map.items()), columns=['Facility group', 'Avg SF with SF'])
sum_df = pd.DataFrame(list(sum_map.items()), columns=['Facility group', 'total SF with SF'])

count_df.set_index('Facility group',inplace=True)
min_df.set_index('Facility group',inplace=True)
max_df.set_index('Facility group',inplace=True)
ave_df.set_index('Facility group',inplace=True)
sum_df.set_index('Facility group',inplace=True)
# result_df = pd.DataFrame.merge(count_df,min_df, on='Category')
result_df = pd.concat([count_df1, count_df,sum_df,max_df,min_df,ave_df],axis=1,sort=False).reset_index()

# print (count_df)
print (result_df)
# column = result_df[0]
# result_df.columns=column
# result_df=result_df.drop(0)
result_df.to_csv('/Users/scottwang/Desktop/Personal/L/3.0/count_result.csv',index=False)

