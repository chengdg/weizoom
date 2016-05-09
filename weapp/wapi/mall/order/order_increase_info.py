# -*- coding: utf-8 -*-

from core import api_resource, paginator
from wapi.decorators import param_required

from mall import models as mall_models
from mall import module_api as mall_api
from modules.member import models as member_models
from tools.regional.views import get_str_value_by_string_ids_new

from utils import dateutil as utils_dateutil

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
		today = datetime.now()..strftime('%Y-%m-%d 00:00:00')
		monday, sunday = dateutil.get_week_bounds()
		fisrt_day_of_month = dateutil.get_first_day_of_month()

		member_increase_info = {}
		today_count = mall_models.Order.objects.filter(webapp_id=webapp_id, status__in=VALID_STATUS, created_at__gte=today).count()
		week_count = mall_models.Order.objects.filter(webapp_id=webapp_id, status__in=VALID_STATUS, created_at__range=(monday, sunday)).count()
		month_count = mall_models.Order.objects.filter(webapp_id=webapp_id, status__in=VALID_STATUS, created_at__gte=get_first_day_of_month).count()


		return {
				'today_count': today_count,
				'week_count': week_count,
				'month_count': month_count
			}