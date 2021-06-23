import pandas as pd

dataframe = pd.read_csv('../object_list.csv')

for index in [2,5,8]:
    print(dataframe.iloc[index,0])