# -*- coding: utf-8 -*-
import json
import time
from datetime import datetime, timedelta

from behave import *
from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from mall.models import *

@When(u"{ignore}:wglass")
def step_impl(context, ignore):
	import sys
	#print >> sys.stderr, u'ignore weapp operation: %s' % ignore
	sys.stderr.write(u'ignore weapp operation: %s' % ignore)

@Given(u"{ignore}:wglass")
def step_impl(context, ignore):
	import sys
	sys.stderr.write('ignore weapp operation: %s' % ignore)

@Then(u"{ignore}:wglass")
def step_impl(context, ignore):
	import sys
	sys.stderr.write(u'ignore weapp operation: %s' % ignore)

@When(u"执行weapp操作")
def step_impl(context):
	pass


def __process_stock_type(model):
	#处理库存类型
	if ('stock_type' in model) and (model['stock_type'] == u'有限'):
		model['stock_type'] = PRODUCT_STOCK_TYPE_LIMIT
	else:
		model['stock_type'] = PRODUCT_STOCK_TYPE_UNLIMIT
		model['stocks'] = -1


def __get_product_model_property(webapp_owner_id):
	name2id = {}
	id2name = {}
	property_ids = [property.id for property in ProductModelProperty.objects.filter(owner_id=webapp_owner_id, is_deleted=False)]
	for property_value in ProductModelPropertyValue.objects.filter(property_id__in=property_ids, is_deleted=False):
		name = property_value.name
		id = '%d:%d' % (property_value.property_id, property_value.id)
		# TODO to fix bug. jz
		name2id[name] = id
		id2name[id] = name

	return name2id, id2name


def __get_custom_model_id_from_name(webapp_owner_id, model_name):
	#获取所有product model property value
	name2id, _ = __get_product_model_property(webapp_owner_id)

	model_property_value_names = model_name.split(' ')
	value_ids = [name2id[model_property_value_name] for model_property_value_name in model_property_value_names]
	value_ids = '_'.join(value_ids)
	return value_ids


def __get_custom_model_name_from_id(webapp_owner_id, model_id):
	#获取所有product model property value
	_, id2name = __get_product_model_property(webapp_owner_id)

	names = []
	for model_property_value_id in model_id.split('_'):
		names.append(id2name[model_property_value_id])

	return ' '.join(names)


def __postage_config(owner_id, postage_name):
	if postage_name is None:
		# 默认运费
		return PostageConfig.objects.filter(owner_id=owner_id, is_used=True)[0].id

	# print postage_name
	postage_name = u'{}'.format(postage_name)
	if postage_name == -1 or postage_name == u'免运费':
		return -1
	else:
		try:
			return PostageConfig.objects.filter(owner_id=owner_id, name=postage_name)[0].id
		except:
			return -1


def __pay_interface(pay_interfaces):
	if pay_interfaces is None:
		return True, True

	for pay_interface in pay_interfaces:
		if pay_interface['type'] == u"货到付款":
			return True, True

	return True, False


#######################################################################
# __supplement_product: 补足一个商品的数据
#######################################################################
def __supplement_product(context, product):
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

	# print product_prototype

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
				if not 'price' in custom_model:
					custom_model['price'] = '1.0'
				if not 'market_price' in custom_model:
					custom_model['market_price'] = '1.0'
				if not 'weight' in custom_model:
					custom_model['weight'] = '0.0'
				if not 'market_price' in custom_model:
					custom_model['market_price'] = '1.0'
				if not 'user_code' in custom_model:
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


#######################################################################
# __process_product_data: 转换一个商品的数据
#######################################################################
def __process_product_data(product):
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


#######################################################################
# __add_product: 添加一个商品
#######################################################################
def __add_product(context, product):
	__process_product_data(product)
	product = __supplement_product(context, product)
	response = context.client.post('/mall/product/create/', product)
	if product.get('status', None) == u'待售' or product["shelve_type"] == PRODUCT_SHELVE_TYPE_OFF:
		pass
	else:
		latest_product = Product.objects.all().order_by('-id')[0]
		Product.objects.filter(id=latest_product.id).update(shelve_type=1)


@given(u"{user}已添加商品")
def step_impl(context, user):
	user = UserFactory(username=user)
	context.products = json.loads(context.text)
	if hasattr(context, 'client') is False:
		context.client = bdd_util.login(user, password=None, context=context)
	for product in context.products:
		if product.get('stocks'):
			product['stock_type'] = 1

		product['type'] = PRODUCT_DEFAULT_TYPE
		__add_product(context, product)

		new_product = Product.objects.all().order_by('-id')[0]
		new_created_at = datetime.strptime('2014-06-01 00:00:00', '%Y-%m-%d %H:%M:%S') + timedelta(seconds=new_product.id)
		new_product.created_at = new_created_at
		new_product.display_index = new_product.id
		new_product.save()


