from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import httpx
import seaborn as sns
import plotly.express as px
import io
import base64

app = FastAPI()

OPENAQ_API_URL = "https://api.openaq.org/v3/measurements"

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
    
# Plotly example
async def plotly_chart(data):
    timestamps = [item["timestamp"] for item in data]
    values = [item["value"] for item in data]

    fig = px.line(
        x=timestamps, y=values, labels={"x": "Timestamp", "y": "PM2.5 (µg/m³)"},
        title="Air Quality Data"
    )
    fig.update_xaxes(type="category")  # For date/time x-axis handling
    fig.update_layout(xaxis_tickangle=-45)  # Rotate the x-axis labels
    return fig.to_html(full_html=False)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = await fetch_data(city="Los Angeles")
    if not data:
        return HTMLResponse("<h1>No data found for Los Angeles</h1>")
    
    plot_html = await plotly_chart(data)
    return HTMLResponse(content=f"<html><body>{plot_html}</body></html>")