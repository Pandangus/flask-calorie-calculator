import time
from list_ingredients import list_ingredients
from exit import exit
from reset_calories import reset_calories
from delete_calories import delete_calories
from enter_calories import enter_calories


def menu():
    calorie_count = 0
    ingredients = []
    print("\nHello.")
    time.sleep(0.5)
    print("\nWelcome to the Calorie Counter.")
    time.sleep(0.25)

    while True:
        time.sleep(0.25)
        print(f"\nTotal calories: {round(calorie_count)}")
        user_input = input(
            "\nMAIN MENU\n---------\nPlease specify [e]nter calories, [d]elete calories, [l]ist total calories, [r]eset calories or e[x]it:\n\n-> "
        ).lower()

        if user_input == "e":
            enter_calories_result = enter_calories(ingredients, calorie_count)
            if enter_calories_result:
                ingredients, calorie_count = (
                    enter_calories_result[0],
                    enter_calories_result[1],
                )

        if user_input == "d":
            delete_calories_result = delete_calories(ingredients, calorie_count)
            if delete_calories_result:
                ingredients, calorie_count = (
                    delete_calories_result[0],
                    delete_calories_result[1],
                )

        if user_input == "l":
            list_ingredients(ingredients, calorie_count)

        if user_input == "r":
            if reset_calories() == "reset":
                calorie_count = 0
                ingredients = []

        if user_input == "x":
            if exit() == "shutdown":
                break


menu()
