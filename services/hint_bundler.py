import asyncio
import aiohttp
from aiohttp import ClientSession


async def fetch_hints(country, session):
    url = f'https://restcountries.com/v4/name/{country}?fullText=true&fields=name,region,capital,population,flag,currencies'
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

def create_hints(hints):
    hint_bundle = []
    for hint in hints:
        if hint is None:
            continue
        hint_bundle.append([{
            'Capital': hint[0]['capital'][0],
            'Region': hint[0]['region'],
            'Population': hint[0]['population'],
            'Flag': hint[0]['flag']['png'],
            'Currencies': hint[0]['currencies'][0]['symbol'] + ' - ' + hint[0]['currencies'][0]['code'],
        }])
    return hint_bundle

def bundle_hints(countries):
    hints = asyncio.run(fetch_all_hints(countries))
    return create_hints(hints)