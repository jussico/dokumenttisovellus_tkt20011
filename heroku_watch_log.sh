#!/bin/bash

source common.sh

heroku logs -t --app "$heroku_application_name"

