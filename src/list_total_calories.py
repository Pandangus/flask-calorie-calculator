import time


def list_total_calories(ingredientList, totalCalories):
    time.sleep(0.25)
    print("\n------------------------")
    for entry in ingredientList:
        time.sleep(0.25)
        print(entry)
    time.sleep(0.25)
    print(
        f"------------------------\n{totalCalories} kcal total\n------------------------"
    )