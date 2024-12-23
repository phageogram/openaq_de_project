import pandas as pd
import json
from .base_processor import BaseProcessor

class CountryProcessor(BaseProcessor):
    def __init__(self,data):
        super().__init__(data)
    
    def process(self):
        # Explode and normalize data
        self.validate_data()

        if "parameters" not in self.data.columns:
            raise ValueError("Missing 'parameters' column")
        if self.data is None:
            raise ValueError("No response")

        df =  pd.DataFrame(self.data)

        df["parameters"] = df.apply(
            lambda row: [
                {**param, 'location_code': row["id"]} for param in row["parameters"]
                ], axis=1)
        
        expanded_params = pd.json_normalize(df["parameters"].explode())

        merged_df = pd.merge(
            df, expanded_params, left_on='id', right_on='location_code', how="left"
        )

        merged_df.drop(["parameters", "location_code"], axis=1, inplace=True)

        merged_df["display_name"] = merged_df["display_name"].astype(str)

        merged_df = merged_df.rename(columns={
            "id_x": "id",
            "name_x": "name",
            "id_y": "param_id",
            "name_y": "param_name"
            })

        merged_df["pk"] = merged_df["id"].astype(str) + merged_df["param_id"].astype(str)

        return merged_df