import re
import time


def convert_to_integer(value, unit_of_measurement):
    try:
        if isinstance(value, (int, float)):
            return round(value)

        if isinstance(value, str):
            re_match = re.search(r"[-+]?[0-9]*\.?[0-9]+", value)
            if re_match:
                return round(float(re_match.group()))

        print(
            f"\nerror! could not parse integer from {unit_of_measurement} input. please enter either an integer (0, 1, 2) or float value (0.5, 1.5, 2.5)"
        )
        time.sleep(0.25)
        return

    except Exception as e:
        print(f"convert_to_integer - an unexpected error occurred: {e}")
