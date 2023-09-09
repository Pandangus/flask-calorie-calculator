def calories_to_add(weight_in_g, calories_per_100g):
    try:
        return round(calories_per_100g * (weight_in_g / 100))
    except ValueError as e:
        print(
            f"\ncalories_to_add - ValueError: {e}\n"
        )
