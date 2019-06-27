#!/bin/bash

export PY=/home/doris/.local/share/virtualenvs/immo_cool-UOny7QwX/bin/python
export SECRET_KEY="ck8k8bzjqxgsqxax_!na5!s0nd$a2?"
export DJANGO_SETTINGS_MODULE=immocool.settings.production
export IMMOCOOL_DB_NAME="immocool"
export IMMOCOOL_DB_USER="adminic"
export IMMOCOOL_DB_PWD="Pikool84"

cd /home/doris/immo_cool
$PY manage.py echeance_base --settings=$DJANGO_SETTINGS_MODULE
