from services.hint_bundler import bundle_hints
from utils.country_randomiser import random_countries

class GameInstance:
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
            print('\n------------\n')
            print('Correct!')
            self.score += (6-self.hints_shown_this_round)*5
            self.init_new_round()
            print('\n------------\n')
        else:
            print('\n------------\n')
            print(f'\nIncorrect!')
            print(f'The country was {self.countries[self.rounds_played - 1]}')
            print('\n------------\n')
            self.score -= 5
            self.init_new_round()
    
    def end_game(self):
        print('\n------------\n')
        print('Game Over!')
        print(f'Final Score: {self.score}')
        print('\n------------\n')
        return input("Play again? (y/n): ")
    
class GameInstanceMixin(GameInstance):
    def show_used_hints(self):
        print('\nUsed hints: ')
        print('-----------')
        for hint in self.shown_hints:
            print(f'  {hint}')
        print('-----------')

    def show_game_status(self):
        print("\nScore: ", self.score)
        print("Round: ", self.rounds_played)
        if self.current_hint < len(self.hint_names):
            print(f"\nCurrent Hint: {self.hint_names[self.current_hint]}: {self.hints[self.rounds_played - 1][self.hint_names[self.current_hint]]}")
        else:
            print('No more hints available.')
    
    def show_game_menu(self):
        print("\n1. Reveal next hint")
        print("2. Guess")
        print("3. Quit")
        return input("Enter your choice: ")

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