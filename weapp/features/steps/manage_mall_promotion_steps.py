# -*- coding: utf-8 -*-
import json
from behave import when, then

from mall.promotion import models
from mall.promotion.models import Promotion
from modules.member.models import MemberGrade
from features.testenv.model_factory import ProductFactory
from test import bdd_util


@when(u"{user}\"{action}\"促销活动\"{promotion_name}\"")
def step_terminate_promotion(context, user, action, promotion_name):
		"""促销活动通用更新单个促销状态

		@param action 操作:开始、结束、删除
		@param promotion_name 需要更新的促销活动名称
		"""
		__update_promotion_status(context, [promotion_name], action)


@when(u"{user}批量'{action}'促销活动")
def step_terminate_promotion(context, user, action):
		"""促销活动通用更新多个促销状态

		@param action 操作:开始、结束、删除
		@param context.text 促销活动数组，有效数据格式
				[{
						"name": str # 促销活动名称,必填
				}]
		** 注：所有促销活动必须是相同类型
		"""
		promotions = json.loads(context.text)
		promotion_names = [promotion['name'] for promotion in promotions]
		__update_promotion_status(context, promotion_names, action)


@when(u"{user}创建积分应用活动")
def step_impl(context, user):
		if context.table:
			promotions = [promotion.as_dict() for promotion in context.table]
		else:
			promotions = json.loads(context.text)
		if type(promotions) == dict:
				# 处理单个积分应用活动创建
				promotions = [promotions]

		for promotion in promotions:
				db_product = ProductFactory(name=promotion['product_name'])
				product_ids = [{
						'id': db_product.id
				}]
				if 'rules' in promotion:
						rules = promotion['rules']
						for rule in rules:
								if rule.has_key('member_grade'):
										rule['member_grade_id'] = __get_member_grade(rule, context.webapp_id)
				else:
						rules = [{
								"member_grade_id": -1,
								"discount": promotion.get('discount', 100),
								"discount_money": promotion.get('discount_money', 0.0)
						}]
				data = {
						'name': promotion['name'],
						'promotion_title': promotion.get('promotion_title', ''),
						'member_grade': __get_member_grade(promotion, context.webapp_id),
						'products': json.dumps(product_ids),
						'rules': json.dumps(rules),
						'discount': promotion.get('discount', 100),
						'discount_money': promotion.get('discount_money', 0.0),
						'integral_price': promotion.get('integral_price', 0.0),
						'is_permanant_active': str(promotion.get('is_permanant_active', False)).lower(),
				}
				if data['is_permanant_active'] != 'true':
						data['start_date'] = bdd_util.get_datetime_no_second_str(promotion['start_date']),
						data['end_date'] = bdd_util.get_datetime_no_second_str(promotion['end_date']),
				url = '/mall2/api/integral_sale/?_method=put'
				response = context.client.post(url, data)
				if promotion.get('created_at'):
						models.Promotion.objects.filter(
						owner_id=context.webapp_owner_id,
						name=data['name']).update(created_at=bdd_util.get_datetime_str(promotion['created_at']))
				bdd_util.assert_api_call_success(response)


@when(u"{user}创建满减活动")
def step_impl(context, user):
		if context.table:
			promotions = [promotion.as_dict() for promotion in context.table]
		else:
			promotions = json.loads(context.text)
		if type(promotions) == dict:
				promotions = [promotions]

		for promotion in promotions:
				product_ids = []
				for product in promotion['products']:
						db_product = ProductFactory(name=product)
						product_ids.append({
								'id': db_product.id
						})

				data = {
						'name': promotion['name'],
						'promotion_title': promotion.get('promotion_title', ''),
						'member_grade': __get_member_grade(promotion, context.webapp_id),
						'start_date': bdd_util.get_datetime_no_second_str(promotion['start_date']),
						'end_date': bdd_util.get_datetime_no_second_str(promotion['end_date']),
						'products': json.dumps(product_ids),

						'price_threshold': promotion['price_threshold'],
						'cut_money': promotion['cut_money'],
						'is_enable_cycle_mode': "true" if promotion.get('is_enable_cycle_mode', False) else "false",
				}

				url = '/mall2/api/price_cut/?_method=put'
				response = context.client.post(url, data)
				bdd_util.assert_api_call_success(response)


