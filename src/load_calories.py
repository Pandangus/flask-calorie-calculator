import os
import re
import time
import pandas as pd
from utility_functions.return_to_main_menu import return_to_main_menu

def load_calories():
    saved_files_dir = os.listdir("/Users/angushirst/Northcoders_followup/calorie-calculator/saved_calorie_data")
    os.system("clear")
    time.sleep(0.25)
    print("\nLOAD CALORIES\n-------------")
    saved_file_count = 0
    for file in saved_files_dir:
        if str(file)[-13:].lower() == "_calories.csv":
            time.sleep(0.25)
            if saved_file_count == 0:
                print("\nsaved files:\n-------------")
            saved_file_count +=1
            print(">", re.search("^[a-z]+", file).group())
    if saved_file_count == 0:
        os.system('clear')
        print("\nno saved files found\n\nreturning to main menu\n")
        return None    
    else:
        user_load_input = input("-------------\n\nenter the name of the file you wish to load: (enter 'x' to return to main menu)\n\n-> ")
        if user_load_input == "x":
            return return_to_main_menu()
        if f"{user_load_input}_calories.csv" in saved_files_dir:
            loaded_data = []
            df = pd.read_csv(f"/Users/angushirst/Northcoders_followup/calorie-calculator/saved_calorie_data/{user_load_input}_calories.csv")
            load_count = 0
            while load_count < len(df):
                loaded_data.append(f"{df.at[load_count, 'calories']} kcal from {df.at[load_count, 'weight']} of {df.at[load_count, 'name']}")
                load_count += 1
            return loaded_data, df["calories"].sum()
