#!/bin/bash

source common.sh

heroku login

heroku apps:create "$heroku_application_name"

# database

heroku addons:create heroku-postgresql

heroku psql < prelude/schema.sql

heroku psql < scripts/test_data.sql

heroku config

source prelude/.env

heroku config:set SECRET_KEY="$SECRET_KEY"

