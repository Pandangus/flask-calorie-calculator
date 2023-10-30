def get_entry_name(entry_string):
    """

    Extract the name from an entry string.

    This function extracts the name of an entry from a given string that follows the format
    "{calories} kcal from {weight}g of {name}".

    Args:
        entry_string (str): The entry string to extract the name from.

    Returns:
        str: The extracted name from the entry.

    Raises:
        IndexError: If the entry string does not follow the expected format.
        Exception: If an unexpected error occurs during extraction.

    """

    try:
        return entry_string.split(" of ", 1)[1]

    except IndexError as e:
        print(f"\nget_entry_name - IndexError: {e}")

    except Exception as e:
        print(f"\nget_entry_name - an unexpected error occurred: {e}")

