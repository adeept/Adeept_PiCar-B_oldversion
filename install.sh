#!/bin/bash

BASEDIR=$(dirname "$0")
BASEDIR=$(cd $BASEDIR; pwd)

cd $BASEDIR/webserver
pipenv install

cd $BASEDIR/react/robot
npm install