@given(u"{user}已添加积分商品")
def step_impl(context, user):
	user = UserFactory(username=user)
	context.products = json.loads(context.text)
	if hasattr(context, 'client') is False:
		context.client = bdd_util.login(user, password=None, context=context)
	for product in context.products:
		if product.get('stocks'):
			product['stock_type'] = 1

		product['type'] = PRODUCT_INTEGRAL_TYPE
		__add_product(context, product)

		new_product = Product.objects.all().order_by('-id')[0]
		new_created_at = datetime.strptime('2014-06-01 00:00:00', '%Y-%m-%d %H:%M:%S') + timedelta(seconds=new_product.id)
		new_product.created_at = new_created_at
		new_product.display_index = new_product.id
		new_product.save()


@when(u"{user}添加商品")
def step_impl(context, user):
	client = context.client
	context.products = json.loads(context.text)
	for product in context.products:
		product['type'] = PRODUCT_DEFAULT_TYPE
		__add_product(context, product)
		time.sleep(1)


@when(u"{user}更新商品'{product_name}'")
def step_impl(context, user, product_name):
	existed_product = ProductFactory(name=product_name)

	if hasattr(context, 'caller_step_json'):
		product = context.caller_step_json
		delattr(context, 'caller_step_json')
	else:
		product = json.loads(context.text)
	if not 'name' in product:
		product['name'] = existed_product.name
	__process_product_data(product)
	product = __supplement_product(context, product)

	url = '/mall/product/update/?id=%d&source=offshelf' % existed_product.id
	response = context.client.post(url, product)
	bdd_util.tc.assertEquals(302, response.status_code)


@when(u"{user}添加积分商品")
def step_impl(context, user):
	client = context.client
	context.products = json.loads(context.text)
	for product in context.products:
		product['type'] = PRODUCT_INTEGRAL_TYPE
		__add_product(context, product)
		time.sleep(1)


############################################################################################
# __get_product_from_web_page: 通过web page获取一个用户的特定商品
############################################################################################
def __get_product_from_web_page(context, product_name):
	existed_product = Product.objects.get(owner_id=context.webapp_owner_id, name=product_name)
	response = context.client.get('/mall/product/update/?id=%d' % existed_product.id)
	product = response.context['product']

	#处理category
	categories = response.context['categories']
	category_name = ''
	for category in categories:
		if category.has_key('is_selected') and category['is_selected']:
			category_name += ',' + category['name']
	if len(category_name) > 0:
		category_name = category_name[1:]

	actual = {
		"name": product.name,
		"physical_unit": product.physical_unit,
		"thumbnails_url": product.thumbnails_url,
		"pic_url": product.pic_url,
		"introduction": product.introduction,
		"detail": product.detail,
		"remark": product.remark,
		"stock_type": u'无限' if product.stock_type == PRODUCT_STOCK_TYPE_UNLIMIT else u'有限',
		"shelve_type": u'上架' if product.shelve_type == PRODUCT_SHELVE_TYPE_ON else u'下架',
		'stocks': product.stocks,
		'category': category_name,
		'swipe_images': product.swipe_images,
		'is_use_custom_model': u'是' if product.is_use_custom_model else u'否',
		'is_enable_model': u'启用规格' if product.is_use_custom_model else u'不启用规格',
		'model':{},
		'postage': u'免运费',
		'pay_interfaces': []
	}

	#填充运费
	if product.postage_id > 0:
		actual['postage']=PostageConfig.objects.get(id=product.postage_id).name

	# 填充支付方式
	if product.is_use_online_pay_interface:
		actual['pay_interfaces'].append({'type': u"在线支付"})
	if product.is_use_cod_pay_interface:
		actual['pay_interfaces'].append({'type': u"货到付款"})

	#填充model信息
	if product.is_use_custom_model:
		product_models = product.models
		models = {}
		for product_model in product_models:
			if product_model['name'] == 'standard':
				continue
			else:
				display_name = __get_custom_model_name_from_id(context.webapp_owner_id, product_model['name'])
				models[display_name] = {
					"price": product_model['price'],
					"weight": product_model['weight'],
					"market_price": "" if product_model['market_price'] == 0 else product_model['market_price'],
					"stock_type": u'无限' if product_model['stock_type'] == PRODUCT_STOCK_TYPE_UNLIMIT else u'有限',
					"stocks": product_model['stocks']
				}
				# 积分商品
				if product.type == PRODUCT_INTEGRAL_TYPE:
					models[display_name]["integral"] = product_model['price']

		actual['model']['models'] = models
	else:
		product_models = product.models
		models = {}
		for product_model in product_models:
			if product_model['name'] == 'standard':
				models['standard'] = {
					"price": product_model['price'],
					"weight": product_model['weight'],
					"market_price": "" if product_model['market_price'] == 0 else product_model['market_price'],
					"stock_type": u'无限' if product_model['stock_type'] == PRODUCT_STOCK_TYPE_UNLIMIT else u'有限',
					"stocks": product_model['stocks']
				}
				# 积分商品
				if product.type == PRODUCT_INTEGRAL_TYPE:
					models['standard']["integral"] = product_model['price']

		actual['model']['models'] = models

	return actual


