import re


def get_entry_calories(entry_string):
    try:
        return round(float(re.search(r"^[0-9]+", entry_string).group()))
    except TypeError:
        print(f"could not parse calorie value from entry: {entry_string}")
