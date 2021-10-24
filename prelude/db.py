from app import app
from flask_sqlalchemy import SQLAlchemy
from flask import session
from os import getenv
from jutils import pretty, can_edit_user


# fix heroku postgres / postgresql -problem
# https://help.heroku.com/ZKNTJQSK/why-is-sqlalchemy-1-4-x-not-connecting-to-heroku-postgres
import os
import re
uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
# fix end

app.config["SQLALCHEMY_DATABASE_URI"] = uri
# app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

def check_login_ok(username, password):
    sql = "SELECT username FROM user_account WHERE username = :username and password = :password and enabled = true"
    result = db.session.execute(sql, {"username":username, "password":password})
    result_username = result.fetchone()
    if (result_username == None):
        return False
    else:
        return True

def get_user(username):
    sql = "SELECT * FROM user_account WHERE username = :username"
    result = db.session.execute(sql, {"username":username})
    ruser = result.fetchone()
    return ruser

def get_user_with_id(id):
    sql = "SELECT * FROM user_account WHERE id = :id"
    result = db.session.execute(sql, {"id":id})
    ruser = result.fetchone()
    return ruser

def get_temporal_notes_with_id(id):
    sql = "SELECT * FROM doc_note_history WHERE doc_note_id = :id ORDER BY id desc"
    result = db.session.execute(sql, {"id":id})
    notes = result.fetchall()
    return notes

def get_notes_with_doc_id(id):
    sql = "SELECT * FROM doc_note WHERE doc_id = :id ORDER BY id"
    result = db.session.execute(sql, {"id":id})
    notes = result.fetchall()
    return notes

def get_keywords_string_with_doc_id(id):
    sql = "SELECT string_agg(word, ' ') FROM keyword LEFT OUTER JOIN \
        doc_keyword ON keyword.id = doc_keyword.keyword_id \
        WHERE doc_keyword.doc_id = :id"
    result = db.session.execute(sql, {"id":id})
    keywords_string = result.fetchone()
    return_value = keywords_string[0]
    if None == return_value:
        return_value = ""
    return return_value

# def get_keywords_string_with_doc_id(id):
#     sql = "SELECT word FROM keyword LEFT OUTER JOIN \
#         doc_keyword ON keyword.id = doc_keyword.keyword_id \
#         WHERE doc_keyword.doc_id = :id ORDER BY doc_keyword.id"
#     result = db.session.execute(sql, {"id":id})
#     words = result.fetchall()
#     keywords = ""
#     for keyword in words:
#         keywords = f"{keywords} {keyword}"
#     return keywords

def get_note_with_id(id):
    sql = "SELECT * FROM doc_note WHERE \
        id = :id"
    result = db.session.execute(sql, {"id":id})
    note = result.fetchone()
    return note

def update_doc_keywords(form):
    new_keywords_string=form["keywords"]
    old_keywords_string=get_keywords_string_with_doc_id(form["id"])
    new_keywords=set(new_keywords_string.split())
    old_keywords=old_keywords_string.split()
    # find out did we lose some and lose them.
    old_keywords_to_remove=\
        [x for x in old_keywords if x not in new_keywords]
    if len(old_keywords_to_remove) > 0:
        sql="DELETE FROM doc_keyword WHERE keyword_id IN \
            (SELECT id FROM keyword WHERE word = :remove_word)"
        for remove in old_keywords_to_remove:
            db.session.execute(sql, {"remove_word":remove})
            db.session.commit()
    # find out if we have new keywords
    new_keywords_to_add =\
        [x for x in new_keywords if x not in old_keywords]
    if len(new_keywords_to_add) > 0:
        for add in new_keywords_to_add:
            # find out if already in keyword-table, if not, add.
            sql="SELECT id FROM keyword where word = :add"
            result = db.session.execute(sql, {"add":add})
            keyword_id = result.fetchone()
            if None == keyword_id:
                sql="INSERT INTO keyword(word, created_by) \
                    VALUES(:word, :user_id) RETURNING id"
                result = db.session.execute(sql, {"word":add, "user_id":session["id"]})
                keyword_id = result.fetchone()[0]
            sql="INSERT INTO doc_keyword(keyword_id, doc_id, created_by) \
                    VALUES(:keyword_id, :doc_id, :user_id)"
            db.session.execute(sql, \
                {"keyword_id":keyword_id, "doc_id":form["id"], "user_id":session["id"]})
            db.session.commit()
    # clean possibly orphade keywords from keyword table
    sql = "DELETE FROM keyword WHERE id NOT IN \
        ( SELECT keyword_id FROM doc_keyword )"
    db.session.execute(sql)
    db.session.commit()
    print("successfully updated/inserted keywords!")    
    return

def update_note(form):
    sql = "UPDATE doc_note SET \
        title = :title, \
        content = :content, \
        modified_by = :user_id \
        WHERE id = :id"
    db.session.execute(sql, {
        "title":form["title"],
        "content":form["content"],
        "user_id":session["id"],
        "id":form["id"]})
    db.session.commit()
    print(f"note updated!")
    return

