import os
import time
import requests
from utility_functions.return_to_main_menu import return_to_main_menu
from utility_functions.update_calorie_data import update_calorie_data
from manually_enter_calories import manually_enter_calories


def enter_calories(ingredients_list, total_calories):
    try:
        menu_header = "ENTER CALORIES\n--------------"
        time.sleep(0.25)
        os.system("clear")
        print("\nYou selected enter calories.")
        ingredient_user_input = input(
            f"\n{menu_header}\nPlease enter name of raw ingredient. (enter 'x' to cancel, and return to main menu)\n\n-> "
        ).lower()
        if ingredient_user_input != "x":
            time.sleep(0.25)
            os.system("clear")
            json_response = requests.get(
                f"https://api.edamam.com/api/food-database/parser?app_id=ca747d07&app_key=722fabaee32b8118f7b1cb2e32b137cf&ingr=${ingredient_user_input}"
            ).json()
            if len(json_response) == 4:
                calories_per_100g = json_response["hints"][0]["food"]["nutrients"][
                    "ENERC_KCAL"
                ]
                weight_user_input = input(
                    f"\n{menu_header}\nNow please enter weight in grams (g). (enter 'x' to cancel, and return to main menu)\n\n-> "
                ).strip().lower()
                if weight_user_input != "x":
                    os.system("clear")
                    return update_calorie_data(
                        calories_per_100g,
                        weight_user_input,
                        ingredient_user_input,
                        ingredients_list,
                        total_calories,
                    )
                else:
                    return return_to_main_menu()
            else:
                time.sleep(0.25)
                print("\nsearch request returned no results")
                time.sleep(0.25)
                user_choice = input(
                    "\nwould you like to manually add calories?\n\nplease enter:\n\n[m]anually enter calories or [r]eturn to main menu\n\n-> "
                ).lower()
                if user_choice == "m":
                    return manually_enter_calories(ingredients_list, total_calories)
                else:
                    return return_to_main_menu()
        else:
            return return_to_main_menu()
    except (ValueError, TypeError):
        print(
            "\nan unexpected error occurred"
        )
        return return_to_main_menu()
