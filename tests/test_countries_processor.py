import os
import pandas as pd
import pytest
from pipeline.api.client import OpenAQClient
from pipeline.processors.countries_processor import CountryProcessor
from dotenv import load_dotenv

load_dotenv()

# Open API connection (persistent)
# OpenAQ API is persistent (httpx), must be closed explicitly
@pytest.fixture(scope="session")
def api_client():
    load_dotenv()
    api_key = os.getenv("OPENAQ-API-KEY")
    client = OpenAQClient(api_key=api_key)

    # provide client to tests
    yield client

    # cleanup after tests have completed
    client.close()

@pytest.fixture
def country_df(api_client):
    sample_data = api_client.fetch_data(endpoint="countries", limit=1)
    return pd.DataFrame(sample_data)

def test_country_response(country_df):
    # Test for Parameters column
    assert "parameters" in list(country_df.columns)
    assert country_df["parameters"].dtype == object

def test_country_processor(country_df):
    
    # Transform data for load
    processor = CountryProcessor(country_df)
    new_df = processor.process()

    # tests
    assert list(new_df.columns) == [
        "id",
        "code",
        "name",
        "datetime_first",
        "datetime_last",
        "param_id",
        "param_name",
        "units",
        "display_name"
        ]
    assert "ID" in new_df["code"].unique()
    assert len(new_df["param_name"].unique()) == 12