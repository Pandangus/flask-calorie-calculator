import re


def convert_to_integer(string):
    return round(float(re.search(r"[-+]?[0-9]*\.?[0-9]+", string).group()))
