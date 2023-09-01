import os
import time
from utility_functions.return_to_main_menu import return_to_main_menu


def exit():
    try:
        time.sleep(0.25)
        os.system('clear')
        user_input_2 = input(
            "\nYou selected exit.\n\nEXIT\n----\nThis will close the calorie counter.\n\n-----------------------\nData will not be saved.\n-----------------------\nare you sure?\nenter:\n[y]es or [n]o\n\n-> "
        ).lower()
        if user_input_2 == "y":
            os.system('clear')
            print("\n-------\nGoodbye\n-------")
            return True
        else:
            return return_to_main_menu()
    except Exception:
        print("\nEXIT\n----\nan unexpected error occurred")
        return return_to_main_menu()
