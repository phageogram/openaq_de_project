import asyncio
from main import fetch_data

async def test():
    results = await fetch_data(city="Los Angeles", parameter="pm25")
    print(results)

asyncio.run(test())