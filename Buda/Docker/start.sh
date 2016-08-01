#!/bin/sh
supervisord -c /etc/supervisor/supervisord.conf
supervisorctl -c /etc/supervisor/supervisord.conf
supervisorctl reread && supervisorctl update
supervisorctl -c /etc/supervisor/supervisord.conf
python /project/Buda/manage.py runserver 0.0.0.0:8000