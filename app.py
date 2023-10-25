from flask import Flask, request, render_template, redirect, url_for, flash, session
from modules.utility_functions.get_entry_calories import get_entry_calories
from modules.utility_functions.get_entry_name import get_entry_name
from modules.utility_functions.get_entry_weight import get_entry_weight
from routes.delete_saved_list import delete_saved_list_bp
from routes.session_functions import session_functions_bp
from routes.portion_calories import portion_calories_bp
from routes.authentication import authentication_bp
from routes.delete_entries import delete_entries_bp
from routes.manage_account import manage_account_bp
from routes.add_entries import add_entries_bp
from routes.menus import menu_bp
from datetime import timedelta
from models import Users, Lists, Ingredients, db, init_db
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "9-\TTNg4Ct9O"
app.permanent_session_lifetime = timedelta(minutes=5)


init_db(app)


app.register_blueprint(menu_bp)
app.register_blueprint(delete_saved_list_bp)
app.register_blueprint(add_entries_bp)
app.register_blueprint(delete_entries_bp)
app.register_blueprint(portion_calories_bp)
app.register_blueprint(session_functions_bp)
app.register_blueprint(authentication_bp)
app.register_blueprint(manage_account_bp)


@app.route("/save_entries_list", methods=["GET", "POST"])
def save_entries_list():
    if "username" in session:
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


@app.route("/load_entries_list", methods=["GET", "POST"])
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
            return render_template(
                "load_entries_list.html", lists=user_lists_names
            )
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
                    loaded_entries.append(f"{ingredient_calories} kcal from {weight}g of {name}")
                    loaded_calories += ingredient_calories
                    session["loaded_calories"] = loaded_calories
                    session["loaded_entries"] = loaded_entries
                return render_template(
                    "load_entries_list_confirm.html", list_name=list_name, list=loaded_entries, loaded_calories=loaded_calories
                )

            except Exception as e:
                flash("error loading list - please try again later")

    return render_template("load_entries_list.html", lists=user_lists_names)


@app.route("/load_entries_list_complete", methods=["GET"])
def load_entries_list_complete():
    global entries, calories
    list_name = request.args.get("list_name")
    list = session["loaded_entries"]
    loaded_calories = session["loaded_calories"]
    print(list_name, list, loaded_calories)
    calories = loaded_calories
    entries = list
    return render_template("load_entries_list_complete.html", list_name=list_name)


if __name__ == "__main__":
    app.run(debug=True)
