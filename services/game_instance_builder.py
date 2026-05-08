from services.hint_bundler import bundle_json
from utils.country_randomiser import random_country_codes
import time
import sys

class GameInstanceMixin:
    def reset_game(self):
        self.score = 30
        self.rounds_played = 0
        self.hints_shown_this_round = 0
        self.countries = []
        self.hints = []
        self.hint_names = list(self.DEFAULT_HINT_NAMES)
        self.shown_hints = []
        self.answers = []
        self.current_hint = 0
        self.difficulty = self.DEFAULT_DIFFICULTY
    
    def new_game(self):
        if self.rounds_played > 0:
            self.reset_game()
        self.start()
        self.init_new_round()

    def stash_timer(self, time_remaining):
        self.timer = time_remaining

class GameInstance(GameInstanceMixin):
    DEFAULT_HINT_NAMES = ['Capital', 'Region', 'Population', 'Flag', 'Currencies']
    DEFAULT_DIFFICULTY = 0

    def __init__(self, json_bundler=bundle_json):
        self.json_bundler = json_bundler
        self.reset_game()

    def start(self):
        t = time.time()
        self.hints, self.countries = self.json_bundler(self.difficulty)
        print(f"Countries: {self.countries}", file=sys.stderr)
        print(f"Hints: {self.hints}", file=sys.stderr)
        print(f"Time taken to generate hints: {time.time() - t:.2f}", file=sys.stderr)

    def init_new_round(self):
        self.rounds_played += 1
        self.hints_shown_this_round = 1
        self.current_hint = 0
        self.shown_hints = []
        if hasattr(self, 'timer'):
            self.timer = 60 

    def show_next_hint(self):
        if self.current_hint >= len(self.hint_names):
            print('No more hints available.')
        else:
            self.shown_hints.append(f"{self.hint_names[self.current_hint]}: {self.hints[self.rounds_played - 1][self.hint_names[self.current_hint]]}")
            self.current_hint += 1
            self.hints_shown_this_round += 1
            if self.score > 0:
                self.score -= 5
    
    def guess(self, guess):
        if guess.lower() == self.countries[self.rounds_played - 1].lower():
            self.score += (6-self.hints_shown_this_round)*5
            self.answers.append(1)
        else:
            if self.score > 0:
                self.score -= 5
            self.answers.append(0)
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
            'answers': self.answers,
            'difficulty': self.difficulty,
            'timer': self.timer if hasattr(self, 'timer') else None
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
        instance.answers = data['answers']
        instance.difficulty = data['difficulty']
        if data['timer']:
            instance.timer = data['timer']
        return instance

class HardGameInstance(GameInstance):
    DEFAULT_HINT_NAMES = ['Region', 'Population', 'Flag', 'Currencies']
    DEFAULT_DIFFICULTY = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class TimedGameInstance(GameInstance):
    DEFAULT_HINT_NAMES = ['Capital', 'Region', 'Population', 'Flag', 'Currencies']
    DEFAULT_DIFFICULTY = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timer = 60
    
    def guess(self, guess):
        time_remaining = self.timer
        if guess.lower() == self.countries[self.rounds_played - 1].lower():
            self.score += (6-self.hints_shown_this_round)*5*(time_remaining/3)
            self.answers.append(1)
            self.init_new_round()
        else:
            if self.score > 0:
                self.score -= 5
            self.answers.append(0)
            self.init_new_round()


    

    
