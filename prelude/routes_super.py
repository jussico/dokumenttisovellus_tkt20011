from app import app

from db import update_user, create_user

from flask import redirect, render_template, request, session, flash

from jutils import pretty, is_logged_in, is_admin, is_superuser, get_highest_access_level

@app.route("/create_new_user/", methods=['GET', 'POST'])
def create_new_user():
    print(f"creating new user.")
    if not is_superuser():
        return render_template("forbidden.html", forbidden_message=get_highest_access_level())
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
    if not is_superuser():
        return render_template("forbidden.html", forbidden_message=get_highest_access_level())
    try:
        create_user(request.form)
    except:
        print("FAIL!")
        return render_template("/create_new_user.html", prefilled=request.form)
    return redirect("settings")


