# -*- coding: utf-8 -*-

import logging
from django.core.management.base import BaseCommand, CommandError

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weapp.settings")

# from django.core.management import execute_from_command_line

# execute_from_command_line(sys.argv)

from mall.models import *
from mall.module_api import update_order_status



import datetime

class Command(BaseCommand):
	help = "get weizoom order every week"
	args = ''
	
	def handle(self,*args, **options):
		

		date_7_days_ago = datetime.datetime.now() - datetime.timedelta(7)
		if len(args) == 1:
				if args[0] == 'test':
					date_7_days_ago = datetime.datetime.now()


		orders  = Order.objects.filter(status=ORDER_STATUS_PAYED_SHIPED, is_100=False, express_number='', origin_order_id__gte=0, created_at__lte=date_7_days_ago)

		print 'orders_count>>>>>>>>',orders.count()
		for order in orders:
			if OrderStatusLog.objects.filter(order_id=order.order_id, to_status=ORDER_STATUS_PAYED_SHIPED, created_at__lte=date_7_days_ago) > 0:
				update_order_status(user=None, action=u'finish-自动确认', order=order)

		print "execute over"
