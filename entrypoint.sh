#!/bin/sh
set -eu
python manage.py wait_for_db
python manage.py migrate --noinput
exec "$@"
