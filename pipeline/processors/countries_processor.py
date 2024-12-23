import pandas as pd
from .base_processor import BaseProcessor

class CountryProcessor(BaseProcessor):
    
    def process(self):
        # Explode and normalize data
        if "parameters" not in self.data.columns:
            raise ValueError("Missing 'parameters' column")
        if self.data is None:
            raise ValueError("No response")
        
        exploded_df = self.data.explode("parameters")
        explode_df['parameters'] = explode_df.apply(lambda row: {**row['parameters'], 'location_code': row['id']}, axis=1)
        expanded_params = pd.json_normalize(exploded_df["parameters"])

        merged_df = pd.merge(
            exploded_df, expanded_data, left_on='id', right_on='location_code', how="left"
        )

        merged_df.drop(["parameters", "location_code"], axis=1, inplace=True)
        return merged_df