@when(u"{user}创建买赠活动")
def step_create_premium_sale(context, user):
		if context.table:
			promotions = [promotion.as_dict() for promotion in context.table]
		else:
			promotions = json.loads(context.text)
		if type(promotions) == dict:
				promotions = [promotions]

		for promotion in promotions:
				product_ids = []
				db_product = ProductFactory(name=promotion['product_name'])
				product_ids =[{
						'id': db_product.id
				}]

				premium_products = []
				for premium_product in promotion.get('premium_products', [{"name": u"赠品"}]):
						product_name = premium_product['name']
						db_product = ProductFactory(name=product_name)
						premium_products.append({
								'id': db_product.id,
								'count': premium_product.get('count', 1),
								'unit': premium_product.get('unit', '')
						})

				data = {
						'name': promotion['name'],
						'promotion_title': promotion.get('promotion_title', ''),
						'member_grade': __get_member_grade(promotion, context.webapp_id),
						'start_date': bdd_util.get_datetime_no_second_str(promotion['start_date']),
						'end_date': bdd_util.get_datetime_no_second_str(promotion['end_date']),
						'products': json.dumps(product_ids),

						'count': promotion.get('count', 1),
						'is_enable_cycle_mode': "true" if promotion.get('is_enable_cycle_mode', False) else "false",
						'premium_products': json.dumps(premium_products)
				}

				url = '/mall2/api/premium_sale/?_method=put'
				response = context.client.post(url, data)
				bdd_util.assert_api_call_success(response)


@when(u"{user}创建限时抢购活动")
def step_create_flash_sales(context, user):
		if context.table:
			promotions = [promotion.as_dict() for promotion in context.table]
		else:
			promotions = json.loads(context.text)
		if type(promotions) == dict:
				promotions = [promotions]

		for promotion in promotions:
				if promotion.has_key('products'):
						products = promotion['products']
						product_ids = [{'id': ProductFactory(name=product_name).id} for product_name in products]
				else:
						db_product = ProductFactory(name=promotion['product_name'])
						product_ids =[{
								'id': db_product.id
						}]

				data = {
						'name': promotion['name'],
						'promotion_title': promotion.get('promotion_title', ''),
						'member_grade': __get_member_grade(promotion, context.webapp_id),
						'start_date': bdd_util.get_datetime_no_second_str(promotion['start_date']),
						'end_date': bdd_util.get_datetime_no_second_str(promotion['end_date']),
						'products': json.dumps(product_ids),

						'limit_period': promotion.get('limit_period', 0),
						'promotion_price': promotion.get('promotion_price', 1),
						'count_per_purchase': promotion.get('count_per_purchase', 9999999),
				}

				url = '/mall2/api/flash_sale/?_method=put'
				response = context.client.post(url, data)
				bdd_util.assert_api_call_success(response)

### 分页相关的 step 实现 ###
@when(u"{user}设置查询条件")
def step_impl(context, user):
	context.query_param = json.loads(context.text)


@then(u"{user}获取分页信息")
def step_impl(context, user):
	if hasattr(context, 'pageinfo'):
		excepted = json.loads(context.text)
		bdd_util.assert_dict(excepted, context.pageinfo)
### 分页相关的 step 实现 ###

