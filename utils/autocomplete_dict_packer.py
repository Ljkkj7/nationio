import csv
import json

def pack_dict(filename='../countrynames.csv'):
    with open(filename, 'r', encoding='utf-8') as f:
        filewriter = csv.reader(f)
        countries = []
        for item in filewriter:
            countries.append(item[0])
    return countries

def create_autocomplete_dict(country_list):
    autodict = {
    }
    letterSet = set()

    for country in country_list:
        letterSet.add(country[0].lower())

    for letter in letterSet:
        autodict[letter] = []

    for country in country_list:
        autodict[country[0].lower()].append(country)

    return autodict

if __name__ == '__main__':
    country_list = pack_dict()
    autocomplete_dict = create_autocomplete_dict(country_list)
    with open('../static/autocomplete.json', 'w', encoding='utf-8') as f:
        json.dump(autocomplete_dict, f)
    print("Dictionary packed successfully.")