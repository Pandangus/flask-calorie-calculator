from flask import Flask, request, render_template, redirect, url_for
from modules.enter_calories_script import enter_calories_script

app = Flask(__name__)

entries = []
calories = 0


@app.route("/")
def index():
    return render_template("navbar.html")


@app.route("/enter_calories", methods=["GET", "POST"])
def enter_calories():
    global entries, calories, enter_calories_script

    if request.method == "POST":
        # Capture user input from the form and call the enter_calories function
        ingredient_name = request.form["ingredient_name"].strip().lower()
        weight_grams = round(float(request.form["weight_grams"]))

        # Call the enter_calories function here with the captured data
        # The function should update entries and calories

        entries, calories = enter_calories_script(
            entries, calories, ingredient_name, weight_grams
        )

        # Redirect to the result page
        return redirect(url_for("result", entries=entries, calories=calories))

    return render_template("enter_calories.html")


@app.route("/result")
def result():
    return render_template("result.html", entries=entries, calories=calories)
