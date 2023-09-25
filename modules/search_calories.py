import requests
from modules.utility_functions.convert_to_integer import convert_to_integer
from modules.utility_functions.calories_to_add import calories_to_add


def search_calories(entry_name, entry_weight):
    try:
        json_response = requests.get(
            f"https://api.edamam.com/api/food-database/parser?app_id=ca747d07&app_key=722fabaee32b8118f7b1cb2e32b137cf&ingr=${entry_name}"
        ).json()

        if len(json_response) == 4:
            calories_per_100g = json_response["hints"][0]["food"]["nutrients"][
                "ENERC_KCAL"
            ]

            new_entry_weight = convert_to_integer(entry_weight, "weight")
            new_entry_calories_100g = convert_to_integer(calories_per_100g, "calories")
            new_entry_calories = calories_to_add(
                new_entry_weight, new_entry_calories_100g
            )

            return f"{new_entry_calories} kcal from {new_entry_weight}g of {entry_name}"

        return None

    except TypeError as e:
        print(f"\nenter_calories - TypeError: {e}")

    except Exception as e:
        print(f"\nenter_calories - an unexpected error occurred: {e}")
