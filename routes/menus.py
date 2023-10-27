from flask import Blueprint, render_template, flash, session


menu_bp = Blueprint("menu", __name__)


@menu_bp.route("/")
def index():
    if "entries" not in session:
        session["entries"] = []

    if "calories" not in session:
        session["calories"] = 0

    calories = session["calories"]
    if "username" in session:
        username = session["username"]
        flash(f"currently logged in as: {username}", "info")
    return render_template("navbar.html", calories=calories)


@menu_bp.route("/my_account")
def my_account():
    if "username" in session:
        username = session["username"]
        flash(f"currently logged in as: {username}", "info")
        return render_template("my_account.html")
    else:
        flash("not logged in", "info")
        return render_template("login.html")
