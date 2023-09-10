import os
import time
from utility_functions.return_to_main_menu import return_to_main_menu


def list_total_calories(existing_ingredients, total_calories=None):
    try:
        MENU_HEADER = "\nLIST TOTAL CALORIES\n------------------------"
        time.sleep(0.25)

        if total_calories:
            os.system("clear")
            print(f"{MENU_HEADER}")

        if len(existing_ingredients) == 0:
            print("ingredient list contains no entries\n")
            time.sleep(0.25)
            input("press enter to return to main menu\n\n-> ")
            return return_to_main_menu()

        else:
            for entry in existing_ingredients:
                time.sleep(0.25)
                print(entry)
            time.sleep(0.25)

            if total_calories:
                print(
                    f"------------------------\n{total_calories} kcal total\n------------------------"
                )
            return True
        
    except ValueError as e:
        print(f"\nlist_total_calories - ValueError: {e}")

    except TypeError as e:
        print(f"\nlist_total_calories - TypeError: {e}")

    except IndexError as e:
        print(f"\nlist_total_calories - IndexError: {e}")

    except Exception as e:
        print(f"\nlist_total_calories - an unexpected error occurred: {e}")
