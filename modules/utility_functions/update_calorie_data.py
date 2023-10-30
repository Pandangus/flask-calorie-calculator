from modules.utility_functions.convert_to_integer import convert_to_integer
from modules.utility_functions.calories_to_add import calories_to_add
from copy import deepcopy


def update_calorie_data(
    calories_per_100g,
    weight_user_input,
    ingredient_user_input,
    ingredients_list,
    total_calories,
):
    """

    Update calorie data based on user input.

    This function takes user inputs, converts them to integers, calculates the calories
    for the new entry, and updates the ingredients list and total calories accordingly.

    Args:
        calories_per_100g (str): Calories per 100g of the ingredient.
        weight_user_input (str): Weight of the ingredient in grams.
        ingredient_user_input (str): Name of the ingredient.
        ingredients_list (list): List of existing ingredient entries.
        total_calories (int): Total calories of all ingredients.

    Returns:
        tuple: A tuple containing the updated ingredients list and the new total calories,
               or None if input conversion fails.

    Raises:
        TypeError: If input conversion to integers fails.
        Exception: If an unexpected error occurs.

    """

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
