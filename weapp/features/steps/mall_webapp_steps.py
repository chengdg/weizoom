# -*- coding: utf-8 -*-
import json
import time
from datetime import datetime, timedelta

from behave import *

from test import bdd_util
from features.testenv.model_factory import *
from tools.regional.models import *

from django.test.client import Client
from webapp.modules.mall.models import *
from mall.promotion.models import *
from modules.member.models import *
import mall_product_steps as product_step_util

def __get_date(str):
	#处理expected中的参数
	today = datetime.now()
	if str == u'今天':
		delta = 0
	elif str == u'昨天':
		delta = -1
	elif str == u'前天':
		delta = -2
	elif str == u'明天':
		delta = 1
	elif str == u'后天':
		delta = 2
	elif u'天后' in str:
		delta = int(str[:-2])
	elif u'天前' in str:
		delta = 0-int(str[:-2])
	else:
		return str

	return today + timedelta(delta)


@then(u"webapp页面标题为'{page_title}'")
def step_impl(context, page_title):
	expected = page_title
	actual = context.page_title

	context.tc.assertEquals(expected, actual)


@when(u"{webapp_user_name}浏览{webapp_owner_name}的webapp的'{category_name}'商品列表页")
def step_impl(context, webapp_user_name, webapp_owner_name, category_name):
	bdd_util.use_webapp_template(webapp_owner_name, 'simple_fashion')
	if category_name == u'全部':
		category_id = 0
	else:
		category = ProductCategoryFactory(name=category_name)
		category_id = category.id

	url = '/workbench/jqm/preview/?woid=%s&module=mall&model=products&action=list&category_id=%d&workspace_id=mall' % (context.webapp_owner_id, category_id)
	response = context.client.get(bdd_util.nginx(url), follow=True)

	context.products = response.context['products']
	context.page_title = response.context['page_title']


@then(u"{webapp_user_name}获得webapp商品列表")
def step_impl(context, webapp_user_name):
	expected = json.loads(context.text)
	actual = context.products
	bdd_util.assert_list(expected, actual)


@when(u"{webapp_user_name}浏览{webapp_owner_name}的webapp的'{product_name}'商品页")
def step_impl(context, webapp_user_name, webapp_owner_name, product_name):
	bdd_util.use_webapp_template(webapp_owner_name, 'simple_fashion')
	product = Product.objects.get(owner_id=context.webapp_owner_id, name=product_name)
	url = '/workbench/jqm/preview/?woid=%s&module=mall&model=product&rid=%d' % (context.webapp_owner_id, product.id)
	response = context.client.get(bdd_util.nginx(url), follow=True)

	context.product = response.context['product']
	context.page_title = response.context['page_title']


@then(u"{webapp_user_name}获得webapp商品")
def step_impl(context, webapp_user_name):
	expected = json.loads(context.text)

	actual = context.product
	actual.stock_type = u'无限' if actual.stock_type == PRODUCT_STOCK_TYPE_UNLIMIT else u'有限'
	actual.shelve_type = u'上架' if actual.shelve_type == PRODUCT_SHELVE_TYPE_ON else u'下架'
	actual.swipe_images = json.loads(actual.swipe_images_json)

	#填充model信息
	actual.model = {'property':{}}
	if actual.is_use_custom_model:
		pass
	else:
		product_models = actual.models
		models = {}
		for product_model in product_models:
			if product_model['name'] == 'standard':
				models['standard'] = {
					"price": product_model['price'],
					"market_price": product_model['market_price'],
					"weight": product_model['weight'],
					"market_price": "" if product_model['market_price'] == 0 else product_model['market_price'],
					"stock_type": u'无限' if product_model['stock_type'] == PRODUCT_STOCK_TYPE_UNLIMIT else u'有限',
					"stocks": product_model['stocks']
				}
		actual.model['models'] = models

	bdd_util.assert_dict(expected, actual)


@then(u"{webapp_user_name}获得待编辑订单")
def step_impl(context, webapp_user_name):
	context_text = json.loads(context.text)
	if context_text == []:
		actual_products = []
		expected_products = []
	else:
		expected_products = context_text['products']
		actual_products = context.response.context['order'].products
		for product in actual_products:
			product.count = product.purchase_count

	bdd_util.assert_list(expected_products, actual_products)


