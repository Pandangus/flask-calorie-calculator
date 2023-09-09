import re
import time


def convert_to_integer(value, unit_of_measurement):
    try:
        if isinstance(value, str):
            if any(chr.isdigit() for chr in value):
                return round(float(re.search(r"[-+]?[0-9]*\.?[0-9]+", value).group()))

            else:
                print(
                    f"\nerror! could not parse integer from {unit_of_measurement} input. please enter either an integer (0, 1, 2) or float value (0.5, 1.5, 2.5)"
                )
                time.sleep(0.25)
                return

        if isinstance(value, (int, float)):
            return round(value)

    except TypeError as e:
        print(f"convert_to_integer - TypeError: {e}")

    except Exception as e:
        print(f"convert_to_integer - an unexpected error occurred: {e}")
