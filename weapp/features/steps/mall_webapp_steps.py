# -*- coding: utf-8 -*-
import json
import requests
from urllib import unquote
from datetime import datetime, timedelta

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from mall.models import *
from mall.promotion.models import *
from modules.member.models import *
import mall_product_steps as product_step_util
from .steps_db_util import (
    get_custom_model_id_from_name, get_product_model_keys, get_area_ids
)

PAYNAME2ID = {
    u'全部': -1,
    u'微信支付': 2,
    u'货到付款': 9,
    u'支付宝': 0,
    u'优惠抵扣': 10
}

# jz 2015-09-02
# def __get_date(str):
# 	#处理expected中的参数
# 	today = datetime.now()
# 	if str == u'今天':
# 		delta = 0
# 	elif str == u'昨天':
# 		delta = -1
# 	elif str == u'前天':
# 		delta = -2
# 	elif str == u'明天':
# 		delta = 1
# 	elif str == u'后天':
# 		delta = 2
# 	elif u'天后' in str:
# 		delta = int(str[:-2])
# 	elif u'天前' in str:
# 		delta = 0-int(str[:-2])
# 	else:
# 		return str

# 	return today + timedelta(delta)


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
	if context.table:
		expected = []
		for promotion in context.table:
			promotion = promotion.as_dict()
			expected.append(promotion)
	else:
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

@when(u"{webapp_user_name}把{webapp_owner_name}的'{product_name_one}'链接的商品ID修改成'{product_name_two}'的商品ID")
def step_impl(context, webapp_user_name, webapp_owner_name, product_name_one,product_name_two):
	bdd_util.use_webapp_template(webapp_owner_name, 'simple_fashion')
	product_two = Product.objects.get(owner_id=context.webapp_owner_id, name=product_name_two)
	url = '/workbench/jqm/preview/?woid=%s&module=mall&model=product&rid=%d' % (context.webapp_owner_id, product_two.id)
	context.url = url

@when(u"{webapp_user_name}把{webapp_owner_name}的'{product_name_one}'链接的商品ID修改成{webapp_owner_name_other}的'{product_name_two}'的商品ID")
def step_impl(context, webapp_user_name, webapp_owner_name, product_name_one,webapp_owner_name_other,product_name_two):
	user_other = User.objects.get(username=webapp_owner_name_other).id
	product_two = Product.objects.get(owner_id=user_other, name=product_name_two)
	url = '/termite/workbench/jqm/preview/?woid=%s&module=mall&model=product&rid=%d' % (context.webapp_owner_id, product_two.id)
	context.url = url


@when(u"{webapp_user_name}访问修改后的链接")
def step_impl(context,webapp_user_name):
	if hasattr(context,'url'):
		response = context.client.get(bdd_util.nginx(context.url), follow=True)
		try:
			context.product = response.context['product']
			context.page_title = response.context['page_title']
		except:
			context.server_error_msg = u'404页面'


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


# jz 2015-09-02
# @then(u"{webapp_user_name}获得待编辑订单")
# def step_impl(context, webapp_user_name):
# 	"""
# 		e.g.:
# 		[{'name': "asdfasdfa",
# 		  'count': "111"
# 		},{...}]
# 	"""
# 	context_text = json.loads(context.text)
# 	if context_text == []:
# 		actual = []
# 		expected_products = []
# 	else:
# 		actual = []
# 		expected_products = context_text['products']
# 		product_groups = context.response.context['product_groups']
# 		for i in product_groups:
# 			for product in i['products']:
# 				_a = {}
# 				_a['name'] = product.name
# 				_a['count'] = product.count
# 				actual.append(_a)
#
# 	bdd_util.assert_list(expected_products, actual)



