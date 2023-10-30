def calories_to_add(weight_in_g, calories_per_100g):
    """

    Calculate the calories for a given weight and calories per 100g.

    This function calculates the calories for a given weight (in grams) and calories per 100g
    of an ingredient.

    Args:
        weight_in_g (float): Weight of the ingredient in grams.
        calories_per_100g (float): Calories per 100g of the ingredient.

    Returns:
        int: Calculated calories for the given weight and calories per 100g.

    Raises:
        ValueError: If weight_in_g or calories_per_100g are not valid numbers.
        Exception: If an unexpected error occurs during the calculation.

    """

    try:
        return round(calories_per_100g * (weight_in_g / 100))

    except ValueError as e:
        print(f"\ncalories_to_add - ValueError: {e}")

    except Exception as e:
        print(f"\ncalories_to_add - an unexpected error occurred: {e}")


