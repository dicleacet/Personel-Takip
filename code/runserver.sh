#!/bin/bash

cd /code
/venv/bin/python3 ./manage.py migrate
#/venv/bin/python3 ./manage.py makemessages --all -i venv* -i usr*
#/venv/bin/python3 ./manage.py compilemessages
/venv/bin/python3 ./manage.py collectstatic --noinput
 rm -f /var/run/celeryd.pid
 /venv/bin/python3 -u -m celery -A app.celery.celery_app worker --loglevel=INFO --concurrency=3 --pidfile=/var/run/celeryd.pid --logfile=/harddisk/logs/celeryd.log --detach


echo "server started 0.0.0.0:8008"
/venv/bin/python3 ./manage.py runserver 0.0.0.0:8008
