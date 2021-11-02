#!/bin/bash

cd webserver
pipenv run python manage.py collectstatic --noinput

cd ../react/robot
npm run build
