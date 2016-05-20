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

VALID_STATUS = [mall_models.ORDER_STATUS_PAYED_NOT_SHIP, mall_models.ORDER_STATUS_PAYED_SHIPED, mall_models.ORDER_STATUS_SUCCESSED]

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
		today = datetime.now().strftime('%Y-%m-%d 00:00:00')
		monday, sunday = dateutil.get_week_bounds()
		fisrt_day_of_month = dateutil.get_first_day_of_month()

		member_increase_info = {}
		total_count = member_models.Member.objects.filter(webapp_id=webapp_id, is_subscribed=True, is_for_test=False).count()
		today_count = member_models.Member.objects.filter(webapp_id=webapp_id, is_subscribed=True, is_for_test=False, created_at__gte=today).count()
		week_count = member_models.Member.objects.filter(webapp_id=webapp_id, is_subscribed=True, is_for_test=False, created_at__range=(monday, sunday)).count()
		month_count = member_models.Member.objects.filter(webapp_id=webapp_id, is_subscribed=True, is_for_test=False, created_at__gte=fisrt_day_of_month).count()

		#获取新增的购买用户数，暂时忽略买完就取关的情况
		# total_buy_member_count =  member_models.Member.objects.filter(webapp_id=webapp_id, is_subscribed=True, pay_times__gte=1).count()
		orders = mall_models.Order.objects.filter(webapp_id=webapp_id, status__in=VALID_STATUS)
		total_buy_member_count = get_member_count(orders)

		orders = mall_models.Order.objects.filter(webapp_id=webapp_id, status__in=VALID_STATUS, is_first_order=True, created_at__gte=today)
		today_buy_member_count = get_member_count(orders)

		orders = mall_models.Order.objects.filter(webapp_id=webapp_id, status__in=VALID_STATUS, is_first_order=True, created_at__range=(monday, sunday))
		week_buy_member_count = get_member_count(orders)

		orders = mall_models.Order.objects.filter(webapp_id=webapp_id, status__in=VALID_STATUS, is_first_order=True, created_at__gte=fisrt_day_of_month)
		month_buy_member_count = get_member_count(orders)


		return {
				'total_count': total_count,
				'today_count': today_count,
				'week_count': week_count,
				'month_count': month_count,
				'total_buy_member_count': total_buy_member_count,
				'today_buy_member_count': today_buy_member_count,
				'week_buy_member_count': week_buy_member_count,
				'month_buy_member_count': month_buy_member_count
			}

def get_member_count(orders):
	webapp_user_ids = set()
	for order in orders:
		webapp_user_ids.add(order.webapp_user_id)
	webapp_users = member_models.WebAppUser.objects.filter(id__in=webapp_user_ids)
	member_ids = [w.member_id for w in webapp_users]
	member_count = member_models.Member.objects.filter(id__in=member_ids, is_subscribed=True, is_for_test=False).count()

	return member_count