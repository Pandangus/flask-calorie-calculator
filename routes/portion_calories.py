from flask import Blueprint, request, render_template, session


portion_calories_bp = Blueprint("portion_calories", __name__)


@portion_calories_bp.route("/portion_calories", methods=["GET", "POST"])
def portion_calories():
    if request.method == "POST":
        calories = session["calories"]
        form_portions = request.form.get("number_of_portions", type=int)
        calories_per_portion = round(calories / form_portions)
        return render_template(
            "portion_result.html",
            calories=calories,
            form_portions=form_portions,
            calories_per_portion=calories_per_portion,
        )

    return render_template("portion_number.html")
