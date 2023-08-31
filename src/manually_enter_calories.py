import time
from copy import deepcopy
from return_to_main_menu import return_to_main_menu
from convert_to_integer import convert_to_integer
from calories_to_add import calories_to_add


def manually_enter_calories(ingredients_list, total_calories):
    try:
        time.sleep(0.25)
        print("\nYou selected enter calories.")
        ingredient_user_input = input(
            "\nMANUALLY ENTER CALORIES\n-----------------------\nPlease enter name of raw ingredient. (enter 'x' to cancel, and return to main menu)\n\n-> "
        ).lower()
        if ingredient_user_input != "x":
            time.sleep(0.25)
            calories_per_100g_user_input = input(
                "\nMANUALLY ENTER CALORIES\n-----------------------\nNow please enter number of calories per 100g (kcal). (enter 'x' to cancel, and return to main menu)\n\n-> "
            ).lower()
            if calories_per_100g_user_input != "x":
                processed_calories_100g = convert_to_integer(
                    calories_per_100g_user_input
                )
                time.sleep(0.25)
                weight_user_input = input(
                    "\nMANUALLY ENTER CALORIES\n-----------------------\nNow please enter weight in grams (g). (enter 'x' to cancel, and return to main menu)\n\n-> "
                ).lower()
                if weight_user_input != "x":
                    processed_weight_input = convert_to_integer(weight_user_input)
                    new_calories = calories_to_add(
                        processed_calories_100g, processed_weight_input
                    )
                    total_calories += new_calories
                    summary = f"{new_calories} kcal from {weight_user_input}g of {ingredient_user_input} added"
                    updated_ingredients = deepcopy(ingredients_list)
                    updated_ingredients.append(summary)
                    print(
                        f"\nMANUALLY ENTER CALORIES\n-----------------------\nsuccess! {summary} added"
                    )
                    return (updated_ingredients, total_calories)
                else:
                    return_to_main_menu()
            else:
                return_to_main_menu()
        else:
            return_to_main_menu()
    except ValueError:
        print(
            "\n----------------------------------------------------------------------------------------------------\ncould not parse integer from weight input. Please enter only either an integer, or float value, only\n----------------------------------------------------------------------------------------------------"
        )
        return_to_main_menu()
