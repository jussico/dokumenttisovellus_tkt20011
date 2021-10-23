#!/bin/bash

heroku_application_name='prelude-to-document-app'

heroku login

heroku apps:create "$heroku_application_name"



