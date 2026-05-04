#!/bin/bash

rm db.sqlite3
rm -rf ./trippyapi/migrations
python manage.py migrate
python manage.py makemigrations trippyapi
python manage.py migrate trippyapi
python manage.py loaddata users
python manage.py loaddata tokens