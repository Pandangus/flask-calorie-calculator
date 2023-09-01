import os
import time
from utility_functions.return_to_main_menu import return_to_main_menu


def list_total_calories(ingredientList, totalCalories):
    try:
        menu_header = "\nLIST TOTAL CALORIES\n------------------------"
        time.sleep(0.25)
        os.system('clear')
        print(f"{menu_header}")
        for entry in ingredientList:
            time.sleep(0.25)
            print(entry)
        time.sleep(0.25)
        print(
            f"------------------------\n{totalCalories} kcal total\n------------------------"
        )
    except TypeError:
        print(f"{menu_header}\nan unexpected error occurred")
        return return_to_main_menu()