@then(u"{user}获取{promotion_type}活动列表")
def step_impl(context, user, promotion_type):
	if promotion_type == u"促销":
		promotion_type = "all"
	elif promotion_type == u"限时抢购":
		promotion_type = "flash_sale"
	elif promotion_type == u"买赠":
		promotion_type = "premium_sale"
	elif promotion_type == u"积分应用":
		promotion_type = "integral_sale"
	# elif type == u"优惠券":
	#     type = "coupon"
	url = '/mall2/api/promotion_list/?design_mode=0&version=1&type=%s' % promotion_type
	if hasattr(context, 'query_param'):
		if context.query_param.get('product_name'):
			url += '&name=' + context.query_param['product_name']
		if context.query_param.get('bar_code'):
			url += '&barCode='+ context.query_param['bar_code']
		if context.query_param.get('start_date'):
			url += '&startDate='+ bdd_util.get_datetime_str(context.query_param['start_date'])[:16]
		if context.query_param.get('end_date'):
			url += '&endDate='+ bdd_util.get_datetime_str(context.query_param['end_date'])[:16]
		if context.query_param.get('status', u'全部') != u'全部':
			if context.query_param['status'] == u'未开始':
				status = 1
			elif context.query_param['status'] == u'进行中':
				status = 2
			elif context.query_param['status'] == u'已结束':
				status = 3
			url += '&promotionStatus=%s' % status
	response = context.client.get(url)
	actual = json.loads(response.content)['data']['items']

	# 实际数据
	for promotion in actual:
		if promotion['status'] != u'已结束':
			# 开启这2项操作(实际上在模板中，此时次2项不含hidden属性)。参考 flash_sales.html
			promotion['actions'] = [u'详情', u'结束']
		else:
			promotion['actions'] = [u'详情', u'删除']

		if promotion['promotionTitle'] != '':
			# 含有促销标题的
			promotion['promotion_title'] = promotion['promotionTitle']

		promotion['product_name'] = promotion['product']['name']
		if promotion['product']['display_price_range'] != '':
			promotion['product_price'] = promotion['product']['display_price_range']
		else:
			promotion['product_price'] = promotion['product']['display_price']
		promotion['bar_code'] = promotion['product']['bar_code']
		promotion['price'] = promotion['product']['display_price']
		promotion['stocks'] = promotion['product']['stocks']

		if promotion_type == "flash_sale":
			promotion['promotion_price'] = promotion['detail']['promotion_price']
		if promotion_type == 'integral_sale':
			promotion['is_permanant_active'] = str(promotion['detail']['is_permanant_active']).lower()
			detail = promotion['detail']
			rules = detail['rules']
			if len(rules) == 1 and rules[0]['member_grade_id'] < 1:
					rule = rules[0]
					rule['member_grade'] = u'全部会员'
					promotion['discount'] = str(rule['discount']) + '%'
					promotion['discount_money'] = rule['discount_money']
			else:
					promotion['discount'] = detail['discount'].replace(' ', '')
					promotion['discount_money'] = detail['discount_money'].replace(' ', '')
					for rule in rules:
							rule['member_grade'] = MemberGrade.objects.get(id=rule['member_grade_id']).name

			promotion['rules'] = rules
		else:
			member_grade_id = Promotion.objects.get(id=promotion['id']).member_grade_id
			try:
				promotion['member_grade'] = MemberGrade.objects.get(id=member_grade_id).name
			except MemberGrade.DoesNotExist:
				webapp_id = bdd_util.get_webapp_id_for(user)
				promotion['member_grade'] = MemberGrade.get_default_grade(webapp_id).name
	expected = []
	if context.table:
		expected = [promotion.as_dict() for promotion in context.table]
	else:
		expected = json.loads(context.text)

	# 转化feature中的格式，与actual一致
	for promotion in expected:
		if promotion_type == 'integral_sale':
			promotion['is_permanant_active'] = str(promotion.get('is_permanant_active', False)).lower()
		if promotion.has_key('start_date') and promotion.has_key('end_date'):
			if promotion.get('is_permanant_active','false') == 'true':
				promotion.pop('start_date')
				promotion.pop('end_date')
			else:
				promotion['start_date'] = bdd_util.get_datetime_str(promotion['start_date'])
				promotion['end_date'] = bdd_util.get_datetime_str(promotion['end_date'])
		if promotion.get('created_at'):
			promotion['created_at'] = bdd_util.get_datetime_str(promotion['created_at'])
	bdd_util.assert_list(expected, actual)



def __update_promotion_status(context, promotion_names, action):
	"""使用促销活动名称更新促销状态

	@param promotion_names 促销活动名称列表
	@param action 操作:开始、结束、删除
	"""
	data = {
		'ids[]': []
	}
	promotion_type = 0
	for db_promotion in models.Promotion.objects.filter(name__in=promotion_names):
		data['ids[]'].append(db_promotion.id)
		promotion_type = db_promotion.type
	data['type'] = models.PROMOTION2TYPE[promotion_type]['name'],
	if action == u'开始':
		data['start'] = 'true'
	elif action == u'结束':
		data['start'] = 'false'
	elif action == u'删除':
		data['_method'] = 'delete'
	url = '/mall2/api/promotion/'

	response = context.client.post(url, data)
	bdd_util.assert_api_call_success(response)


def __get_member_grade(promotion, webapp_id):
	"""使用促销信息获取会员等级

	@param promotion 促销信息，有效数据格式
		{
			"member_grade": str # 会员等级名称 *全部、全部会员返回 0
		}
	@param webapp_id
	"""
	member_grade = promotion.get('member_grade', 0)
	if member_grade == u'全部' or member_grade == u'全部会员':
		member_grade = 0
	elif member_grade:
		member_grade = MemberGrade.objects.get(name=member_grade, webapp_id=webapp_id).id
	return member_grade


@then(u"{user}获取上架商品查询列表")
def step_impl(context, user):
	real = json.loads(context.text)
	url = '/mall2/api/promotion/?type=usable_promotion_products&filter_type=flash_sale&name=&barCode=&selectedProductIds=&count_per_page=10&page=1&enable_paginate=1'
	response = context.client.get(url)
	bdd_util.assert_api_call_success(response)
	data = json.loads(response.content)['data']
	expected = [{
		"name": item['name'],
		"stock_type": item['total_stocks'],
		"operate": item['can_select'],
		"price": item['standard_model']['price']
	} for item in data['items']]
	bdd_util.assert_list(expected, real)


@when(u"{user}使'{coupon_name}'失效")
def step_disable_coupon(context, user, coupon_name):
	"""
	手动取消优惠券
	"""
	data = {
		"ids[]": [],
		"type": "coupon",
		"start": False
	}
	owner_id = context.client.user.id
	promotion = models.Promotion.objects.get(owner_id=owner_id, name=coupon_name)
	data['ids[]'] = promotion.id

	url = '/mall2/api/promotion/'
	print("data: {}".format(data))
	response = context.client.post(url, data)
	bdd_util.assert_api_call_success(response)
