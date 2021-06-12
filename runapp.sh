#!/bin/bash

cd /app/

DJANGO_SECRET=${DJANGO_SECRET:-"fw2wa4gp+hc7H4l3nwl=y2r-dnbl-q(P3uqa3qmv7y0e+qw128"}

./manage.py migrate
./manage.py collectstatic

gunicorn -w 3 avgregister.wsgi --bind 0.0.0.0