# -*- coding: utf-8 -*-

__author__ = 'jiangzhe'

import time
from datetime import datetime, timedelta
import array

from django.core.management.base import BaseCommand, CommandError

from utils import cache_util
from bson import json_util
import json

from mall.models import *
from modules.member.models import *


class Command(BaseCommand):
	help = "json.dumps cached value"
	args = ''
	
	def handle(self, order_id,today_str,**options):
		created_at = today_str + ' 08:08:08'
		order = Order.objects.get(order_id=order_id)
		order.created_at=created_at
		order.payment_time=created_at
		order.save()
		print u'更新成功'

		