@when(u"{webapp_user_name}购买{webapp_owner_name}的商品")
def step_impl(context, webapp_user_name, webapp_owner_name):
	url = '/webapp/api/project_api/call/'
	if hasattr(context, 'caller_step_purchase_info'):
		args = context.caller_step_purchase_info
	else:
		args = json.loads(context.text)

	def __get_current_promotion_id_for_product(product):
		promotion_ids = [r.promotion_id for r in ProductHasPromotion.objects.filter(product_id=product.id)]
		promotions = Promotion.objects.filter(id__in=promotion_ids, status=PROMOTION_STATUS_STARTED).exclude(type__gt=3)
		if len(promotions) > 0:
			return promotions[0].id
		else:
			return 0
	integral_each_yuan = 10
	settings = IntegralStrategySttings.objects.filter(webapp_id=context.webapp_id)
	if settings.count() > 0:
		integral_each_yuan = settings[0].integral_each_yuan
	member = bdd_util.get_member_for(webapp_user_name, context.webapp_id)
	group2integralinfo = dict()
	if webapp_owner_name == u'订单中':
		is_order_from_shopping_cart = "true"
		webapp_owner_id = context.webapp_owner_id
		product_ids = []
		product_counts = []
		promotion_ids = []
		product_model_names = []
		products = context.response.context['order'].products
		for product in products:
			product_counts.append(str(product.purchase_count))
			product_ids.append(str(product.id))
			if product.has_key('promotion'):
				promotion = Promotion.objects.get(name=product['promotion']['name'])
				promotion_ids.append(str(promotion.id))
			else:
				promotion_ids.append(str(__get_current_promotion_id_for_product(product_obj)))
			product_model_names.append(_get_product_model_ids_from_name(webapp_owner_id, product.model_name))
			# TODO 没有用例
			if hasattr(product, 'integral') and product.integral > 0:
				group2integralinfo['%s_%s' % (product_obj.id, _product_model_name)] = {
					"member_grade_id": member.grade_id,
					"product_model_names": '%s_%s' % (product_obj.id, _product_model_name),
					"integral": product.integral,
					"money": int(product.integral) / integral_each_yuan
					}
	else:
		is_order_from_shopping_cart = "false"
		webapp_owner_id = bdd_util.get_user_id_for(webapp_owner_name)
		product_ids = []
		product_counts = []
		product_model_names = []
		promotion_ids = []
		products = args['products']
		for product in products:
			product_counts.append(str(product['count']))
			product_name = product['name']
			product_obj = Product.objects.get(owner_id=webapp_owner_id, name=product_name)
			product_ids.append(str(product_obj.id))
			if product.has_key('promotion'):
				promotion = Promotion.objects.get(name=product['promotion']['name'])
				promotion_ids.append(str(promotion.id))
			else:
				promotion_ids.append(str(__get_current_promotion_id_for_product(product_obj)))
			_product_model_name = _get_product_model_ids_from_name(webapp_owner_id, product.get('model', None))
			product_model_names.append(_product_model_name)
			if 'integral' in product and product['integral'] > 0:
				group2integralinfo['%s_%s' % (product_obj.id, _product_model_name)] = {
					"member_grade_id": member.grade_id,
					"product_model_names": '%s_%s' % (product_obj.id, _product_model_name),
					"integral": product['integral'],
					"money": int(product['integral']) / integral_each_yuan
					}

	order_type = args.get('type', 'normal')

	# 处理中文地区转化为id，如果数据库不存在的地区则自动添加该地区
	ship_area = args.get('ship_area')
	if ship_area:
		areas = ship_area.split(' ')
	else:
		areas = '北京市 北京市 海淀区'.split(' ')
		#print u'没有邮寄地区'
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
		"promotion_ids": '_'.join(promotion_ids),
		"product_counts": '_'.join(product_counts),
		"product_model_names": '$'.join(product_model_names),
		"ship_name": args.get('ship_name', "未知姓名"),
		"area": ship_area,
		"ship_id": 0,
		"ship_address": args.get('ship_address', "长安大街"),
		"ship_tel": args.get('ship_tel', "11111111111"),
		"is_use_coupon": "false",
		"coupon_id": 0,
		"coupon_coupon_id": "",
		"message": args.get('customer_message', ''),
		"group2integralinfo": json.JSONEncoder().encode(group2integralinfo),
		"card_name": '',
		"card_pass": ''
	}
	if 'integral' in args and args['integral'] > 0:
		# 整单积分抵扣
		# orderIntegralInfo:{"integral":20,"money":"10.00"}"
		orderIntegralInfo = dict()
		orderIntegralInfo['integral'] = args['integral']
		if 'integral_money' in args:
			orderIntegralInfo['money'] = args['integral_money']
		else:
			orderIntegralInfo['money'] = round(int(args['integral'])/integral_each_yuan, 2)
		data["orderIntegralInfo"] = json.JSONEncoder().encode(orderIntegralInfo)
	if order_type == u'测试购买':
		data['order_type'] = PRODUCT_TEST_TYPE
	if u'weizoom_card' in args:
		for card in args[u'weizoom_card']:
			data['card_name'] += card[u'card_name'] + ','
			data['card_pass'] += card[u'card_pass'] + ','

	#填充商品积分
	# for product_model_id, integral in product_integrals:
	# 	data['is_use_integral_%s' % product_model_id] = 'on'
	# 	data['integral_%s' % product_model_id] = integral

	#填充优惠券信息
	coupon_id = args.get('coupon', None)
	if coupon_id:
		data['is_use_coupon'] = 'true'
		data['coupon_id'] = coupon_id

	#填充积分信息
	# integral = args.get('integral', None)
	# if integral:
	# 	data['is_use_integral'] = 'true'
	# 	data['integral'] = integral

	# use_integral = args.get('use_integral', None)
	# if use_integral == u"是":
	# 	data['is_use_integral'] = 'true'
	# 	data['integral'] = get_use_integral(webapp_user_name, context.webapp_id, data)

	# 访问下订单的API
	response = context.client.post(url, data)
	context.response = response
	#response结果为: {"errMsg": "", "code": 200, "data": {"msg": null, "order_id": "20140620180559"}}
	response_json = json.loads(context.response.content)
	if response_json['code'] == 200:
		# context.created_order_id为订单ID
		context.created_order_id = response_json['data']['order_id']
	else:
		context.created_order_id = -1
		context.server_error_msg = response_json['data']['msg']
	if context.created_order_id != -1:
		if 'date' in args:
			Order.objects.filter(order_id=context.created_order_id).update(created_at=__get_date(args['date']))

	context.product_ids = product_ids
	context.product_counts = product_counts
	context.product_model_names = product_model_names
	context.webapp_owner_name = webapp_owner_name

