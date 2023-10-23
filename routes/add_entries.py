from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from modules.search_calories import search_calories
from modules.enter_calories_script import enter_calories_script

add_entries_bp = Blueprint('add_entries', __name__)

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
            return redirect(
                url_for("not_found", form_ingredient_name=form_ingredient_name)
            )

        session["entries"], session["calories"] = enter_calories_script(
            entries, calories, form_ingredient_name, form_weight_grams
        )
        print('entries: ', entries, 'calories: ', calories, '| hello')
        return redirect(url_for("list"))

    return render_template("search_entry.html")