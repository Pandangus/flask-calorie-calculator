import time
import requests
import re
from return_to_main_menu import return_to_main_menu


def enter_calories(ingredients_list, total_calories):
    try:
        time.sleep(0.25)
        print("\nYou selected enter calories.")
        ingredient_user_input = input(
            "\nENTER CALORIES\n--------------\nPlease enter name of raw ingredient. (enter 'x' to cancel, and return to main menu)\n\n-> "
        ).lower()
        if ingredient_user_input != "x":
            time.sleep(0.25)
            weight_user_input = input(
                "\nENTER CALORIES\n--------------\nNow please enter weight in grams (g). (enter 'x' to cancel, and return to main menu)\n\n-> "
            ).lower()
            if weight_user_input != "x":
                processed_weight_input = round(
                    float(re.search(r"[-+]?[0-9]*\.?[0-9]+", weight_user_input).group())
                )
                calories_to_add = 0
                response = requests.get(
                    f"https://api.edamam.com/api/food-database/parser?app_id=ca747d07&app_key=722fabaee32b8118f7b1cb2e32b137cf&ingr=${ingredient_user_input}"
                )
                json_response = response.json()
                if len(json_response) == 4:
                    calories_per_100g = json_response["hints"][0]["food"]["nutrients"][
                        "ENERC_KCAL"
                    ]
                    calories_to_add += round(
                        calories_per_100g * (int(processed_weight_input) / 100)
                    )
                    total_calories += calories_to_add
                    summary = f"{calories_to_add} kcal from {weight_user_input}g of {ingredient_user_input}"
                    ingredients_list.append(summary)
                    print(f"\nENTER CALORIES\n--------------\n{summary} added")
                    return (ingredients_list, total_calories)
                else:
                    time.sleep(0.25)
                    print(
                        "\nENTER CALORIES\n--------------\nNo results found. Try checking spelling, or simplifying request."
                    )
                    return return_to_main_menu()
            else:
                return return_to_main_menu()
        else:
            return return_to_main_menu()
    except ValueError:
        print(
            "\n-----------------------------------------------------------------------------------------\ncould not parse integer from weight input. please enter either an integer, or float value\n-----------------------------------------------------------------------------------------"
        )
        return_to_main_menu()
