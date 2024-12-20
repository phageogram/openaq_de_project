from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import httpx
import seaborn as sns
import plotly.express as px
import io
import base64

app = FastAPI()

OPENAQ_API_URL = "https://api.openaq.org/v2/measurements"

async def fetch_data(city="Los Angeles", parameter="pm25"):
    async with httpx.AsyncClient() as client:
        params = {
            "city": city,
            "parameter": parameter,
            "limit": 100,
            "order_by":"desc",
            "date_from": "2023-01-01",
            "date_to": "2023-12-31"
        }
        response = await client.get(OPENAQ_API_URL, params=params)
        data=response.json()
        return data["results"]
    
@app.get("/", response_class=HTMLResponse)