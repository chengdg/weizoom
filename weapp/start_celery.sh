#!/bin/bash
#celery -A weapp worker -l info
# test by jz2
rm -f celery.pid
nohup python run_celery.py   &
