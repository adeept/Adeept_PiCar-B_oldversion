#!/bin/bash

NAME="PiPatroller"                              #Name of the application (*)
BASEDIR=$(dirname "$0")
BASEDIR=$(cd $BASEDIR; pwd)

DJANGODIR=$BASEDIR/webserver            # Django project directory (*)
SOCKFILE=$BASEDIR/gunicorn.sock         # we will communicate using this unix socket (*)
USER=nginx                              # the user to run as (*)
GROUP=webdata                           # the group to run as (*)
NUM_WORKERS=1                           # how many worker processes should Gunicorn spawn (*)
DJANGO_SETTINGS_MODULE=$NAME.settings   # which settings file should Django use (*)
DJANGO_WSGI_MODULE=$NAME.wsgi           # WSGI module name (*)

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec pipenv run gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user $USER \
  --bind=unix:$SOCKFILE
