from flask import Flask, request, render_template, redirect, url_for
from modules.enter_calories_script import enter_calories_script
from modules.utility_functions.update_calorie_data import update_calorie_data

app = Flask(__name__)

entries = []
calories = 0


@app.route("/")
def index():
    global calories
    return render_template("navbar.html", calories=calories)


@app.route("/enter_calories", methods=["GET", "POST"])
def enter_calories():
    global entries, calories, enter_calories_script

    if request.method == "POST":
        # Capture user input from the form and call the enter_calories function
        form_weight_grams = request.form["weight_grams"]
        form_ingredient_name = request.form["ingredient_name"].strip().lower()

        # Call the enter_calories function here with the captured data
        # The function should update entries and calories

        entries, calories = enter_calories_script(
            entries, calories, form_ingredient_name, form_weight_grams
        )

        # Redirect to the result page
        return redirect(url_for("list", entries=entries, calories=calories))

    return render_template("enter_calories.html")


@app.route("/manual_entry", methods=["GET", "POST"])
def manual_entry():
    global entries, calories

    if request.method == "POST":
        # Capture user input from the form and call the enter_calories function
        form_weight_grams = request.form["weight_grams"]
        form_calories_100g = request.form["calories_100g"]
        form_ingredient_name = request.form["ingredient_name"].strip().lower()

        # Call the enter_calories function here with the captured data
        # The function should update entries and calories

        entries, calories = update_calorie_data(
            form_calories_100g,
            form_weight_grams,
            form_ingredient_name,
            entries,
            calories,
        )

        # Redirect to the result page
        return redirect(url_for("list", entries=entries, calories=calories))

    return render_template("manually_enter_calories.html")


@app.route("/portion_number", methods=["GET", "POST"])
def portion_number():
    global calories

    if request.method == "POST":
        form_portions = int(request.form["number_of_portions"])
        # Redirect to the result page
        return redirect(url_for("portion_result", calories=calories, form_portions=form_portions))

    return render_template("portion_number.html")


@app.route("/portion_result", methods=["POST"])
def portion_result():
    form_portions = request.form.get('number_of_portions', type=int)
    calories_per_portion = round(calories / form_portions)
    return render_template("portion_result.html", calories=calories, form_portions=form_portions, calories_per_portion=calories_per_portion)


@app.route("/list")
def list():
    return render_template("list.html", entries=entries, calories=calories)
