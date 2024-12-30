from .pipeline.processors.countries_processor import CountryProcessor
from .pipeline.processors.locations_processor import LocationProcessor
from .pipeline.api.client import OpenAQClient
from .pipeline.api.exceptions import exceptions
import pandas as pd
from OpenAQClient import fetch_data, close

def test_location_response(location_code):
    response = fetch_data(locations, )