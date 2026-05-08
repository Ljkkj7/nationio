import csv
import requests


def fetch_all_countries():
    try:
        res = requests.get('https://restcountries.com/v3.1/all?fields=name')
        if res.status_code == 200:
            data = res.json()
            return data
    except:
        print('Error in fetching data from the API.')

def fetch_all_country_codes():
    try:
        res = requests.get('https://restcountries.com/v3.1/all?fields=cca2')
        if res.status_code == 200:
            data = res.json()
            return data
    except:
        print('Error in fetching data from the API.')
    

def write_country_names_to_file(filename, data):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        filewriter = csv.writer(f)
        for item in data:
            filewriter.writerow([item['name']['common']])

def write_country_codes_to_file(filename, data):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        filewriter = csv.writer(f)
        for item in data:
            filewriter.writerow([item['cca2']])

if __name__ == '__main__':
    data = fetch_all_countries()
    write_country_names_to_file('countrynames.csv', data)    
    data = fetch_all_country_codes()
    write_country_codes_to_file('countrycodes.csv', data)