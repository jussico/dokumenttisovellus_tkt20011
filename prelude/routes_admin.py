
from app import app
from flask import redirect, render_template, request, session, flash
from os import getenv
from db import check_login_ok, get_user, get_users, get_docs, get_user_with_id, get_normal_users
from db import update_user, create_user
from db import get_doc_with_id, update_doc, create_doc, get_keywords_with_doc_id, get_notes_with_doc_id
from jutils import pretty, is_logged_in, is_admin, is_superuser, get_highest_access_level, can_edit_user
from db import get_note_with_id, update_note, can_edit_user_with_id
from db import update_doc_keywords, get_temporal_notes_with_id, create_note
from routes_super import *
from validator import validate_edit_user, validate_edit_doc, validate_edit_note

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
    if not can_edit_user(user_to_edit):
        return render_template("forbidden.html", forbidden_message=get_highest_access_level())
    print(f"editing user with id: {id}")
    return render_template("edit_user.html", user=user_to_edit, prefilled=user_to_edit)

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
    flash("document keywords successfully edited.")
    return redirect(f"/view_doc/{request.form['id']}")

@app.route("/submit_edit_doc", methods=['GET', 'POST'])
def submit_edit_doc():
    if not is_admin():
        return render_template("forbidden.html", forbidden_message=get_highest_access_level())
    print(f"@submit_edit_doc")
    if not validate_edit_doc(request.form):
        return render_template("/edit_doc.html", doc=request.form)

    update_doc(request.form)

    flash("document successfully edited.")

    return redirect("/")

@app.route("/submit_edit_user", methods=['GET', 'POST'])
def submit_edit_user():
    if not is_admin():
        return render_template("forbidden.html", forbidden_message=get_highest_access_level())
    print(f"@submit_edit_user")
    if not can_edit_user_with_id(request.form["id"]):
        return render_template("forbidden.html", forbidden_message=get_highest_access_level())
    user_to_edit = get_user_with_id(request.form["id"])
    if not validate_edit_user(request.form):
        return render_template("/edit_user.html", prefilled=request.form, user=user_to_edit)
    try:
        update_user(request.form)
    except:
        print("FAIL!")
        flash("updating new user failed.", "warning")
        return render_template("/edit_user.html", prefilled=request.form, user=user_to_edit)

    flash("user successfully edited.")

    return redirect("settings")

@app.route("/create_new_doc", methods=['GET', 'POST'])
def create_new_doc():
    print(f"creating new doc.")
    if not is_admin():
        return render_template("forbidden.html", forbidden_message=get_highest_access_level())
    prefilled_map = {}
    prefilled_map["title"] = "your title"
    prefilled_map["file_name"] = "file.pdf"
    prefilled_map["description"] = "descriptive"
    return render_template("create_new_doc.html", prefilled=prefilled_map)

@app.route("/submit_create_new_doc", methods=['GET', 'POST'])
def submit_create_new_doc():
    print(f"@submit_create_new_doc")
    if not is_admin():
        return render_template("forbidden.html", forbidden_message=get_highest_access_level())
    if not validate_edit_doc(request.form):
        return render_template("/create_new_doc.html", prefilled=request.form)
    try:
        create_doc(request.form)
    except:
        print("FAIL!")
        flash("creating new document failed.", "warning")
        return render_template("/create_new_doc.html", prefilled=request.form)
    flash("new document successfully created.", "info")
    return redirect("/")

@app.route("/create_new_note/<int:id>", methods=['GET', 'POST'])
def create_new_note(id):
    print(f"creating new note.")
    if not is_admin():
        return render_template("forbidden.html", forbidden_message=get_highest_access_level())
    prefilled_map = {}
    prefilled_map["title"] = "your title"
    prefilled_map["content"] = "your note"
    prefilled_map["doc_id"] = id
    return render_template("create_new_note.html", prefilled=prefilled_map)

@app.route("/submit_create_new_note/<int:id>", methods=['GET', 'POST'])
def submit_create_new_note(id):
    print(f"@submit_create_new_note")
    if not is_admin():
        return render_template("forbidden.html", forbidden_message=get_highest_access_level())
    if not validate_edit_note(request.form):
        return render_template(f"/create_new_note.html", prefilled=request.form)
    try:
        create_note(request.form)
    except Exception as e: 
        print(e)
        print("FAIL!")
        flash("creating new note failed.", "warning")
        return render_template("/create_new_note.html", prefilled=request.form)
    flash("new note successfully created.", "info")
    return redirect("/")
