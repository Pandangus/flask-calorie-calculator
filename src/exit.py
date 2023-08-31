import time
from utility_functions.return_to_main_menu import return_to_main_menu


def exit():
    time.sleep(0.25)
    user_input_2 = input(
        "\nYou selected exit.\n\nEXIT\n----\nThis will close the calorie counter.\n\n-----------------------\nData will not be saved.\n-----------------------\nare you sure?\nenter:\n[y]es or [n]o\n\n-> "
    ).lower()
    if user_input_2 == "y":
        print("\n-------\nGoodbye\n-------")
        return True
    else:
        return return_to_main_menu()
