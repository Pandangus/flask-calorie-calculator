from flask import Flask
from routes.manage_saved_data import manage_saved_data_bp
from routes.delete_saved_list import delete_saved_list_bp
from routes.session_functions import session_functions_bp
from routes.portion_calories import portion_calories_bp
from routes.authentication import authentication_bp
from routes.delete_entries import delete_entries_bp
from routes.manage_account import manage_account_bp
from routes.add_entries import add_entries_bp
from routes.menus import menu_bp
from datetime import timedelta
from models import init_db


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
app.register_blueprint(manage_saved_data_bp)


if __name__ == "__main__":
    app.run(debug=True)
