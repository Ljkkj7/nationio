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
    

def write_to_file(filename, data):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        filewriter = csv.writer(f)
        for item in data:
            filewriter.writerow([item['name']['common']])

if __name__ == '__main__':
    data = fetch_all_countries()
    write_to_file('countrynames.csv', data)    