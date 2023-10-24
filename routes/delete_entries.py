from flask import Blueprint, request, render_template, session
import re


delete_entries_bp = Blueprint("delete_entries", __name__)


@delete_entries_bp.route("/delete_entry", methods=["GET", "POST"])
def delete_entry():
    if "entries" not in session:
        session["entries"] = []
    if "calories" not in session:
        session["calories"] = 0

    entries = session["entries"]
    calories = session["calories"]
    
    if request.method == "GET":
        return render_template("delete_entry.html", entries=entries)

    else:
        form_entry_to_delete = request.form.get("entry_to_delete").strip().lower()
        for entry in entries:
            if form_entry_to_delete in entry:
                entries.remove(entry)
                calories -= int(re.search(r"^\d+", entry).group())
                session["entries"] = entries
                session["calories"] = calories
                return render_template(
                    "delete_confirmation.html", deleted_entry=form_entry_to_delete, entries=entries
                )

        return render_template(
        "delete_not_found.html", form_entry_to_delete=form_entry_to_delete
    )
