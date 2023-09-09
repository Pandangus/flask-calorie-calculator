import os
import time
import re
from utility_functions.return_to_main_menu import return_to_main_menu


def portion_calories(calories):
    try:
        menu_header = "PORTION CALORIES\n----------------"
        time.sleep(0.25)
        os.system("clear")
        portion_user_input = input(
            f"\n{menu_header}\nhow many portions? (enter 'x' to cancel, and return to main menu)\n\n-> "
        ).strip().lower()

        if portion_user_input != "x":
            os.system("clear")
            processed_portion_input = round(
                float(re.search(r"[-+]?[0-9]*\.?[0-9]+", portion_user_input).group())
            )
            print(
                f"\n{menu_header}\n{calories} total calories (kcal)\ndivided into {portion_user_input} portions\n---------------------------\n{round(calories / processed_portion_input)} calories per portion\n---------------------------"
            )
            return

        else:
            return_to_main_menu()

    except ImportError as e:
        print(f"portion_calories - ImportError: {e}")

    except AttributeError as e:
        print(f"portion_calories - AttributeError: {e}")

    except NameError as e:
        print(f"portion_calories - NameError: {e}")

    except TypeError as e:
        print(f"portion_calories - TypeError: {e}")

    except ValueError as e:
        print(f"portion_calories - TypeError: {e}")

    except re.error as e:
        print(f"portion_calories - re.error (regex error): {e}")

    except KeyboardInterrupt:
        print("portion_calories - operation interrupted by the user.")

    except Exception as e:
        print(f"portion_calories - an unexpected error occurred: {e}")
