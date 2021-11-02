#!/bin/bash

BASEDIR=$(dirname "$0")
BASEDIR=$(cd $BASEDIR; pwd)

cd $BASEDIR/webserver
pipenv install
pipenv run manage.py migrate

cd $BASEDIR/react/robot
npm install
