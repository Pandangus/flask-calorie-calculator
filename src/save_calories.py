import re
import os
import time
import pandas as pd


def save_calories(ingredients):
    try:
        time.sleep(0.25)
        os.system("clear")
        user_input = input(
            "\nSAVE CALORIES\n-------------\nEnter a name for this calorie list: (enter 'x' to return to main menu)\n\n-> "
        )
        calories = []
        weights = []
        names = []
        for row in ingredients:
            calories.append(re.search(r"^[0-9]+", row).group())
            weights.append(re.search(r"[0-9]+g", row).group())
            names.append(re.search(r"(\w+)$", row).group())
        df = pd.DataFrame(data={"calories": calories, "weight": weights, "name": names})
        df.to_csv(
            f"/Users/angushirst/Northcoders_followup/calorie-calculator/saved_calorie_data/{user_input}_calories.csv",
            index=False,
        )
    except TypeError:
        print("ingredient list error\nreturning to main menu")
        return
