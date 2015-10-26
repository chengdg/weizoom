# -*- coding: utf-8 -*-
from core import api_resource
from wapi.decorators import param_required
from wapi.wapi_utils import get_webapp_id_via_username

from mall.outline import utils

class PurchaseTrend(api_resource.ApiResource):
	"""
	获取购买趋势的接口
	"""
	app = 'stats'
	resource = 'purchase_trend'

	@param_required(['un'])
	def get(args):
		"""
		获取微品牌价值

		@param un username
		@param sd 起始日期(可选参数)
		@param ed 结束日期(可选参数)
		"""
		username = args.get('un')
		start_date = args.get('sd', None)
		end_date = args.get('ed', None)
		print '============',username,start_date,end_date

		webapp_id = get_webapp_id_via_username(username)
		print '----------------webapp_id:',webapp_id
		purchase_trend_data = utils.get_purchase_trend(webapp_id, start_date, end_date)
		print '==========purchase_trend_data:',purchase_trend_data
		
		return purchase_trend_data
