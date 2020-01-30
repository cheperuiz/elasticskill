#!/bin/bash
cd $PROJECT_SRC/app
gunicorn --config=$GUNICORN_CONFIG wsgi:flask_app