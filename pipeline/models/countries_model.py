import pandas as pd

class CountryModel:

    def __init__(self, data):
        self.data = data

    def as_dataframe(self):
        # return response data as pandas dataframe
        return pd.DataFrame(self.data)