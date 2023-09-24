from flask import Flask, request, render_template, redirect, url_for
from modules.enter_calories_script import enter_calories_script
from modules.utility_functions.update_calorie_data import update_calorie_data
from modules.search_calories import search_calories
import re

app = Flask(__name__)

entries = []
calories = 0


@app.route("/")
def index():
    global calories
    return render_template("navbar.html", calories=calories)


@app.route("/search_entry", methods=["GET", "POST"])
def search_entry():
    global entries, calories, enter_calories_script

    if request.method == "POST":
        form_weight_grams = request.form["weight_grams"]
        form_ingredient_name = request.form["ingredient_name"].strip().lower()

        new_entry = search_calories(form_ingredient_name, form_weight_grams)

        if new_entry:
            for existing_entry in entries:
                if form_ingredient_name == existing_entry.split(" of ", 1)[1]:
                    return redirect(
                        url_for(
                            "search_conflict",
                            form_ingredient_name=form_ingredient_name,
                            form_weight_grams=form_weight_grams,
                            existing_entry=existing_entry,
                            new_entry=new_entry,
                        )
                    )

        else:
            return redirect(
                url_for("not_found", form_ingredient_name=form_ingredient_name)
            )

        entries, calories = enter_calories_script(
            entries, calories, form_ingredient_name, form_weight_grams
        )

        return redirect(url_for("list"))

    return render_template("search_entry.html")


@app.route("/search_conflict", methods=["GET", "POST"])
def search_conflict():
    conflicting_entry_name = request.args.get("form_ingredient_name")
    conflicting_entry_weight = request.args.get("form_weight grams")
    existing_entry = request.args.get("existing_entry")
    new_entry = request.args.get("new_entry")
    return render_template(
        "search_conflict.html",
        conflicting_entry=conflicting_entry_name,
        conflicting_entry_weight=conflicting_entry_weight,
        existing_entry=existing_entry,
        new_entry=new_entry
    )


# app.route("/merge_conflict", methods=["GET", "POST"])
# def merge_conflict():

# app.route("/keep_existing_conflict", methods=["GET", "POST"])
# def merge_conflict():

# app.route("/replace_existing_conflict", methods=["GET", "POST"])
# def merge_conflict():


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

        return redirect(url_for("list"))

    return render_template("manually_enter_calories.html")


@app.route("/delete_entry", methods=["GET", "POST"])
def delete_entry():
    global entries, calories
    if request.method == "GET":
        return render_template("delete_entry.html", entries=entries)

    else:
        form_entry_to_delete = request.form.get("entry_to_delete").strip().lower()
        for entry in entries:
            if form_entry_to_delete in entry:
                entries.remove(entry)
                calories -= int(re.search(r"^\d+", entry).group())
                return redirect(
                    url_for(
                        "delete_confirmation", form_entry_to_delete=form_entry_to_delete
                    )
                )

        return redirect(
            url_for("delete_not_found", form_entry_to_delete=form_entry_to_delete)
        )


@app.route("/delete_confirmation", methods=["GET"])
def delete_confirmation():
    global entries
    deleted_entry = request.args.get("form_entry_to_delete")
    return render_template(
        "delete_confirmation.html", deleted_entry=deleted_entry, entries=entries
    )


@app.route("/delete_not_found", methods=["GET"])
def delete_not_found():
    form_entry_to_delete = request.args.get("form_entry_to_delete")
    return render_template(
        "delete_not_found.html", form_entry_to_delete=form_entry_to_delete
    )


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
