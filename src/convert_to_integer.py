import re


def convert_to_integer(value):
    try:
        if isinstance(value, str):
            return round(float(re.search(r"[-+]?[0-9]*\.?[0-9]+", value).group()))
        elif isinstance(value, (int, float)):
            return round(value)
        else:
            raise ValueError
    except ValueError:
        print(
            "\n-------------------------------\nerror during integer conversion\n-------------------------------\n"
        )
        return None
