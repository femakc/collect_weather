import aiohttp
from settings import X_API_KEY

# BASE_URL = "https://api.openweathermap.org/"
# API_KEY = "0101452058a9a7945c8b353b7f8d618f"
# X_API_KEY = "hgwMzL0zKdvwe2cljulQ9g==ToLekCxPkDwwFoON"

"https://api.api-ninjas.com/v1/city?max_population=100000000&limit=50"

# async def make_geo_url(city):
#     result = f"{BASE_URL}geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
#     return result


async def get_geo(city):
    url = f"https://api.api-ninjas.com/v1/city?name={city}"
    headers = {'X-Api-Key': X_API_KEY}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False, headers=headers) as response:
            html = await response.json()
    return html[0]
