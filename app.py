from flask import Flask, request, render_template, redirect, url_for, flash, session
from modules.utility_functions.get_entry_calories import get_entry_calories
from modules.utility_functions.get_entry_name import get_entry_name
from modules.utility_functions.get_entry_weight import get_entry_weight
from routes.delete_saved_list import delete_saved_list_bp
from routes.portion_calories import portion_calories_bp
from routes.delete_entries import delete_entries_bp
from routes.add_entries import add_entries_bp
from routes.menus import menu_bp
from datetime import timedelta
from models import Users, Lists, Ingredients, db, init_db
from werkzeug.security import generate_password_hash, check_password_hash
import re

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


@app.route("/reset_request", methods=["GET", "POST"])
def reset_request():
    return render_template("reset_request.html")


@app.route("/reset_confirmed", methods=["GET"])
def reset_confirmed():
    global entries, calories
    entries = []
    calories = 0
    return render_template("reset_confirmed.html")


@app.route("/list")
def list():
    entries = session["entries"]
    calories = session["calories"]
    return render_template("list.html", entries=entries, calories=calories)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.permanent = True
        username = request.form["username"].strip().lower()
        password = request.form["password"]
        matched_user = Users.query.filter_by(username=username).first()
        if matched_user:
            if check_password_hash(matched_user.password, password):
                session["username"] = username
                flash(f"logged in as: {username}", "info")
                return render_template("navbar.html")
            else:
                flash("invalid password")
                return render_template("login.html")
        else:
            flash(f"no existing account for {username} was found")
            return render_template("login.html")
    else:
        if "username" in session:
            return redirect(url_for("logout.html"))
        else:
            return render_template("login.html")


@app.route("/logout_request", methods=["GET", "POST"])
def logout_request():
    if "username" in session:
        username = session["username"]
        flash(f"currently logged in as: {username}", "info ")
        flash("are you sure you want to log out?", "info")
        return render_template("logout_request.html")
    else:
        flash("not logged in", "info")
        return render_template("login.html")


@app.route("/logout_confirm", methods=["GET", "POST"])
def logout_confirm():
    if "username" in session:
        session.pop("username", None)
        flash("you have been logged out", "info")
        return render_template("navbar.html")
    else:
        flash("not logged in", "info")
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if "username" in session:
        username = session["username"]
        return redirect(url_for("logout_request"))
    else:
        if request.method == "POST":
            username = request.form["username"].strip().lower()
            password = request.form["password"]
            re_enter_password = request.form["re-enter_password"]
            usernames = Users.query.with_entities(Users.username).all()
            usernames_list = [existing_username[0] for existing_username in usernames]
            if username in usernames_list:
                flash(f"an account already exists for: {username}")
                return render_template("register.html")
            if password == re_enter_password:
                hashed_password = generate_password_hash(password, method="sha256")
                new_user = Users(username=username, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                flash(f"{username} successfully registered")
                return redirect(url_for("login"))
            else:
                flash("password entries did not match")
                return render_template("register.html")
        else:
            return render_template("register.html")


@app.route("/delete_account", methods=["GET"])
def delete_account():
    if "username" in session:
        return render_template("delete_account.html")
    else:
        flash("not logged in", "info")
        return render_template("login.html")


@app.route("/delete_account_confirm", methods=["GET"])
def delete_account_confirm():
    if "username" in session:
        return render_template("delete_account_confirm.html")
    else:
        flash("not logged in", "info")
        return render_template("login.html")


@app.route("/delete_account_execute", methods=["GET"])
def delete_account_execute():
    if "username" in session:
        username = session["username"]
        user_to_delete = Users.query.filter_by(username=username).first()
        db.session.delete(user_to_delete)
        db.session.commit()
        session.pop("username", None)
        flash("account successfully deleted")
        return redirect(url_for("index"))
    else:
        flash("not logged in", "info")
        return render_template("login.html")


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


@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    if "username" in session:
        if request.method == "POST":
            username = session["username"]
            current_password = request.form["current_password"]
            new_password = request.form["new_password"]
            re_new_password = request.form["re_new_password"]
            user_match = Users.query.filter_by(username=username).first()
            if user_match:
                if check_password_hash(user_match.password, current_password):
                    if new_password == re_new_password:
                        hashed_password = generate_password_hash(
                            new_password, method="sha256"
                        )
                        user_match.password = hashed_password
                        try:
                            db.session.commit()
                            return render_template("password_change_successful.html")
                        except Exception as e:
                            flash("error changing password - please try again later")

                    else:
                        flash("new passwords do not match")
                else:
                    flash("current password entered was invalid")
        return render_template("change_password.html")
    else:
        flash("not logged in")
        return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
