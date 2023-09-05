import os
import time
import re
from utility_functions.return_to_main_menu import return_to_main_menu
from list_total_calories import list_total_calories


def delete_calories(ingredients_list, total_calories):
    try:
        menu_header = "DELETE CALORIES\n---------------"
        time.sleep(0.25)
        os.system("clear")
        print("\nYou selected delete calories.")
        time.sleep(0.25)
        print(f"\n{menu_header}")
        if not list_total_calories(ingredients_list):
            return None
        delete_user_input = input(
            f"\nPlease enter name of ingredient to remove\n\n-> "
        )
        item_deleted = False
        for entry in ingredients_list:
            if delete_user_input.lower() in entry:
                ingredients_list.remove(entry)
                total_calories -= int(re.search(r"\d+", entry).group())
                os.system("clear")
                print(
                    f"\nsuccess! {delete_user_input} removed from ingredient list"
                )
                item_deleted = True
                time.sleep(0.25)
                print("\nreturning to main menu")
                return (ingredients_list, total_calories)
        if not item_deleted:
            os.system('clear')
            print(
                f"\n{delete_user_input} returned no matches. Nothing was deleted from ingredients list."
            )
            time.sleep(0.25)
            print("\nreturning to main menu")
            return None
    except TypeError:
        print(f"\n{menu_header}\nan unexpected error occurred")
        return return_to_main_menu()