@when(u"微信用户批量消费{webapp_owner_name}的商品")
def step_impl(context, webapp_owner_name):
	for row in context.table:
		webapp_user_name = row['consumer']
		if webapp_user_name[0] == u'-':
			webapp_user_name = webapp_user_name[1:]
			#clear last member's info in cookie and context
			context.execute_steps(u"When 清空浏览器")
		else:
			context.execute_steps(u"When 清空浏览器")
			context.execute_steps(u"When %s访问%s的webapp" % (webapp_user_name, webapp_owner_name))

		#购买商品
		product, count = row['product'].strip().split(',')
		purchase_type = u'测试购买' if row['type'] == u'测试' else None
		data = {
			"date": row['date'].strip(),
			"products": [{
				"name": product,
				"count": count
			}]
		}
		if purchase_type:
			data['type'] = purchase_type
		context.caller_step_purchase_info = data
		context.execute_steps(u"when %s购买%s的商品" % (webapp_user_name, webapp_owner_name))

		#支付订单
		if row['payment'] == u'支付':
			context.execute_steps(u"when %s使用支付方式'货到付款'进行支付" % webapp_user_name)

		#取消订单
		action = row['action'].strip()
		if action:
			actor, operation = action.split(',')
			context.execute_steps(u"given %s登录系统" % actor)
			context.caller_step_cancel_reason = {"reason":"cancel"}
			context.execute_steps(u"When %s取消最新订单" % actor)

		order_id = row.get('order_id', None)
		if order_id:
			latest_order = Order.objects.all().order_by('-id')[0]
			latest_order.order_id = order_id
			latest_order.save()


