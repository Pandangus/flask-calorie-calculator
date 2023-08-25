import requests
from pprint import pprint


def retrieve_calories(food_name, weight_in_grams):
    try:
        response = requests.get(
            f"https://api.edamam.com/api/food-database/parser?app_id=ca747d07&app_key=722fabaee32b8118f7b1cb2e32b137cf&ingr=${food_name}"
        )
        json_response = response.json()
        if len(json_response) == 4:
            calories = json_response["hints"][0]["food"]["nutrients"]["ENERC_KCAL"]
            return round(calories * (weight_in_grams / 100), 1)
        else:
            pprint(
                "\n1 - No results found. Try checking spelling, or simplifying request."
            )
    except:
        pprint("\n2 - Food name error. Try checking spelling.")
