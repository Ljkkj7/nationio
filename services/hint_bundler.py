import asyncio
import aiohttp
from aiohttp import ClientSession
from utils.country_randomiser import random_countries

async def fetch_hints(country, session):
    url = f'https://restcountries.com/v3.1/name/{country}?fullText=true&fields=name,region,capital,population,flags,currencies'
    try:
        async with session.get(url) as res:
            if res.status == 200:
                return await res.json()
    except:
        print('Error in fetching data from the API.')

async def fetch_all_hints(countries):
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_hints(country, session)
            for country in countries
        ]
        
        return await asyncio.gather(*tasks)

if __name__ == '__main__':
    countries = random_countries()
    hints = asyncio.run(fetch_all_hints(countries))
    print(hints)