@when(u"微信用户批量访问{webapp_owner_name}的webapp")
def step_impl(context, webapp_owner_name):
	dates = []
	for row in context.table:
		webapp_user_name = row['user']
		if webapp_user_name[0] == u'-':
			webapp_user_name = webapp_user_name[1:]
			#clear last member's info in cookie and context
			context.execute_steps(u"When 清空浏览器")
			context.execute_steps(u"When %s浏览%s的webapp的'全部'商品列表页" % (webapp_user_name, webapp_owner_name))
		else:
			context.execute_steps(u"When 清空浏览器")
			context.execute_steps(u"When %s访问%s的webapp" % (webapp_user_name, webapp_owner_name))

		from webapp import models as webapp_models
		date = __get_date(row['date']).strftime('%Y-%m-%d')
		latest_log = webapp_models.PageVisitLog.objects.all().order_by('-id')[0]
		latest_log.create_date = date
		latest_log.save()

		dates.append(date)

	#进行统计
	from services.daily_page_visit_statistic_service.tasks import daily_page_visit_statistic_service
	for date in dates:
		print '>>>>>>>>>>>>>>>>>>>'
		print date
		print daily_page_visit_statistic_service
		result = daily_page_visit_statistic_service.delay(None, date)
		print result


# 获取规格ids, 根据名称
def _get_product_model_ids_from_name(webapp_owner_id, model_name):
	if model_name is None or model_name == "standard":
		return "standard"
	return product_step_util.__get_custom_model_id_from_name(webapp_owner_id ,model_name)

# 获取规格名称, 根据ids
def _get_product_model_name_from_ids(webapp_owner_id, ids):
	if ids is None or ids == "standard":
		return "standard"
	return product_step_util.__get_custom_model_name_from_id(webapp_owner_id ,ids)

@then(u"{webapp_user_name}成功创建订单")
def step_impl(context, webapp_user_name):
	order_id = context.created_order_id
	if order_id == -1:
		print 'Server Error: ', json.dumps(json.loads(context.response.content), indent=True)
		assert False, "order_id must NOT be -1"
		return

	order = Order.objects.get(order_id=order_id)

	url = '/workbench/jqm/preview/?woid=%s&module=mall&model=order&action=pay&order_id=%s' % (context.webapp_owner_id, order_id)
	response = context.client.get(bdd_util.nginx(url), follow=True)
	actual_order = response.context['order']
	actual_order.ship_area = actual_order.area
	actual_order.status = ORDERSTATUS2TEXT[actual_order.status]
	#获取coupon规则名
	if (actual_order.coupon_id != 0) and (actual_order.coupon_id != -1):
		coupon = Coupon.objects.get(id=actual_order.coupon_id)
		actual_order.coupon_id = coupon.coupon_rule.name

	for product in actual_order.products:
		# print '---product---', product
		if 'custom_model_properties' in product and product['custom_model_properties']:
			product['model'] = ' '.join([property['property_value'] for property in product['custom_model_properties']])

	# print '---actual_order---', actual_order
	expected = json.loads(context.text)
	bdd_util.assert_dict(expected, actual_order)


@then(u"{webapp_user_name}'{pay_type}'使用支付方式'{pay_interface}'进行支付")
def step_impl(context, webapp_user_name, pay_type, pay_interface):
	if hasattr(context, 'product_ids'):
		product_ids = context.product_ids
		product_counts = context.product_counts
		product_model_names = context.product_model_names
		# 加默认地址
		context.webapp_user.update_ship_info(ship_name='11', ship_address='12', ship_tel='12345678970', area='1')
	else:
		# 获取购物车参数
		product_ids, product_counts, product_model_names = _get_shopping_cart_parameters(context)

	if len(product_ids) == 1:
		url = '/workbench/jqm/preview/?woid=%s&module=mall&model=order&action=edit&product_id=%s&product_count=%s&product_model_name=%s' % (context.webapp_owner_id, product_ids[0], product_counts[0], product_model_names[0])
	else:
		url = '/workbench/jqm/preview/?woid=%s&module=mall&model=shopping_cart_order&action=edit&product_ids=%s&product_counts=%s&product_model_names=%s' % (context.webapp_owner_id, product_ids, product_counts, product_model_names)

	response = context.client.get(bdd_util.nginx(url), follow=True)

	pay_interface_names = [p.get_str_name() for p in response.context['order'].pay_interfaces]
	# print pay_interface_names
	# print pay_type

	if pay_type == u'能':
		context.tc.assertTrue(pay_interface in pay_interface_names)
	else:
		context.tc.assertTrue(pay_interface not in pay_interface_names)


