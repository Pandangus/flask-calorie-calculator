import os
from src.utility_functions.return_to_main_menu import return_to_main_menu
from src.utility_functions.get_entry_calories import get_entry_calories
from src.utility_functions.get_entry_name import get_entry_name
from src.utility_functions.get_entry_weight import get_entry_weight


def add_current_to_loaded(
    loaded_calories,
    existing_calories,
    loaded_data,
    existing_ingredients_list,
    file_name,
):
    try:
        combined_calories = loaded_calories + existing_calories
        combined_ingredient_list = []
        os.system("clear")

        for existing_entry in existing_ingredients_list:
            existing_entry_name = get_entry_name(existing_entry)
            no_conflict = True

            for new_entry in loaded_data:
                new_entry_name = get_entry_name(new_entry)

                if existing_entry_name == new_entry_name:
                    no_conflict = False
                    entry_conflict_message = f"\nATTENTION!\nan entry for {existing_entry_name} already exists in the current ingredient list\n----------------------------------------------------------------\n- existing entry: {existing_entry}\n\n - - - new entry: {new_entry}\n----------------------------------------------------------------"
                    entry_conflict_input = (
                        input(
                            f"{entry_conflict_message}\n\nplease enter [k]eep existing entry, [r]eplace with new entry or [m]erge entries (enter 'x' to return to main menu):\n\n-> "
                        )
                        .strip()
                        .lower()
                    )
                    os.system("clear")

                    while entry_conflict_input not in ["k", "r", "m", "x"]:
                        print(
                            f"{entry_conflict_message}\n\ninvalid input\n\nplease enter [k]eep existing entry, [r]eplace with new entry or [m]erge entries (enter 'x' to return to main menu):"
                        )
                        entry_conflict_input = input("-> ").strip().lower()

                    if entry_conflict_input == "k":
                        combined_calories -= get_entry_calories(new_entry)
                        combined_ingredient_list.append(existing_entry)

                    elif entry_conflict_input == "r":
                        combined_calories -= get_entry_calories(existing_entry)
                        combined_ingredient_list.append(new_entry)

                    elif entry_conflict_input == "m":
                        merged_entries = f"{get_entry_calories(existing_entry) + get_entry_calories(new_entry)} kcal from {get_entry_weight(existing_entry) + get_entry_weight(new_entry)}g of {existing_entry_name}"
                        print(
                            f"\nsuccess! conflicting {existing_entry_name} entries were merged into: '{merged_entries}'"
                        )
                        combined_ingredient_list.append(merged_entries)

                    elif entry_conflict_input == "x":
                        return return_to_main_menu()

            if no_conflict:
                combined_ingredient_list.append(existing_entry)

        for new_entry in loaded_data:
            no_conflict = True

            for entry in combined_ingredient_list:
                if get_entry_name(new_entry) == get_entry_name(entry):
                    no_conflict = False

            if no_conflict:
                combined_ingredient_list.append(new_entry)

        print(f"\nsuccess! current calories have been added to {file_name}\n")
        return combined_ingredient_list, combined_calories

    except TypeError as e:
        print(f"add_current_to_loaded - TypeError: {e}")

    except Exception as e:
        print(f"add_current_to_loaded - an unexpected error occurred: {e}")
