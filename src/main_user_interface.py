import os
import time
from src.list_total_calories import list_total_calories
from src.exit import exit
from src.reset_calories import reset_calories
from src.delete_calories import delete_calories
from src.enter_calories import enter_calories
from src.manually_enter_calories import manually_enter_calories
from src.portion_calories import portion_calories
from src.save_calories import save_calories
from src.load_calories import load_calories


def menu():
    try:
        calorie_count = 0
        ingredients = []

        os.system("clear")
        print("\nHello.")
        time.sleep(0.5)
        os.system("clear")
        print("\nWelcome to the Calorie Counter.")
        time.sleep(0.25)

        while True:
            time.sleep(0.25)
            print(f"\n\nTotal calories: {calorie_count}")
            user_input = (
                input(
                    "\nMAIN MENU\n---------\nSelect [e]nter calories, [m]anually enter calories, [d]elete calories, [l]ist total calories, [p]ortion calories, l[o]ad calories, [s]ave calories, [r]eset calories or e[x]it:\n\n-> "
                )
                .strip()
                .lower()
            )

            if user_input == "e":
                os.system("clear")
                enter_calories_result = enter_calories(ingredients, calorie_count)

                if enter_calories_result:
                    ingredients, calorie_count = (
                        enter_calories_result[0],
                        enter_calories_result[1],
                    )

            if user_input == "m":
                os.system("clear")
                manually_enter_result = manually_enter_calories(
                    ingredients, calorie_count
                )

                if manually_enter_result:
                    ingredients, calorie_count = (
                        manually_enter_result[0],
                        manually_enter_result[1],
                    )

            if user_input == "d":
                os.system("clear")
                delete_calories_result = delete_calories(ingredients, calorie_count)

                if delete_calories_result:
                    ingredients, calorie_count = (
                        delete_calories_result[0],
                        delete_calories_result[1],
                    )

            if user_input == "l":
                os.system("clear")
                list_total_calories(ingredients, calorie_count)

            if user_input == "p":
                os.system("clear")
                portion_calories(calorie_count)

            if user_input == "o":
                os.system("clear")
                load_calories_result = load_calories(ingredients, calorie_count)

                if load_calories_result:
                    ingredients, calorie_count = (
                        load_calories_result[0],
                        load_calories_result[1],
                    )

            if user_input == "s":
                os.system("clear")
                save_calories(ingredients)

            if user_input == "r":
                os.system("clear")
                reset_calories_result = reset_calories()

                if reset_calories_result:
                    ingredients, calorie_count = (
                        reset_calories_result[0],
                        reset_calories_result[1],
                    )

            if user_input == "x":
                os.system("clear")

                if exit() == True:
                    break

            if user_input not in ["e", "m", "d", "l", "p", "o", "s", "r", "x"]:
                os.system("clear")

    except TypeError as e:
        print(f"\nmain_user_interface - TypeError: {e}")

    except Exception as e:
        print(f"\nmain_user_interface - an unexpected error occurred: {e}")


if __name__ == "__main__":
    menu()
