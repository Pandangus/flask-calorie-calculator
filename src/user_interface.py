import time
import requests
import re
from list_ingredients import list_ingredients
from exit import exit
from reset_calories import reset_calories
from delete_calories import delete_calories


def menu():
    calorie_count = 0
    ingredients = []
    print("\nHello.")
    time.sleep(0.5)
    print("\nWelcome to the Calorie Counter.")
    time.sleep(0.25)

    while True:
        time.sleep(0.25)
        print(f"\nTotal calories: {round(calorie_count)}")
        user_input = input(
            "\nMAIN MENU\n---------\nPlease specify [e]nter calories, [d]elete calories, [l]ist total calories, [r]eset calories or e[x]it:\n\n-> "
        ).lower()

        if user_input == "e":
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
                    calories_to_add = 0
                    response = requests.get(
                        f"https://api.edamam.com/api/food-database/parser?app_id=ca747d07&app_key=722fabaee32b8118f7b1cb2e32b137cf&ingr=${ingredient_user_input}"
                    )
                    json_response = response.json()
                    if len(json_response) == 4:
                        calories_per_100g = json_response["hints"][0]["food"][
                            "nutrients"
                        ]["ENERC_KCAL"]
                        calories_to_add += round(
                            calories_per_100g * (int(weight_user_input) / 100)
                        )
                        calorie_count += calories_to_add
                        summary = f"{calories_to_add} kcal from {weight_user_input}g of {ingredient_user_input}"
                        ingredients.append(summary)
                        print(f"\nENTER CALORIES\n--------------\n{summary} added")
                    else:
                        time.sleep(0.25)
                        print(
                            "\nENTER CALORIES\n--------------\nNo results found. Try checking spelling, or simplifying request."
                        )
                        time.sleep(0.25)
                        print(
                            "\nENTER CALORIES\n--------------\nReturning to main menu\n"
                        )
                else:
                    time.sleep(0.25)
                    print("\nENTER CALORIES\n--------------\nReturning to main menu")
            else:
                time.sleep(0.25)
                print("\nENTER CALORIES\n--------------\nReturning to main menu")

        if user_input == "d":
            delete_calories_result = delete_calories(ingredients, calorie_count)
            if delete_calories_result:
                ingredients, calorie_count = delete_calories_result[0], delete_calories_result[1]

        if user_input == "l":
            list_ingredients(ingredients, calorie_count)

        if user_input == "r":
            if reset_calories() == "reset":
                calorie_count = 0
                ingredients = []

        if user_input == "x":
            if exit() == "shutdown":
                break


menu()
