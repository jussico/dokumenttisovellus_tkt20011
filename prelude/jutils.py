
from flask import redirect, render_template, request, session, flash

def pretty(mappi):
    return_value=""
    for avain in mappi.keys():
        return_value = return_value + f"[{avain}] = {mappi[avain]}\n"
    return return_value

def is_logged_in():
    return not (session.get("id") == None)

def is_admin():
    return session.get("is_admin")

def is_superuser():
    return session.get("is_superuser")

def get_highest_access_level():
    if is_superuser():
        return "superuser"
    if is_admin():
        return "administrator"
    if is_logged_in():
        return "common people"
    return "stranger with no rights"

def can_edit_user(user_to_edit):
    if is_superuser():
        return True
    if is_admin() and (user_to_edit['is_admin'] == False) and (user_to_edit['is_superuser'] == False):
        return True
    return False

