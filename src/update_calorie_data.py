from copy import deepcopy
from convert_to_integer import convert_to_integer
from calories_to_add import calories_to_add


def update_calorie_data(
    calories_per_100g,
    weight_user_input,
    ingredient_user_input,
    ingredients_list,
    total_calories,
    menu_header,
):
    processed_weight_input = convert_to_integer(weight_user_input)
    processed_calories_100g = convert_to_integer(calories_per_100g)
    new_calories = calories_to_add(processed_calories_100g, processed_weight_input)
    total_calories += new_calories
    summary = (
        f"{new_calories} kcal from {weight_user_input}g of {ingredient_user_input}"
    )
    updated_ingredients = deepcopy(ingredients_list)
    updated_ingredients.append(summary)
    print(f"\n{menu_header}\nsuccess! {summary} added")
    return updated_ingredients, total_calories