@when(u"{webapp_user_name}购买{webapp_owner_name}的商品")
def step_impl(context, webapp_user_name, webapp_owner_name):
	"""最近修改: duhao 20160401
	weapp中一些BDD仍然需要购买相关的测试场景，在这里调用apiserver的接口实现购买操作
	e.g.:
		{
			"order_id": "" # 订单号
			"ship_area": "",
			"ship_name": "bill",
			"ship_address": "",
			"ship_tel": "",
			"customer_message": "",
			"integral": "10",
			"integral_money": "10",
			"weizoom_card": [{"card_name":"", "card_pass": ""}],
			"coupon": "coupon_1",
			"date": "" # 下单时间
			"products": [
				{
					"count": "",
					"name": "",
					"promotion": {"name": ""},
					integral: ""
				},...
			]
		}
	"""
	if hasattr(context, 'caller_step_purchase_info') and context.caller_step_purchase_info:
		args = context.caller_step_purchase_info
	else:
		args = json.loads(context.text)

	def __get_current_promotion_id_for_product(product, member_grade_id):
		promotion_ids = [r.promotion_id for r in ProductHasPromotion.objects.filter(product_id=product.id)]
		promotions = Promotion.objects.filter(id__in=promotion_ids, status=PROMOTION_STATUS_STARTED).exclude(type__gt=3)
		if len(promotions) > 0 and (promotions[0].member_grade_id <= 0 or \
				promotions[0].member_grade_id == member_grade_id):
			# 存在促销信息，且促销设置等级对该会员开放
			if promotions[0].type != PROMOTION_TYPE_INTEGRAL_SALE:
				return promotions[0].id
		return 0

	settings = IntegralStrategySttings.objects.filter(webapp_id=context.webapp_id)
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
		integral = 0
		integral_group_items = []
		for product in products:
			product_counts.append(str(product.purchase_count))
			product_ids.append(str(product.id))

			if hasattr(product, 'promotion'):
				promotion = Promotion.objects.get(name=product.promotion.name)
				promotion_ids.append(str(promotion.id))
			else:
				promotion_ids.append(str(__get_current_promotion_id_for_product(product_obj, member.grade_id)))
			product_model_names.append(_get_product_model_ids_from_name(webapp_owner_id, product.model_name))

			if hasattr(product, 'integral') and product.integral > 0:
				integral += product.integral
				integral_group_items.append('%s_%s' % (product.id, product.model['name']))
		if integral:
			group2integralinfo['-'.join(integral_group_items)] = {
				"integral": integral,
				"money": round(integral / integral_each_yuan, 2)
			}
	else:
		is_order_from_shopping_cart = "false"
		webapp_owner_id = bdd_util.get_user_id_for(webapp_owner_name)
		product_ids = []
		product_counts = []
		product_model_names = []
		promotion_ids = []
		products = args['products']
		# integral = 0
		# integral_group_items = []
		for product in products:
			product_counts.append(str(product['count']))
			product_name = product['name']
			product_obj = Product.objects.get(owner_id=webapp_owner_id, name=product_name)
			product_ids.append(str(product_obj.id))
			if product.has_key('promotion'):
				promotion = Promotion.objects.get(name=product['promotion']['name'])
				promotion_ids.append(str(promotion.id))
			else:
				promotion_ids.append(str(__get_current_promotion_id_for_product(product_obj, member.grade_id)))
			_product_model_name = _get_product_model_ids_from_name(webapp_owner_id, product.get('model', None))
			product_model_names.append(_product_model_name)
			if 'integral' in product and product['integral'] > 0:
				# integral += product['integral']
				# integral_group_items.append('%s_%s' % (product_obj.id, _product_model_name))
				group2integralinfo['%s_%s' % (product_obj.id, _product_model_name)] = {
					"integral": product['integral'],
					"money": round(product['integral'] / integral_each_yuan, 2)
				}
		# if integral:
		# 	group2integralinfo['-'.join(integral_group_items)] = {
		# 		"integral": integral,
		# 		"money": round(integral / integral_each_yuan, 2)
		# 	}

	order_type = args.get('type', 'object')

	# 处理中文地区转化为id，如果数据库不存在的地区则自动添加该地区
	ship_area = get_area_ids(args.get('ship_area'))

	data = {
		"webapp_user_name": webapp_user_name,
		"webapp_owner_name": webapp_owner_name,  #参数中携带webapp_user_name和webapp_owner_name，方便apiserver处理
		"woid": webapp_owner_id,
		"is_order_from_shopping_cart": is_order_from_shopping_cart,
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
		# "coupon_coupon_id": "",
		"message": args.get('customer_message', ''),
		"group2integralinfo": json.JSONEncoder().encode(group2integralinfo),
		"card_name": '',
		"card_pass": '',
		"xa-choseInterfaces": PAYNAME2ID.get(args.get("pay_type",u"微信支付"),-1)
	}

	if 'product_integral' in args and args['product_integral'] > 0:
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
	else:
		data['order_type'] = order_type
	if u'weizoom_card' in args:
		for card in args[u'weizoom_card']:
			data['card_name'] += card[u'card_name'] + ','
			data['card_pass'] += card[u'card_pass'] + ','

	#填充商品积分
	# for product_model_id, integral in product_integrals:
	# 	data['is_use_integral_%s' % product_model_id] = 'on'
	# 	data['integral_%s' % product_model_id] = integral

	#填充优惠券信息
	# 根据优惠券规则名称填充优惠券ID
	coupon = args.get('coupon', None)
	if coupon:
		data['is_use_coupon'] = 'true'
		data['coupon_id'] = coupon

	access_token = bdd_util.get_access_token(member.id, webapp_owner_id)
	openid = bdd_util.get_openid(member.id, webapp_owner_id)

	url = 'http://api.weapp.com/wapi/mall/order/?_method=put'
	data['access_token'] = access_token
	data['openid'] = openid
	data['woid'] = webapp_owner_id
	response = requests.post(url, data=data)
	#response结果为: {"errMsg": "", "code": 200, "data": {"msg": null, "order_id": "20140620180559"}}

	response_json = json.loads(response.text)
	context.response = response_json

	# raise '----------------debug test----------------------'
	if response_json['code'] == 200:
		# context.created_order_id为订单ID
		context.created_order_id = response_json['data']['order_id']

		#访问支付结果链接
		pay_url_info = response_json['data']['pay_url_info']
		pay_type = pay_url_info['type']
		del pay_url_info['type']
		# if pay_type == 'cod':
		# 	pay_url = 'http://api.weapp.com/wapi/pay/pay_result/?_method=put'
		# 	data = {
		# 		'pay_interface_type': pay_url_info['pay_interface_type'],
		# 		'order_id': pay_url_info['order_id'],
		# 		'access_token': access_token
		# 	}
		# 	pay_response = requests.post(url, data=data)
		# 	pay_response_json = json.loads(pay_response.text)

		#同步更新支付时间
		if Order.objects.get(order_id=context.created_order_id).status > ORDER_STATUS_CANCEL and args.has_key('payment_time'):
			Order.objects.filter(order_id=context.created_order_id).update(payment_time=bdd_util.get_datetime_str(args['payment_time']))
	else:
		context.created_order_id = -1
		context.response_json = response_json
		context.server_error_msg = response_json['innerErrMsg']
		print("buy_error----------------------------",context.server_error_msg,response)
	if context.created_order_id != -1:
		if 'date' in args:
			Order.objects.filter(order_id=context.created_order_id).update(created_at=bdd_util.get_datetime_str(args['date']))
		if 'order_id' in args:
			db_order = Order.objects.get(order_id=context.created_order_id)
			db_order.order_id=args['order_id']
			db_order.save()
			if db_order.origin_order_id <0:
				for order in Order.objects.filter(origin_order_id=db_order.id):
					order.order_id = '%s^%s' % (args['order_id'], order.supplier)
					order.save()
			context.created_order_id = args['order_id']

	context.product_ids = product_ids
	context.product_counts = product_counts
	context.product_model_names = product_model_names
	context.webapp_owner_name = webapp_owner_name

