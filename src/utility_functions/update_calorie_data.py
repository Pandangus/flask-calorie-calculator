import re
import os
import time
from copy import deepcopy
from utility_functions.convert_to_integer import convert_to_integer
from utility_functions.calories_to_add import calories_to_add
from utility_functions.return_to_main_menu import return_to_main_menu


def update_calorie_data(
    calories_per_100g,
    weight_user_input,
    ingredient_user_input,
    ingredients_list,
    total_calories
):
    try:
        updated_ingredients = deepcopy(ingredients_list)
        new_entry_weight = convert_to_integer(weight_user_input, "weight")
        new_entry_calories_100g = convert_to_integer(calories_per_100g, "calories")
        if not new_entry_weight or not new_entry_calories_100g:
            print("\nreturning to main menu")
            return None
        new_entry_calories = calories_to_add(new_entry_weight, new_entry_calories_100g)
        if not new_entry_calories:
            return_to_main_menu()
        new_entry_summary = (
            f"{new_entry_calories} kcal from {new_entry_weight}g of {ingredient_user_input}"
        )

        
        for existing_entry in updated_ingredients:
            if ingredient_user_input == existing_entry.split(' of ', 1)[1]:
                print(f"\nATTENTION! the current ingredient list already contains an existing entry for '{ingredient_user_input}':\n\n- '{existing_entry}' already exists")
                print(f"\n- '{new_entry_summary}' is currently being created")
                user_duplicate_input = input(f"\n\nenter [m]erge entries, [r]eplace existing entry or [c]ancel new entry\n\n-> ").lower()

                if user_duplicate_input == "m":
                    merged_calories = new_entry_calories + round(float(re.search(r"^[0-9]+", existing_entry).group()))
                    merged_weights = new_entry_weight + round(float(re.search(r"[0-9]+g", existing_entry).group()[:-1]))
                    merged_entry_summary = (f"{merged_calories} kcal from {merged_weights}g of {ingredient_user_input}")
                    target_index = updated_ingredients.index(existing_entry)
                    del(updated_ingredients[target_index])
                    total_calories += new_entry_calories
                    updated_ingredients.insert(target_index, merged_entry_summary)
                    os.system('clear')
                    print(f"\nsuccess! entries merged into new entry: '{merged_entry_summary}'")
                    return updated_ingredients, total_calories
                
                elif user_duplicate_input == "r":
                    total_calories -= round(float(re.search(r"^[0-9]+", existing_entry).group()))
                    target_index = updated_ingredients.index(existing_entry)
                    del(updated_ingredients[target_index])
                    total_calories += new_entry_calories
                    updated_ingredients.insert(target_index, new_entry_summary)
                    os.system('clear')
                    print(f"\nsuccess! '{existing_entry}' replaced with '{new_entry_summary}'")
                    return updated_ingredients, total_calories

                else:
                    return return_to_main_menu()
                
        total_calories += new_entry_calories
        updated_ingredients.append(new_entry_summary)
        print(f"\nsuccess! '{new_entry_summary}' added")
        return updated_ingredients, total_calories
    
    except (TypeError, AttributeError):
        print(f"\nan unexpected error occurred\n")
        time.sleep(3)
        return None

