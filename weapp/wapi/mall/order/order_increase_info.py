# -*- coding: utf-8 -*-

from core import api_resource, paginator
from wapi.decorators import param_required

from mall import models as mall_models
from mall import module_api as mall_api
from modules.member import models as member_models
from tools.regional.views import get_str_value_by_string_ids_new

from utils import dateutil
from datetime import datetime

VALID_STATUS = [mall_models.ORDER_STATUS_PAYED_NOT_SHIP, mall_models.ORDER_STATUS_PAYED_SHIPED, mall_models.ORDER_STATUS_SUCCESSED]

class OrderIncrease(api_resource.ApiResource):
	"""
	订单数据概况
	"""
	app = 'mall'
	resource = 'order_increase'

	@param_required(['webapp_id'])
	def get(args):
		"""
		订单数据概况
		"""

		webapp_id = args['webapp_id']
		today = datetime.now().strftime('%Y-%m-%d 00:00:00')
		monday, sunday = dateutil.get_week_bounds()
		fisrt_day_of_month = dateutil.get_first_day_of_month()

		member_increase_info = {}
		total_count = mall_models.Order.objects.filter(webapp_id=webapp_id, status__in=VALID_STATUS, origin_order_id__lte=0).count()
		today_count = mall_models.Order.objects.filter(webapp_id=webapp_id, status__in=VALID_STATUS, created_at__gte=today, origin_order_id__lte=0).count()
		week_count = mall_models.Order.objects.filter(webapp_id=webapp_id, status__in=VALID_STATUS, created_at__range=(monday, sunday), origin_order_id__lte=0).count()
		month_count = mall_models.Order.objects.filter(webapp_id=webapp_id, status__in=VALID_STATUS, created_at__gte=fisrt_day_of_month, origin_order_id__lte=0).count()

		price_day = 0.0
		price_day_card = 0.0
		price_day_money = 0.0
		price_week = 0.0
		price_week_card = 0.0
		price_week_money = 0.0
		price_month = 0.0
		price_month_card = 0.0
		price_month_money = 0.0

		orders = mall_models.Order.objects.filter(webapp_id=webapp_id, status__in=VALID_STATUS, created_at__gte=today, origin_order_id__lte=0)
		for order in orders:
			price_day_card += order.weizoom_card_money
			price_day_money += order.final_price
		price_day = price_day_card + price_day_money

		orders = mall_models.Order.objects.filter(webapp_id=webapp_id, status__in=VALID_STATUS, created_at__range=(monday, sunday), origin_order_id__lte=0)
		for order in orders:
			price_week_card += order.weizoom_card_money
			price_week_money += order.final_price
		price_week = price_week_card + price_week_money

		orders = mall_models.Order.objects.filter(webapp_id=webapp_id, status__in=VALID_STATUS, created_at__gte=fisrt_day_of_month, origin_order_id__lte=0)
		for order in orders:
			price_month_card += order.weizoom_card_money
			price_month_money += order.final_price
		price_month = price_month_card + price_month_money


		return {
				'total_count': total_count,
				'today_count': today_count,
				'week_count': week_count,
				'month_count': month_count,
				'price_day': price_day,
				'price_day_card': price_day_card,
				'price_day_money': price_day_money,
				'price_week': price_week,
				'price_week_card': price_week_card,
				'price_week_money': price_week_money,
				'price_month': price_month,
				'price_month_card': price_month_card,
				'price_month_money': price_month_money
			}