from services.hint_bundler import bundle_hints
from utils.country_randomiser import random_countries

class GameInstance:
    def __init__(self):
        self.score = 0
        self.hints_shown = []
        self.countries = []
        self.hints = []
        self.current_hint = 0

    def start(self):
        self.countries = random_countries()
        self.hints = bundle_hints(self.countries)


if __name__ == '__main__':
    instance = GameInstance()
    instance.start()
    print(instance.countries)
    print(instance.hints)