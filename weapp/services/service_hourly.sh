#!/bin/bash
# 每小时调用的service

DATE="`date +%Y%m%d`"
TIME="`date +%Y%m%d%H%M%S`"
ROOT_DIR="/weapp/web/weapp"
#ROOT_DIR="`pwd`"
LOG_DIR="$ROOT_DIR/../log/services/$DATE"
mkdir -p $LOG_DIR

LOG="$LOG_DIR/hourly_$TIME.log"
echo "called time: $TIME" > $LOG
echo "LOG_DIR=$LOG_DIR"

echo "ROOT_DIR=$ROOT_DIR"
cd $ROOT_DIR
echo "========================================================" >> $LOG

# add more services here
echo ">> calling 'services.send_express_poll_service.tasks.send_express_poll_request'" >> $LOG
echo "--------------------------------------------------------" >> $LOG
python services/send_task.py "services.send_express_poll_service.tasks.send_express_poll_request" {} "{\"id\": 0}" >> $LOG 2>&1

echo "========================================================" >> $LOG
echo "done!" >> $LOG