@then(u"{webapp_user_name}获得创建订单失败的信息'{error_msg}'")
def step_impl(context, webapp_user_name, error_msg):
	error_data = json.loads(context.response.content)
	# print error_data
	# print error_msg
	context.tc.assertTrue(200 != error_data['code'])
	response_msg = error_data['data']['msg']
	if response_msg == '':
		response_msg = error_data['data']['detail'][0]['msg']
	context.tc.assertEquals(error_msg, response_msg)


@then(u"{webapp_user_name}获得创建订单失败的信息")
def step_impl(context, webapp_user_name):
	error_data = json.loads(context.response.content)
	expected = json.loads(context.text)
	webapp_owner_id = bdd_util.get_user_id_for(context.webapp_owner_name)
	for detail in expected['detail']:
		product = Product.objects.get(owner_id=webapp_owner_id, name=detail['id'])
		detail['id'] = product.id

	actual = error_data['data']
	context.tc.assertTrue(200 != error_data['code'])
	bdd_util.assert_dict(expected, actual)


@then(u"{webapp_owner_name}能获取订单")
def step_impl(context, webapp_owner_name):
	db_order = Order.objects.all().order_by('-id')[0]
	response = context.client.get('/mall/editor/order/get/?order_id=%d' % db_order.id, follow=True)

	order = response.context['order']

	expected = json.loads(context.text)
	bdd_util.assert_dict(expected, order)


@when(u"{webapp_user_name}加入{webapp_owner_name}的商品到购物车")
def step_impl(context, webapp_user_name, webapp_owner_name):
	#webapp_owner_id = bdd_util.get_user_id_for(webapp_owner_name)
	#context.webapp_owner_id = webapp_owner_id
	webapp_owner_id = context.webapp_owner_id

	products_info = json.loads(context.text)
	for product_info in products_info:
		product_name = product_info['name']
		product_count = product_info.get('count', 1)
		product = Product.objects.get(owner_id=webapp_owner_id, name=product_name)

		if 'model' in product_info:
			for key, value in product_info['model']['models'].items():
				product_model_name = _get_product_model_ids_from_name(webapp_owner_id, key)
				data = {
					"product_id": product.id,
					"count": value['count'],
					"product_model_name": product_model_name,
					"webapp_owner_id": webapp_owner_id,
					"module": 'mall',
					"target_api": "shopping_cart/add",
					"timestamp": '1404469450205'
				}

				response = context.client.post('/webapp/api/project_api/call/', data)
				bdd_util.assert_api_call_success(response)
		else:
			data = {
				"product_id": product.id,
				"count": product_count,
				"webapp_owner_id": webapp_owner_id,
				"module": 'mall',
				"target_api": "shopping_cart/add",
				"timestamp": '1404469450205'
			}

			response = context.client.post('/webapp/api/project_api/call/', data)
			bdd_util.assert_api_call_success(response)


@then(u"{webapp_user_name}能获得购物车")
def step_impl(context, webapp_user_name):
	url = '/workbench/jqm/preview/?woid=%d&module=mall&model=shopping_cart&action=show' % context.webapp_owner_id
	response = context.client.get(bdd_util.nginx(url), follow=True)
	product_groups = response.context['product_groups']
	invalid_products = response.context['invalid_products']

	def fill_products_model(products):
		for product in products:
			model = []
			if hasattr(product, 'custom_model_properties') and product.custom_model_properties:
				for property in product.custom_model_properties:
					model.append('%s' % (property['property_value']))
			product.model = ' '.join(model)
	fill_products_model(invalid_products)
	for product_group in product_groups:
		from copy import copy
		promotion = None
		promotion = product_group['promotion']
		products = product_group['products']
		if not promotion:
			product_group['promotion'] = None
		elif not product_group['can_use_promotion']:
			product_group['promotion'] = None
		else:
			#由于相同promotion产生的不同product group携带着同一个promotion对象，所以这里要通过copy来进行写时复制
			new_promotion = copy(promotion)
			product_group['promotion'] = new_promotion
			new_promotion['type'] = product_group['promotion_type']
			new_promotion['result'] = product_group['promotion_result']
			if new_promotion['type'] == 'flash_sale':
				products[0].price = new_promotion['detail']['promotion_price']
			if new_promotion['type'] == 'premium_sale':
				new_promotion['result'] = product_group['promotion']['detail']

		fill_products_model(product_group['products'])

	actual = {
		'product_groups': product_groups,
		'invalid_products': invalid_products
	}

	expected = json.loads(context.text)
	bdd_util.assert_dict(expected, actual)


