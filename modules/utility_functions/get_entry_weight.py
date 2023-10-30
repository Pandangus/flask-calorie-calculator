import re


def get_entry_weight(entry_string):
    """

    Extract the weight from an entry string.

    This function extracts the weight from a given entry string that follows the format
    "{calories} kcal from {weight}g of {name}".

    Args:
        entry_string (str): The entry string to extract the weight from.

    Returns:
        int: The extracted weight (in grams) from the entry.

    Raises:
        IndexError: If the entry string does not follow the expected format.
        re.error: If a regular expression error occurs during extraction.
        Exception: If an unexpected error occurs during extraction.

    """

    try:
        re_match = re.search(r"[0-9]+g", entry_string)

        if re_match:
            return round(float(re_match.group()[:-1]))

    except IndexError as e:
        print(f"get_entry_weight - IndexError: {e}")

    except re.error as e:
        print(f"get_entry_weight - re.error: {e}")

    except Exception as e:
        print(f"get_entry_weight - an unexpected error occurred: {e}")