OPERATION2STEPID = {
	u'支付': u"When %s'支付'最新订单",
	u'发货': u"When %s对最新订单进行发货",
	u'完成': u"When %s'完成'最新订单",
	u'退款': u"When %s'退款'最新订单",
	u'完成退款': u"When %s'完成退款'最新订单",
	u'取消': u"When %s'取消'最新订单",
}

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
		product_infos = row['product'].strip().split(',')
		model = None
		if len(product_infos) == 2:
			product, count = product_infos
		elif len(product_infos) == 3:
			product, model, count = product_infos
		data = {
			"date": row['date'].strip(),
			"products": [{	
				"name": product,
				"count": count,
				"model": model
			}]
		}
		if hasattr(context, 'ship_address'):
			data.update(context.ship_address)

		# TODO 统计BDD使用，需要删掉
		# purchase_type = u'测试购买' if row['type'] == u'测试' else None
		# if purchase_type:
		# 	data['type'] = purchase_type
		# TODO 统计BDD使用，需要删掉
		# data['ship_name'] = webapp_user_name
		if row.get('product_integral', None):
			tmp = 0
			try:
				tmp = int(row['product_integral'])
			except:
				pass

			# if tmp > 0:
			if tmp > 0 and row.get('integral', None):  #duhao 20150929 消费积分不能依赖于现获取积分,让integral列可以不填
				# 先为会员赋予积分,再使用积分
				# TODO 修改成jobs修改bill积分
				context.execute_steps(u"When %s获得%s的%s会员积分" % (webapp_user_name, webapp_owner_name, row['integral']))
			# data['products'][0]['integral'] = tmp  #duhao 20160405注释掉，改用product_integral，用来区分整单抵扣积分和积分应用抵扣积分
			data['products'][0]['product_integral'] = tmp

		if row.get('coupon', '') != '':
			if ',' in row['coupon']:
				coupon_name, coupon_id = row['coupon'].strip().split(',')
				coupon_dict = {}
				coupon_dict['name'] = coupon_name
				coupon_dict['coupon_ids'] = [ coupon_id ]
				coupon_list = [ coupon_dict ]
				context.coupon_list = coupon_list
				context.execute_steps(u"when %s领取%s的优惠券" % (webapp_user_name, webapp_owner_name))
			else:
				coupon_id = row['coupon'].strip()
			data['coupon'] = coupon_id

		if row.get('weizoom_card', None) and ',' in row['weizoom_card']:
			card_name, card_pass = row['weizoom_card'].strip().split(',')
			card_dict = {}
			card_dict['card_name'] = card_name
			card_dict['card_pass'] = card_pass
			data['weizoom_card'] = [ card_dict ]

		if row.get('integral', '') != '':
			data['integral'] = int(row.get('integral'))
		if row.get('date') != '':
			data['date'] = row.get('date')
		if row.get('order_id', '') != '':
			data['order_id'] = row.get('order_id')


		if row.get('pay_type', '') != '':
			data['pay_type'] = row.get('pay_type')


		print("SUB STEP: to buy products, param: {}".format(data))
		context.caller_step_purchase_info = data
		context.execute_steps(u"when %s购买%s的商品" % (webapp_user_name, webapp_owner_name))
		order = Order.objects.all().order_by('-id')[0]
		#支付订单

		if row.get('payment_time', '') != '' or row.get('payment', '') == u'支付':
			pay_type = row.get('pay_type', u'货到付款')
			if pay_type != '' != u'优惠抵扣':
				if 'order_id' in data:
					context.created_order_id = data['order_id']
				context.execute_steps(u"when %s使用支付方式'%s'进行支付" % (webapp_user_name, pay_type))
			if row.get('payment_time', '') != '':
				Order.objects.filter(id=order.id).update(
					payment_time=bdd_util.get_datetime_str(row['payment_time']))

		# 操作订单
		action = row['action'].strip()
		if action:
			actor, operation = action.split(',')
			context.execute_steps(u"given %s登录系统" % actor)
			if row.get('delivery_time') or operation == u'完成':
				step_id = OPERATION2STEPID.get(u'发货', None)
				context.latest_order_id = order.id
				context.execute_steps(step_id % actor)
			if row.get('delivery_time'):
				log = OrderOperationLog.objects.filter(
				order_id=order.order_id, action='订单发货').get()
				log.created_at =  bdd_util.get_date(row.get('delivery_time'))
				log.save()
			# if operation == u'取消' or operation == u'退款' or operation == u'完成退款':
			if operation == u'完成退款':  # 完成退款的前提是要进行退款操作
				step_id = OPERATION2STEPID.get(u'发货', None)
				context.latest_order_id = order.id
				context.execute_steps(step_id % actor)

				step_id = OPERATION2STEPID.get(u'完成', None)
				context.latest_order_id = order.id
				context.execute_steps(step_id % actor)
				step_id = OPERATION2STEPID.get(u'退款', None)
				context.latest_order_id = order.id
				context.execute_steps(step_id % actor)
			# if operation == u'退款':  # 完成退款的前提是要进行发货和完成操作
			# 	step_id = OPERATION2STEPID.get(u'发货', None)
			# 	context.latest_order_id = order.id
			# 	context.execute_steps(step_id % actor)

			# 	step_id = OPERATION2STEPID.get(u'完成', None)
			# 	context.latest_order_id = order.id
			# 	context.execute_steps(step_id % actor)

			step_id = OPERATION2STEPID.get(operation, None)
			if step_id:
				context.latest_order_id = order.id
				context.execute_steps(step_id % actor)
			elif operation == u'无操作':
				# 为了兼容之前默认为取消操作所做的处理
				pass
			else:
				raise
	context.caller_step_purchase_info = None


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
		date = bdd_util.get_date(row['date']).strftime('%Y-%m-%d')
		latest_log = webapp_models.PageVisitLog.objects.all().order_by('-id')[0]
		latest_log.create_date = date
		latest_log.save()

		dates.append(date)

	#进行统计
	from services.daily_page_visit_statistic_service.tasks import daily_page_visit_statistic_service
	for date in dates:
		result = daily_page_visit_statistic_service.delay(None, date)


