from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from modules.search_calories import search_calories
from modules.enter_calories_script import enter_calories_script
from modules.utility_functions.update_calorie_data import update_calorie_data


add_entries_bp = Blueprint("add_entries", __name__)


@add_entries_bp.route("/search_entry", methods=["GET", "POST"])
def search_entry():
    entries = session["entries"]
    calories = session["calories"]

    if request.method == "POST":
        form_weight_grams = request.form["weight_grams"]
        form_ingredient_name = request.form["ingredient_name"].strip().lower()

        new_entry = search_calories(form_ingredient_name, form_weight_grams)

        if new_entry:
            for existing_entry in entries:
                if form_ingredient_name == existing_entry.split(" of ", 1)[1]:
                    return redirect(
                        url_for(
                            "entry_conflict",
                            form_ingredient_name=form_ingredient_name,
                            form_weight_grams=form_weight_grams,
                            existing_entry=existing_entry,
                            new_entry=new_entry,
                        )
                    )

        else:
            return render_template(
                "not_found.html", ingredient_name=form_ingredient_name
            )

        session["entries"], session["calories"] = enter_calories_script(
            entries, calories, form_ingredient_name, form_weight_grams
        )
        return redirect(url_for("list"))

    return render_template("search_entry.html")


@add_entries_bp.route("/manual_entry", methods=["GET", "POST"])
def manual_entry():
    entries = session["entries"]
    calories = session["calories"]

    if request.method == "POST":
        form_weight_grams = request.form["weight_grams"]
        form_calories_100g = request.form["calories_100g"]
        form_ingredient_name = request.form["ingredient_name"].strip().lower()

        if form_ingredient_name not in [entry.split(" of ")[1] for entry in entries]:
            session["entries"], session["calories"] = update_calorie_data(
                form_calories_100g,
                form_weight_grams,
                form_ingredient_name,
                entries,
                calories,
            )

            return redirect(url_for("list"))

        else:
            existing_entry = [
                entry
                for entry in entries
                if entry.split(" of ")[1] == form_ingredient_name
            ][0]
            new_entry = f"{round((int(form_weight_grams)/100) * int(form_calories_100g))} kcal from {form_weight_grams}g of {form_ingredient_name}"
            return render_template(
                "entry_conflict.html",
                existing_entry=existing_entry,
                new_entry=new_entry,
            )

    return render_template("manually_enter_calories.html")
