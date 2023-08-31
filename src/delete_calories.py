import time
import re
from utility_functions.return_to_main_menu import return_to_main_menu


def delete_calories(ingredients_list, total_calories):
    try:
        time.sleep(0.25)
        print("\nYou selected delete calories.")
        time.sleep(0.25)
        delete_user_input = input(
            "\nDELETE CALORIES\n---------------\nPlease enter name of ingredient to remove\n\n-> "
        )
        item_deleted = False
        for entry in ingredients_list:
            if delete_user_input.lower() in entry:
                ingredients_list.remove(entry)
                total_calories -= int(re.search(r"\d+", entry).group())
                print(
                    f"\nDELETE CALORIES\n---------------\nsuccess! {delete_user_input} removed from ingredient list"
                )
                item_deleted = True
                time.sleep(0.25)
                print("\nreturning to main menu")
                return (ingredients_list, total_calories)
        if not item_deleted:
            print(
                f"\nDELETE CALORIES\n----------------------------------------------------------------------\n{delete_user_input} returned no matches. Nothing was deleted from ingredients list.\n----------------------------------------------------------------------"
            )
            return return_to_main_menu()
    except TypeError:
        print("\nan unexpected error occurred")
        return return_to_main_menu()
    
delete_calories(0, 0)
