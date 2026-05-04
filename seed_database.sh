#!/bin/bash

rm db.sqlite3
rm -rf ./trippyapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations trippyapi
python3 manage.py migrate trippyapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens