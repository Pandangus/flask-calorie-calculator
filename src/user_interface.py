import time
import requests
import re


def menu():
    calorie_count = 0
    ingredients = []
    print("\nHello.")
    time.sleep(0.5)
    print("\nWelcome to the Calorie Counter.")
    time.sleep(0.5)

    while True:
        print(f"\nTotal calories: {round(calorie_count)}")
        user_input = input(
            "\nMAIN MENU\n---------\nPlease specify [e]nter calories, [d]elete calories, [l]ist total calories, [r]eset calories or e[x]it:\n\n"
        ).lower()

        if user_input == "e":
            time.sleep(0.25)
            print("\nYou selected enter calories.")
            ingredient_user_input = input(
                "\nENTER CALORIES\n--------------\nPlease enter name of raw ingredient. (enter 'x' to cancel, and return to main menu)\n\n"
            ).lower()
            if ingredient_user_input != "x":
                time.sleep(0.25)
                weight_user_input = input(
                    "\nENTER CALORIES\n--------------\nNow please enter weight in grams (g). (enter 'x' to cancel, and return to main menu)\n\n"
                ).lower()
                if weight_user_input != "x":
                    calories_to_add = 0
                    response = requests.get(
                        f"https://api.edamam.com/api/food-database/parser?app_id=ca747d07&app_key=722fabaee32b8118f7b1cb2e32b137cf&ingr=${ingredient_user_input}"
                    )
                    json_response = response.json()
                    if len(json_response) == 4:
                        calories_per_100g = json_response["hints"][0]["food"]["nutrients"]["ENERC_KCAL"]
                        calories_to_add += round(calories_per_100g * (int(weight_user_input) / 100))
                        calorie_count += calories_to_add
                        summary = f"{calories_to_add} kcal from {weight_user_input}g of {ingredient_user_input}"
                        ingredients.append(summary)
                        print(f"\nENTER CALORIES\n--------------\n{summary} added")
                    else:
                        time.sleep(0.25)
                        print("\nENTER CALORIES\n--------------\nNo results found. Try checking spelling, or simplifying request.")
                        time.sleep(0.25)
                        print("\nENTER CALORIES\n--------------\nReturning to main menu\n")
                else:
                    time.sleep(0.25)
                    print("\nENTER CALORIES\n--------------\nReturning to main menu")
            else:
                time.sleep(0.25)
                print("\nENTER CALORIES\n--------------\nReturning to main menu")


        if user_input == "d":
            time.sleep(0.25)
            print("\nYou selected delete calories.\n------------------------------")
            time.sleep(0.5)
            delete_user_input = input("\nDELETE ENTRY\n------------\nPlease enter name of ingredient to remove:\n\n")
            item_deleted = False
            for entry in ingredients:
                if delete_user_input in entry:
                    ingredients.remove(entry)
                    calorie_count -= int(re.search(r'\d+', entry).group())
                    print(f"\nDELETE ENTRY\n------------\nsuccess! {delete_user_input} removed from ingredient list")
                    item_deleted = True
                    time.sleep(0.25)
            if not item_deleted:
                print(f"\nDELETE ENTRY\n------------\nx----------------------------------------------------------------------------\n{delete_user_input} returned no matches. Nothing was deleted from ingredients list.\n----------------------------------------------------------------------------")


        if user_input == 'l':
            time.sleep(0.25)
            print("\n------------------------")
            for entry in ingredients:
                time.sleep(0.25)
                print(entry)
            time.sleep(0.25)
            print(f"------------------------\n{calorie_count} kcal total\n------------------------")

        if user_input == "r":
            time.sleep(0.25)
            print("\nYou selected reset calories.")
            print(
                "\n--------------------------------------------------------------------------------\nThis will reset total calories to 0 and erase all entries from ingredients list.\n--------------------------------------------------------------------------------"
            )
            time.sleep(0.5)
            reset_user_input = input("\nare you sure?\nenter:\n[y]es or [n]o\n").lower()
            if reset_user_input == "y":
                calorie_count = 0
                ingredients = []

        if user_input == "x":
            time.sleep(0.25)
            print("\nYou selected exit.\n\nThis will close the calorie counter.\n\nData will not be saved.")
            time.sleep(0.5)
            user_input_2 = input(
                "\n-----------------\nare you sure?\nenter:\n[y]es or [n]o\n\n"
            ).lower()
            if user_input_2 == "y":
                print("\n-------\nGoodbye\n-------")
                break

print(len("This will reset total calories to 0 and erase all current ingredients."))
menu()
