from services.hint_bundler import bundle_hints
from utils.country_randomiser import random_countries
from services.game_instance_builder import GameInstance, GameInstanceMixin

def game():
    instance = GameInstanceMixin()
    instance.start()
    instance.init_new_round()
    while True:

        print("\nScore: ", instance.score)
        print("Round: ", instance.rounds_played)
        if instance.current_hint < len(instance.hint_names):
            print(f"\nCurrent Hint: {instance.hint_names[instance.current_hint]}: {instance.hints[instance.rounds_played - 1][instance.hint_names[instance.current_hint]]}")
        else:
            print('No more hints available.')
        instance.show_used_hints()
        print("\n1. Reveal next hint")
        print("2. Guess")
        print("3. Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            instance.show_next_hint()
        elif choice == '2':
            instance.guess(input("Enter your guess: "))
        elif choice == '3':
            return
        else:
            print("Invalid choice. Please try again.")

def menu():
    print("1. Play")
    print("2. Quit")

def main():
    print("Welcome to NationIO!")
    menu()
    choice = input("Enter your choice: ")
    if choice == '1':
        game()
    elif choice == '2':
        return
    else:
        print("Invalid choice. Please try again.")
        menu()
    

if __name__ == '__main__':
    main()    