def get_entry_name(entry_string):
    try:
        return entry_string.split(" of ", 1)[1]

    except IndexError as e:
        print(f"get_entry_name - TypeError: {e}")

    except Exception as e:
        print(f"get_entry_name - an unexpected error occurred: {e}")
