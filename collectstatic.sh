#!/bin/bash

BASEDIR=$(dirname "$0")
BASEDIR=$(cd $BASEDIR; pwd)

cd $BASEDIR/webserver
pipenv run python manage.py collectstatic --noinput

cd $BASEDIR/react/robot
npm run build
