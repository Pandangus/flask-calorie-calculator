import re
from copy import deepcopy
from utility_functions.convert_to_integer import convert_to_integer
from utility_functions.calories_to_add import calories_to_add
from utility_functions.return_to_main_menu import return_to_main_menu
from utility_functions.replace_entry import replace_entry


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
            print("\nreturning to main menu")
            return None
        
        new_entry_calories = calories_to_add(new_entry_weight, new_entry_calories_100g)

        if not new_entry_calories:
            return_to_main_menu()

        new_entry_summary = f"{new_entry_calories} kcal from {new_entry_weight}g of {ingredient_user_input}"

        for existing_entry in ingredients_list:
            if ingredient_user_input == existing_entry.split(" of ", 1)[1]:
                print(
                    f"\nATTENTION! the current ingredient list already contains an existing entry for '{ingredient_user_input}':\n\n- '{existing_entry}' already exists"
                )
                print(f"\n- '{new_entry_summary}' is currently being created")
                user_duplicate_input = (
                    input(
                        f"\n\nenter [m]erge entries or [r]eplace existing entry. (enter 'x' to cancel, and return to main menu)\n\n-> "
                    )
                    .strip()
                    .lower()
                )

                existing_entry_calories = round(
                    float(re.search(r"^[0-9]+", existing_entry).group())
                )

                if user_duplicate_input not in ["m", "r"]:
                    return return_to_main_menu()

                elif user_duplicate_input == "m":
                    merged_calories = new_entry_calories + existing_entry_calories
                    merged_weights = new_entry_weight + round(
                        float(re.search(r"[0-9]+g", existing_entry).group()[:-1])
                    )
                    merged_entry_summary = f"{merged_calories} kcal from {merged_weights}g of {ingredient_user_input}"
                    return replace_entry(
                        total_calories,
                        ingredients_list,
                        new_entry_calories,
                        existing_entry,
                        merged_entry_summary,
                        True,
                    )

                elif user_duplicate_input == "r":
                    total_calories -= existing_entry_calories
                    return replace_entry(
                        total_calories,
                        ingredients_list,
                        new_entry_calories,
                        existing_entry,
                        new_entry_summary,
                        False,
                    )

        total_calories += new_entry_calories
        updated_ingredients = deepcopy(ingredients_list)
        updated_ingredients.append(new_entry_summary)
        print(f"\nsuccess! '{new_entry_summary}' added")
        return updated_ingredients, total_calories

    except TypeError as e:
        print(f"\nupdate_calorie_data - TypeError: {e}")

    except Exception as e:
        print(f"\nupdate_calorie_data - an unexpected error occurred: {e}")
