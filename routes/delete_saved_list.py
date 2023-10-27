from flask import Blueprint, request, render_template, flash, session
from models import Users, Lists, Ingredients, db


delete_saved_list_bp = Blueprint("delete_saved_list", __name__)


@delete_saved_list_bp.route("/delete_saved_list", methods=["GET", "POST"])
def delete_saved_list():
    username = session["username"]
    user = Users.query.filter_by(username=username).first()
    user_id = user.id

    user_lists = Lists.query.filter_by(user_id=user_id).all()
    user_lists_names = [list.list_name for list in user_lists]

    if request.method == "POST":
        list_name = request.form["list_to_delete"]

        if list_name not in user_lists_names:
            flash(f"no matches for: {list_name}")
            return render_template("delete_saved_list.html", lists=user_lists_names)

        else:
            return render_template(
                "delete_saved_list_confirm.html", list_name=list_name
            )

    return render_template("delete_saved_list.html", lists=user_lists_names)


@delete_saved_list_bp.route("/delete_saved_list_complete", methods=["GET"])
def delete_saved_entries_list_complete():
    try:
        username = session["username"]
        user = Users.query.filter_by(username=username).first()
        user_id = user.id

        list_name = request.args.get("list_name")
        list = Lists.query.filter_by(list_name=list_name, user_id=user_id).first()
        list_id = list.id

        ingredients = Ingredients.query.filter_by(list_id=list_id)

        for ingredient in ingredients:
            db.session.delete(ingredient)

        db.session.delete(list)
        db.session.commit()

        return render_template("delete_saved_list_complete.html", list_name=list_name)

    except Exception as e:
        flash("error deleting list - please try again later")
