import os
import pandas as pd

def load_calories():
    print(os.listdir("/Users/angushirst/Northcoders_followup/calorie-calculator/saved_calorie_data"))
    for file in os.listdir("/Users/angushirst/Northcoders_followup/calorie-calculator/saved_calorie_data"):
        print(file)


load_calories()