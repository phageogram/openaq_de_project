import os
import pandas as pd
from pipeline.processors.countries_processor import CountryProcessor

def test_country_processor():
    sample_data = './tests/countries_output.csv'
    df = pd.read_csv(sample_data)
    processor = CountryProcessor(df)
    new_df = processor.process()
    print(new_df.head())
    assert new_df[0][0] == 1

test_country_processor()