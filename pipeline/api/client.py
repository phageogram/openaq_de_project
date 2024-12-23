from .exceptions import APIClientError
from openaq import OpenAQ

class OpenAQClient:
    def __init__(self, api_key):
        self.client = OpenAQ(api_key=api_key)

    def fetch_data(self, endpoint, **params):
        try:
            if endpoint == "countries":
                response = self.client.countries.list(**params)
            elif endpoint == "locations":
                response = self.client.countries.list(**params)
            elif endpoint == "measurements":
                response = self.client.measurements.list(**params)
            elif endpoint == "parameters":
                response = self.client.parameters.list(**params)
            else:
                raise ValueError(f"Unknown endpoint: {endpoint}")
            return response.results
        except Exception as e:
            raise APIClientError(f"API request failed {str(e)}")
    
    def close(self):
        # handle API client
        self.client.close()