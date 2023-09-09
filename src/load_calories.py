import os
import re
import time
import pandas as pd
from utility_functions.return_to_main_menu import return_to_main_menu
from utility_functions.add_current_to_loaded import add_current_to_loaded


def load_calories(existing_entries, total_calories):
    try:
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
            print("\nno saved files found\n\nreturning to main menu")
            return None
        else:
            while True:
                load_file_input = (
                    input(
                        "-------------\n\nenter the name of the file you wish to load: (enter 'x' to return to main menu)\n\n-> "
                    )
                    .strip()
                    .lower()
                )
                if load_file_input == "x":
                    return return_to_main_menu()
                elif f"{load_file_input}_calories.csv" in os.listdir(SAVED_FILES_DIR):
                    os.system("clear")
                    loaded_entries = []
                    df = pd.read_csv(
                        f"{SAVED_FILES_DIR}/{load_file_input}_calories.csv"
                    )
                    load_count = 0
                    while load_count < len(df):
                        loaded_entries.append(
                            f"{df.at[load_count, 'calories']} kcal from {df.at[load_count, 'weight']} of {df.at[load_count, 'name']}"
                        )
                        load_count += 1
                    print(f"success! {load_file_input} has been loaded")
                    loaded_calories = df["calories"].sum()
                    if len(existing_entries) > 0:
                        while True:
                            user_choice_input = (
                                input(
                                    "\nwould you like to add current calories to loaded calories?\n\nplease enter [a]dd current calories or [l]oaded calories only (enter 'x' to return to main menu):\n\n-> "
                                )
                                .strip()
                                .lower()
                            )
                            if user_choice_input == "a":
                                return add_current_to_loaded(
                                    loaded_calories,
                                    total_calories,
                                    loaded_entries,
                                    existing_entries,
                                    load_file_input,
                                )
                            elif user_choice_input == "l":
                                os.system("clear")
                                print(
                                    f"success! current session has been replaced with the previously saved '{load_file_input}' session"
                                )
                                return loaded_entries, loaded_calories
                            elif user_choice_input == "x":
                                return return_to_main_menu()
                            else:
                                os.system("clear")
                                print("user input error")
                    else:
                        return loaded_entries, loaded_calories
                else:
                    print(
                        f"\n{load_file_input} could not be found in saved files\n\nplease enter [a]dd current calories or [l]oaded calories only (enter 'x' to return to main menu):\n\n-> "
                    )
    except ImportError as e:
        print(f"add_current_to_loaded - ImportError: {e}")
    except AttributeError as e:
        print(f"add_current_to_loaded - AttributeError: {e}")
    except NameError as e:
        print(f"add_current_to_loaded - NameError: {e}")
    except TypeError as e:
        print(f"add_current_to_loaded - TypeError: {e}")
    except KeyboardInterrupt:
        print("add_current_to_loaded - operation interrupted by the user.")
    except Exception as e:
        print(f"add_current_to_loaded - an unexpected error occurred: {e}")
