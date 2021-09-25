#!/bin/bash

set -x # echo all commands
set -e # fail on error

source common.sh

echo "pre-installs now."

echo "tietokantasovellus-kurssi."

echo "Osa 1"

echo "Johdatus web-sovelluksiin"

mkdir -p "$application_name"

cd "$application_name"

function set_up_flask {
    python3 -m venv venv

    source venv/bin/activate

    pip install flask
}

if [ ! -f "venv/bin/activate" ]
then
    set_up_flask
fi

cat << CODE > app.py
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Heipparallallaa!"
CODE

echo "Sivupyynnöt"

cat << CODE > app.py
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Heipparallallaa!"

@app.route("/page1")
def page1():
    return "Tämä on sivu 1"

@app.route("/page2")
def page2():
    return "Tämä on sivu 2"

CODE

cat << CODE >> app.py

@app.route("/test")
def test():
    content = ""
    for i in range(100):
        content = content + str(i + 1) + " "
    return content
    
CODE

cat << CODE >> app.py

@app.route("/test/<int:id>")
def page(id):
    return "Tämä on sivu " + str(id)
    
CODE

cat << CODE >> app.py

@app.route("/html_commands/")
def html_commandos():
    return "<b>Tervetuloa</b> <i>sovellukseen</i>!"
    
CODE

# comment out to skip first part examples
# flask run
# continues here after user presses CTRL+C

mkdir -p templates/

cat << CODE > templates/index.html
<title>Etusivu</title>
<h1>Etusivu</h1>
<b>Tervetuloa</b> <i>sovellukseen</i>!
CODE

cat << CODE > app.py
from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
CODE

# image
mkdir -p static/
cp -ar "../resource/image" static/

cat << CODE > templates/bee.html
<title>Etusivu</title>
<h1>Etusivu</h1>
<p>{{ message }}</p>
<ul>
{% for item in items %}
<li> {{ item }}
{% endfor %}
</ul>

<img src="/static/image/mustikkamaa.jpg" width="640" height="480" >
<ul><li>mustikkamaa</li></ul>

CODE


cat << CODE >> app.py

@app.route("/bee/")
def bee():
    words = ["apina", "banaani", "cembalo"]
    return render_template("bee.html", message="Tervetuloa!", items=words)
CODE

# flask run

echo "Lomakkeiden käsittely"

cat << CODE >> templates/form.html
<form action="/result" method="POST">
Anna nimesi:
<input type="text" name="name">
<br>
<input type="submit" value="Lähetä">
</form>
CODE

cat << CODE >> templates/result.html
Moikka, {{ name }}
CODE

cat << CODE >> app.py
from flask import Flask
from flask import render_template, request
app = Flask(__name__)

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/result", methods=["POST"])
def result():
    return render_template("result.html", name=request.form["name"])
CODE

cat << CODE >> templates/order.html
<form action="/result" method="POST">
Valitse pizza:
<p>
<input type="radio" name="pizza" value="1"> Frutti di Mare
<input type="radio" name="pizza" value="2"> Margherita
<input type="radio" name="pizza" value="3"> Quattro Formaggi
<input type="radio" name="pizza" value="4"> Quattro Stagioni
<p>
Valitse lisät:
<p>
<input type="checkbox" name="extra" value="A"> oregano
<input type="checkbox" name="extra" value="B"> valkosipuli
<p>
Erikoistoiveet: <br>
<textarea name="message" rows="3" cols="50"></textarea>
<p>
<input type="submit" value="Lähetä">
</form>
CODE

cat << CODE >> templates/result.html
Valitsit pizzan {{ pizza }}
<p>
Seuraavat lisät:
<ul>
{% for extra in extras %}
<li> {{ extra }}
{% endfor %}
</ul>
Erikoistoiveet: <br>
{{ message }}
CODE

cat << CODE >> app.py
from flask import Flask
from flask import render_template, request

app = Flask(__name__)

@app.route("/order")
def order():
    return render_template("order.html")

@app.route("/result", methods=["POST"])
def result():
    pizza = request.form["pizza"]
    extras = request.form.getlist("extra")
    message = request.form["message"]
    return render_template("result.html", pizza=pizza,
                                          extras=extras,
                                          message=message)
CODE

echo "Sovelluksen toiminta"

flask run

deactivate

cd ..

echo "@end"
