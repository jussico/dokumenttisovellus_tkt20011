#!/bin/bash

set -x # echo all commands
set -e # fail on error

source common.sh

echo "tietokantasovellus-kurssi."

echo "Osa 2"

mkdir -p "$application_name"

cd "$application_name"

echo "pre-installs now."

function install_and_setup_postgres {

    sudo apt-get install postgresql-12

    sudo /etc/init.d/postgresql start

sudo -u postgres psql postgres  <<CODE
    \password postgres
CODE

sudo -u postgres psql postgres <<CODE
create user jussi with encrypted password 'jussi';

--grant all privileges on database sample_db to jussi;
-- ALTER USER jussi CREATEDB;

-- just make me a superuser
ALTER USER jussi WITH SUPERUSER;
-- ALTER USER jussi WITH NOSUPERUSER;

-- use unix username as database name so its used as default database when running psql -command.
CREATE DATABASE jussi;
GRANT ALL PRIVILEGES ON DATABASE jussi TO jussi;

CODE

# open postgres ports to everywhere so Windows PgAdmin works correctly with this WSL Ubuntu install.
sudo sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" /etc/postgresql/12/main/postgresql.conf 

}

# only install and setup if psql command is missing.
if ! command -v psql &> /dev/null
then
    install_and_setup_postgres
fi

function set_up_flask {
    python3 -m venv venv

    source venv/bin/activate

    pip install flask
}

if [ ! -f "venv/bin/activate" ]
then
    set_up_flask
fi

echo "Tietokannan käyttäminen"

psql <<CODE
CREATE TABLE messages (id SERIAL PRIMARY KEY, content TEXT);
DELETE FROM messages;
INSERT INTO messages (content) VALUES ('moikka');
INSERT INTO messages (content) VALUES ('apina banaani cembalo');
INSERT INTO messages (content) VALUES ('kolmas viesti');
SELECT * FROM messages;

-- describe/list tables
\dt 

-- describe <table_name>
\d messages 

-- DROP TABLE messages;
CODE

pip install flask-sqlalchemy
# pip install psycopg2 # won't install
pip install psycopg2-binary

cat << CODE > app.py
from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///${USER}"
db = SQLAlchemy(app)

@app.route("/")
def index():
    result = db.session.execute("SELECT content FROM messages")
    messages = result.fetchall()
    return render_template("index.html", count=len(messages), messages=messages) 

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    sql = "INSERT INTO messages (content) VALUES (:content)"
    db.session.execute(sql, {"content":content})
    db.session.commit()
    return redirect("/")
CODE

mkdir -p templates
cat << CODE > templates/index.html
Viestien määrä: {{ count }}
<hr>
{% for message in messages %}
{{ message.content }}
<hr>
{% endfor %}
<a href="/new">Lähetä viesti</a>
CODE

cat << CODE > templates/new.html
<form action="/send" method="POST">
Viesti: <br>
<textarea name="content" rows="3" cols="40"></textarea>
<br>
<input type="submit" value="Lähetä">
</form>
CODE

# echo "http://127.0.0.1:5000/"
# flask run

pip install python-dotenv

cat << CODE > .env
DATABASE_URL=postgresql:///${USER}
CODE

# getting url from code:
# from os import getenv
# app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")

# disabling SQLALCHEMY message
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

echo "Kyselyt"

echo ".. rest of the code is in git-repository:"
echo "https://github.com/hy-tsoha/tsoha-polls"

cd ..

echo "@end"

exit 0

cat << CODE > tiedostonimi
koodii
CODE
