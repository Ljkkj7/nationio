from services.hint_bundler import bundle_hints
from utils.country_randomiser import random_countries
from services.game_instance_builder import GameInstance, GameInstanceMixin

def game():
    instance = GameInstanceMixin()
    instance.new_game()
    while True:

        if instance.rounds_played > len(instance.countries):
            choice = instance.end_game()
            if choice.lower() == 'y':
                instance.new_game()
                continue
            elif choice.lower() != 'n':
                print("\nInvalid choice. Please try again.")
                continue
            break

        instance.show_game_status()
        instance.show_used_hints()
        choice = instance.show_game_menu()

        if choice == '1':
            instance.show_next_hint()
        elif choice == '2':
            instance.guess(input("Enter your guess: "))
        elif choice == '3':
            return
        else:
            print("\nInvalid choice. Please try again.")

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