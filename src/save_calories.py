import re
import os
import time
import pandas as pd
from utility_functions.return_to_main_menu import return_to_main_menu


def save_calories(ingredients):
    try:
        SAVED_FILES_DIR = "saved_calorie_data"
        time.sleep(0.25)
        os.system("clear")

        if len(ingredients) == 0:
            print("no entries in current session\n\nreturning to main menu")
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

        calories = []
        weights = []
        names = []

        for row in ingredients:
            calories.append(re.search(r"^[0-9]+", row).group())
            weights.append(re.search(r"[0-9]+g", row).group())
            names.append(row.split(" of ", 1)[1])

        df = pd.DataFrame(data={"calories": calories, "weight": weights, "name": names})
        df.to_csv(
            f"{SAVED_FILES_DIR}/{user_input}_calories.csv",
            index=False,
        )
        os.system('clear')
        print(f"success! '{user_input}' calorie entries were saved\n\nreturning to main menu")
        return
        

    except NameError as e:
        print(f"\nmain_user_interface - NameError: {e}")

    except TypeError as e:
        print(f"\nmain_user_interface - TypeError: {e}")

    except Exception as e:
        print(f"\nmain_user_interface - an unexpected error occurred: {e}")