# 获取规格ids, 根据名称
def _get_product_model_ids_from_name(webapp_owner_id, model_name):
	if model_name is None or model_name == "standard":
		return "standard"
	return get_custom_model_id_from_name(webapp_owner_id ,model_name)

# 获取规格名称, 根据ids
def _get_product_model_name_from_ids(webapp_owner_id, ids):
	if ids is None or ids == "standard":
		return "standard"
	return get_custom_model_id_from_name(webapp_owner_id ,ids)

# jz 2015-09-02
# @then(u"{webapp_user_name}成功创建订单")
# def step_impl(context, webapp_user_name):
# 	order_id = context.created_order_id
# 	if order_id == -1:
# 		print('Server Error: ', json.dumps(json.loads(context.response.content), indent=True))
# 		assert False, "order_id must NOT be -1"
# 		return
# @then(u"{webapp_user_name}成功创建订单")
# def step_impl(context, webapp_user_name):
# 	order_id = context.created_order_id
# 	if order_id == -1:
# 		print('Server Error: ', json.dumps(json.loads(context.response.content), indent=True))
# 		assert False, "order_id must NOT be -1"
# 		return
#
# 	order = Order.objects.get(order_id=order_id)
#
# 	url = '/workbench/jqm/preview/?woid=%s&module=mall&model=order&action=pay&order_id=%s' % (context.webapp_owner_id, order_id)
# 	response = context.client.get(bdd_util.nginx(url), follow=True)
# 	actual_order = response.context['order']
# 	actual_order.ship_area = actual_order.area
# 	actual_order.status = ORDERSTATUS2TEXT[actual_order.status]
# 	#获取coupon规则名
# 	if (actual_order.coupon_id != 0) and (actual_order.coupon_id != -1):
# 		coupon = Coupon.objects.get(id=actual_order.coupon_id)
# 		actual_order.coupon_id = coupon.coupon_rule.name
#
# 	for product in actual_order.products:
# 		# print('---product---', product)
# 		if 'custom_model_properties' in product and product['custom_model_properties']:
# 			product['model'] = ' '.join([property['property_value'] for property in product['custom_model_properties']])
#
# 	# print('---actual_order---', actual_order)
# 	expected = json.loads(context.text)
# 	bdd_util.assert_dict(expected, actual_order)
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
		# print('---product---', product)
		if 'custom_model_properties' in product and product['custom_model_properties']:
			product['model'] = ' '.join([property['property_value'] for property in product['custom_model_properties']])

	# print('---actual_order---', actual_order)
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
		arugment = json.loads(context.text)
		product_ids, product_counts, product_model_names = _get_shopping_cart_parameters(context.webapp_user.id, arugment)

	if len(product_ids) == 1:
		url = '/workbench/jqm/preview/?woid=%s&module=mall&model=order&action=edit&product_id=%s&product_count=%s&product_model_name=%s' % (context.webapp_owner_id, product_ids[0], product_counts[0], product_model_names[0])
	else:
		url = '/workbench/jqm/preview/?woid=%s&module=mall&model=shopping_cart_order&action=edit&product_ids=%s&product_counts=%s&product_model_names=%s' % (context.webapp_owner_id, product_ids, product_counts, product_model_names)

	response = context.client.get(bdd_util.nginx(url), follow=True)

	pay_interface_names = [p.get_str_name() for p in response.context['order'].pay_interfaces]
	# print(pay_interface_names)
	# print(pay_type)

	if pay_type == u'能':
		if pay_interface == u"微众卡支付":
			from market_tools.tools.weizoom_card.models import AccountHasWeizoomCardPermissions
			context.tc.assertTrue(AccountHasWeizoomCardPermissions.is_can_use_weizoom_card_by_owner_id(context.webapp_owner_id))
		else:
			context.tc.assertTrue(pay_interface in pay_interface_names)
	else:
		context.tc.assertTrue(pay_interface not in pay_interface_names)


