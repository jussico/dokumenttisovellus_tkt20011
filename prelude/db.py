from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from models import User

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

def check_login_ok(username, password):
    sql = "SELECT username FROM doc_user WHERE username = :username and password = :password"
    result = db.session.execute(sql, {"username":username, "password":password})
    print(f"result: {result}")
    result_username = result.fetchone()
    if (result_username == None):
        return False
    else:
        return True

def get_user(username):
    sql = "SELECT * FROM doc_user WHERE username = :username"
    result = db.session.execute(sql, {"username":username})
    ruser = result.fetchone()
    # print(f"resultset_user: {ruser}")
    return User(ruser["username"], 
        ruser["first_name"], 
        ruser["last_name"], 
        ruser["password"], 
        ruser["is_admin"])

def get_users():
    sql = "SELECT * FROM doc_user"
    results = db.session.execute(sql)
    all_users = results.fetchall()
    return all_users

def get_docs():
    sql = "SELECT * FROM doc"
    results = db.session.execute(sql)
    all_documents = results.fetchall()
    return all_documents