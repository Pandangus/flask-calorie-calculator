import os
import time


def list_total_calories(existing_entries, total_calories=None):
    try:
        MENU_HEADER = "\nLIST TOTAL CALORIES\n------------------------"
        time.sleep(0.25)

        if total_calories:
            os.system("clear")
            print(f"{MENU_HEADER}")

        if len(existing_entries) == 0:
            print("current calories list contains no entries")
            time.sleep(0.25)
            print("\nreturning to main menu")
            return None

        else:
            for entry in existing_entries:
                time.sleep(0.25)
                print(f"- {entry}")
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
