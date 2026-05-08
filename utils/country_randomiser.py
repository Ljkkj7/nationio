import random
import csv

def read_country_codes(filename):
    with open(filename, 'r', encoding='utf-8' ) as f:
        reader = csv.reader(f)
        return [row[0] for row in reader if row]

def random_country_codes():
    return random.sample(read_country_codes('countrycodes.csv'), k=5)
