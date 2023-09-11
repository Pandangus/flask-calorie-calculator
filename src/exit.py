import os
import time
from utility_functions.return_to_main_menu import return_to_main_menu


def exit():
    try:
        time.sleep(0.25)
        os.system("clear")
        print("\nYou selected exit.\n\nEXIT\n----")

        while True:
            exit_user_input = (
                input(
                    "\ndo you want to exit calorie counter?\n\n---------------------------------\neverything not saved will be lost\n---------------------------------\n\nplease enter [y]es (enter 'x' to return to main menu)\n\n-> "
                )
                .strip()
                .lower()
            )

            if exit_user_input == "x":
                return return_to_main_menu()

            if exit_user_input == "y":
                os.system("clear")
                print("-------\nGoodbye\n-------\n")
                return True

            os.system("clear")
            print("invalid input")

    except TypeError as e:
        print(f"\nexit - TypeError: {e}")

    except Exception as e:
        print(f"\nexit - an unexpected error occurred: {e}")
