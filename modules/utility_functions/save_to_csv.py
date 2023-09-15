import os
import re
import pandas as pd


def save_to_csv(ingredients, directory_name, save_filename):
    try:
        calories = []
        weights = []
        names = []

        for row in ingredients:
            calories.append(re.search(r"^[0-9]+", row).group())
            weights.append(re.search(r"[0-9]+g", row).group())
            names.append(row.split(" of ", 1)[1])

        df = pd.DataFrame(data={"calories": calories, "weight": weights, "name": names})
        df.to_csv(
            f"{directory_name}/{save_filename}_calories.csv",
            index=False,
        )
        os.system("clear")
        print(
            f"success! '{save_filename}' calorie entries were saved\n\nreturning to main menu"
        )
        return

    except TypeError as e:
        print(f"replace_entry - TypeError: {e}")

    except re.error as e:
        print(f"portion_calories - re.error (regex error): {e}")

    except Exception as e:
        print(f"replace_entry - an unexpected error occurred: {e}")
