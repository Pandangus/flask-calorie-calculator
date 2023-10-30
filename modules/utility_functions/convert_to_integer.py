import re


def convert_to_integer(value, unit_of_measurement):
    """

    Convert a value to an integer.

    This function attempts to convert a value to an integer. It handles various input types,
    including integers, floats, and strings with numeric representations.

    Args:
        value (int, float, str): The value to be converted.
        unit_of_measurement (str): A description of the unit of measurement for the value.

    Returns:
        int: The converted integer value.

    Raises:
        Exception: If the value cannot be parsed as an integer, an error message is raised.

    """

    try:
        if isinstance(value, (int, float)):
            return round(value)

        if isinstance(value, str):
            re_match = re.search(r"[-+]?[0-9]*\.?[0-9]+", value)
            if re_match:
                return round(float(re_match.group()))

        raise Exception(
            f"Error! Could not parse integer from {unit_of_measurement} input. Expected either an integer (0, 1, 2) or float value (0.5, 1.5, 2.5)."
        )

    except Exception as e:
        print(f"convert_to_integer - an unexpected error occurred: {e}")
