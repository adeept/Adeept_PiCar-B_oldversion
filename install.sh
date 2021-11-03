#!/bin/bash

BASEDIR=$(dirname "$0")
BASEDIR=$(cd $BASEDIR; pwd)

cd $BASEDIR/webserver
/usr/bin/pipenv install
/usr/bin/pipenv run manage.py migrate

cd $BASEDIR/react/robot
npm install