@then(u"{user}能获取商品'{product_name}'")
def step_impl(context, user, product_name):
	expected = json.loads(context.text)
	actual = __get_product_from_web_page(context, product_name)

	bdd_util.assert_dict(expected, actual)


@then(u"{user}找不到商品'{product_name}'")
def step_impl(context, user, product_name):
	context.tc.assertEquals(0, Product.objects.filter(name=product_name).count())


def __get_product_list(context, type_name):
	NAME2TYPE = {
		u'待售': 'offshelf',
		u'在售': 'onshelf',
		u'回收站': 'recycled'
	}
	type = NAME2TYPE[type_name]
	response = context.client.get('/mall/api/products/get/?version=1&type=%s&count_per_page=15&page=1' % type)
	data = json.loads(response.content)['data']

	products = data['items']
	for product in products:
		#价格
		product['price'] = product['display_price']
		#分类
		categories = []
		for category in product['categories']:
			if category['is_selected']:
				categories.append(category['name'])
		product['categories'] = categories
		#是否启用定制规格
		product['is_enable_model'] = u'启用规格' if product['is_use_custom_model'] else u'不启用规格'
		#处理规格
		if product['is_use_custom_model']:
			models = {}
			for model in product['models']:
				buf = []
				for property_value in model['property_values']:
					buf.append(property_value['name'])
				model_name = " ".join(buf)
				models[model_name] = {
					"price": model['price'],
					"user_code": model['user_code'],
					"stock_type": u'无限' if model['stock_type'] == 0 else u'有限',
					"stocks": model['stocks']
				}
			product['model'] = {
				"models": models
			}
		else:
			standard_model = product['standard_model']
			standard_model['stock_type'] = u'无限' if standard_model['stock_type'] == 0 else u'有限'
			product['model'] = {
				'models': {
					'standard': product['standard_model']
				}
			}

	return products

@then(u"{user}能获得'{type_name}'商品列表")
def step_impl(context, user, type_name):
	actual = __get_product_list(context, type_name)
	context.products = actual

	if hasattr(context, 'caller_step_text'):
		expected = json.loads(context.caller_step_text)
		delattr(context, 'caller_step_text')
	else:
		expected = json.loads(context.text)

	bdd_util.assert_list(expected, actual)


@then(u"{user}能获取商品列表'{product_list}'")
def step_impl(context, user, product_list):
	context.caller_step_text = product_list
	context.execute_steps(u"then %s能获取商品列表" % user)

def __get_products(context):
	response = context.client.get('/mall/api/products/get/?version=1&type=onshelf&count_per_page=15&page=1')
	data = json.loads(response.content)['data']

	products = []
	for product in data["items"]:
		products.append({
			"name": product['name']
		})
	return products



@then(u"{user}能获取商品列表")
def step_impl(context, user):
	actual = __get_products(context)
	expected = json.loads(context.text)
	bdd_util.assert_list(expected, actual)


@when(u"{user}'{direction}'调整'{product_name}'")
def step_impl(context, user, direction, product_name):
	products = list(Product.objects.all())
	products.sort(lambda x,y: cmp(y.display_index, x.display_index))

	index = 0
	src_product = None
	for i, product in enumerate(products):
		if product_name == product.name:
			index = i
			src_product = product
			break

	if direction == 'up':
		dst_product = products[index-1]
	else:
		dst_product = products[index+1]

	client = context.client
	client.get('/mall/api/product_display_index/update/?version=1&src_id=%d&dst_id=%d' % (src_product.id, dst_product.id))


@when(u"{user}置顶商品'{product_name}'")
def step_impl(context, user, product_name):
	product = ProductFactory(name=product_name)

	client = context.client
	url = '/mall/api/product_display_index/update/?version=1&src_id=%d&dst_id=0' % product.id
	client.get(url)


@when(u"{user}删除已存在的商品'{product_name}'")
def step_impl(context, user, product_name):
	existed_product = ProductFactory(name=product_name)

	url = '/mall/editor/product/delete/%d/' % existed_product.id
	context.client.get(url)


@when(u"{user}删除商品'{product_name}'的商品规格'{product_model_name}'")
def step_impl(context, user, product_name, product_model_name):
	product = __get_product_from_web_page(context, product_name)
	del product['model']['models'][product_model_name]
	context.caller_step_json = product
	context.execute_steps(u"when %s更新商品'%s'" % (user, product_name))


