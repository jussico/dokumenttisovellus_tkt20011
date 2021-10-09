
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