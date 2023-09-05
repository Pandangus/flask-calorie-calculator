import os
import time
from utility_functions.return_to_main_menu import return_to_main_menu


def list_total_calories(ingredient_list, total_calories=None):
    try:
        MENU_HEADER = "\nLIST TOTAL CALORIES\n------------------------"
        time.sleep(0.25)
        if total_calories:
            os.system('clear')
            print(f"{MENU_HEADER}")
        if len(ingredient_list) == 0:
            print("ingredient list contains no entries\n")
            time.sleep(0.25)
            input("press enter to return to main menu\n\n-> ")
            return return_to_main_menu()
        else:    
            for entry in ingredient_list:
                time.sleep(0.25)
                print(entry)
            time.sleep(0.25)
            if total_calories:
                print(
                    f"------------------------\n{total_calories} kcal total\n------------------------"
                )
            return True
    except TypeError:
        if total_calories:
            print(f"{MENU_HEADER}\nan unexpected error occurred")
        else:
            print(f"\nan unexpected error occurred")
        return return_to_main_menu()
