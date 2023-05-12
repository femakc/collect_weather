from fastapi import FastAPI
from make_url import make_weather_url
from collect_weather_service import get_temp

app = FastAPI()


@app.get("/")
async def hello() -> str:
    return "Hello!!!"


@app.get("/api/get_weather/{city}")
async def get_weather(city: str) -> str:
    url = await make_weather_url(city)
    temp = await get_temp(url)
    result = f"Temp in {city}: {temp}"
    return result

