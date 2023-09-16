from flask import Flask, request, render_template, redirect, url_for
from modules.enter_calories_script import enter_calories_script
from modules.utility_functions.convert_to_integer import convert_to_integer

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


@app.route("/list")
def list():
    return render_template("list.html", entries=entries, calories=calories)
