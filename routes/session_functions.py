from flask import Blueprint, request, render_template, session


session_functions_bp = Blueprint("session_functions", __name__)


@session_functions_bp.route("/reset_session", methods=["GET", "POST"])
def reset_request():
    if "entries" not in session:
        session["entries"] = []
    if "calories" not in session:
        session["calories"] = 0

    if request.method == "POST":
        session["entries"] = []
        session["calories"] = 0
        return render_template("reset_confirmed.html")

    return render_template("reset_request.html")


@session_functions_bp.route("/list")
def list():
    if "entries" not in session:
        session["entries"] = []
    if "calories" not in session:
        session["calories"] = 0

    entries = session["entries"]
    calories = session["calories"]
    
    return render_template("list.html", entries=entries, calories=calories)