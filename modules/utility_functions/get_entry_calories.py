import re


def get_entry_calories(entry_string):
    try:
        re_match = re.search(r"^[0-9]+", entry_string)
        
        if re_match:
            return round(float(re_match.group()))

    except Exception as e:
        print(f"get_entry_calories - an unexpected error occurred: {e}")
