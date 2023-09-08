import os
from utility_functions.get_entry_calories import get_entry_calories
from utility_functions.get_entry_name import get_entry_name
from utility_functions.get_entry_weight import get_entry_weight


def add_current_to_loaded(
    loaded_calories,
    existing_calories,
    loaded_data,
    existing_ingredients_list,
    file_name,
):
    combined_calories = loaded_calories + existing_calories
    combined_ingredient_list = []
    for existing_entry in existing_ingredients_list:
        existing_entry_name = get_entry_name(existing_entry)
        no_conflict = True
        for new_entry in loaded_data:
            new_entry_name = get_entry_name(new_entry)
            if existing_entry_name == new_entry_name:
                no_conflict = False
                os.system("clear")
                entry_conflict_input = (
                    input(
                        f"an entry for {existing_entry_name} already exists in the current ingredient list\n\nselect [k]eep existing entry, [r]eplace with new entry or [m]erge entries:\n\n-> "
                    )
                    .strip()
                    .lower()
                )
                if entry_conflict_input == "k":
                    combined_calories -= get_entry_calories(new_entry)
                    combined_ingredient_list.append(existing_entry)
                elif entry_conflict_input == "r":
                    combined_calories -= get_entry_calories(existing_entry)
                    combined_ingredient_list.append(new_entry)
                elif entry_conflict_input == "m":
                    combined_ingredient_list.append(
                        f"{get_entry_calories(existing_entry) + get_entry_calories(new_entry)} kcal from {get_entry_weight(existing_entry) + get_entry_weight(new_entry)}g of {existing_entry_name}"
                    )
        if no_conflict:
            combined_calories.append(existing_entry)
    for new_entry in loaded_data:
        no_conflict = True
        for entry in combined_ingredient_list:
            if get_entry_name(new_entry) == get_entry_name(entry):
                no_conflict = False
        if no_conflict:
            combined_ingredient_list.append(new_entry)
    os.system("clear")
    print(f"\nsuccess! current calories have been added to {file_name}")
    return combined_ingredient_list, combined_calories
