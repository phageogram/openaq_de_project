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

        """
        df["parameters"] = df["parameters"].apply(
            lambda x: x.replace("'", '"') if isinstance(x, str) else x
        )

        df["parameters"] = df["parameters"].apply( lambda row: self.safe_json_load(row))
        """

        exploded_df = df.explode("parameters")
        print(type(exploded_df["parameters"]))

        exploded_df['parameters'] = exploded_df.apply(
            lambda row: {**row['parameters'], 'location_code': row['id']}
            , axis=1)
        
        expanded_params = pd.json_normalize(exploded_df["parameters"])

        merged_df = pd.merge(
            exploded_df, expanded_params, left_on='id', right_on='location_code', how="left"
        )

        merged_df.drop(["parameters", "location_code"], axis=1, inplace=True)

        merged_df = merged_df.rename(columns={
            "id_x": "id",
            "name_x": "name",
            "id_y": "param_id",
            "name_y": "param_name"
            })
        return merged_df

    def safe_json_load(self, value):
        if value in [None, '', ' ', 'null', 'NaN']:
            return None
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return None