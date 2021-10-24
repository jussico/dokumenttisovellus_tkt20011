from flask import flash

def validate_edit_user(form):

    max_text = 80
    min_password = 4

    if len(form["username"]) == 0:
        flash("username can't be empty.")
        return False

    if len(form["username"]) > max_text:
        flash(f"username can't be longer than {max_text}.")
        return False

    if len(form["first_name"]) == 0:
        flash("first name can't be empty.")
        return False

    if len(form["first_name"]) > max_text:
        flash(f"first name can't be longer than {max_text}.")
        return False

    if len(form["last_name"]) == 0:
        flash("last name can't be empty.")
        return False

    if len(form["last_name"]) > max_text:
        flash(f"last name can't be longer than {max_text}.")
        return False

    if len(form["password"]) == 0:
        flash("password can't be empty.")
        return False

    if len(form["password"]) < min_password:
        flash(f"password can't be shorter than {min_password}.")
        return False

    if len(form["password"]) > max_text:
        flash(f"password can't be longer than {max_text}.")
        return False

    if form["enabled"] not in ["True", "False"]:
        flash("enable must be True or False")
        return False

    return True

def validate_new_user(form):

    if form["is_admin"] not in ["True", "False"]:
        flash("is_admin must be True or False")
        return False

    return validate_edit_user(form)

def validate_edit_doc(form):

    max_text = 80

    if len(form["title"]) == 0:
        flash("title can't be empty.")
        return False

    if len(form["title"]) > max_text:
        flash(f"title can't be longer than {max_text}.")
        return False

    if len(form["file_name"]) == 0:
        flash("file name name can't be empty.")
        return False

    if len(form["file_name"]) > 512:
        flash(f"file name can't be longer than 512.")
        return False

    if len(form["description"]) == 0:
        flash("description can't be empty.")
        return False

    if len(form["description"]) > max_text:
        flash(f"description can't be longer than {max_text}.")
        return False

    return True

def validate_edit_note(form):

    max_text = 80

    if len(form["title"]) == 0:
        flash("title can't be empty.")
        return False

    if len(form["title"]) > max_text:
        flash(f"title can't be longer than {max_text}.")
        return False

    if len(form["content"]) == 0:
        flash("content can't be empty.")
        return False

    if len(form["content"]) > 512:
        flash(f"content can't be longer than 512.")
        return False

    return True

