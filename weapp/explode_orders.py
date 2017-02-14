# -*- coding: utf-8 -*-
import sys
import datetime
import copy

reload(sys)
sys.setdefaultencoding("utf-8")
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weapp.settings")

from django.core.management import execute_from_command_line

execute_from_command_line(sys.argv)

import json
from mall import models as mall_models

orders = mall_models.Order.objects.filter(origin_order_id=0)

print('----start...')

def __get_order_has_products(order):
	order_has_products = mall_models.OrderHasProduct.objects.filter(order_id=order.id)
	return order_has_products


for order in orders:
	new_order = copy.copy(order)
	new_order.id = None
	new_order.origin_order_id = order.id
	new_order.order_id = str(new_order.order_id) + str('^0s')
	new_order.save()

	order_has_products = __get_order_has_products(order)


	for ohp in order_has_products:
		new_ohp = copy.copy(ohp)
		new_ohp.id = None
		new_ohp.save()

print('end...')
