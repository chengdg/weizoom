# -*- coding: utf-8 -*-
import os
import json
import time
from datetime import datetime, timedelta

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from mall.models import *
from modules.member.models import Member
from tools.regional.models import *
from mall.promotion.models import Coupon

@when(u'{webapp_owner_name}给会员{webapp_user_name}"{action}"测试权限')
def step_impl(context, webapp_owner_name, webapp_user_name, action):	
	if hasattr(context, 'client'):
		context.client.logout()
	context.client = bdd_util.login(webapp_owner_name)
	webapp_id = bdd_util.get_webapp_id_for(webapp_owner_name)
	member = bdd_util.get_member_for(webapp_user_name, webapp_id)
	context.client.request_member = member

	member_json = dict()
	member_json['member_id'] = member.id
	member_json['is_for_buy_test'] = 1
	member_json['grade_id'] = member.grade_id
	member_json['integral'] = member.integral
	member_json['sex'] = 0

	if action == u'分配':
		url = u'/webapp/user_center/api/member/update/'
		response = context.client.post(bdd_util.nginx(url), member_json)


@then(u"{webapp_user_name}获取测试权限")
def step_impl(context, webapp_user_name):
	member = context.client.request_member
	url = '/webapp/user_center/member/{}/'.format(member.id)
	response = context.client.get(bdd_util.nginx(url))
	member = response.context['show_member']

	expected_member = json.loads(context.text)

	actual_member = dict()
	if member.is_for_buy_test:
		actual_member['test_whether_permission'] = u"是"
	else:
		actual_member['test_whether_permission'] = u"否"
		
	bdd_util.assert_dict(expected_member, actual_member)


@when(u"{webapp_user_name}'{order_type}'{webapp_owner_name}的'{product_name}'")
def step_impl(context, webapp_user_name, order_type, webapp_owner_name, product_name):
	url = '/webapp/api/project_api/call/'
	args = {	
		"products": [{
			"name": product_name,
			"count": 1
		}],
		"customer_message": "bill的订单备注1"
	}

	is_order_from_shopping_cart = "false"
	webapp_owner_id = bdd_util.get_user_id_for(webapp_owner_name)	
	product_ids = []
	product_counts = []
	product_model_names = []
	products = args['products']
	for product in products:
		product_counts.append(str(product['count']))
		product_name = product['name']
		product_obj = Product.objects.get(owner_id=webapp_owner_id, name=product_name)
		product_ids.append(str(product_obj.id))

		product_model_names.append("standard")

	# 处理中文地区转化为id，如果数据库不存在的地区则自动添加该地区
	ship_area = args.get('ship_area')
	if ship_area:
		areas = ship_area.split(' ')
	else:
		areas = '北京市 北京市 海淀区'.split(' ')

	if len(areas) > 0:
		pros = Province.objects.filter(
			name = areas[0]
		)
		pro_count = pros.count()
		if pro_count == 0:
			province = Province.objects.create(
				name = areas[0]
			)
			pro_id = province.id
		else:
			pro_id = pros[0].id
		ship_area = str(pro_id)
	if len(areas) > 1:
		cities = City.objects.filter(
			name = areas[1]
		)
		city_count = cities.count()
		if city_count == 0:
			city = City.objects.create(
				name=areas[1],
				zip_code = '',
				province_id = pro_id
			)
			city_id = city.id
		else:
			city_id = cities[0].id
		ship_area = ship_area + '_' + str(city_id)
	if len(areas) > 2:
		dis = District.objects.filter(
			name = areas[2]
		)
		dis_count = dis.count()
		if dis_count == 0:
			district = District.objects.create(
				name = areas[2],
				city_id = city_id
			)
			ship_area = ship_area + '_' + str(district.id)
		else:
			ship_area = ship_area + '_' + str(dis[0].id)
	
	data = {
		"woid": webapp_owner_id,
		"module": 'mall',
		"is_order_from_shopping_cart": is_order_from_shopping_cart,
		"target_api": "order/save",
		"product_ids": '_'.join(product_ids),
		"product_counts": '_'.join(product_counts),
		"product_model_names": '$'.join(product_model_names),
		"ship_name": args.get('ship_name', "未知姓名"),
		"area": ship_area,
		"ship_id": 0,
		"ship_address": args.get('ship_address', "长安大街"),
		"ship_tel": args.get('ship_tel', "11111111111"),
		"integral": "",
		"is_use_coupon": "false",
		"coupon_id": 0,
		"coupon_coupon_id": "",
		"message": args.get('customer_message', '')
	}

	if order_type == u'测试购买':
		data['order_type'] = PRODUCT_TEST_TYPE

	#填充优惠券信息
	coupon_id = args.get('coupon', None)
	if coupon_id:
		data['is_use_coupon'] = 'true'
		if args['coupon_type'] == u'选择':
			coupon = Coupon.objects.get(coupon_id=coupon_id)
			data['coupon_id'] = coupon.id
		elif args['coupon_type'] == u'输入':
			data['coupon_coupon_id'] = coupon_id

	#填充积分信息
	integral = args.get('integral', None)
	if integral:
		data['is_use_integral'] = 'true'
		data['integral'] = integral

	response = context.client.post(url, data)
	context.response = response
	#response结果为: {"errMsg": "", "code": 200, "data": {"msg": null, "order_id": "20140620180559"}}
	response_json = json.loads(context.response.content)
	if response_json['code'] == 200:
		context.created_order_id = response_json['data']['order_id']
	else:
		context.created_order_id = -1

	context.webapp_owner_name = webapp_owner_name


@then(u"{webapp_owner_name}生成{order_type}")
def step_impl(context, webapp_owner_name, order_type):
	if order_type == u'测试订单':
		type = PRODUCT_DEFAULT_TYPE
	else:
		type = PRODUCT_TEST_TYPE

	order_id = context.created_order_id

	order = Order.objects.get(order_id=order_id)

	url = '/workbench/jqm/preview/?woid=%s&module=mall&model=order&action=pay&order_id=%s' % (context.webapp_owner_id, order_id)
	response = context.client.get(bdd_util.nginx(url), follow=True)
	actual_order = response.context['order']
	# actual_order.ship_area = actual_order.area
	actual_order.order_status = ORDERSTATUS2TEXT[actual_order.status]
	actual_order.order_type = ORDER_TYPE2TEXT[actual_order.type]
	actual_order.price = str(actual_order.final_price)

	#获取order的products
	actual_order.products = []
	for relation in OrderHasProduct.objects.filter(order=order):
		product = relation.product
		actual_order.name = product.name

	expected = json.loads(context.text)

	bdd_util.assert_dict(expected, actual_order)