def get_keywords_with_doc_id(id):
    sql = "SELECT * FROM keyword LEFT OUTER JOIN \
        doc_keyword ON keyword.id = doc_keyword.keyword_id \
        WHERE doc_keyword.doc_id = :id ORDER BY doc_keyword.id"
    result = db.session.execute(sql, {"id":id})
    doc = result.fetchall()
    return doc

def get_doc_with_id(id):
    sql = "SELECT * FROM doc WHERE id = :id"
    result = db.session.execute(sql, {"id":id})
    temp = result.fetchone() # because TypeError: 'RowProxy' object does not support item assignment
    doc = {}
    doc.update(temp)
    # also get keywords as one string at the same time
    keywords = ""
    for keyword in get_keywords_with_doc_id(id):
        keywords = f"{keywords} {keyword.word}"
    doc["keywords"] = keywords
    return doc

def update_doc(form):
    print(f"saving values from doc-form: {pretty(form)}")
    sql = "UPDATE doc SET \
        title = :title, \
        file_name = :file_name, \
        description = :description \
        WHERE id = :id"
    db.session.execute(sql, {
        "title":form["title"],
        "file_name":form["file_name"],
        "description":form["description"],
        "id":form["id"]})
    db.session.commit()
    print(f"document updated!")
    return

def get_users():
    sql = "SELECT * FROM user_account order by id"
    results = db.session.execute(sql)
    all_users = results.fetchall()
    return all_users

def get_normal_users():
    sql = "SELECT * FROM user_account where is_admin = 'false' and is_superuser = 'false' order by id"
    results = db.session.execute(sql)
    all_users = results.fetchall()
    return all_users

def update_user(form):
    print(f"saving values from user-form: {pretty(form)}")
    sql = "UPDATE user_account SET \
        username = :username, \
        first_name = :first_name, \
        last_name = :last_name, \
        password = :password, \
        enabled = :enabled \
        WHERE id = :id"
    db.session.execute(sql, {
        "username":form["username"],
        "first_name":form["first_name"],
        "last_name":form["last_name"],
        "password":form["password"],
        "enabled":form["enabled"],
        "id":form["id"]})
    db.session.commit()
    print(f"user updated!")
    return

def create_doc(form):
    print(f"creating doc - values from form: {pretty(form)}")
    sql = "INSERT INTO doc(\
        title, \
        file_name, \
        description, \
        modified_by, \
        created_by) \
        VALUES( \
            :title, \
            :file_name, \
            :description, \
            :modified_by, \
            :created_by \
            ) RETURNING id"
    result = db.session.execute(sql, {
        "title":form["title"],
        "file_name":form["file_name"],
        "description":form["description"],
        "modified_by":session["id"],
        "created_by":session["id"]}
        )
    new_doc_id = result.fetchone()[0]        
    sql2 = "INSERT INTO doc_owner(\
        doc_id, \
        owner_id \
        )\
        VALUES( \
            :doc_id, \
            :owner_id \
        )"
    db.session.execute(sql2, {
        "doc_id":new_doc_id,
        "owner_id":session["id"],
        }
        )
    db.session.commit()
    print(f"NEW DOC CREATED!")
    return

def create_user(form):
    print(f"creating user - values from user-form: {pretty(form)}")
    sql = "INSERT INTO user_account(\
        username, \
        first_name, \
        last_name, \
        password, \
        enabled, \
        is_admin, \
        is_superuser, \
        modified_by, \
        created_by) \
        VALUES( \
            :username, \
            :first_name, \
            :last_name, \
            :password, \
            :enabled, \
            :is_admin, \
            false, \
            1, \
            1)"
    db.session.execute(sql, {
        "username":form["username"],
        "first_name":form["first_name"],
        "last_name":form["last_name"],
        "password":form["password"],
        "enabled":form["enabled"],
        "is_admin":form["is_admin"]})
    db.session.commit()
    print(f"NEW USER CREATED!")
    return

def get_docs():
    sql = "SELECT * FROM doc order by id"
    results = db.session.execute(sql)
    all_documents = results.fetchall()
    return all_documents

def can_edit_user_with_id(user_id):
    user_to_edit = get_user_with_id(user_id)
    return can_edit_user(user_to_edit)

def create_note(form):
    print(f"creating note - values from form: {pretty(form)}")
    sql = "INSERT INTO doc_note(\
        doc_id, \
        title, \
        content, \
        modified_by, \
        created_by) \
        VALUES( \
            :doc_id, \
            :title, \
            :content, \
            :modified_by, \
            :created_by \
            )"
    db.session.execute(sql, {
        "doc_id":form["doc_id"],
        "title":form["title"],
        "content":form["content"],
        "modified_by":session["id"],
        "created_by":session["id"]}
        )
    db.session.commit()
    print(f"NEW NOTE CREATED!")
    return
