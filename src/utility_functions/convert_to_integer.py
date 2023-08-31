import re


def convert_to_integer(value):
    try:
        if isinstance(value, str):
            if any(chr.isdigit() for chr in value):
                return round(float(re.search(r"[-+]?[0-9]*\.?[0-9]+", value).group()))
            else:
                print(
                    "\n----------------------------------------\ncould not extract number from user input\n----------------------------------------"
                )
                return None
        if isinstance(value, (int, float)):
            return round(value)
    except ValueError:
        print(
            "\n-------------------------------\nerror during integer conversion\n-------------------------------"
        )
        return None
