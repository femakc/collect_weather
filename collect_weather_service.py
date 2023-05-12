import aiohttp
KELVIN_TO_CELSIUS = -271.15


async def get_temp(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as response:
            html = await response.json()
            temp = int(html.get('main').get('temp') + KELVIN_TO_CELSIUS)
    return temp
