import os
import time
import re


def list_saved_files(dir_name):
    try:
        saved_file_count = 0

        for file in os.listdir(dir_name):
            if str(file)[-13:].lower() == "_calories.csv":
                time.sleep(0.25)

                if saved_file_count == 0:
                    print("\nall saved files:\n----------------")

                saved_file_count += 1
                print(">", re.search(r"^[a-z]+", file).group())

        print("----------------")

        if saved_file_count == 0:
            os.system("clear")
            print("\nno saved files found")
            return False
        else:
            return True

    except TypeError as e:
        print(f"replace_entry - TypeError: {e}")

    except Exception as e:
        print(f"replace_entry - an unexpected error occurred: {e}")
