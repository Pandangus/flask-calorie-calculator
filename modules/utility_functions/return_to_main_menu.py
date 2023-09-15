import os
import time


def return_to_main_menu():
    try:
        time.sleep(0.25)
        os.system("clear")
        print("\nreturning to main menu")
        return None

    except Exception as e:
        print(f"return_to_main_menu - an unexpected error occurred: {e}")
