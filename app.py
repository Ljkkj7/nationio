from services.hint_bundler import bundle_hints
from utils.country_randomiser import random_countries
from services.game_instance_builder import GameInstance

def game():
    instance = GameInstance()
    instance.start()
    print(instance.countries)
    print(instance.hints)
    

if __name__ == '__main__':
    game()    