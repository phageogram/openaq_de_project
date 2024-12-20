import pandas as pd
import json
from pandas import json_normalize

df = pd.read_csv('out.csv')
#print(df.head())
#print(df["parameters"].apply(type).value_counts())

df["parameters"] = df["parameters"].str.replace("'", '"')
df["parameters"] = df["parameters"].apply(json.loads)

expanded_params = df["parameters"].explode()
print(expanded_params.head())
normalized_df = json_normalize(expanded_params)

#print(normalized_df.head())

