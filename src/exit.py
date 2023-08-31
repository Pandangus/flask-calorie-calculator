import time
from utility_functions.return_to_main_menu import return_to_main_menu


def exit():
    menu_header = "EXIT\n----"
    try:
        time.sleep(0.25)
        user_input_2 = input(
            f"\nYou selected exit.\n\n{menu_header}\nThis will close the calorie counter.\n\n-----------------------\nData will not be saved.\n-----------------------\nare you sure?\nenter:\n[y]es or [n]o\n\n-> "
        ).lower()
        if user_input_2 == "y":
            print("\n-------\nGoodbye\n-------")
            return True
        else:
            return return_to_main_menu()
    except Exception:
        print(f"\n{menu_header}\nan unexpected error occurred")
        return return_to_main_menu()
