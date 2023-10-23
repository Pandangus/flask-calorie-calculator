from flask import render_template, flash, session
from app import app

@app.route("/")
def index():
    global calories
    if "username" in session:
        username = session["username"]
        flash(f"currently logged in as: {username}", "info")
    return render_template("navbar.html", calories=calories)