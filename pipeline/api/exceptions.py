class APIClientError:
    def __init__(self, e):
        raise ConnectionError(f"Error connecting to OpenAQ API: {e}")