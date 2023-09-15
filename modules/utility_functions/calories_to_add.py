def calories_to_add(weight_in_g, calories_per_100g):
    try:
        return round(calories_per_100g * (weight_in_g / 100))

    except ValueError as e:
        print(f"calories_to_add - ValueError: {e}")

    except TypeError as e:
        print(f"calories_to_add - TypeError: {e}")

    except Exception as e:
        print(f"calories_to_add - an unexpected error occurred: {e}")
