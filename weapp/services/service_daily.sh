#!/bin/bash
export PATH=/usr/local/bin:$PATH


echo ">> calling 'apps_powerme_timer_task'"
echo "--------------------------------------------------------" >> $LOG
python manage.py update_member_purchase_frequency