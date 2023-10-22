from flask import Flask, request, render_template, redirect, url_for, flash, session
from modules.enter_calories_script import enter_calories_script
from modules.utility_functions.update_calorie_data import update_calorie_data
from modules.utility_functions.get_entry_calories import get_entry_calories
from modules.utility_functions.get_entry_name import get_entry_name
from modules.utility_functions.get_entry_weight import get_entry_weight
from modules.search_calories import search_calories
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "9-\TTNg4Ct9O"
app.permanent_session_lifetime = timedelta(minutes=5)
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    lists = db.relationship("Lists", backref="user", lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Lists(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    list_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    ingredients = db.relationship("Ingredients", backref="list", lazy=True)

    def __init__(self, list_name, user_id):
        self.list_name = list_name
        self.user_id = user_id


class Ingredients(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    ingredient_name = db.Column(db.String(100), nullable=False)
    ingredient_weight = db.Column(db.Integer, nullable=False)
    ingredient_calories = db.Column(db.Integer, nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey("lists.id"), nullable=False)

    def __init__(
        self, ingredient_name, ingredient_weight, ingredient_calories, list_id
    ):
        self.ingredient_name = ingredient_name
        self.ingredient_weight = ingredient_weight
        self.ingredient_calories = ingredient_calories
        self.list_id = list_id


with app.app_context():
    db.create_all()


entries = []
calories = 0


@app.route("/")
def index():
    global calories
    if "username" in session:
        username = session["username"]
        flash(f"currently logged in as: {username}", "info")
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

        entries, calories = enter_calories_script(
            entries, calories, form_ingredient_name, form_weight_grams
        )

        return redirect(url_for("list"))

    return render_template("search_entry.html")


@app.route("/not_found", methods=["GET"])
def not_found():
    ingredient_name = request.args.get("form_ingredient_name")
    return render_template("not_found.html", ingredient_name=ingredient_name)


@app.route("/entry_conflict", methods=["GET", "POST"])
def entry_conflict():
    conflicting_entry_name = request.args.get("form_ingredient_name")
    conflicting_entry_weight = request.args.get("form_weight grams")
    existing_entry = request.args.get("existing_entry")
    new_entry = request.args.get("new_entry")
    return render_template(
        "entry_conflict.html",
        conflicting_entry=conflicting_entry_name,
        conflicting_entry_weight=conflicting_entry_weight,
        existing_entry=existing_entry,
        new_entry=new_entry,
    )


@app.route("/merge_conflict", methods=["GET", "POST"])
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


@app.route("/confirm_merge", methods=["GET", "POST"])
def confirm_merge():
    global entries, calories
    merged_entry = request.args.get("merged_entry")
    existing_entry = request.args.get("existing_entry")
    entries.remove(existing_entry)
    entries.insert(0, merged_entry)
    calories -= int(re.search(r"^\d+", existing_entry).group())
    calories += int(re.search(r"^\d+", merged_entry).group())
    return redirect(url_for("list"))


@app.route("/replace_existing_conflict", methods=["GET", "POST"])
def replace_existing_conflict():
    new_entry = request.args.get("new_entry")
    existing_entry = request.args.get("existing_entry")
    return render_template(
        "replace_existing_conflict.html",
        new_entry=new_entry,
        existing_entry=existing_entry,
    )


@app.route("/confirm_replace", methods=["GET", "POST"])
def confirm_replace():
    global entries, calories
    new_entry = request.args.get("new_entry")
    existing_entry = request.args.get("existing_entry")
    entries.remove(existing_entry)
    entries.insert(0, new_entry)
    calories -= int(re.search(r"^\d+", existing_entry).group())
    calories += int(re.search(r"^\d+", new_entry).group())
    return redirect(url_for("list"))


@app.route("/manual_entry", methods=["GET", "POST"])
def manual_entry():
    global entries, calories

    if request.method == "POST":
        form_weight_grams = request.form["weight_grams"]
        form_calories_100g = request.form["calories_100g"]
        form_ingredient_name = request.form["ingredient_name"].strip().lower()

        if form_ingredient_name not in [entry.split(" of ")[1] for entry in entries]:
            entries, calories = update_calorie_data(
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


@app.route("/reset_confirmed", methods=["GET"])
def reset_confirmed():
    global entries, calories
    entries = []
    calories = 0
    return render_template("reset_confirmed.html")


@app.route("/list")
def list():
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


@app.route("/my_account", methods=["GET", "POST"])
def my_account():
    if "username" in session:
        username = session["username"]
        flash(f"currently logged in as: {username}", "info")
        return render_template("my_account.html")
    else:
        flash("not logged in", "info")
        return render_template("login.html")


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


@app.route("/delete_saved_entries_list", methods=["GET", "POST"])
def delete_saved_entries_list():
    username = session["username"]

    user = Users.query.filter_by(username=username).first()
    user_id = user.id

    user_lists = Lists.query.filter_by(user_id=user_id).all()
    user_lists_names = [list.list_name for list in user_lists]

    if request.method == "POST":
        list_name = request.form["list_to_delete"]

        if list_name not in user_lists_names:
            flash(f"no matches for: {list_name}")
            return render_template(
                "delete_saved_entries_list.html", lists=user_lists_names
            )

        else:
            try:
                list = Lists.query.filter_by(
                    list_name=list_name, user_id=user_id
                ).first()
                list_id = list.id
                ingredients = Ingredients.query.filter_by(list_id=list_id)

                for ingredient in ingredients:
                    db.session.delete(ingredient)

                db.session.delete(list)
                db.session.commit()
                return render_template(
                    "delete_saved_entries_list_confirm.html", list_name=list_name
                )

            except Exception as e:
                flash("error deleting list - please try again later")

    return render_template("delete_saved_entries_list.html", lists=user_lists_names)


@app.route("/delete_saved_entries_list_complete", methods=["GET"])
def delete_saved_entries_list_complete():
    list_name = request.args.get("list_name")
    return render_template(
        "delete_saved_entries_list_complete.html", list_name=list_name
    )


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
