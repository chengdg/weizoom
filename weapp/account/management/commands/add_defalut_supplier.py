#-*- coding: utf-8 -*-
from datetime import datetime, timedelta
import time
import json
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from core.exceptionutil import unicode_full_stack
from watchdog.utils import watchdog_error, watchdog_info, watchdog_warning
from mall.promotion import models as promotion_models
from mall.models import *


class Command(BaseCommand):
	help = "add default supplier"
	args = ''

	def handle(self, *args, **options):
		print options
		print args

		if len(args) != 1:
			print ' need owner_id!'
			return 
		if User.objects.filter(id=args[0]).count() == 0:
			print 'invalid owner_id' 
			return 
		owner_id = args[0]

		# if Supplier.objects.filter(owner_id=owner_id, name="自营").count() > 0:
		supplier =  Supplier.objects.filter(owner_id=owner_id, name="自营").first()
		if supplier:
			supplier_id = supplier
		else:
			supplier_id = Supplier.objects.create(owner_id=owner_id, name="自营").id
			
		Product.objects.filter(supplier=0, owner_id=owner_id).update(supplier=supplier)