# jz 2015-09-02
# @then(u"{webapp_user_name}获得创建订单失败的信息'{error_msg}'")
# def step_impl(context, webapp_user_name, error_msg):
# 	error_data = json.loads(context.response.content)
# 	# print(error_data)
# 	# print(error_msg)
# 	context.tc.assertTrue(200 != error_data['code'])
# 	response_msg = error_data['data']['msg']
# 	if response_msg == '':
# 		response_msg = error_data['data']['detail'][0]['msg']
# 	context.tc.assertEquals(error_msg, response_msg)
# @then(u"{webapp_user_name}获得创建订单失败的信息'{error_msg}'")
# def step_impl(context, webapp_user_name, error_msg):
# 	error_data = json.loads(context.response.content)
# 	# print(error_data)
# 	# print(error_msg)
# 	context.tc.assertTrue(200 != error_data['code'])
# 	response_msg = error_data['data']['msg']
# 	if response_msg == '':
# 		response_msg = error_data['data']['detail'][0]['msg']
# 	context.tc.assertEquals(error_msg, response_msg)
#
#
# @then(u"{webapp_user_name}获得创建订单失败的信息")
# def step_impl(context, webapp_user_name):
# 	error_data = json.loads(context.response.content)
# 	expected = json.loads(context.text)
# 	webapp_owner_id = bdd_util.get_user_id_for(context.webapp_owner_name)
# 	for detail in expected['detail']:
# 		product = Product.objects.get(owner_id=webapp_owner_id, name=detail['id'])
# 		detail['id'] = product.id
#
# 	actual = error_data['data']
# 	context.tc.assertTrue(200 != error_data['code'])
# 	bdd_util.assert_dict(expected, actual)
# @then(u"{webapp_owner_name}能获取订单")
# def step_impl(context, webapp_owner_name):
# 	db_order = Order.objects.all().order_by('-id')[0]
# 	response = context.client.get('/mall/order_detail/get/?order_id=%d' % db_order.id, follow=True)
#
# 	order = response.context['order']
#
# 	expected = json.loads(context.text)
# 	bdd_util.assert_dict(expected, order)


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
	"""
	e.g.:1
		{
			"product_groups": [{
				"promotion": {
					"type": "premium_sale",
					"result": {
						"premium_products": [{
							"name": "商品4",
							"premium_count": 3
						}]
					}
				},
				"can_use_promotion": true,
				"products": [{
					"name": "商品5",
					"model": "M",
					"price": 7.0,
					"count": 1
				}, {
					"name": "商品5",
					"model": "S",
					"price": 8.0,
					"count": 2
				}]
			}],
			"invalid_products": []
		}
	e.g.:2
		{
			"product_groups": [{
				"promotion": null,
				"can_use_promotion": false,
				"products": [{
					"name": "商品1",
					"count": 1
				}]
			}, {
				"promotion": null,
				"can_use_promotion": false,
				"products": [{
					"name": "商品2",
					"count": 2
				}]
			}],
			"invalid_products": []
		}
	"""
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
			product.count = product.count

	fill_products_model(invalid_products)
	for product_group in product_groups:
		from copy import deepcopy
		promotion = None
		promotion = product_group['promotion']
		products = product_group['products']

		if not promotion:
			product_group['promotion'] = None
		elif not product_group['can_use_promotion']:
			product_group['promotion'] = None
		else:
			#由于相同promotion产生的不同product group携带着同一个promotion对象，所以这里要通过copy来进行写时复制
			new_promotion = deepcopy(promotion)
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
	"""
	action = "click" or "pay"

	e.g.:
		{
			"action": "click"
			"context": [
				{'name': 'basketball', 'model': "standard"},
				{...}
			]
		}
	"""
	# 设置默认收货地址
	if ShipInfo.objects.all().count() == 0:
		context.execute_steps(u"When %s设置%s的webapp的默认收货地址" % (webapp_user_name, 'jobs'))
	__i = json.loads(context.text)
	if __i.get("action") == u"pay":
		argument = __i.get('context')
		# 获取购物车参数
		product_ids, product_counts, product_model_names = _get_shopping_cart_parameters(context.webapp_user.id, argument)
		url = '/termite/workbench/jqm/preview/?woid=%s&module=mall&model=shopping_cart_order&action=edit&product_ids=%s&product_counts=%s&product_model_names=%s' % (context.webapp_owner_id, product_ids, product_counts, product_model_names)
		product_infos = {
			'product_ids': product_ids,
			'product_counts': product_counts,
			'product_model_names': product_model_names
		}
		if __i.get('coupon'):
			product_infos['coupon_id'] = __i['coupon']

	elif __i.get("action") == u"click":
		# 加默认地址
		#context.webapp_user.update_ship_info(ship_name='11', ship_address='12', ship_tel='12345678970', area='1')
		url = '/termite/workbench/jqm/preview/?woid=%s&module=mall&model=shopping_cart&action=show' % (context.webapp_owner_id)
		product_infos = {}

	response = context.client.get(bdd_util.nginx(url), follow=True)
	assert response.status_code == 200
	context.product_infos = product_infos
	context.response = response
	context.pay_url = url


