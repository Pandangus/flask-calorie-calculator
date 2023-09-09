import re


def get_entry_calories(entry_string):
    try:
        return round(float(re.search(r"^[0-9]+", entry_string).group()))
    
    except TypeError as e:
        print(f"get_entry_calories - TypeError: {e}")

    except Exception as e:
        print(f"get_entry_calories - an unexpected error occurred: {e}")
