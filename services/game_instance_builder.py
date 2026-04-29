from services.hint_bundler import bundle_hints
from utils.country_randomiser import random_countries

class GameInstance:
    def __init__(self):
        self.score = 30
        self.rounds_played = 0
        self.hints_shown_this_round = 0
        self.hints_shown_total = 0
        self.rounds_completed = 0
        self.countries = []
        self.hints = []
        self.current_hint = 0

    def start(self):
        self.countries = random_countries()
        self.hints = bundle_hints(self.countries)

    def init_new_round(self):
        self.rounds_played += 1
        self.hints_shown_this_round = 0
        self.current_hint = 0