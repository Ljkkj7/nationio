from services.hint_bundler import bundle_hints
from utils.country_randomiser import random_countries

def game():
    countries = random_countries()
    hints = bundle_hints(countries)
    for i in range(0, 5):
        print(countries[i])
        print(hints[i]['Capital'])
        print(hints[i]['Region'])
        print(hints[i]['Population'])
        print(hints[i]['Flag'])
        print(hints[i]['Currencies'])

if __name__ == '__main__':
    game()    