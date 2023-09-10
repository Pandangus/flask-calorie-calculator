import os
from copy import deepcopy


def replace_entry(
    existing_calories,
    existing_entries,
    new_entry_calories,
    existing_entry,
    summary,
    merged,
):
    try:
        updated_entries = deepcopy(existing_entries)
        target_index = updated_entries.index(existing_entry)
        del updated_entries[target_index]
        updated_entries.insert(target_index, summary)
        existing_calories += new_entry_calories
        os.system("clear")

        if merged:
            print(f"\nsuccess! entries merged into new entry: '{summary}'")

        else:
            print(f"\nsuccess! '{existing_entry}' replaced with '{summary}'")

        return updated_entries, existing_calories

    except TypeError as e:
        print(f"replace_entry - TypeError: {e}")

    except Exception as e:
        print(f"replace_entry - an unexpected error occurred: {e}")
