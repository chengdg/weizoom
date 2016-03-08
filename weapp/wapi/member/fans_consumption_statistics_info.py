# -*- coding: utf-8 -*-

from core import api_resource
from core import paginator, dateutil
from wapi.decorators import param_required
from django.db.models import Q
from core.jsonresponse import create_response
from modules.member import models as member_models
from mall import models as mall_models
from mall.models import *
from datetime import datetime
import json

SKEP_ACCOUNT2WEBAPP_ID = {
	'jingxuan': '3621',
	'xuesheng': '3807',
	'mama': '3806',
	'club': '3936'
}

class ConsumptionStatistics(api_resource.ApiResource):
	"""
	获取会员基本信息
	购买次数，付款金额，最后一次支付时间，客单价，推荐人，创建时间
	"""
	app = 'fans'
	resource = 'consumption_statistics'

	@param_required(['member_ids','start_date','end_date'])
	def get(args):
		"""
		获取商品和供应商信息

		@param member_ids 会员id
		@param start_date 查询开始时间
		@param end_date 查询截止时间
		"""

		member_ids = args['member_ids']
		start_date = args['start_date']
		end_date = args['end_date']


		member_ids2info = {}
		webapp_user_ids2order = {}
		webapp_users_obj = member_models.WebAppUser.objects.filter(member_id__in=member_ids.split(','))
		webapp_user_id2member_id = dict([(u.id, u.member_id) for u in webapp_users_obj])
		member_id2webapp_user_id = dict([(u.member_id,u.id) for u in webapp_users_obj])
		webapp_user_ids = set(webapp_user_id2member_id.keys())
		orders = Order.by_webapp_user_id(webapp_user_ids).filter(status=ORDER_STATUS_SUCCESSED,
			created_at__range=(start_date, end_date)).order_by('-created_at')

		for order in orders:
			if not order.webapp_user_id in webapp_user_ids2order:
				webapp_user_ids2order[order.webapp_user_id] = {}
				webapp_user_ids2order[order.webapp_user_id]['cash'] = 0
				webapp_user_ids2order[order.webapp_user_id]['card'] = 0
				webapp_user_ids2order[order.webapp_user_id]['order_count'] = 0
				webapp_user_ids2order[order.webapp_user_id]['last_pay_time'] = datetime.strptime('2000-01-01', '%Y-%m-%d')
			webapp_user_ids2order[order.webapp_user_id]['cash'] += order.final_price
			webapp_user_ids2order[order.webapp_user_id]['card'] += order.weizoom_card_money

			webapp_user_ids2order[order.webapp_user_id]['order_count'] += 1
			if order.payment_time > webapp_user_ids2order[order.webapp_user_id]['last_pay_time']:
				webapp_user_ids2order[order.webapp_user_id]['last_pay_time'] = order.payment_time
			webapp_user_ids2order[order.webapp_user_id]['last_pay_time'] =\
				webapp_user_ids2order[order.webapp_user_id]['last_pay_time'].strftime('%Y-%m-%d %H:%M:%S')

		for member_id,webapp_user_id in member_id2webapp_user_id:
			if not member_id in member_ids2info:
				member_ids2info[member_id] = {}
			if webapp_user_id in webapp_user_ids2order:
				member_ids2info[member_id]['cash'] = webapp_user_ids2order[webapp_user_id]['cash']
				member_ids2info[member_id]['card'] = webapp_user_ids2order[webapp_user_id]['card']
				member_ids2info[member_id]['pay_money'] = webapp_user_ids2order[webapp_user_id]['cash'] + webapp_user_ids2order[webapp_user_id]['card']
				member_ids2info[member_id]['order_count'] = webapp_user_ids2order[webapp_user_id]['order_count']
				if int(member_ids2info[member_id]['order_count']) != 0:
					member_ids2info[member_id]['unit_price'] = member_ids2info[member_id]['pay_money']/webapp_user_ids2order[webapp_user_id]['order_count']
				else:
					member_ids2info[member_id]['unit_price'] = 0
				member_ids2info[member_id]['last_pay_time'] = webapp_user_ids2order[webapp_user_id]['last_pay_time']
			else:
				member_ids2info[member_id]['cash'] = 0
				member_ids2info[member_id]['card'] = 0
				member_ids2info[member_id]['pay_money'] = 0
				member_ids2info[member_id]['unit_price'] = 0
				member_ids2info[member_id]['order_count'] = 0
				member_ids2info[member_id]['last_pay_time'] = None
		return {
				'member_ids2info':member_ids2info
				}