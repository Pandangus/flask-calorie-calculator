def get_entry_name(entry_string):
    try:
        return entry_string.split(" of ", 1)[1]
    except TypeError:
        print(f"could not parse ingredient name value from entry: {entry_string}")
