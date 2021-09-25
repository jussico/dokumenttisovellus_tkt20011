#!/bin/bash

set -x # echo all commands
set -e # fail on error

echo "setup environment."

sudo apt install python3.8-venv

pip install flask
pip install flask-sqlalchemy
pip install psycopg2-binary
pip install python-dotenv    

function install_and_setup_postgres {

    sudo apt-get install postgresql-12

    sudo /etc/init.d/postgresql start

sudo -u postgres psql postgres  <<CODE
    \password postgres
CODE

sudo -u postgres psql postgres <<CODE
CREATE USER jussi WITH ENCRYPTED PASSWORD 'jussi';
ALTER USER jussi WITH SUPERUSER;
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

echo "on desktop environment install also:"
echo "sudo apt install pgadmin3"

echo "@end"
