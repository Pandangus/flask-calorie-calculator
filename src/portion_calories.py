import os
import time
import re
from src.utility_functions.return_to_main_menu import return_to_main_menu


def portion_calories(calories):
    try:
        MENU_HEADER = "PORTION CALORIES\n----------------"
        time.sleep(0.25)
        os.system("clear")
        print(f"you selected portion calories\n\n{MENU_HEADER}")
        while True:
            portion_user_input = (
                input(
                    f"\nplease enter number of portions? (enter 'x' to cancel, and return to main menu)\n\n-> "
                )
                .strip()
                .lower()
            )

            re_match = re.search(r"[-+]?[0-9]*\.?[0-9]+", portion_user_input)

            if re_match:
                os.system("clear")
                processed_portion_input = round(float(re_match.group()))
                print(
                    f"\n{MENU_HEADER}\n{calories} total calories (kcal)\ndivided into {portion_user_input} portions\n---------------------------\n{round(calories / processed_portion_input)} calories per portion\n---------------------------"
                )
                return

            if portion_user_input == "x":
                return return_to_main_menu()

            os.system("clear")
            print("\ninvalid input\n")

    except TypeError as e:
        print(f"portion_calories - TypeError: {e}")

    except ValueError as e:
        print(f"portion_calories - TypeError: {e}")

    except re.error as e:
        print(f"portion_calories - re.error (regex error): {e}")

    except Exception as e:
        print(f"portion_calories - an unexpected error occurred: {e}")
