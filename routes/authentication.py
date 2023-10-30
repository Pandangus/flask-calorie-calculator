from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from modules.utility_functions.validate_email import is_valid_email
from models import Users, db


authentication_bp = Blueprint("authentication", __name__)


@authentication_bp.route("/login", methods=["GET", "POST"])
def login():
    """

    Handle user login and session management.

    This route handles user login, displaying appropriate messages and managing user sessions.
    If the request method is POST, it attempts to log in the user based on the provided credentials.
    If the login is successful, it sets the user's session and provides a confirmation message.
    If the login fails, it displays a message indicating invalid credentials or the absence of an account.

    If the request method is GET and the user is already logged in, it redirects to the logout page.
    If the user is not logged in, it displays the login page.

    Returns:
        Flask response: Renders a template and displays flash messages accordingly.

    """

    try:
        if request.method == "POST":
            session.permanent = True
            username = request.form["username"].strip().lower()
            password = request.form["password"]
            matched_user = Users.query.filter_by(username=username).first()

            if matched_user:
                if check_password_hash(matched_user.password, password):
                    session["username"] = username
                    flash(f"Logged in as: {username}", "info")
                    return render_template("navbar.html")

                else:
                    flash("Invalid password")
                    return render_template("login.html")

            else:
                flash(f"No existing account for {username} was found")
                return render_template("login.html")

        else:
            if "username" in session:
                return render_template("logout.html")

            else:
                return render_template("login.html")

    except Exception as e:
        flash(f"An unexpected error occurred: {e}")
        return render_template("login.html")


@authentication_bp.route("/logout", methods=["GET", "POST"])
def logout():
    """

    Handle user logout and session management.

    This route handles user logouts, displaying appropriate messages and managing user sessions.
    If the request method is POST and the user is logged in, it logs the user out and provides a confirmation message.
    If the user is not logged in, it displays a message indicating that the user is not logged in.

    If the request method is GET and the user is logged in, it displays a message indicating the current user and
    prompts the user to confirm the logout. If the user is not logged in, it displays a message indicating that
    the user is not logged in.

    Returns:
        Flask response: Renders a template and displays flash messages accordingly.

    """

    try:
        if request.method == "POST":
            if "username" in session:
                session.pop("username", None)
                flash("You have been logged out", "info")
                return render_template("navbar.html")

            else:
                flash("Not logged in", "info")
                return render_template("login.html")

        if "username" in session:
            username = session["username"]
            flash(f"Currently logged in as: {username}", "info")
            flash("Are you sure you want to log out?", "info")
            return render_template("logout.html")

        else:
            flash("Not logged in", "info")
            return render_template("login.html")

    except Exception as e:
        flash(f"An unexpected error occurred: {e}")
        return render_template("login.html")


@authentication_bp.route("/register", methods=["GET", "POST"])
def register():
    """

    Register a new user.

    This route allows users to register by submitting a registration form. It checks for the presence
    of the user's session and handles registration, email validation, and password confirmation.
    Users are redirected to the login page upon successful registration.

    Returns:
        Flask response: Renders a template based on the registration outcome.

    """

    if "username" in session:
        username = session["username"]
        return redirect(url_for("logout"))
    else:
        try:
            if request.method == "POST":
                username = request.form["username"].strip().lower()
                email = request.form["email"].strip().lower()
                password = request.form["password"]
                re_enter_password = request.form["re-enter_password"]

                usernames = Users.query.with_entities(Users.username).all()
                usernames_list = [
                    existing_username[0] for existing_username in usernames
                ]

                if username in usernames_list:
                    flash(f"An account already exists for: {username}")
                    return render_template("register.html")

                if not is_valid_email(email):
                    return render_template("register.html")

                if password == re_enter_password:
                    hashed_password = generate_password_hash(password, method="scrypt")
                    new_user = Users(
                        username=username, email=email, password=hashed_password
                    )
                    db.session.add(new_user)
                    db.session.commit()
                    flash(f"{username} successfully registered")
                    return render_template("login.html")

                else:
                    flash("Password entries did not match")
                    return render_template("register.html")

            else:
                return render_template("register.html")

        except Exception as e:
            flash(f"An unexpected error occurred: {e}")
            return render_template("register.html")
