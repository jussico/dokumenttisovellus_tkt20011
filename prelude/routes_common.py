from app import app
from flask import redirect, render_template, request, session, flash
from os import getenv
from db import check_login_ok, get_user, get_users, get_docs, get_user_with_id
from db import update_user, create_user
from db import get_doc_with_id, update_doc, create_doc, get_keywords_with_doc_id, get_notes_with_doc_id
from jutils import pretty, is_logged_in, is_admin, is_superuser
from db import get_note_with_id, update_note
from db import update_doc_keywords, get_temporal_notes_with_id
from routes_admin import *

@app.route("/login", methods=['GET', 'POST'])
def login():
    username = request.form["username"]
    password = request.form["password"]    
    login_ok = check_login_ok(username, password)
    print(f"login_ok: {login_ok}")
    if login_ok:
        user = get_user(username)
        print(f"user logged in: {pretty(user)}")
        print(f"session: {pretty(session)}")
        for avain in user.keys():
            session[avain] = user[avain]
        print(f"session-now: {pretty(session)}")
        flash(f"user {username} successfully logged in.", "info")
        return redirect("/")
    else:
        flash("Login failed!")
        return render_template("login.html")

@app.route("/logout")
def logout():
    username = request.form["username"]
    to_remove=[]
    for keyx in session.keys():
        to_remove.append(keyx)
    for keyx in to_remove:
        del session[keyx]
    flash(f"user {username} successfully logged out.", "info")
    return render_template("logged_out.html")

@app.route("/")
def index():
    print(f"session-now: {pretty(session)}")
    if not is_logged_in():
        return render_template("login.html", message="login now.")
    docs = get_docs()
    return render_template("index.html", docs=docs)

@app.route("/edit_doc_note/<int:id>", methods=['GET', 'POST'])
def edit_doc_note(id):
    if not is_logged_in():
        return render_template("forbidden.html", forbidden_message=get_highest_access_level())    
    note_to_edit = get_note_with_id(id)
    print(f"viewing doc_note with doc_note.id: {id}")
    return render_template("edit_doc_notes.html", note=note_to_edit)

@app.route("/view_doc_note_history/<int:id>", methods=['GET', 'POST'])
def view_doc_note_history(id):
    if not is_logged_in():
        return render_template("forbidden.html", forbidden_message=get_highest_access_level())
    temporal_notes = get_temporal_notes_with_id(id)
    print(f"viewing doc note history with id: {id}")
    return render_template("view_doc_note_history.html", temporal_notes=temporal_notes)

@app.route("/view_doc/<int:id>", methods=['GET', 'POST'])
def view_doc(id):
    if not is_logged_in():
        return render_template("forbidden.html", forbidden_message=get_highest_access_level())
    doc_to_view = get_doc_with_id(id)
    doc_keywords = get_keywords_with_doc_id(id)
    doc_notes = get_notes_with_doc_id(id)
    print(f"viewing doc with id: {id}")
    return render_template("view_doc.html", doc=doc_to_view, keywords=doc_keywords, notes=doc_notes)

@app.route("/submit_edit_doc_notes", methods=['GET', 'POST'])
def submit_edit_doc_notes():
    if not is_logged_in():
        return render_template("forbidden.html", forbidden_message=get_highest_access_level())
    print(f"@submit_edit_doc_notes")
    update_note(request.form)
    flash(f"document notes successfully edited.", "info")
    return redirect(f"/view_doc/{request.form['doc_id']}")
