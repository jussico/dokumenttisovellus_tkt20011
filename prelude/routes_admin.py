
from app import app
from flask import redirect, render_template, request, session, flash
from os import getenv
from db import check_login_ok, get_user, get_users, get_docs, get_user_with_id, get_normal_users
from db import update_user, create_user
from db import get_doc_with_id, update_doc, create_doc, get_keywords_with_doc_id, get_notes_with_doc_id
from jutils import pretty, is_logged_in, is_admin, is_superuser, get_highest_access_level
from db import get_note_with_id, update_note
from db import update_doc_keywords, get_temporal_notes_with_id
from routes_super import *

@app.route("/settings", methods=['GET', 'POST'], endpoint='settings')
def settings():
    print(f"@settings/")
    if not is_admin():
        return render_template("forbidden.html", forbidden_message=get_highest_access_level())
    if is_superuser():
        all_users = get_users()
    else:
        all_users = get_normal_users()

    return render_template("settings.html", all_users=all_users)

@app.route("/edit_user/<int:id>", methods=['GET', 'POST'])
def edit_user(id):
    if not is_admin():
        return render_template("forbidden.html", forbidden_message=get_highest_access_level())
    user_to_edit = get_user_with_id(id)
    # TODO: lisää access rights check käyttäjäkohtaisesti..
    # uusi methodi can_edit_user(id) jonnekin.
    print(f"editing user with id: {id}")
    return render_template("edit_user.html", user=user_to_edit)

@app.route("/edit_doc_keywords/<int:id>", methods=['GET', 'POST'])
def edit_doc_keywords(id):
    if not is_admin():
        return render_template("forbidden.html", forbidden_message=get_highest_access_level())
    doc = get_doc_with_id(id)
    print(f"edit doc keywords with doc id: {id}")
    return render_template("edit_doc_keywords.html", doc=doc)

@app.route("/edit_doc/<int:id>", methods=['GET', 'POST'])
def edit_doc(id):
    if not is_admin():
        return render_template("forbidden.html", forbidden_message=get_highest_access_level())
    doc_to_edit = get_doc_with_id(id)
    print(f"editing doc with id: {id}")
    return render_template("edit_doc.html", doc=doc_to_edit)

@app.route("/submit_edit_doc_keywords", methods=['GET', 'POST'])
def submit_edit_doc_keywords():
    if not is_admin():
        return render_template("forbidden.html", forbidden_message=get_highest_access_level())
    print(f"@submit_edit_doc_keywords")
    update_doc_keywords(request.form)
    print("SELVIS!")
    return redirect(f"/view_doc/{request.form['id']}")

@app.route("/submit_edit_doc", methods=['GET', 'POST'])
def submit_edit_doc():
    if not is_admin():
        return render_template("forbidden.html", forbidden_message=get_highest_access_level())
    print(f"@submit_edit_doc")
    update_doc(request.form)
    return redirect("/")

@app.route("/submit_edit_user", methods=['GET', 'POST'])
def submit_edit_user():
    if not is_admin():
        return render_template("forbidden.html", forbidden_message=get_highest_access_level())
    print(f"@submit_edit_user")
    # TODO: tähänkin tarkistus voiko tämä käyttäjä muokata tätä käyttäjää
    update_user(request.form)
    return redirect("settings")
