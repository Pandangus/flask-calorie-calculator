import os
import re
import time
import pandas as pd
from utility_functions.return_to_main_menu import return_to_main_menu
from utility_functions.add_current_to_loaded import add_current_to_loaded


def load_calories(existing_entries, total_calories):
    SAVED_FILES_DIR = "saved_calorie_data"
    os.system("clear")
    time.sleep(0.25)
    print("\nLOAD CALORIES\n-------------")
    saved_file_count = 0
    for file in os.listdir(SAVED_FILES_DIR):
        if str(file)[-13:].lower() == "_calories.csv":
            time.sleep(0.25)
            if saved_file_count == 0:
                print("\nsaved files:\n-------------")
            saved_file_count += 1
            print(">", re.search(r"^[a-z]+", file).group())
    if saved_file_count == 0:
        os.system("clear")
        print("\nno saved files found\n\nreturning to main menu\n")
        return None
    else:
        user_load_input = input(
            "-------------\n\nenter the name of the file you wish to load: (enter 'x' to return to main menu)\n\n-> "
        )
        os.system("clear")
        if user_load_input == "x":
            return return_to_main_menu()
        if f"{user_load_input}_calories.csv" in os.listdir(SAVED_FILES_DIR):
            loaded_entries = []
            df = pd.read_csv(f"{SAVED_FILES_DIR}/{user_load_input}_calories.csv")
            load_count = 0
            while load_count < len(df):
                loaded_entries.append(
                    f"{df.at[load_count, 'calories']} kcal from {df.at[load_count, 'weight']} of {df.at[load_count, 'name']}"
                )
                load_count += 1
            print(f"success! {user_load_input} has been loaded")
            loaded_calories = df["calories"].sum()
            if len(existing_entries) > 0:
                first_user_choice_input = (
                    input(
                        "\nwould you like to add current calories to loaded calories?\n\nenter [a]dd current calories, [l]oaded calories only, or [r]eturn to main menu:\n\n-> "
                    )
                    .strip()
                    .lower()
                )
                if first_user_choice_input == "a":
                    return add_current_to_loaded(
                        loaded_calories,
                        total_calories,
                        loaded_entries,
                        existing_entries,
                        user_load_input,
                    )
                if first_user_choice_input == "r":
                    return return_to_main_menu()
                if first_user_choice_input != "l":
                    os.system("clear")
                    second_user_choice_input = input(
                        "user input error.\n\nplease enter [a]dd current calories, [l]oaded calories only, or [r]eturn to main menu:\n\n-> "
                    ).lower()
                    if second_user_choice_input == "a":
                        return add_current_to_loaded(
                            loaded_calories,
                            total_calories,
                            loaded_entries,
                            existing_entries,
                            user_load_input,
                        )
                    if second_user_choice_input != "l":
                        return return_to_main_menu()
            return loaded_entries, loaded_calories
        else:
            print(
                f"\n{user_load_input} could not be found in saved files\nreturning to main menu"
            )
            return
