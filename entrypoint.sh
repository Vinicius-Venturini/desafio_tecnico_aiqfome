#!/bin/sh
set -e

python client_api/manage.py migrate --noinput

uwsgi --ini uwsgi.ini
