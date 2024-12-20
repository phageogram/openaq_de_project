import pandas as pd
import os
from openaq import OpenAQ
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAQ-API-KEY")


class CountryTable:
    def __init__(self, api_key):
        self.client = OpenAQ(api_key=api_key)
        self.data = None

    def __enter__(self):
        # returns runtime context for this object
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Exit runtime context and clean up
        self.close()

    def get_countries(self, limit):
        # Fetch 10 countries attributes from the OpenAQ API
        results = self.client.countries.list(limit=limit)
        self.data = results.results
        return self.data

    def explode_parameters(self):
        # Process nested parameters column
        if self.data is not None:
            explode_df = self.data.explode("parameters")
            explode_df['parameters'] = explode_df.apply(lambda row: {**row['parameters'], 'location_code': row['id']}, axis=1)
        else:
            raise ValueError("Data is not loaded, call get_countries first.")
            
    def normalize_and_merge(self):
        #Normalize 'parameters' and merge with the original data.
        exploded_df = self.explode_parameters()
        expanded_data = pd.json_normalize(exploded_df['parameters'])
        merged_df = pd.merge(exploded_df, expanded_data, left_on='id', right_on='location_code', how='left')
        merged_df = merged_df.drop(["parameters", "location_code"], axis=1)
        merged_df.rename(columns={"id_x": "country_id", "name_x": "country_name", "id_y": "param_id", "name_y": "param_name"}, inplace=True)
        return merged_df

    def display_data(self):
        """Display the current state of the data."""
    if self.data is not None:
        return self.data.head()
    else:
        raise ValueError("Data is not loaded. Please call get_countries() first.")

    def close(self):
        # Close httpx connection to OpenAQ
        self.client.close()

