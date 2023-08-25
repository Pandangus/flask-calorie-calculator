from retrieve_calories import retrieve_calories
from pprint import pprint
import time


def menu():
    calorie_count = 0
    ingredients = []
    print("\nHello.")
    time.sleep(0.75)
    print("\nWelcome to the Calorie Counter.")
    time.sleep(1)

    while True:
        print(f"\nTotal calories: {calorie_count}\n")
        time.sleep(1)
        user_input = input(
            "Please specify [e]nter calories, [d]elete calories, [l]ist total calories, [r]eset calories or e[x]it:\n\n"
        ).lower()

        if user_input == "e":
            time.sleep(0.25)
            print("\nYou selected enter calories.")
            time.sleep(0.25)
            ingredient_user_input = input(
                "\nPlease enter name of raw ingredient. (enter 'x' to cancel, and return to main menu)\n\n"
            )
            if ingredient_user_input != "x":
                weight_user_input = input(
                    "\nNow please enter weight in grams (g). (enter 'x' to cancel, and return to main menu)\n\n"
                )
                if weight_user_input != "x":
                    calories = retrieve_calories(ingredient_user_input, int(weight_user_input))
                    calorie_count += calories
                    summary = f"\n{calories} kcal from {weight_user_input}g of {ingredient_user_input}"
                    ingredients.append(summary)
                    print(f"{summary} added")

        if user_input == "d":
            print("You selected delete calories.")

        if user_input == "r":
            print("You selected reset calories.\nThis will reset total calories to 0 and erase the all current ingredients.")
            reset_user_input = input("are you sure?\nenter:\n[y]es or [n]o\n")
            if reset_user_input == "y":
                calorie_count = 0
                ingredients = []

        if user_input == "x":
            user_input_2 = input(
                "\nYou selected exit.\n-----------------\nare you sure?\nenter:\n[y]es or [n]o\n"
            )
            if user_input_2 == "y":
                print("-------\nGoodbye\n-------")
                break

        # if user_input != 'e':


menu()
