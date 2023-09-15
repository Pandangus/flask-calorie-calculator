import os
import time
from src.utility_functions.return_to_main_menu import return_to_main_menu
from src.utility_functions.save_to_csv import save_to_csv


def save_calories(ingredients):
    try:
        SAVED_FILES_DIR = "saved_calorie_data"
        time.sleep(0.25)
        os.system("clear")
        print("you selected save calories")

        if len(ingredients) == 0:
            print("\nno entries in current session\n\nreturning to main menu")
            return

        user_input = (
            input(
                "\nSAVE CALORIES\n-------------\nenter a name for this calorie list: (enter 'x' to return to main menu)\n\n-> "
            )
            .strip()
            .lower()
        )

        if user_input == "x":
            return return_to_main_menu()

        if f"{user_input}_calories.csv" in os.listdir(SAVED_FILES_DIR):
            os.system("clear")
            while True:
                existing_conflict_input = input(
                    f"a file named '{user_input}' already exists\n\nare you sure you want to save? (saving now will overwrite the existing file)\n\nplease enter [s]ave and overwrite (enter 'x' to return to main menu):\n\n-> "
                )

                if existing_conflict_input == "x":
                    return return_to_main_menu()

                if existing_conflict_input == "s":
                    return save_to_csv(ingredients, SAVED_FILES_DIR, user_input)

                os.system("clear")
                print("invalid input\n")
                time.sleep(0.25)

        return save_to_csv(ingredients, SAVED_FILES_DIR, user_input)

    except NameError as e:
        print(f"\nmain_user_interface - NameError: {e}")

    except TypeError as e:
        print(f"\nmain_user_interface - TypeError: {e}")

    except Exception as e:
        print(f"\nmain_user_interface - an unexpected error occurred: {e}")