@when(u"{webapp_user_name}从购物车中删除商品")
def step_impl(context, webapp_user_name):
	product_names = json.loads(context.text)
	product_ids = []
	for product_name in product_names:
		product = Product.objects.get(owner_id=context.webapp_owner_id, name=product_name)
		product_ids.append(product.id)

	#忽略model的处理，所以feature中要保证购物车中不包含同一个商品的不同规格
	shopping_cart_item_ids = [str(item.id) for item in ShoppingCart.objects.filter(webapp_user_id=context.webapp_user.id, product_id__in=product_ids)]
	#product = Product.objects.get(owner_id=context.webapp_owner_id, name=product_name)
	data = {
		"shopping_cart_item_ids": ','.join(shopping_cart_item_ids),
		"webapp_owner_id": context.webapp_owner_id,
		"module": 'mall',
		"target_api": "shopping_cart/delete",
		"timestamp": '1404469450205'
	}

	response = context.client.post('/webapp/api/project_api/call/', data)
	response_data = json.loads(response.content)
	context.tc.assertEquals(200, response_data['code'])


@when(u"{webapp_user_name}编辑购物车中商品信息")
def step_impl(context, webapp_user_name):
	product_infos = json.loads(context.text)
	api_data = {}
	for product_info in product_infos:
		product_name = product_info['name']
		product = Product.objects.get(name= product_info['name'])
		item = ShoppingCart.objects.get(webapp_user_id=context.webapp_user.id, product = product)
		api_data[item.id] = product_info['count']

	data = {
		"update_info": json.dumps(api_data),
		"webapp_owner_id": context.webapp_owner_id,
		"module": 'mall',
		"target_api": "shopping_cart/update",
		"timestamp": '1404469450205'
	}

	response = context.client.post('/webapp/api/project_api/call/', data)
	response_data = json.loads(response.content)
	context.tc.assertEquals(200, response_data['code'])


@when(u"{webapp_user_name}从购物车中清空无效商品")
def step_impl(context, webapp_user_name):
	invalid_shopping_cart_item_ids = [str(product.shopping_cart_id) for product in context.products['invalid_products']]

	data = {
		"shopping_cart_item_ids": ','.join(invalid_shopping_cart_item_ids),
		"webapp_owner_id": context.webapp_owner_id,
		"module": 'mall',
		"target_api": "shopping_cart_invalid_products/clear",
		"timestamp": '1404469450205'
	}

	response = context.client.post('/webapp/api/project_api/call/', data)
	response_data = json.loads(response.content)
	context.tc.assertEquals(200, response_data['code'])


@when(u"{webapp_user_name}从购物车发起购买操作")
def step_impl(context, webapp_user_name):
	# 获取购物车参数
	product_ids, product_counts, product_model_names = _get_shopping_cart_parameters(context)

	# 加默认地址
	#context.webapp_user.update_ship_info(ship_name='11', ship_address='12', ship_tel='12345678970', area='1')

	url = '/workbench/jqm/preview/?woid=%s&module=mall&model=shopping_cart_order&action=edit&product_ids=%s&product_counts=%s&product_model_names=%s' % (context.webapp_owner_id, product_ids, product_counts, product_model_names)
	response = context.client.get(bdd_util.nginx(url), follow=True)
	context.response = response

