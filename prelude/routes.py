from app import app
from flask import redirect, render_template, request, session, flash
from os import getenv
# from models import User
from db import check_login_ok, get_user, get_users, get_docs, get_user_with_id
from db import update_user, create_user
from db import get_doc_with_id, update_doc, create_doc, get_keywords_with_doc_id, get_notes_with_doc_id
from jutils import pretty, is_logged_in, is_admin, is_superuser
from db import get_note_with_id, update_note
from db import update_doc_keywords, get_temporal_notes_with_id

@app.route("/")
def index():
    print(f"session-now: {pretty(session)}")
    if not is_logged_in(): # TODO: add everywhere and rights-check too.
        return render_template("login.html", message="login now.")
    docs = get_docs()
    return render_template("index.html", docs=docs)

@app.route("/logout")
def logout():
    to_remove=[]
    for keyx in session.keys():
        to_remove.append(keyx)
    for keyx in to_remove:
        del session[keyx]
    return render_template("logged_out.html")

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
        return redirect("/")
    else:
        flash("Login failed!")
        return render_template("login.html")

@app.route("/settings", methods=['GET', 'POST'])
def settings():
    all_users = get_users()
    return render_template("settings.html", all_users=all_users)

@app.route("/edit_user/<int:id>", methods=['GET', 'POST'])
def edit_user(id):
    # todo: tee isadmin yms. -metodit tohon tyyliin.
    # https://hy-tsoha.github.io/materiaali/osa-4/#ulkoasun-toteutus
    user_to_edit = get_user_with_id(id)
    print(f"editing user with id: {id}")
    return render_template("edit_user.html", user=user_to_edit)

@app.route("/edit_doc_keywords/<int:id>", methods=['GET', 'POST'])
def edit_doc_keywords(id):
    doc = get_doc_with_id(id)
    print(f"edit doc keywords with doc id: {id}")
    return render_template("edit_doc_keywords.html", doc=doc)

@app.route("/edit_doc_note/<int:id>", methods=['GET', 'POST'])
def edit_doc_note(id):
    note_to_edit = get_note_with_id(id)
    print(f"viewing doc_note with doc_note.id: {id}")
    return render_template("edit_doc_notes.html", note=note_to_edit)

@app.route("/view_doc_note_history/<int:id>", methods=['GET', 'POST'])
def view_doc_note_history(id):
    temporal_notes = get_temporal_notes_with_id(id)
    print(f"viewing doc note history with id: {id}")
    return render_template("view_doc_note_history.html", temporal_notes=temporal_notes)

@app.route("/view_doc/<int:id>", methods=['GET', 'POST'])
def view_doc(id):
    doc_to_view = get_doc_with_id(id)
    doc_keywords = get_keywords_with_doc_id(id)
    doc_notes = get_notes_with_doc_id(id)
    print(f"viewing doc with id: {id}")
    return render_template("view_doc.html", doc=doc_to_view, keywords=doc_keywords, notes=doc_notes)

@app.route("/edit_doc/<int:id>", methods=['GET', 'POST'])
def edit_doc(id):
    doc_to_edit = get_doc_with_id(id)
    print(f"editing doc with id: {id}")
    return render_template("edit_doc.html", doc=doc_to_edit)

@app.route("/submit_edit_doc_keywords", methods=['GET', 'POST'])
def submit_edit_doc_keywords():
    print(f"@submit_edit_doc_keywords")
    update_doc_keywords(request.form)
    print("SELVIS!")
    return redirect(f"/view_doc/{request.form['id']}")

@app.route("/submit_edit_doc_notes", methods=['GET', 'POST'])
def submit_edit_doc_notes():
    print(f"@submit_edit_doc_notes")
    update_note(request.form)
    return redirect(f"/view_doc/{request.form['doc_id']}")

@app.route("/submit_edit_doc", methods=['GET', 'POST'])
def submit_edit_doc():
    print(f"@submit_edit_doc")
    update_doc(request.form)
    return redirect("/")

@app.route("/submit_edit_user", methods=['GET', 'POST'])
def submit_edit_user():
    print(f"@submit_edit_user")
    update_user(request.form)
    return redirect("settings")

@app.route("/create_new_user/", methods=['GET', 'POST'])
def create_new_user():
    print(f"creating new user.")
    prefilled_map = {}
    prefilled_map["username"] = ""
    prefilled_map["password"] = "1234"
    prefilled_map["first_name"] = ""
    prefilled_map["last_name"] = ""
    prefilled_map["enabled"] = "True"
    prefilled_map["is_admin"] = "False"

    return render_template("create_new_user.html", prefilled=prefilled_map)

@app.route("/submit_create_new_user", methods=['GET', 'POST'])
def submit_create_new_user():
    print(f"@submit_new_user")
    try:
        create_user(request.form)
    except:
        print("FAIL!")
        return render_template("/create_new_user.html", prefilled=request.form)
    return redirect("settings")
