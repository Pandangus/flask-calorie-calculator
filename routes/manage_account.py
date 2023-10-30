from flask import Blueprint, request, render_template, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import Users, db


manage_account_bp = Blueprint("manage_account", __name__)


@manage_account_bp.route("/delete_account", methods=["GET", "POST"])
def delete_account():
    if "username" in session:
        if request.method == "POST":
            return render_template("delete_account_confirm.html")
        return render_template("delete_account.html")
    else:
        flash("not logged in", "info")
        return render_template("login.html")


@manage_account_bp.route("/delete_account_execute", methods=["GET"])
def delete_account_execute():
    if "username" in session:
        username = session["username"]
        user_to_delete = Users.query.filter_by(username=username).first()
        db.session.delete(user_to_delete)
        db.session.commit()
        session.pop("username", None)
        flash("account successfully deleted")
        return render_template("navbar.html")
    else:
        flash("not logged in", "info")
        return render_template("login.html")


@manage_account_bp.route("/change_password", methods=["GET", "POST"])
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
                            new_password, method="scrypt"
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
        return render_template("login.html")
