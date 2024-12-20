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
df = pd.DataFrame(data)
client.close()

print(df.head())

df.to_csv('out.csv', index=False)