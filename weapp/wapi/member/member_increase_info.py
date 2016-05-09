# -*- coding: utf-8 -*-

from core import api_resource
from core import paginator
from wapi.decorators import param_required
from django.db.models import Q
from core.jsonresponse import create_response
from modules.member import models as member_models
from mall import models as mall_models
from mall.models import *
from datetime import datetime
from utils import dateutil
import json


class MemberIncrease(api_resource.ApiResource):
	"""
	获取会员增长数据
	"""
	app = 'member'
	resource = 'member_increase'

	@param_required(['webapp_id'])
	def get(args):
		"""
		获取会员增长数据
		"""

		webapp_id = args['webapp_id']
		today = datetime.now()..strftime('%Y-%m-%d 00:00:00')
		monday, sunday = dateutil.get_week_bounds()
		fisrt_day_of_month = dateutil.get_first_day_of_month()

		member_increase_info = {}
		total_count = member_models.Member.objects.filter(webapp_id=webapp_id, is_subscribed=True).count()
		today_count = member_models.Member.objects.filter(webapp_id=webapp_id, is_subscribed=True, created_at__gte=today).count()
		week_count = member_models.Member.objects.filter(webapp_id=webapp_id, is_subscribed=True, created_at__range=(monday, sunday)).count()
		month_count = member_models.Member.objects.filter(webapp_id=webapp_id, is_subscribed=True, created_at__gte=get_first_day_of_month).count()


		return {
				'total_count': total_count,
				'today_count': today_count,
				'week_count': week_count,
				'month_count': month_count
			}