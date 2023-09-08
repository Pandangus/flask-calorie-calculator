import re


def get_entry_weight(entry_string):
    try:
        return round(float(re.search(r"[0-9]+g", entry_string).group()[:-1]))
    except TypeError:
        print(f"could not parse weight value from entry: {entry_string}")
