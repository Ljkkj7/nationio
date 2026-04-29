import random

def read_country_names(filename):
    with open(filename, 'r', encoding='utf-8' ) as f:
        return f.read().splitlines()

def random_countries():
    return random.choices(read_country_names('countrynames.csv'), k=5)
