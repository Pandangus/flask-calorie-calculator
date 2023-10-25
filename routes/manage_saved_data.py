from flask import Blueprint, request, render_template, flash, session
from modules.utility_functions import get_entry_calories
from modules.utility_functions import get_entry_weight
from modules.utility_functions import get_entry_name
from models import Users, Ingredients, Lists, db


manage_saved_data_bp = Blueprint("manage_saved_data", __name__)


@manage_saved_data_bp.route("/save_entries_list", methods=["GET", "POST"])
def save_entries_list():
    if "username" in session:
        entries = session["entries"]
        calories = session["calories"]

        if request.method == "POST":
            username = session["username"]
            user = Users.query.filter_by(username=username).first()
            user_id = user.id
            user_lists = Lists.query.filter_by(user_id=user_id).all()
            user_lists_names = [list.list_name for list in user_lists]
            new_list_name = request.form["saved_list_name"].strip().lower()

            if new_list_name in user_lists_names:
                flash(f"- a list named {new_list_name} already exists -", "info")
                return render_template(
                    "save_entries_list.html", entries=entries, calories=calories
                )
            else:
                new_list = Lists(list_name=new_list_name, user_id=user_id)

                try:
                    db.session.add(new_list)
                    db.session.commit()
                except Exception as e:
                    flash("- error saving list name to database -")

                list = Lists.query.filter_by(list_name=new_list_name).first()
                list_id = list.id

                try:
                    for entry in entries:
                        calorie_int = get_entry_calories(entry)
                        weight_int = get_entry_weight(entry)
                        ingredient_str = get_entry_name(entry)
                        new_list_entry = Ingredients(
                            ingredient_name=ingredient_str,
                            ingredient_weight=weight_int,
                            ingredient_calories=calorie_int,
                            list_id=list_id,
                        )
                        db.session.add(new_list_entry)
                        db.session.commit()
                except Exception as e:
                    flash("- error saving list entries to database -")

                return render_template(
                    "save_entries_list_confirm.html", list_name=new_list_name
                )

        return render_template(
            "save_entries_list.html", entries=entries, calories=calories
        )
    else:
        flash("not logged in", "info")
        return render_template("login.html")


@manage_saved_data_bp.route("/load_entries_list", methods=["GET", "POST"])
def load_entries_list():
    username = session["username"]

    user = Users.query.filter_by(username=username).first()
    user_id = user.id

    user_lists = Lists.query.filter_by(user_id=user_id).all()
    user_lists_names = [list.list_name for list in user_lists]

    if request.method == "POST":
        list_name = request.form["list_to_load"]

        if list_name not in user_lists_names:
            flash(f"no matches for: {list_name}")
            return render_template("load_entries_list.html", lists=user_lists_names)
        else:
            try:
                loaded_entries = []
                loaded_calories = 0
                list = Lists.query.filter_by(
                    list_name=list_name, user_id=user_id
                ).first()
                list_id = list.id
                ingredients = Ingredients.query.filter_by(list_id=list_id)
                for ingredient in ingredients:
                    name = ingredient.ingredient_name
                    weight = ingredient.ingredient_weight
                    ingredient_calories = ingredient.ingredient_calories
                    loaded_entries.append(
                        f"{ingredient_calories} kcal from {weight}g of {name}"
                    )
                    loaded_calories += ingredient_calories
                    session["loaded_calories"] = loaded_calories
                    session["loaded_entries"] = loaded_entries
                return render_template(
                    "load_entries_list_confirm.html",
                    list_name=list_name,
                    list=loaded_entries,
                    loaded_calories=loaded_calories,
                )

            except Exception as e:
                flash("error loading list - please try again later")

    return render_template("load_entries_list.html", lists=user_lists_names)


@manage_saved_data_bp.route("/load_entries_list_complete", methods=["GET"])
def load_entries_list_complete():
    global entries, calories
    list_name = request.args.get("list_name")
    list = session["loaded_entries"]
    loaded_calories = session["loaded_calories"]
    print(list_name, list, loaded_calories)
    calories = loaded_calories
    entries = list
    return render_template("load_entries_list_complete.html", list_name=list_name)
