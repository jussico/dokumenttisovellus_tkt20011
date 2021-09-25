#!/bin/bash

set -x # echo all commands
set -e # fail on error

source common.sh

echo "create app skeleton."

mkdir -p "$application_name"

cd "$application_name"

function set_up_flask {
    python3 -m venv venv
    source venv/bin/activate
}

if [ ! -f "venv/bin/activate" ]
then
    set_up_flask
fi

mkdir -p templates/

# images
mkdir -p static/image/

cat << CODE > .env
DATABASE_URL=postgresql:///${USER}
CODE

cat << CODE > app.py
from flask import Flask

app = Flask(__name__)

import routes
CODE

cat << CODE > db.py
from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")

# TODO: really needed?
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
CODE

cat << CODE > routes.py
from app import app
import visits
from flask import render_template

@app.route("/")
def index():
    visits.add_visit()
    counter = visits.get_counter()
    return render_template("index.html", counter=counter)
CODE

cat << CODE > visits.py
from db import db

def add_visit():
    db.session.execute("INSERT INTO visitors (time) VALUES (NOW())")
    db.session.commit()

def get_counter():
    result = db.session.execute("SELECT COUNT(*) FROM visitors")
    counter = result.fetchone()[0]
    return counter
CODE

cat << CODE > schema.sql
DROP TABLE messages;
DROP TABLE users;
DROP TABLE visitors;

CREATE TABLE visitors (id SERIAL PRIMARY KEY, time TIMESTAMP);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    sent_at TIMESTAMP
);
CODE

cat << CODE > templates/layout.html
<!doctype html>
<title>Document Application - {% block title %}{% endblock %}</title>
<h1>Document Application</h1>
<a href="/">Main page</a>
<a href="/login">Login</a>
<hr>
{% block content %}{% endblock %}
<hr>
CODE

cat << CODE > templates/index.html
{% extends "layout.html" %}
{% block title %}Etusivu{% endblock %}
{% block content %}
<h2>Etusivu</h2>
Tervetuloa sovellukseen!
{% endblock %}
CODE

cat << CODE > templates/login.html
{% extends "layout.html" %}
{% block title %}Kirjautuminen{% endblock %}
{% block content %}
<h2>Kirjautuminen</h2>
<form action="/login" method="POST">
Tunnus: <input type="text" name="username"> <br>
Salasana: <input type="password" name="password"> <br>
<input type="submit" value="Kirjaudu">
</form>
{% endblock %}
CODE

echo "@end"
