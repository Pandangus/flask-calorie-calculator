import requests
from modules.utility_functions.update_calorie_data import update_calorie_data


def enter_calories_script(entries, calories, entry_name, entry_weight):
    try:
        json_response = requests.get(
            f"https://api.edamam.com/api/food-database/parser?app_id=ca747d07&app_key=722fabaee32b8118f7b1cb2e32b137cf&ingr=${entry_name}"
        ).json()

        if len(json_response) == 4:
            calories_per_100g = json_response["hints"][0]["food"]["nutrients"][
                "ENERC_KCAL"
            ]
            updated_entries, updated_calories = update_calorie_data(
                calories_per_100g,
                entry_weight,
                entry_name,
                entries,
                calories,
            )
            return updated_entries, updated_calories
        else:
            return None

    except TypeError as e:
        print(f"\nenter_calories - TypeError: {e}")

    except Exception as e:
        print(f"\nenter_calories - an unexpected error occurred: {e}")
