# -*- coding: utf-8 -*-

from core import api_resource
from wapi.decorators import param_required, ApiParamaterError

from wapi.wapi_utils import get_webapp_id_via_username

from stats.manage.brand_value_utils import get_brand_value
from utils import dateutil as utils_dateutil

class BrandValue(api_resource.ApiResource):
	"""
	获取微品牌价值的接口
	"""
	app = 'stats'
	resource = 'brand_value'

	# @param_required(['wid', 'dates'])
	def get(args):
		"""
		获取微品牌价值

		@param un username
		@param wid webapp_id
		@param dates 日期列表，多日期用逗号(,)分隔。默认是当天。
		"""
		username = args.get('un', None)
		webapp_id = args.get('wid', None)
		if (not username) and (not webapp_id):
			raise ApiParamaterError('no parameter wid or un!')

		dates = args.get('dates', None)
		if dates is None or len(dates)<1:
			dates = [ utils_dateutil.date2string(utils_dateutil.now()) ]
		else:
			dates = dates.split(',')

		if username:
			webapp_id = get_webapp_id_via_username(username)

		values = {date_str: get_brand_value(webapp_id, date_str) for date_str in dates}

		return {"values": values}
