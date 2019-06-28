#!/bin/bash

export PY=/home/doris/.local/share/virtualenvs/immo_cool-UOny7QwX/bin/python
export SECRET_KEY=
export DJANGO_SETTINGS_MODULE=immocool.settings.production
export IMMOCOOL_DB_NAME=
export IMMOCOOL_DB_USER=
export IMMOCOOL_DB_PWD=
export IMMOCOOL_ADMNS=
export IMMOCOOL_EMAIL_HOST=
export IMMOCOOL_EMAIL_HOST_USER=
export IMMOCOOL_EMAIL_HOST_PASSWORD=
export IMMOCOOL_EMAIL_PORT=

cd /home/doris/immo_cool
$PY manage.py alert_admin --settings=$DJANGO_SETTINGS_MODULE
