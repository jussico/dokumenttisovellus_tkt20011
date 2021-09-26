from app import app
from flask import redirect, render_template, request, session, flash
from os import getenv
from models import User
from db import check_login_ok, get_user, get_users, get_docs

@app.route("/")
def index():

    # check if user is signed in, if not go to login-page.
    if session.get("user_username") == None:
        return render_template("login.html", message="login now.")

    docs = get_docs()

    return render_template("index.html", docs=docs)

@app.route("/logout")
def logout():
    del session["user_username"]
    del session["user_first_name"]
    del session["user_last_name"]
    del session["user_is_admin"]
    return render_template("logged_out.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    username = request.form["username"]
    password = request.form["password"]    

    login_ok = check_login_ok(username, password)

    print(f"login_ok: {login_ok}")

    if login_ok:
        user = get_user(username)
        print(f"user from database: {user}")
        session["user_username"] = user.username
        session["user_first_name"] = user.first_name
        session["user_last_name"] = user.last_name
        session["user_is_admin"] = user.is_admin
        return redirect("/")
    else:
        flash("Login failed! Do try again.")
        return render_template("login.html")

@app.route("/settings", methods=['GET', 'POST'])
def settings():
    all_users = get_users()
    return render_template("settings.html", all_users=all_users)

