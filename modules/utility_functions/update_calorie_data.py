import re
from copy import deepcopy
from modules.utility_functions.convert_to_integer import convert_to_integer
from modules.utility_functions.calories_to_add import calories_to_add
from modules.utility_functions.return_to_main_menu import return_to_main_menu
from modules.utility_functions.replace_entry import replace_entry


def update_calorie_data(
    calories_per_100g,
    weight_user_input,
    ingredient_user_input,
    ingredients_list,
    total_calories,
):
    try:
        new_entry_weight = convert_to_integer(weight_user_input, "weight")
        new_entry_calories_100g = convert_to_integer(calories_per_100g, "calories")

        if not new_entry_weight or not new_entry_calories_100g:
            return None
        
        new_entry_calories = calories_to_add(new_entry_weight, new_entry_calories_100g)
        new_entry_summary = f"{new_entry_calories} kcal from {new_entry_weight}g of {ingredient_user_input}"
        total_calories += new_entry_calories
        updated_ingredients = deepcopy(ingredients_list)
        updated_ingredients.append(new_entry_summary)
        return updated_ingredients, total_calories

    except TypeError as e:
        print(f"\nupdate_calorie_data - TypeError: {e}")

    except Exception as e:
        print(f"\nupdate_calorie_data - an unexpected error occurred: {e}")