def _get_shopping_cart_parameters(webapp_user_id, context):
	"""
	webapp_user_id-> int
	context -> list
		e.g.:
			[
				{'name': "",
				 'model': },
				{...},
			]
	"""

	shopping_cart_items = ShoppingCart.objects.filter(webapp_user_id=webapp_user_id)
	if context is not None:
		product_infos = context
		product_ids = []
		product_counts = []
		product_model_names = []
		for product_info in product_infos:
			product_name = product_info['name']
			product_model_name = product_info.get('model', 'standard')
			product_model_name = get_product_model_keys(product_model_name)
			try:
				product = Product.objects.get(name= product_info['name'])
				cart = shopping_cart_items.get(product=product, product_model_name=product_model_name)
				product_ids.append(str(product.id))
				product_counts.append(str(cart.count))
				product_model_names.append(product_model_name)
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
	expected = json.loads(context.text)
	area_str = expected['area'].replace(',', ' ')
	area_id = bdd_util.get_ship_area_id_for(area_str)
	data = {
		'area': area_id,
		'ship_address': expected['ship_address'],
		'ship_name': expected['ship_name'],
		'ship_tel': expected['ship_tel']
	}

	#from modules.member.models import ShipInfo
	#ship_info = ShipInfo.objects.get(webapp_user_id=context.webapp_user.id)
	url = '/workbench/jqm/preview/?woid=%s&module=user_center&model=ship_info&action=save' % (context.webapp_owner_id)
	response = context.client.post(bdd_util.nginx(url), data, follow=True)
	context.ship_address = data

