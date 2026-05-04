from services.hint_bundler import bundle_hints
from utils.country_randomiser import random_countries

class GameInstanceMixin:
    def reset_game(self):
        self.score = 30
        self.rounds_played = 0
        self.hints_shown_this_round = 0
        self.countries = []
        self.hints = []
        self.hint_names = ['Capital', 'Region', 'Population', 'Flag', 'Currencies']
        self.shown_hints = []
        self.current_hint = 0
    
    def new_game(self):
        if self.rounds_played > 0:
            self.reset_game()
        self.start()
        self.init_new_round()

class GameInstance(GameInstanceMixin):
    def __init__(self):
        self.score = 30
        self.rounds_played = 0
        self.hints_shown_this_round = 0
        self.countries = []
        self.hints = []
        self.hint_names = ['Capital', 'Region', 'Population', 'Flag', 'Currencies']
        self.shown_hints = []
        self.current_hint = 0

    def start(self):
        self.countries = random_countries()
        self.hints = bundle_hints(self.countries)

        count = 0
        while self.hints is None and count < 3:
            self.countries = random_countries()
            self.hints = bundle_hints(self.countries)
            count += 1
        
        if self.hints is None:
            raise ValueError("Failed to generate hints. Try again later.")

    def init_new_round(self):
        self.rounds_played += 1
        self.hints_shown_this_round = 1
        self.current_hint = 0
        self.shown_hints = []

    def show_next_hint(self):
        if self.current_hint >= len(self.hint_names):
            print('No more hints available.')
        else:
            self.shown_hints.append(f"{self.hint_names[self.current_hint]}: {self.hints[self.rounds_played - 1][self.hint_names[self.current_hint]]}")
            self.current_hint += 1
            self.hints_shown_this_round += 1
            self.score -= 5
    
    def guess(self, guess):
        if guess.lower() == self.countries[self.rounds_played - 1].lower():
            self.score += (6-self.hints_shown_this_round)*5
            self.init_new_round()
        else:
            self.score -= 5
            self.init_new_round()
    
    def to_dict(self):
        return {
            'score': self.score,
            'rounds_played': self.rounds_played,
            'hints_shown_this_round': self.hints_shown_this_round,
            'countries': self.countries,
            'hints': self.hints,
            'hint_names': self.hint_names,
            'shown_hints': self.shown_hints,
            'current_hint': self.current_hint,
        }

    @classmethod
    def from_dict(cls, data):
        instance = cls()
        instance.score = data['score']
        instance.rounds_played = data['rounds_played']
        instance.hints_shown_this_round = data['hints_shown_this_round']
        instance.countries = data['countries']
        instance.hints = data['hints']
        instance.hint_names = data['hint_names']
        instance.shown_hints = data['shown_hints']
        instance.current_hint = data['current_hint']
        return instance