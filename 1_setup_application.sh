#!/bin/bash

set -x # echo all commands
set -e # fail on error

source common.sh

cd "$application_name"

echo "setup application."

psql < schema.sql

echo "@end"