# jz 2015-09-02
# def __get_address_id(areas):
# 	if not areas:
# 		areas = u'北京市 北京市 海淀区'
# 	areas = areas.split(' ')
# 	province = Province.objects.get(name=areas[0])
# 	city = City.objects.get(name=areas[1])
# 	district = District.objects.get(name=areas[2])
# 	return '%d_%d_%d' % (province.id, city.id, district.id)

@when(u"{webapp_user_name}设置{webapp_owner_name}的webapp的收货地址")
def step_impl(context, webapp_user_name, webapp_owner_name):
	ship_info = json.loads(context.text)
	data = {
		'ship_address': ship_info.get('ship_address', '泰兴大厦'),
		'ship_name': ship_info.get('ship_name', webapp_user_name),
		'ship_tel': ship_info.get('ship_tel', '13811223344'),
		'area': get_area_ids(ship_info['area']),
		'woid': context.webapp_owner_id,
		'module': 'mall',
		'target_api': 'address/save'
	}

	#from modules.member.models import ShipInfo
	#ship_info = ShipInfo.objects.get(webapp_user_id=context.webapp_user.id)
	url = '/webapp/api/project_api/call/'
	response = context.client.post(bdd_util.nginx(url), data)
	context.ship_address = data


def _create_address(context, address_info):
	"""
	"""

	ship_info = {
		'ship_address': address_info.get('ship_address', u'泰兴大厦'),
		'area': get_area_ids(address_info.get('area')),
		'ship_tel': address_info.get("ship_tel", '18612456555'),
		'ship_name': address_info.get("ship_name", u"你大爷"),
	}
	url = '/webapp/api/project_api/call/'
	data = {
		'woid': context.webapp_owner_id,
		'module': 'mall',
		'target_api': 'address/save',
		'ship_id': 0
	}
	data.update(ship_info)
	response = context.client.post(url, data)
	return response

