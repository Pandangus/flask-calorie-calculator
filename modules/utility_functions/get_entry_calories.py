import re


def get_entry_calories(entry_string):
    """

    Extract the calories from an entry string.

    This function extracts the calories from a given entry string that follows the format
    "{calories} kcal from {weight}g of {name}".

    Args:
        entry_string (str): The entry string to extract calories from.

    Returns:
        int: The extracted calories from the entry.

    Raises:
        Exception: If an unexpected error occurs during extraction.

    """
    
    try:
        re_match = re.search(r"^[0-9]+", entry_string)

        if re_match:
            return round(float(re_match.group()))

    except Exception as e:
        print(f"\nget_entry_calories - an unexpected error occurred: {e}")
