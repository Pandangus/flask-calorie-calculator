import time
from utility_functions.return_to_main_menu import return_to_main_menu


def reset_calories():
    menu_header = "RESET CALORIES"
    time.sleep(0.25)
    print("\nYou selected reset calories.")
    print(
        f"\n{menu_header}\n--------------------------------------------------------------------------------\nThis will reset total calories to 0 and erase all entries from ingredients list.\n--------------------------------------------------------------------------------\nThis cannot be undone!\n----------------------"
    )
    time.sleep(0.25)
    reset_user_input = input("\nare you sure?\nenter:\n[y]es or [n]o\n\n-> ").lower()
    if reset_user_input == "y":
        print(
            f"\n{menu_header}\n--------------\ncalories reset to 0. contents of ingredient list deleted\n"
        )
        return ([], 0)
    else:
        return return_to_main_menu()
