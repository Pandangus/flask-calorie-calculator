import time
from copy import deepcopy
from return_to_main_menu import return_to_main_menu


def manually_enter_calories(ingredients_list, total_calories):
    time.sleep(0.25)
    print("\nYou selected enter calories.")
    ingredient_user_input = input(
        "\nMANUALLY ENTER CALORIES\n-----------------------\nPlease enter name of raw ingredient. (enter 'x' to cancel, and return to main menu)\n\n-> "
    ).lower()
    if ingredient_user_input != "x":
        time.sleep(0.25)
        calories_per_100_user_input = input(
            "\nMANUALLY ENTER CALORIES\n-----------------------\nNow please enter number of calories per 100g (kcal). (enter 'x' to cancel, and return to main menu)\n\n-> "
        ).lower()
        if calories_per_100_user_input != "x":
            time.sleep(0.25)
            weight_user_input = input(
                "\nMANUALLY ENTER CALORIES\n-----------------------\nNow please enter weight in grams (g). (enter 'x' to cancel, and return to main menu)\n\n-> "
            ).lower()
            if weight_user_input != "x":
                calories_to_add = round(
                    int(calories_per_100_user_input) * (int(weight_user_input) / 100)
                )
                total_calories += calories_to_add
                summary = f"{calories_to_add} kcal from {weight_user_input}g of {ingredient_user_input}"
                updated_ingredients = deepcopy(ingredients_list)
                updated_ingredients.append(summary)
                print(
                    f"\nMANUALLY ENTER CALORIES\n-----------------------\n{summary} added"
                )
                return (updated_ingredients, total_calories)
            else:
                return_to_main_menu()
        else:
            return_to_main_menu()
    else:
        return_to_main_menu()
