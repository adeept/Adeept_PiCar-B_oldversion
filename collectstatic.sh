#!/bin/bash

BASEDIR=$(dirname "$0")
BASEDIR=$(cd $BASEDIR; pwd)

cd $BASEDIR/webserver
/usr/bin/pipenv run python manage.py collectstatic --noinput

cd $BASEDIR/react/robot
npm run build
