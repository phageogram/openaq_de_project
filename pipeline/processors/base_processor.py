import pandas as pd

class BaseProcessor:
    def __init__(self, data):
        self.data = pd.DataFrame(data)
    
    def validate_data(self):
        if self.data.empty:
            raise ValueError("No data found")
        return True
    
    def process(self):
        raise NotImplementedError("Subclasses must implement process method")