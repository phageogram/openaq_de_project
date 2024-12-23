import os
from dotenv import load_dotenv
from pipeline.api.client import OpenAQClient
from pipeline.processors.countries_processor import CountryProcessor
from pipeline.loaders.big_query_loader import BigQueryLoader

def run_pipeline(endpoint, table_id, limit=10):

    load_dotenv()

    google_credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if google_credentials_path is None:
        raise ValueError("Google credentials not in .env file")
    else:
        print(f"Google app credentials set to: {google_credentials_path}")

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_credentials_path
    
    API_KEY = os.getenv("OPENAQ-API-KEY")
    PROJECT_ID = os.getenv('PROJECT_ID')
    DATASET_ID = os.getenv('DATASET_ID')

    api_client = OpenAQClient(API_KEY)
    loader = BigQueryLoader(PROJECT_ID, DATASET_ID, table_id)

    try:
        # Get data
        data = api_client.fetch_data(endpoint, limit=limit)

        if endpoint == "countries":
            processor = CountryProcessor(data)
        # Add future processors here
        else:
            raise ValueError(f"No processor defined for endpoint: {endpoint}")

        processed_data = processor.process()

        # Load data
        loader.load_data(processed_data)
    
    finally:
        api_client.close()
    
if __name__ == "__main__":
    run_pipeline(endpoint="countries", table_id="countries", limit=10)