# 停止使用
# @when(u"{webapp_user_name}填写收货信息")
# def step_add_address_info(context, webapp_user_name):
# 	"""
# 		e.g.:
# 		{
# 			"ship_name": "你大爷",         # 收货人
# 			"ship_tel":  "18612456555",   # 手机号码
# 			"area": "北京市 北京市 海淀区",  # 地区
# 			"ship_address": "泰兴大厦"     # 详细地址
# 		}
# 	"""
# 	# 判断是否需要填写收货信息
# 	address_info = json.loads(context.text)
# 	response = _create_address(context, address_info)
# 	bdd_util.assert_api_call_success(response)



def get_prodcut_ids_info(order):
	product_ids = []
	product_counts = []
	product_model_names = []
	promotion_ids = []


	for product_group in order.product_groups:
		for product in product_group['products']:
			product_ids.append(str(product.id))
			product_counts.append(str(product.purchase_count))
			product_model_names.append(str(product.model_name))
			if product_group['can_use_promotion']:
				promotion_ids.append(str(product_group['promotion'].id))
			else:
				promotion_ids.append('0')
	return {'product_ids': '_'.join(product_ids),
			'product_counts': '_'.join(product_counts),
			'product_model_names': '$'.join(product_model_names),
			'promotion_ids': '_'.join(promotion_ids)
			}


# jz 2015-09-02
# @when(u"{webapp_user_name}在购物车订单编辑中点击提交订单")
# def step_click_check_out(context, webapp_user_name):
# 	"""
# 	{
# 		"pay_type":  "货到付款",
# 	}
# 	"""
# 	from mall.models import PAYNAME2TYPE
# 	argument = json.loads(context.text)
# 	pay_type = argument.get(argument['pay_type'])
#
# 	order = context.response.context['order']
# 	argument_request = get_prodcut_ids_info(order)
#
# 	url = '/webapp/api/project_api/call/'
# 	data = {
# 		'module': 'mall',
# 		'target_api': 'order/save',
# 		'is_order_from_shopping_cart': 'true',
# 		'woid': context.webapp_owner_id,
# 		'ship_id': order.ship_id,
# 		'ship_name': order.ship_name,
# 		'ship_tel': order.ship_tel,
# 		'area': order.area,
# 		'ship_address': order.ship_address,
# 		'xa-choseInterfaces': PAYNAME2TYPE.get(pay_type, -1),
# 		'bill': order.ship_name,
# 		'group2integralinfo': {},
# 	}
# 	data.update(argument_request)
# 	response = context.client.post(url, data)
# 	content = json.loads(response.content)
# 	msg = content["data"].get("msg", "")
# 	match_str = u"有商品已下架<br/>2秒后返回购物车<br/>请重新下单"
# 	if match_str == msg:
# 		context.server_error_msg = msg
# 	else:
# 		context.created_order_id = content['data']['order_id']
# 		context.response = response
	# print("*"*80)
	# from pprint(import pprint)
	# pprint(response_data)
	# raise Exception("hello")


