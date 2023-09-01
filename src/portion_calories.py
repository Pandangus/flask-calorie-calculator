import os
import time
import re
from utility_functions.return_to_main_menu import return_to_main_menu


def portion_calories(calories):
    try:
        menu_header = "PORTION CALORIES\n----------------"
        time.sleep(0.25)
        os.system('clear')
        portion_user_input = input(
            f"\n{menu_header}\nhow many portions? (enter 'x' to cancel, and return to main menu)\n\n-> "
        ).lower()
        if portion_user_input != "x":
            os.system('clear')
            processed_portion_input = round(
                float(re.search(r"[-+]?[0-9]*\.?[0-9]+", portion_user_input).group())
            )
            print(
                f"\n{menu_header}\n{calories} total calories (kcal)\ndivided into {portion_user_input} portions\n---------------------------\n{round(calories / processed_portion_input)} calories per portion\n---------------------------"
            )
            return
        else:
            return_to_main_menu()
    except (TypeError, AttributeError):
        print(f"\n{menu_header}\nan unexpected error occurred")
        return return_to_main_menu()
