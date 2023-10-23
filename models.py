from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


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


def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()