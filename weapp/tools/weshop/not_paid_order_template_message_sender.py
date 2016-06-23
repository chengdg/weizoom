# -*- coding: utf-8 -*-
import json
__author__ = 'duhao'

import os
import sys
import logging
import datetime, time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weapp.settings')

from django.core.management import execute_from_command_line
execute_from_command_line(sys.argv)

from core import dateutil
from mall import models as mall_models
from modules.member import models as member_models
from market_tools.tools.template_message import module_api as template_message_api

OWNER_ID = 216
WEBAPP_ID = '3394'
TEMPLATE_ID = '7maasEvSNPagfo1eXsP2pa2rgWDr_Hc_R7vsWYZpyvw'
TEMPLATE_URL = 'http://mall.weizoom.com/mall/order_list/?woid=%d&type=0' % OWNER_ID
FIRST_TEXT = u'亲，您还有订单未支付哦~~~'
REMARK_TEXT = u'\n未付款订单会在下单1小时后自动取消，即将到手的宝贝不要轻易放弃哟！\n点此前去付款'

def get_time_range():
	"""
	获取时间区间，半小时为单位
	"""
	start_time = ''
	end_time = ''

	minute_num = int(time.strftime("%M"))  #当前分钟数
	if minute_num >= 0 and minute_num < 30:
		date = dateutil.get_datetime_before_by_hour(1)  #一小时前的时间
		dt = date.strftime("%Y-%m-%d %H:")
		start_time = dt + '30:00'
		end_time = dt + '59:59'
	else:
		date = datetime.datetime.now()
		dt = date.strftime("%Y-%m-%d %H:")
		start_time = dt + '00:00'
		end_time = dt + '29:59'

	logging.info('start_time:%s, end_time:%s' % (start_time, end_time))
	return start_time, end_time

def get_not_paid_order_infos():
	"""
	获取用户半小时内未支付的订单，如果单个用户有多个未支付订单的话，只获取一个
	"""
	start_time, end_time = get_time_range()
	orders = mall_models.Order.objects.filter(
		webapp_id=WEBAPP_ID,
		status=mall_models.ORDER_STATUS_NOT,
		created_at__range=[start_time, end_time],
		origin_order_id__lte=0
	)
	webapp_user_id2order = {}
	for order in orders:
		webapp_user_id2order[order.webapp_user_id] = order

	member_id2order_id2created_at = {}
	webapp_users = member_models.WebAppUser.objects.filter(id__in=webapp_user_id2order.keys())
	for webapp_user in webapp_users:
		if webapp_user.member_id != 0 and webapp_user.member_id != -1:
			order = webapp_user_id2order[webapp_user.id]
			member_id2order_id2created_at[webapp_user.member_id] = {order.order_id: order.created_at.strftime('%Y-%m-%d %H:%M:%S')}
	
	return member_id2order_id2created_at

def send_message(owner_id, member_id, template_id, template_url, first_text, created_at, order_id, remark_text):
	detail_data = {}
	detail_data["ordertape"] = {"value" : created_at, "color" : "#173177"}
	detail_data["ordeID"] = {"value" : order_id, "color" : "#173177"}
	detail_data["first"] = {"value" : first_text, "color" : "#000000"}
	detail_data["remark"] = {"value" : remark_text, "color" : "#000000"}
	
	template_data = dict()
	template_data['template_id'] = template_id
	template_data['topcolor'] = "#FF0000"
	template_data['url'] = template_url
	template_data['data'] = detail_data

	template_message_api.send_template_message_for_not_paid_order(owner_id, member_id, template_data)


if __name__ == '__main__':
	member_id2order_id2created_at = get_not_paid_order_infos()
	for member_id in member_id2order_id2created_at:
		order_id2created_at = member_id2order_id2created_at[member_id]
		for order_id in order_id2created_at:
			created_at = order_id2created_at[order_id]
			logging.info(u'member_id:%d, order_id:%s, created_at:%s' % (member_id, order_id, created_at))
			send_message(OWNER_ID, member_id, TEMPLATE_ID, TEMPLATE_URL, FIRST_TEXT, created_at, order_id, REMARK_TEXT)

	logging.info('finish!!!')
