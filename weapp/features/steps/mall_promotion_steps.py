# -*- coding: utf-8 -*-
import json
import time
from datetime import datetime, timedelta

from behave import *
from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from mall import models as mall_models
from mall.promotion import models as promotion_models
from modules.member.models import MemberGrade


# @When(u"{user}创建限时抢购活动")
# def step_impl(context, user):
# 	promotions = json.loads(context.text)
# 	if type(promotions) == dict:
# 		promotions = [promotions]

# 	for promotion in promotions:
# 		product_ids = []
# 		for product in promotion['products']:
# 			db_product = mall_models.Product.objects.get(owner_id=context.webapp_owner_id, name=product)
# 			product_ids.append({
# 				'id': db_product.id
# 			})

# 		data = {
# 			'name': promotion['name'],
# 			'promotion_title': promotion.get('promotion_title', ''),
# 			'member_grade': promotion.get('member_grade', 0),
# 			'start_date': bdd_util.get_datetime_no_second_str(promotion['start_date']),
# 			'end_date': bdd_util.get_datetime_no_second_str(promotion['end_date']),
# 			'products': json.dumps(product_ids),

# 			'limit_period': promotion.get('limit_period', 0),
# 			'promotion_price': promotion['promotion_price'],
# 			'count_per_purchase': promotion.get('count_per_purchase', 9999999),
# 		}

# 		url = '/mall2/api/?_method=put'
# 		response = context.client.post(url, data)
# 		bdd_util.assert_api_call_success(response)


# @When(u"{user}创建积分应用活动")
# def step_impl(context, user):
# 	webapp_id = context.client.user.profile.webapp_id
# 	promotions = json.loads(context.text)
# 	if type(promotions) == dict:
# 		promotions = [promotions]

# 	for promotion in promotions:
# 		product_ids = []
# 		for product in promotion['products']:
# 			db_product = mall_models.Product.objects.get(owner_id=context.webapp_owner_id, name=product)
# 			product_ids.append({
# 				'id': db_product.id
# 			})
# 		if 'rules' in promotion:
# 			for rule in promotion['rules']:
# 				if rule.has_key('member_grade_name'):
# 					if rule['member_grade_name'] == '全部会员':
# 						member_grade_id = -1
# 					else:
# 						member_grade_id = MemberGrade.objects.get(webapp_id=webapp_id,name=rule['member_grade_name']).id
# 					rule.pop('member_grade_name')
# 					rule['member_grade_id'] = member_grade_id
# 		else:
# 			rules = [{
# 				"member_grade_id": -1,
# 				"discount": promotion['discount'],
# 				"discount_money": promotion['discount_money']
# 			}]
# 		data = {
# 			'name': promotion['name'],
# 			'promotion_title': promotion.get('promotion_title', ''),
# 			'member_grade': promotion.get('member_grade', 0),
# 			'start_date': bdd_util.get_datetime_no_second_str(promotion['start_date']),
# 			'end_date': bdd_util.get_datetime_no_second_str(promotion['end_date']),
# 			'products': json.dumps(product_ids),
# 			'rules': json.dumps(promotion['rules']) if 'rules' in promotion else json.dumps(rules),
# 			'discount': promotion.get('discount', 100),
# 			'discount_money': promotion.get('discount_money', 0.0),
# 			'integral_price': promotion.get('integral_price', 0.0),
# 			'is_permanant_active': "true" if promotion.get('is_permanant_active', False) else "false",
# 		}

# 		url = '/mall_promotion/api/integral_sale/create/'
# 		response = context.client.post(url, data)
# 		bdd_util.assert_api_call_success(response)


# @When(u"{user}创建满减活动")
# def step_impl(context, user):
# 	promotions = json.loads(context.text)
# 	if type(promotions) == dict:
# 		promotions = [promotions]

# 	for promotion in promotions:
# 		product_ids = []
# 		for product in promotion['products']:
# 			db_product = mall_models.Product.objects.get(owner_id=context.webapp_owner_id, name=product)
# 			product_ids.append({
# 				'id': db_product.id
# 			})

# 		data = {
# 			'name': promotion['name'],
# 			'promotion_title': promotion.get('promotion_title', ''),
# 			'member_grade': promotion.get('member_grade', 0),
# 			'start_date': bdd_util.get_datetime_no_second_str(promotion['start_date']),
# 			'end_date': bdd_util.get_datetime_no_second_str(promotion['end_date']),
# 			'products': json.dumps(product_ids),

# 			'price_threshold': promotion['price_threshold'],
# 			'cut_money': promotion['cut_money'],
# 			'is_enable_cycle_mode': "true" if promotion.get('is_enable_cycle_mode', False) else "false",
# 		}

# 		url = '/mall_promotion/api/price_cut/create/'
# 		response = context.client.post(url, data)
# 		bdd_util.assert_api_call_success(response)


# @When(u"{user}创建买赠活动")
# def step_impl(context, user):
# 	promotions = json.loads(context.text)
# 	if type(promotions) == dict:
# 		promotions = [promotions]

# 	for promotion in promotions:
# 		product_ids = []
# 		for product in promotion['products']:
# 			db_product = mall_models.Product.objects.get(owner_id=context.webapp_owner_id, name=product)
# 			product_ids.append({
# 				'id': db_product.id
# 			})

# 		premium_products = []
# 		for premium_product in promotion['premium_products']:
# 			product_name = premium_product['name']
# 			db_product = mall_models.Product.objects.get(owner_id=context.webapp_owner_id, name=product_name)
# 			premium_products.append({
# 				'id': db_product.id,
# 				'count': premium_product['count'],
# 				'unit': premium_product['unit'] if premium_product.has_key('unit') else ''
# 			})

# 		data = {
# 			'name': promotion['name'],
# 			'promotion_title': promotion.get('promotion_title', ''),
# 			'member_grade': promotion.get('member_grade', 0),
# 			'start_date': bdd_util.get_datetime_no_second_str(promotion['start_date']),
# 			'end_date': bdd_util.get_datetime_no_second_str(promotion['end_date']),
# 			'products': json.dumps(product_ids),

# 			'count': promotion['count'],
# 			'is_enable_cycle_mode': "true" if promotion.get('is_enable_cycle_mode', False) else "false",
# 			'premium_products': json.dumps(premium_products)
# 		}

# 		url = '/mall2/api/premium_sale/?_method=put'
# 		response = context.client.post(url, data)
# 		bdd_util.assert_api_call_success(response)


# @When(u"{user}结束促销活动'{promotion_name}'")
# def step_impl(context, user, promotion_name):
# 	db_promotion = promotion_models.Promotion.objects.get(owner_id=context.webapp_owner_id, name=promotion_name)
# 	data = {
# 		'type': promotion_models.PROMOTION2TYPE[db_promotion.type]['name'],
# 		'ids[]': [db_promotion.id]
# 	}
# 	response = context.client.post('/mall_promotion/api/promotions/finish/', data)
# 	bdd_util.assert_api_call_success(response)