@when(u"{user}上架商品'{product_name}'")
def step_impl(context, user, product_name):
	product = Product.objects.get(owner_id=context.webapp_owner_id, name=product_name)
	data = {
		'id': product.id,
		'shelve_type': 'onshelf'
	}

	response = context.client.post('/mall/api/product_shelve_type/update/', data)
	bdd_util.assert_api_call_success(response)


@when(u"{user}批量上架商品")
def step_impl(context, user):
	product_names = json.loads(context.text)
	product_ids = []
	for product_name in product_names:
		product = Product.objects.get(owner_id=context.webapp_owner_id, name=product_name)
		product_ids.append(product.id)

	data = {
		'ids[]': product_ids,
		'shelve_type': 'onshelf'
	}

	response = context.client.post('/mall/api/product_shelve_type/batch_update/', data)
	bdd_util.assert_api_call_success(response)


@when(u"{user}下架商品'{product_name}'")
def step_impl(context, user, product_name):
	product = Product.objects.get(owner_id=context.webapp_owner_id, name=product_name)
	data = {
		'id': product.id,
		'shelve_type': 'offshelf'
	}

	response = context.client.post('/mall/api/product_shelve_type/update/', data)
	bdd_util.assert_api_call_success(response)


@when(u"{user}批量下架商品")
def step_impl(context, user):
	product_names = json.loads(context.text)
	product_ids = []
	for product_name in product_names:
		product = Product.objects.get(owner_id=context.webapp_owner_id, name=product_name)
		product_ids.append(product.id)

	data = {
		'ids[]': product_ids,
		'shelve_type': 'offshelf'
	}

	response = context.client.post('/mall/api/product_shelve_type/batch_update/', data)
	bdd_util.assert_api_call_success(response)


@when(u"{user}永久删除商品'{product_name}'")
def step_impl(context, user, product_name):
	product = Product.objects.get(owner_id=context.webapp_owner_id, name=product_name)
	data = {
		'id': product.id,
		'shelve_type': 'delete'
	}

	response = context.client.post('/mall/api/product_shelve_type/update/', data)
	bdd_util.assert_api_call_success(response)


@when(u"{user}批量永久删除商品")
def step_impl(context, user):
	product_names = json.loads(context.text)
	product_ids = []
	for product_name in product_names:
		product = Product.objects.get(owner_id=context.webapp_owner_id, name=product_name)
		product_ids.append(product.id)

	data = {
		'ids[]': product_ids,
		'shelve_type': 'delete'
	}

	response = context.client.post('/mall/api/product_shelve_type/batch_update/', data)
	bdd_util.assert_api_call_success(response)


@when(u"{user}将商品'{product_name}'放入回收站")
def step_impl(context, user, product_name):
	product = Product.objects.get(owner_id=context.webapp_owner_id, name=product_name)
	data = {
		'id': product.id,
		'shelve_type': 'recycled'
	}

	response = context.client.post('/mall/api/product_shelve_type/update/', data)
	bdd_util.assert_api_call_success(response)


@when(u"{user}将商品批量放入回收站")
def step_impl(context, user):
	product_names = json.loads(context.text)
	product_ids = []
	for product_name in product_names:
		product = Product.objects.get(owner_id=context.webapp_owner_id, name=product_name)
		product_ids.append(product.id)

	data = {
		'ids[]': product_ids,
		'shelve_type': 'recycled'
	}

	response = context.client.post('/mall/api/product_shelve_type/batch_update/', data)
	bdd_util.assert_api_call_success(response)


@when(u"{user}查看商品'{product_name}'的规格为")
def step_impl(context, user, product_name):
	target_product = None
	for product in context.products:
		if product['name'] == product_name:
			target_product = product
			break

	product = target_product
	models = []
	for model in product['models']:
		buf = []
		for property_value in model['property_values']:
			buf.append(property_value['name'])
		models.append({
			"name": u' '.join(buf),
			"price": model['price'],
			"stocks": model['stocks'],
			"user_code": model['user_code']
		})
	actual = models

	expected = json.loads(context.text)
	bdd_util.assert_list(expected, actual)


@when(u"{user}更新商品'{product_name}'的库存为")
def step_impl(context, user, product_name):
	stock_infos = json.loads(context.text)

	model_infos = []
	for stock_info in stock_infos:
		model = ProductModel.objects.get(owner_id=context.webapp_owner_id, user_code=stock_info['user_code'])
		stock_info['id'] = model.id
		if stock_info['stock_type'] == u'有限':
			stock_info['stock_type'] = 'limit'
		else:
			stock_info['stock_type'] = 'unlimit'
			stock_info['stocks'] = 0
		model_infos.append(stock_info)

	data = {
		'model_infos': json.dumps(model_infos)
	}

	response = context.client.post('/mall/api/product_model_stocks/update/', data)
	bdd_util.assert_api_call_success(response)
