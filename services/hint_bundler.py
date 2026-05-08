import asyncio
import aiohttp
from aiohttp import ClientSession
from utils.extensions import cache
from utils.country_randomiser import random_country_codes


async def fetch_hints(country_code, session):
    cache_key = f'hints_{country_code}'
    cached = cache.get(cache_key)
    if cached:
        return cached
    url = f'https://restcountries.com/v4/alpha?codes={country_code}&fields=name,region,capital,population,flag,currencies'
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=2)) as res:
            print(f'{res.status} -------------------- {country_code}')
            if res.status == 200:
                data = await res.json()
                cache.set(cache_key, data, timeout=86400)
                return data
            else:
                print(f'Error in fetching data from the API for country {country_code}: {res.status} (timed out)')
                return None
    except Exception as e:
        print(f'Error in fetching data from the API for country {country_code}: {e}')
        return None

async def fetch_all_hints(country_codes):
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_hints(country_code, session)
            for country_code in country_codes
        ]
        
        return await asyncio.gather(*tasks)

def create_hints(hints, difficulty):
    hint_bundle = []
    for hint in hints:
        if hint is None:
            continue
        
        if difficulty == 0 or difficulty == 2:
            hint_bundle.append({
                'Capital': hint[0]['capital'][0],
                'Region': hint[0]['region'],
                'Population': hint[0]['population'],
                'Flag': hint[0]['flag']['png'],
                'Currencies': hint[0]['currencies'][0]['symbol'] + ' - ' + hint[0]['currencies'][0]['code'],
            })
        elif difficulty == 1:
            hint_bundle.append({
                'Region': hint[0]['region'],
                'Population': hint[0]['population'],
                'Flag': hint[0]['flag']['png'],
                'Currencies': hint[0]['currencies'][0]['symbol'] + ' - ' + hint[0]['currencies'][0]['code'],
            })
    return hint_bundle

def bundle_hints(hints, difficulty):
    return create_hints(hints, difficulty)

def bundle_country_names(hints):
    names = []
    for hint in hints:
        names.append(hint[0]['name']['common'])
    return names

def fetch_new_code(num_codes):
    return random_country_codes(num_codes)

def is_complete(entry):
    h = entry[0]
    return h['capital'] and h['region'] and h['population'] and h['flag']['png'] and h['currencies']


def bundle_json(difficulty, target=5):
    all_codes = fetch_new_code(target)
    valid_tries = []

    attempts = 0
    max_attempts = 3

    while len(valid_tries) < target and attempts < max_attempts:
        needed = target - len(valid_tries)

        batch_codes = all_codes[:needed]
        raw_fetch = asyncio.run(fetch_all_hints(batch_codes))

        for entry in raw_fetch:
            if entry is not None and is_complete(entry):
                valid_tries.append(entry)
        
        all_codes = all_codes[needed:]

        still_needed = target - len(valid_tries)
        if still_needed > 0:
            all_codes.extend(fetch_new_code(still_needed))
            
        attempts += 1
    
    if len(valid_tries) != target:
        raise ValueError("Failed to generate hints. Try again later.")

    hints_bundle = create_hints(valid_tries, difficulty)
    country_names = bundle_country_names(valid_tries)

    return hints_bundle, country_names
        
        