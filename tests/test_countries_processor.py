import os
import pandas as pd
from pipeline.api.client import OpenAQClient
from pipeline.processors.countries_processor import CountryProcessor
from dotenv import load_dotenv

load_dotenv()

def test_country_processor():
    api_key = os.getenv("OPENAQ-API-KEY")
    client = OpenAQClient(api_key=api_key)
    sample_data = client.fetch_data(endpoint="countries", limit=1)
    df = pd.DataFrame(sample_data)
    processor = CountryProcessor(df)
    new_df = processor.process()
    print(new_df.head())
    assert new_df[0][0] == 1

test_country_processor()