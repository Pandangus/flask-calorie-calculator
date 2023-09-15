import re


def get_entry_weight(entry_string):
    try:
        re_match = re.search(r"[0-9]+g", entry_string)

        if re_match:
            return round(float(re_match.group()[:-1]))

    except IndexError as e:
        print(f"get_entry_weight - TypeError: {e}")

    except re.error as e:
        print(f"get_entry_weight - re.error: {e}")

    except Exception as e:
        print(f"get_entry_weight - an unexpected error occurred: {e}")
