import pandas as pd
import json
from .base_processor import BaseProcessor

class LocationProcessor(BaseProcessor):
    def __init__(self, data):
        super().__init__(data)

    def process(self):