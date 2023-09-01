def calories_to_add(weight_in_g, calories_per_100g):
    try:
        return round(calories_per_100g * (weight_in_g / 100))
    except ValueError:
        print(
            "\n------------------------------\nerror calculating new calories\n------------------------------\n"
        )
        return None
