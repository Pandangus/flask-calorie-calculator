import os
from copy import deepcopy


def replace_entry(
    total_calories, ingredient_list, new_entry_calories, existing_entry, summary, merged
):
    updated_ingredients = deepcopy(ingredient_list)
    target_index = updated_ingredients.index(existing_entry)
    del updated_ingredients[target_index]
    total_calories += new_entry_calories
    updated_ingredients.insert(target_index, summary)
    os.system("clear")
    if merged:
        print(f"\nsuccess! entries merged into new entry: '{summary}'")
    else:
        print(f"\nsuccess! '{existing_entry}' replaced with '{summary}'")
    return updated_ingredients, total_calories