def _get_shopping_cart_parameters(context):
	shopping_cart_items = ShoppingCart.objects.filter(webapp_user_id=context.webapp_user.id)
	if context.text is not None:
		product_infos = json.loads(context.text)
		product_ids = []
		product_counts = []
		product_model_names = []
		for product_info in product_infos:
			product_name = product_info['name']
			product_model_name = product_info.get('model', 'standard')
			try:
				product = Product.objects.get(name= product_info['name'])
				cart = shopping_cart_items.get(product = product, product_model_name=product_model_name)
				product_ids.append(str(cart.product.id))
				product_counts.append(str(cart.count))
				product_model_names.append(cart.product_model_name)
			except:
				pass
	else:
		shopping_cart_items = list(shopping_cart_items)
		product_ids = [str(item.product_id) for item in shopping_cart_items]
		product_counts = [str(item.count) for item in shopping_cart_items]
		product_model_names = [item.product_model_name for item in shopping_cart_items]

	product_ids = '_'.join(product_ids)
	product_counts = '_'.join(product_counts)
	product_model_names = '$'.join(product_model_names)
	return product_ids, product_counts, product_model_names


@when(u"{webapp_user_name}设置{webapp_owner_name}的webapp的默认收货地址")
def step_impl(context, webapp_user_name, webapp_owner_name):
	data = {
		'area': '1_1_8',
		'ship_address': '泰兴大厦',
		'ship_name': webapp_user_name,
		'ship_tel': '13811223344'
	}

	#from modules.member.models import ShipInfo
	#ship_info = ShipInfo.objects.get(webapp_user_id=context.webapp_user.id)
	url = '/workbench/jqm/preview/?woid=%s&module=user_center&model=ship_info&action=save' % (context.webapp_owner_id)
	response = context.client.post(bdd_util.nginx(url), data, follow=True)


def __get_address_id(areas):
	areas = areas.split(' ')
	province = Province.objects.get(name=areas[0])
	city = City.objects.get(name=areas[1])
	district = District.objects.get(name=areas[2])
	return '%d_%d_%d' % (province.id, city.id, district.id)

@when(u"{webapp_user_name}设置{webapp_owner_name}的webapp的收货地址")
def step_impl(context, webapp_user_name, webapp_owner_name):
	ship_info = json.loads(context.text)
	data = {
		'area': __get_address_id(ship_info['area']),
		'ship_address': ship_info.get('ship_address', '泰兴大厦'),
		'ship_name': ship_info.get('ship_name', webapp_user_name),
		'ship_tel': ship_info.get('ship_tel', '13811223344')
	}

	#from modules.member.models import ShipInfo
	#ship_info = ShipInfo.objects.get(webapp_user_id=context.webapp_user.id)
	url = '/workbench/jqm/preview/?woid=%s&module=user_center&model=ship_info&action=save' % (context.webapp_owner_id)
	response = context.client.post(bdd_util.nginx(url), data)
	print response


# def get_use_integral(webapp_user_name, webapp_id, data):
# 	member = bdd_util.get_member_for(webapp_user_name, webapp_id)
# 	product = Product.objects.get(id=data['product_ids'])
# 	product.fill_standard_model()
# 	totel = int(product.price * float(data['product_counts']))

# 	coupon_id = data.get('coupon_id', None)
# 	if coupon_id:
# 		coupon = Coupon.objects.get(id=coupon_id)
# 		totel = totel - coupon.money

# 	try:
# 		grade = MemberGrade.objects.get(id=member.grade_id)
# 		usable_integral_percentage_in_order = grade.usable_integral_percentage_in_order
# 		# 加运费
# 		pro_id = data.get('area','').split('_')[0]
# 		ps = PostageConfigSpecialHasProvince.objects.filter(province_id=pro_id)
# 		weight_price = 0
# 		if ps.count() > 0:
# 			weight_price = ps[0].postage_config_special.first_weight_price

# 		totel = totel + weight_price

# 		totel = float(totel) * float(usable_integral_percentage_in_order)/float(100)
# 	except:
# 		pass

# 	# 一元等价积分
# 	integral_each_yuan = 10
# 	settings = IntegralStrategySttings.objects.filter(webapp_id=webapp_id)
# 	if settings.count() > 0:
# 		integral_each_yuan = settings[0].integral_each_yuan

# 	totel = int(totel * integral_each_yuan)
# 	if member.integral > totel:
# 		return totel
# 	else:
# 		return member.integral
