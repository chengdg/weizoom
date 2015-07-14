# -*- coding: utf-8 -*-

import os
import subprocess
from datetime import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from tools.express import models as express_models
from mall import models as mall_models


class Command(BaseCommand):
	help = "init express for version 2"
	args = ''
	
	def handle(self, **options):
		print self.help
		express_models.ExpressHasOrderPushStatus.objects.all().update(send_count=1, receive_count=1)

		details = express_models.ExpressDetail.objects.filter(order_id__gt=0)

		order_ids = [d.order_id for d in details]
		orders = mall_models.Order.objects.filter(id__in=order_ids)
		order2id = dict([(o.id, o) for o in orders])

		for detail in details:
			print '-------------[ExpressDetail_id: {}]'.format(detail.id)
			order = order2id[detail.order_id]
			expresses = express_models.ExpressHasOrderPushStatus.objects.filter(
				express_company_name=order.express_company_name,
				express_number=order.express_number)
			if expresses.count() > 0:
				express = expresses[0]
				detail.express_id = express.id
				detail.save()
