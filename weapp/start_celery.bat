celery -A weapp worker -l info --pidfile="celery.pid"
REM celery worker -A weapp --pidfile="celery-%N-%i.pid" --logfile="celery-%N-%i.log" -l info