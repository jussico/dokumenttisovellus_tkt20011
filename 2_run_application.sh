#!/bin/bash

set -x # echo all commands
set -e # fail on error

source common.sh

cd "$application_name"

echo "run application."

echo "URL:"
echo "http://127.0.0.1:5000/"

flask run

deactivate

echo "@end"
