import os
import time
import re
from modules.utility_functions.return_to_main_menu import return_to_main_menu
from modules.utility_functions.list_saved_files import list_saved_files
from modules.list_total_calories import list_total_calories


def delete_calories(ingredients_list, total_calories):
    try:
        MENU_HEADER = "DELETE CALORIES\n---------------"
        time.sleep(0.25)
        os.system("clear")
        print("\nYou selected delete calories.")
        time.sleep(0.25)

        while True:
            delete_type_input = (
                input(
                    f"\n{MENU_HEADER}\n\nplease enter: delete [e]ntry from current calories, or, delete [f]ile from previously saved files (enter 'x' to return to main menu):\n\n-> "
                )
                .strip()
                .lower()
            )

            if delete_type_input == "x":
                return return_to_main_menu()

            elif delete_type_input == "e":
                os.system("clear")
                print(MENU_HEADER)

                if not list_total_calories(ingredients_list):
                    return None
                
                delete_user_input = (
                    input(f"\nplease enter name of ingredient to remove\n\n-> ")
                    .strip()
                    .lower()
                )
                item_deleted = False

                if delete_user_input == "x":
                    return return_to_main_menu()

                for entry in ingredients_list:
                    if delete_user_input in entry:
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
                    os.system("clear")
                    print(
                        f"\n{delete_user_input} returned no matches. Nothing was deleted from ingredients list."
                    )
                    time.sleep(0.25)
                    print("\nreturning to main menu")
                    return None

            elif delete_type_input == "f":
                os.system("clear")
                SAVED_FILES_DIR = "saved_calorie_data"
                

                if list_saved_files(SAVED_FILES_DIR):
                    while True:
                        delete_file_input = (
                            input(
                                "\nenter the name of the file you wish to delete: (enter 'x' to return to main menu)\n\n-> "
                            )
                            .strip()
                            .lower()
                        )

                        if delete_file_input == "x":
                            return return_to_main_menu()

                        elif f"{delete_file_input}_calories.csv" in os.listdir(
                            SAVED_FILES_DIR
                        ):
                            os.system("clear")
                            while True:
                                double_check_input = (
                                    input(
                                        f"ATTENTION!\n----------\nare you sure you want to delete {delete_file_input} from saved files?\n\nthis action can not be undone\n\n\nenter: [y]es (enter 'x' to cancel and return to main menu)\n\n-> "
                                    )
                                    .strip()
                                    .lower()
                                )

                                if double_check_input == "x":
                                    return return_to_main_menu()

                                elif double_check_input == "y":
                                    os.system("clear")
                                    os.remove(
                                        f"saved_calorie_data/{delete_file_input}_calories.csv"
                                    )
                                    print(
                                        f"success! '{delete_file_input}' was deleted from saved files"
                                    )
                                    time.sleep(0.25)
                                    print("\nreturning to main menu")
                                    return None

                                os.system("clear")
                                print("invalid input\n\n")

                        os.system("clear")
                        print("invalid input\n\n")

            else:
                os.system("clear")
                print("invalid input")

    except ValueError as e:
        print(f"\ndelete_calories - ValueError: {e}")

    except TypeError as e:
        print(f"\ndelete_calories - TypeError: {e}")

    except Exception as e:
        print(f"\ndelete_calories - an unexpected error occurred: {e}")
