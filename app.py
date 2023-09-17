from flask import Flask, request, render_template, redirect, url_for
from modules.enter_calories_script import enter_calories_script
from modules.utility_functions.update_calorie_data import update_calorie_data
import re

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
        form_weight_grams = request.form["weight_grams"]
        form_ingredient_name = request.form["ingredient_name"].strip().lower()

        entries, calories = enter_calories_script(
            entries, calories, form_ingredient_name, form_weight_grams
        )

        return redirect(url_for("list", entries=entries, calories=calories))

    return render_template("enter_calories.html")


@app.route("/manual_entry", methods=["GET", "POST"])
def manual_entry():
    global entries, calories

    if request.method == "POST":
        form_weight_grams = request.form["weight_grams"]
        form_calories_100g = request.form["calories_100g"]
        form_ingredient_name = request.form["ingredient_name"].strip().lower()

        entries, calories = update_calorie_data(
            form_calories_100g,
            form_weight_grams,
            form_ingredient_name,
            entries,
            calories,
        )

        return redirect(url_for("list", entries=entries, calories=calories))

    return render_template("manually_enter_calories.html")


@app.route("/delete_entry", methods=["GET", "POST"])
def delete_entry():
    global entries, calories
    if request.method == "GET":
        return render_template("delete_entry.html")

    else:
        form_entry_to_delete = request.form.get("entry_to_delete").strip().lower()
        for entry in entries:
            if form_entry_to_delete in entry:
                entries.remove(entry)
                calories -= int(re.search(r"^\d+", entry).group())
                return redirect(url_for("delete_confirmation"))

        return render_template("navbar.html")


app.route("/delete_confirmation", method=["POST"])


def delete_confirmation():
    return render_template("delete_confirmation.html")


@app.route("/portion_number", methods=["GET", "POST"])
def portion_number():
    if request.method == "POST":
        return redirect(url_for("portion_result"))

    return render_template("portion_number.html")


@app.route("/portion_result", methods=["POST"])
def portion_result():
    form_portions = request.form.get("number_of_portions", type=int)
    calories_per_portion = round(calories / form_portions)
    return render_template(
        "portion_result.html",
        calories=calories,
        form_portions=form_portions,
        calories_per_portion=calories_per_portion,
    )


@app.route("/reset_request", methods=["GET", "POST"])
def reset_request():
    return render_template("reset_request.html")


@app.route("/reset_confirmed", methods=["GET", "POST"])
def reset_confirmed():
    global entries, calories
    entries = []
    calories = 0
    return render_template("reset_confirmed.html")


@app.route("/list")
def list():
    return render_template("list.html", entries=entries, calories=calories)
