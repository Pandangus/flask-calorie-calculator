def menu():
    while True:
        
        calorie_count = 0;
        print("Total calories: ", calorie_count)

        user_input = input(
            "Please specify [e]nter calories, [d]elete calories, [l]ist total calories, [r]eset calories or e[x]it:\n"
        )

        if user_input == "e":
            print("You selected enter calories.")

        if user_input == "d":
            print("You selected delete calories.")

        if user_input == "r":
            print("You selected reset calories.")

        if user_input == "x":
            user_input_2 = input("\nYou selected exit.\n-----------------\nare you sure?\nenter:\n[y]es or [n]o\n")
            if user_input_2 == 'y':
                print("-------\nGoodbye\n-------")
                break

menu()