from services.hint_bundler import bundle_hints
from utils.country_randomiser import random_countries
from services.game_instance_builder import GameInstance

def game(instance):

    instance.new_game()

    while instance.rounds_played - 1 < len(instance.countries):
        round(instance)

    handle_end_game(instance)

def round(instance):
    instance.show_game_status()
    instance.show_used_hints()
    choice = instance.show_game_menu()

    if choice == '1':
        instance.show_next_hint()
    elif choice == '2':
        instance.guess(input("Enter your guess: "))
    elif choice == '3':
        quit()
    else:
        print("\nInvalid choice. Please try again.")

def handle_end_game(instance):
    choice = instance.end_game()
    if choice.lower() == 'y':
        game(instance)
    elif choice.lower() == 'n':
        return
    else:
        print("\nInvalid choice. Please try again.")
        handle_end_game(instance)

def menu():
    print("1. Play")
    print("2. Quit")

def main():
    print("Welcome to NationIO!")
    menu()
    choice = input("Enter your choice: ")
    if choice == '1':
        instance = GameInstance()
        game(instance)
    elif choice == '2':
        return
    else:
        print("Invalid choice. Please try again.")
        menu()
    

if __name__ == '__main__':
    main()    