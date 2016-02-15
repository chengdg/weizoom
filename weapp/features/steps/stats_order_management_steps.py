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

'''
@when(u"{user}设置未付款订单过期时间")
def step_impl(context, user):
	"""
	@note 注意：这里用直接操作数据库的操作。

	@todo 去掉操作数据库的部分
	"""
	config = json.loads(context.text)
	# no_payment_order_expire_day = config['no_payment_order_expire_day'][:-1]
	no_payment_order_expire_day = config['no_payment_order_expire_hour']

	from mall.models import MallConfig
	MallConfig.objects.filter(owner=context.client.user).update(order_expired_day=no_payment_order_expire_day)


@when(u"{user}添加商品")
def step_impl(context, user):
	context.products = json.loads(context.text)
	for product in context.products:
		product['type'] = PRODUCT_DEFAULT_TYPE
		__add_product(context, product)


def __process_product_data(product):
	"""
	转换一个商品的数据
	"""
	#处理上架类型
	if ('shelve_type' in product) and (product['shelve_type'] == u'下架'):
		product['shelve_type'] = PRODUCT_SHELVE_TYPE_OFF
	else:
		product['shelve_type'] = PRODUCT_SHELVE_TYPE_ON
	#处理分类
	product['product_category'] = -1
	if ('category' in product) and (len(product['category']) > 0):
		product_category = ''
		for category_name in product['category'].split(','):
			category = ProductCategoryFactory(name=category_name)
			product_category += str(category.id) + ','
		product['product_category'] = product_category
		del product['category']

	if 'swipe_images' in product:
		for swipe_image in product['swipe_images']:
			swipe_image['width'] = 100
			swipe_image['height'] = 100
		product['swipe_images'] = json.dumps(product['swipe_images'])


def __add_product(context, product):
	"""
	添加一个商品
	"""
	__process_product_data(product)
	product = __supplement_product(context, product)
	response = context.client.post('/mall/product/create/', product)
	if product.get('status', None) == u'待售' or product["shelve_type"] == PRODUCT_SHELVE_TYPE_OFF:
		pass
	else:
		latest_product = Product.objects.all().order_by('-id')[0]
		Product.objects.filter(id=latest_product.id).update(shelve_type=1)


def __pay_interface(pay_interfaces):
	if pay_interfaces is None:
		return True, True

	for pay_interface in pay_interfaces:
		if pay_interface['type'] == u"货到付款":
			return True, True

	return True, False



def __supplement_product(context, product):
	"""
	补足一个商品的数据
	"""
	product_prototype = {
		"name": "product",
		"physical_unit": u"包",
		"price": "11.0",
		"market_price": "11.0",
		"weight": "0",
		"bar_code": "12321",
		"thumbnails_url": "/standard_static/test_resource_img/hangzhou1.jpg",
		"pic_url": "/standard_static/test_resource_img/hangzhou1.jpg",
		"introduction": u"product的简介",
		"detail": u"product的详情",
		"remark": u"product的备注",
		"shelve_type": PRODUCT_SHELVE_TYPE_ON,
		"stock_type": PRODUCT_STOCK_TYPE_UNLIMIT,
		"swipe_images": json.dumps([{
			"url": "/standard_static/test_resource_img/hangzhou1.jpg",
			"width" : 100,
			"height": 100
		}]),
		"postage": -1,
		"postage_deploy": -1,
		"pay_interface_online": True,
		"pay_interface_cod": True,
		"is_enable_cod_pay_interface": True,
		"is_enable_online_pay_interface": True
	}
	# 支付方式
	pay_interface_online, pay_interface_cod = __pay_interface(product.get('pay_interfaces', None))
	product_prototype['pay_interface_online'] = pay_interface_online
	if pay_interface_cod is False:
		product_prototype.pop('pay_interface_cod')
		product_prototype.pop('is_enable_cod_pay_interface')
	if pay_interface_online is False:
		product_prototype.pop('pay_interface_online')
		product_prototype.pop('is_enable_online_pay_interface')

	# 运费
	postage = product.get('postage', None)
	if postage:
		try:
			postage_money = float(postage)
			product_prototype['postage_type'] = 'unified_postage_type'
			product_prototype['unified_postage_money'] = postage_money
		except:
			product_prototype['postage_type'] = 'custom_postage_type'
			product_prototype['unified_postage_money'] = 0.0
	else:
		product_prototype['postage_type'] = 'unified_postage_type'
		product_prototype['unified_postage_money'] = 0.0

	# 积分商品
	if product.get('type', PRODUCT_DEFAULT_TYPE) == PRODUCT_INTEGRAL_TYPE:
		product['price'] = product.get('integral', 0)

	#商品图
	pic_url = product.get('pic_url', None)
	if pic_url:
		product_prototype['pic_url'] = pic_url

	product_prototype.update(product)

	# print(product_prototype)

	#设置启用规格
	if product.get('is_enable_model', None) == u'启用规格':
		product_prototype['is_use_custom_model'] = 'true'

	if 'model' in product:
		if 'standard' in product['model']['models']:
			standard_model = product['model']['models']['standard']
			__process_stock_type(standard_model)

			# 积分商品
			if product.get('type', PRODUCT_DEFAULT_TYPE) == PRODUCT_INTEGRAL_TYPE:
				standard_model['price'] = standard_model.get('integral', 0)

			product_prototype.update({
				"price": standard_model.get('price', 11.0),
				"user_code": standard_model.get('user_code', 1),
				"market_price": standard_model.get('market_price', 11.0),
				"weight": standard_model.get('weight', 0.0),
				"stock_type": standard_model.get('stock_type', PRODUCT_STOCK_TYPE_UNLIMIT),
				"stocks": standard_model.get('stocks', -1)
			})
		else:
			#对每一个model，构造诸如customModel^2:4_3:7^price的key
			custom_models = []
			for custom_model_name, custom_model in product['model']['models'].items():
				__process_stock_type(custom_model)
				if 'price' not in custom_model:
					custom_model['price'] = '1.0'
				if 'market_price' not in custom_model:
					custom_model['market_price'] = '1.0'
				if 'weight' not in custom_model:
					custom_model['weight'] = '0.0'
				if 'market_price' not in custom_model:
					custom_model['market_price'] = '1.0'
				if 'user_code' not in custom_model:
					custom_model['user_code'] = '1'

				# 积分商品
				if product.get('type', PRODUCT_DEFAULT_TYPE) == PRODUCT_INTEGRAL_TYPE:
					custom_model['price'] = custom_model.get('integral', 0)

				custom_model_id = __get_custom_model_id_from_name(context.webapp_owner_id, custom_model_name)
				custom_model['name'] = custom_model_id
				custom_models.append(custom_model)
			product_prototype['customModels'] = json.dumps(custom_models)

	product_prototype['market_price'] = product_prototype['market_price']
	return product_prototype
'''
