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
TEMPLATE_ID = 'b24zJJ8jDnvSQom-VdxQCHCev9KQZxAJscfhquqBHlg'
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
	oids = []
	for order in orders:
		oids.append(order.id)
		webapp_user_id2order[order.webapp_user_id] = order

	order_id2product_name = {}
	order2products = mall_models.OrderHasProduct.objects.filter(order_id__in=oids)
	for order2product in order2products:
		order_id2product_name[order2product.order.order_id] = order2product.product.name

	member_id2order_id2info = {}
	webapp_users = member_models.WebAppUser.objects.filter(id__in=webapp_user_id2order.keys())
	for webapp_user in webapp_users:
		if webapp_user.member_id != 0 and webapp_user.member_id != -1:
			order = webapp_user_id2order[webapp_user.id]
			order_id2info = {
				order.order_id: {
					'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
					'price': '%.2f' % order.final_price,
					'product_name': order_id2product_name[order.order_id]
				}
			}
			member_id2order_id2info[webapp_user.member_id] = order_id2info
	
	return member_id2order_id2info

def send_message(owner_id, member_id, template_id, template_url, first_text, created_at, order_id, product_name, price, remark_text):
	detail_data = {}
	detail_data["type"] = {"value" : u'商品', "color" : "#000000"}
	detail_data["e_title"] = {"value" : product_name, "color" : "#173177"}
	detail_data["order_date"] = {"value" : created_at, "color" : "#173177"}
	detail_data["o_id"] = {"value" : order_id, "color" : "#173177"}
	detail_data["o_money"] = {"value" : price, "color" : "#173177"}
	detail_data["first"] = {"value" : first_text, "color" : "#000000"}
	detail_data["remark"] = {"value" : remark_text, "color" : "#000000"}
	
	template_data = dict()
	template_data['template_id'] = template_id
	template_data['topcolor'] = "#FF0000"
	template_data['url'] = template_url
	template_data['data'] = detail_data

	template_message_api.send_template_message_for_not_paid_order(owner_id, member_id, template_data)


if __name__ == '__main__':
	member_id2order_id2info = get_not_paid_order_infos()
	for member_id in member_id2order_id2info:
		order_id2info = member_id2order_id2info[member_id]
		for order_id in order_id2info:
			info = order_id2info[order_id]
			created_at = info['created_at']
			price = info['price']
			product_name = info['product_name']

			logging.info(u'member_id:%d, order_id:%s, created_at:%s, product_name:%s, price:%s' % (member_id, order_id, created_at, product_name, price))
			send_message(OWNER_ID, member_id, TEMPLATE_ID, TEMPLATE_URL, FIRST_TEXT, created_at, order_id, product_name, price, REMARK_TEXT)

	logging.info('finish!!!')
