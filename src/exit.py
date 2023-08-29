import time


def exit():
    time.sleep(0.25)
    print(
        "\nYou selected exit.\n\nThis will close the calorie counter.\n\nData will not be saved."
    )
    time.sleep(0.5)
    user_input_2 = input(
        "\n-----------------\nare you sure?\nenter:\n[y]es or [n]o\n\n-> "
    ).lower()
    if user_input_2 == "y":
        print("\n-------\nGoodbye\n-------")
        return "shutdown"