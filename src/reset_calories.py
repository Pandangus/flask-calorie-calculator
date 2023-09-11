import os
import time
from utility_functions.return_to_main_menu import return_to_main_menu


def reset_calories():
    try:
        MENU_HEADER = "RESET CALORIES"
        time.sleep(0.25)
        os.system("clear")
        print(
            f"You selected reset calories\n\n{MENU_HEADER}\n-------------------------------------------------------------------------------\nthis will erase all entries from ingredients list and reset total calories to 0\n-------------------------------------------------------------------------------\nthis cannot be undone!\n----------------------"
        )
        time.sleep(0.25)

        while True:
            reset_user_input = (
                input(
                    "\nare you sure you want to erase the current session?\n\nplease enter [y]es (enter 'x' to return to main menu)\n\n-> "
                )
                .strip()
                .lower()
            )

            if reset_user_input == "x":
                return return_to_main_menu()

            if reset_user_input == "y":
                os.system("clear")
                print(f"\ncalories reset to 0. contents of ingredient list deleted\n")
                return ([], 0)

            os.system("clear")
            print("invalid input")

    except Exception as e:
        print(f"reset_calories - an unexpected error occurred: {e}")
