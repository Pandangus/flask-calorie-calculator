from flask import Blueprint, request, render_template, session
from modules.search_calories import search_calories
from modules.enter_calories_script import enter_calories_script
from modules.utility_functions.update_calorie_data import update_calorie_data
import re


add_entries_bp = Blueprint("add_entries", __name__)


@add_entries_bp.route("/search_entry", methods=["GET", "POST"])
def search_entry():
    if "entries" not in session:
        session["entries"] = []
    if "calories" not in session:
        session["calories"] = 0

    entries = session["entries"]
    calories = session["calories"]

    if request.method == "POST":
        form_weight_grams = request.form["weight_grams"]
        form_ingredient_name = request.form["ingredient_name"].strip().lower()

        new_entry = search_calories(form_ingredient_name, form_weight_grams)

        if new_entry:
            for existing_entry in entries:
                if form_ingredient_name == existing_entry.split(" of ", 1)[1]:
                    return render_template(
                        "entry_conflict.html",
                        conflicting_entry=form_ingredient_name,
                        conflicting_entry_weight=form_weight_grams,
                        existing_entry=existing_entry,
                        new_entry=new_entry,
                    )

        else:
            return render_template(
                "not_found.html", ingredient_name=form_ingredient_name
            )

        session["entries"], session["calories"] = enter_calories_script(
            entries, calories, form_ingredient_name, form_weight_grams
        )
        return render_template(
            "list.html", entries=session["entries"], calories=session["calories"]
        )

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

            return render_template(
                "list.html", entries=session["entries"], calories=session["calories"]
            )

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


@add_entries_bp.route("/merge_conflict", methods=["GET"])
def merge_conflict():
    new_entry = request.args.get("new_entry")
    existing_entry = request.args.get("existing_entry")
    merged_entry = f"{round(float(re.search(r'^[0-9]+', new_entry).group())) + round(float(re.search(r'^[0-9]+', existing_entry).group()))} kcal from {round(float(re.search(r'[0-9]+g', existing_entry).group()[:-1])) + round(float(re.search(r'[0-9]+g', new_entry).group()[:-1]))}g of {new_entry.split(' of ')[1]}"
    return render_template(
        "merge_conflict.html",
        new_entry=new_entry,
        existing_entry=existing_entry,
        merged_entry=merged_entry,
    )


@add_entries_bp.route("/confirm_merge", methods=["GET"])
def confirm_merge():
    entries = session["entries"]
    calories = session["calories"]
    merged_entry = request.args.get("merged_entry")
    existing_entry = request.args.get("existing_entry")
    entries.remove(existing_entry)
    entries.insert(0, merged_entry)
    calories -= int(re.search(r"^\d+", existing_entry).group())
    calories += int(re.search(r"^\d+", merged_entry).group())
    session["entries"] = entries
    session["calories"] = calories
    return render_template("list.html", entries=entries, calories=calories)


@add_entries_bp.route("/replace_existing_conflict", methods=["GET"])
def replace_existing_conflict():
    new_entry = request.args.get("new_entry")
    existing_entry = request.args.get("existing_entry")
    return render_template(
        "replace_existing_conflict.html",
        new_entry=new_entry,
        existing_entry=existing_entry,
    )


@add_entries_bp.route("/confirm_replace", methods=["GET"])
def confirm_replace():
    entries = session["entries"]
    calories = session["calories"]
    new_entry = request.args.get("new_entry")
    existing_entry = request.args.get("existing_entry")
    entries.remove(existing_entry)
    entries.insert(0, new_entry)
    calories -= int(re.search(r"^\d+", existing_entry).group())
    calories += int(re.search(r"^\d+", new_entry).group())
    session["entries"] = entries
    session["calories"] = calories
    return render_template("list.html", entries=entries, calories=calories)
