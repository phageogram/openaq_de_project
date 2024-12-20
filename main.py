import pandas as pd
import httpx
#import seaborn as sns
#import plotly.express as px
import io
import base64
import warnings
import os
from openaq import OpenAQ
from settings import Settings
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAQ-API-KEY")

#settings = Settings()
client = OpenAQ(api_key=api_key)

results = client.countries.list(limit=10)
data = results.results
#print(data[:1])

df = pd.DataFrame(data)

explode_df = df.explode("parameters")
print(df.head())

explode_df['parameters'] = explode_df.apply(lambda row: {**row['parameters'], 'location_code': row['id']}, axis=1)
explode_df = explode_df.reset_index(drop=True)

expanded_data = pd.json_normalize(explode_df['parameters'])
print(expanded_data.head())

merged_df = pd.merge(explode_df, expanded_data, left_on='id', right_on='location_code', how='left')
#merged_df = merged_df.reset_index(inplace=False)
merged_df = merged_df.drop("parameters", axis=1)
print(merged_df.head())

"""
normalized_df = pd.json_normalize(expanded_params_df["expanded_data"])

print(expanded_params_df.head())

print(normalized_df.head())
"""
#client.close()

#print(df.head())

#df.to_csv('out.csv', index=False)