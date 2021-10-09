#!/bin/bash

source common.sh

heroku git:remote -a "$heroku_application_name"

git remote -v

