import os
from dotenv import load_dotenv
from pipeline.api.client import OpenAQClient
from pipeline.processors.countries_processor import CountryProcessor
from pipeline.loaders.big_query_loader import BigQueryLoader

load_dotenv()

API_KEY = os.getenv("OPENAQ-API-KEY")
PROJECT_ID = PROJECT_ID
DATASET_ID = DATASET_ID

def run_pipeline(endpoint, table_id, limit=10):
    api_client = OpenAQClient(API_KEY)
    loader = BigQueryLoader(PROJECT_ID, DATASET_ID, table_id)

    try:
        # Get data
        data = api_client.fetch_data(endpoint, limit=limit)

        if endpoint == "countries":
            processor = CountryProcessor(raw_data)
        # Add future processors here
        else:
            raise ValueError(f"No processor defined for endpoint: {endpoint}")

        processed_data = processor.process()

        # Load data
        loader.load_data(processed_data)
    
    finally:
        api_client.close()
    
if __name__ == "__main__":
    run_pipeline(endpoint=="countries", table_id="countries_table", limit=10)
    run_pipeline(endpoint="locations", table_id="locations_table", limit=10)