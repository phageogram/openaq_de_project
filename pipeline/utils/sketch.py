from pipeline.api.client import OpenAQClient  # Adjust the import path to your OpenAQClient class'
from pipeline.api.exceptions import APIClientError
import os
from ratelimit import sleep_and_retry, limits

@sleep_and_retry
@limits(calls=1, period=60)
def test_openaq_client():
    # Retrieve the API key from environment variables (or hardcode it for testing purposes)
    api_key = os.getenv("OPENAQ_API_KEY")  # Make sure your environment variable is set or replace with your key
    
    # Create an instance of OpenAQClient
    client = OpenAQClient(api_key)
    
    try:
        # Fetch data from the "locations" endpoint
        locations = client.fetch_data(endpoint="locations")
        
        # Print the results
        print("Locations:", locations)
    
    except ValueError as e:
        print(f"Error: {e}")
    
    finally:
        # Ensure the client is closed after the test
        client.close()

if __name__ == "__main__":
    test_openaq_client()
