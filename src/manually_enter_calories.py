import os
import time
from utility_functions.return_to_main_menu import return_to_main_menu
from utility_functions.update_calorie_data import update_calorie_data


def manually_enter_calories(ingredients_list, total_calories):
    try:
        menu_header = "MANUALLY ENTER CALORIES\n-----------------------"
        os.system('clear')
        time.sleep(0.25)
        os.system('clear')
        print("\nYou selected enter calories.")
        ingredient_user_input = input(
            f"\n{menu_header}\nPlease enter name of raw ingredient. (enter 'x' to cancel, and return to main menu)\n\n-> "
        ).lower()
        if ingredient_user_input != "x":
            time.sleep(0.25)
            os.system('clear')
            calories_per_100g_user_input = input(
                f"\n{menu_header}\nNow please enter number of calories per 100g (kcal). (enter 'x' to cancel, and return to main menu)\n\n-> "
            ).lower()
            if calories_per_100g_user_input != "x":
                time.sleep(0.25)
                os.system('clear')
                weight_user_input = input(
                    f"\n{menu_header}\nNow please enter weight in grams (g). (enter 'x' to cancel, and return to main menu)\n\n-> "
                ).lower()
                if weight_user_input != "x":
                    os.system('clear')
                    return update_calorie_data(
                        calories_per_100g_user_input,
                        weight_user_input,
                        ingredient_user_input,
                        ingredients_list,
                        total_calories,
                    )
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
