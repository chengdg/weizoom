# -*- coding: utf-8 -*-
"""@package webapp.modules.mall.models

"""
from datetime import datetime


# from hashlib import md5
# import json

from django.db import models
from django.contrib.auth.models import User
# from django.db.models import Count
from django.db.models import F
# from django.db.models import signals
# from django.conf import settings
# from django.db.models import F, Q
from django.dispatch.dispatcher import receiver

# from core import dateutil
from core.alipay.alipay_notify import AlipayNotify
# from core.alipay.alipay_submit import AlipaySubmit
from core.tenpay.tenpay_submit import TenpaySubmit
# from core.tenpay.tenpay_submit import TenpaySubmit
from core.wxpay.wxpay_notify import WxpayNotify
from account.models import UserAlipayOrderConfig
from webapp.modules.mall import signals as mall_signals

from core.exceptionutil import unicode_full_stack
from watchdog.utils import watchdog_fatal

from mall import models as new_mall_models

MALL_CONFIG_PRODUCT_COUNT_NO_LIMIT = 999999999
MALL_CONFIG_PRODUCT_NORMAL = 7
class MallConfig(models.Model):
	owner = models.ForeignKey(User, related_name='mall_config')
	max_product_count = models.IntegerField(default=MALL_CONFIG_PRODUCT_NORMAL) #最大商品数量
	is_enable_bill = models.BooleanField(default=False) #是否启用发票功能
	created_at = models.DateTimeField(auto_now_add=True) #添加时间
	#new add at 13  by bert
	order_expired_day  = models.IntegerField(default=-1) #未付款订单过期时间

	class Meta(object):
		db_table = 'mall_config'
		verbose_name = '商城配置'
		verbose_name_plural = '商城配置'

	@staticmethod
	def set_max_product_count_for(user, max_product_count):
		if user is None or max_product_count < 0:
			return

		MallConfig.objects.filter(owner=user).update(
			max_product_count = max_product_count
			)
	@staticmethod
	def get_order_expired_day(user):
		if user is None:
			return -1

		if MallConfig.objects.filter(owner=user).count() > 0:
			return MallConfig.objects.filter(owner=user)[0].order_expired_day


class MallCounter(models.Model):
	"""
	商城计数器

	表名: mall_counter
	"""
	owner = models.ForeignKey(User, related_name="mall_counter")
	unread_order_count = models.IntegerField(default=0) #新订单个数

	class Meta(object):
		db_table = 'mall_counter'
		verbose_name = '商城计数器'
		verbose_name_plural = '商城计数器'

	"""
	@staticmethod
	def increase_unread_order(webapp_owner_id, count):
		# TODO: to be optimized
		assert False
		print("in increase_unread_order()!")
		if MallCounter.objects.filter(owner_id=webapp_owner_id).count()>0:
			MallCounter.objects.filter(owner_id=webapp_owner_id).update(unread_order_count=F('unread_order_count')+count)
		else:
			MallCounter.objects.create(owner_id=webapp_owner_id, unread_order_count=count).save()
	"""

	@staticmethod
	def clear_unread_order(webapp_owner_id):
		MallCounter.objects.filter(owner_id=webapp_owner_id).update(unread_order_count=0)

def increase_unread_order(webapp_owner_id, count):
	"""
	未读订单数加1
	"""
	# TODO: to be optimized(maybe use Redis to cache stats)
	records = MallCounter.objects.filter(owner_id=webapp_owner_id)
	if records.count()>0:
		records.update(unread_order_count=F('unread_order_count')+count)
	else:
		MallCounter.objects.create(owner_id=webapp_owner_id, unread_order_count=count).save()
	#MallCounter.objects.filter(owner_id=webapp_owner_id).update(unread_order_count=F('unread_order_count')+count)


# MODULE START: productcategory
#########################################################################
# ProductCategory：商品分类
#########################################################################
# class ProductCategory(models.Model):
# 	owner = models.ForeignKey(User)
# 	name = models.CharField(max_length=256) #分类名称
# 	pic_url = models.CharField(max_length=1024) #分类图片
# 	product_count = models.IntegerField(default=0) #包含商品数量
# 	display_index = models.IntegerField(default=1, db_index=True) #显示的排序
# 	created_at = models.DateTimeField(auto_now_add=True) #添加时间

# 	class Meta(object):
# 		db_table = 'mall_product_category'
# 		verbose_name = '商品分类'
# 		verbose_name_plural = '商品分类'
ProductCategory = new_mall_models.ProductCategory


# MODULE START: product
#########################################################################
# Product：商品
#########################################################################
PRODUCT_STOCK_TYPE_LIMIT = 1
PRODUCT_STOCK_TYPE_UNLIMIT = 0
PRODUCT_SHELVE_TYPE_ON = 1
PRODUCT_SHELVE_TYPE_OFF = 0
PRODUCT_DEFAULT_TYPE = 'object'
PRODUCT_DELIVERY_PLAN_TYPE = 'delivery'
PRODUCT_TEST_TYPE = 'test'
PRODUCT_INTEGRAL_TYPE = 'integral'

# PRODUCT_TYPE2TEXT = {
# 	PRODUCT_DEFAULT_TYPE: u'普通商品',
# 	PRODUCT_DELIVERY_PLAN_TYPE: u'套餐商品',
# 	PRODUCT_INTEGRAL_TYPE: u'积分商品'
# }
# class Product(models.Model):
# 	owner = models.ForeignKey(User, related_name='user-product')
# 	name = models.CharField(max_length=256) #商品名称
# 	physical_unit = models.CharField(max_length=256) #计量单位
# 	price = models.FloatField(default=0.0) #商品价格
# 	introduction = models.CharField(max_length=256) #商品简介
# 	weight = models.FloatField(default=0.0) #重量
# 	thumbnails_url = models.CharField(max_length=1024) #商品缩略图
# 	pic_url = models.CharField(max_length=1024) #商品图
# 	detail = models.TextField() #商品详情
# 	remark = models.TextField() #备注
# 	display_index = models.IntegerField(default=1, db_index=True) #显示的排序
# 	created_at = models.DateTimeField(auto_now_add=True) #添加时间
# 	shelve_type = models.IntegerField(default=PRODUCT_SHELVE_TYPE_ON)#0:下架 1:上架 2:定时
# 	shelve_start_time = models.CharField(max_length=50, null=True) #定时上架:上架时间
# 	shelve_end_time = models.CharField(max_length=50, null=True) #定时上架:下架时间
# 	stock_type = models.IntegerField(default=PRODUCT_STOCK_TYPE_UNLIMIT)#0:无限 1:有限
# 	stocks = models.IntegerField(default=-1) #有限：数量
# 	is_deleted = models.BooleanField(default=False) #是否删除
# 	is_support_make_thanks_card = models.BooleanField(default=False)	#是否支持制作感恩贺卡
# 	type = models.CharField(max_length=50, default=PRODUCT_DEFAULT_TYPE)	#产品的类型
# 	update_time = models.DateTimeField(auto_now=True)#商品信息更新时间 2014-11-11
# 	# by liupeiyu
# 	postage_id = models.IntegerField(default=-1) #运费id ，-1为免运费
# 	is_use_online_pay_interface = models.BooleanField(default=True) #在线支付方式
# 	is_use_cod_pay_interface = models.BooleanField(default=False) #货到付款支付方式

# 	class Meta(object):
# 		db_table = 'mall_product'
# 		verbose_name = '商品'
# 		verbose_name_plural = '商品'

# 	#填充标准商品规格信息
# 	def fill_standard_model(self):
# 		try:
# 			product_model = ProductModel.objects.get(product=self, is_standard=True)

# 			self.price = product_model.price
# 			self.weight = product_model.weight
# 			self.stock_type = product_model.stock_type
# 			self.stocks = product_model.stocks
# 			self.market_price = product_model.market_price
# 			return product_model
# 		except:
# 			if settings.DEBUG:
# 				raise
# 			else:
# 				fatal_msg = u"商品填充标准规格信息错误，商品id:{}, cause:\n{}".format(self.id, unicode_full_stack())
# 				watchdog_fatal(fatal_msg)

# 	@property
# 	def is_use_custom_model(self):
# 		if not hasattr(self, '_is_use_custom_model'):
# 			self._is_use_custom_model = (ProductModel.objects.filter(product=self, is_deleted=False).count() > 1) #是否使用定制规格
# 		return self._is_use_custom_model

# 	@staticmethod
# 	def fill_display_price(products):
# 		#获取所有models
# 		product2models = {}
# 		product_ids = [product.id for product in products]
# 		for model in ProductModel.objects.filter(product_id__in=product_ids):
# 			if model.is_deleted:
# 				#model被删除，跳过
# 				continue

# 			product_id = model.product_id
# 			if product_id in product2models:
# 				models = product2models[product_id]
# 			else:
# 				models = {'standard_model': None, 'custom_models':[], 'is_use_custom_model': False}
# 				product2models[product_id] = models

# 			if model.name == 'standard':
# 				models['standard_model'] = model
# 			else:
# 				models['is_use_custom_model'] = True
# 				models['custom_models'].append(model)

# 		#为每个product确定显示价格
# 		for product in products:
# 			product_id = product.id
# 			if product_id in product2models:
# 				models = product2models[product.id]
# 				if models['is_use_custom_model']:
# 					custom_models = models['custom_models']
# 					if len(custom_models) == 1:
# 						product.display_price = custom_models[0].price
# 					else:
# 						prices = [model.price for model in custom_models]
# 						prices.sort()
# 						# 列表页部分显示商品的最小价格
# 						# add by liupeiyu at 19.0
# 						# product.display_price = '%s-%s' % (prices[0], prices[-1])
# 						product.display_price = prices[0]
# 				else:
# 					product.display_price = models['standard_model'].price
# 			else:
# 				product.display_price = product.price

# 	@staticmethod
# 	def get_from_model(product_id, product_model_name):
# 		product = Product.objects.get(id=product_id)
# 		model = ProductModel.objects.get(product=product, name=product_model_name)

# 		product.price = model.price
# 		product.weight = model.weight
# 		product.stock_type = model.stock_type
# 		product.stocks = model.stocks
# 		product.model_name = product_model_name
# 		product.market_price = model.market_price

# 		property_ids = []
# 		property_value_ids = []
# 		name = product.model_name
# 		if product.model_name != 'standard':
# 			for model_property_info in product.model_name.split('_'):
# 				property_id, property_value_id = model_property_info.split(':')
# 				property_ids.append(property_id)
# 				property_value_ids.append(property_value_id)

# 				id2property = dict([(property.id, {"id":property.id, "name":property.name}) for property in ProductModelProperty.objects.filter(id__in=property_ids)])
# 				for property_value in ProductModelPropertyValue.objects.filter(id__in=property_value_ids):
# 					id2property[property_value.property_id]['property_value'] = property_value.name
# 					id2property[property_value.property_id]['property_pic_url'] = property_value.pic_url
# 			product.custom_model_properties = id2property.values()
# 			product.custom_model_properties.sort(lambda x,y: cmp(x['id'], y['id']))
# 		else:
# 			product.custom_model_properties = None

# 		return product

# 	#填充特定的规格信息
# 	def fill_specific_model(self, model_name):
# 		model = ProductModel.objects.get(product_id=self.id, name=model_name)

# 		product = self
# 		product.price = model.price
# 		product.weight = model.weight
# 		product.stock_type = model.stock_type
# 		product.stocks = model.stocks
# 		product.model_name = model_name
# 		product.model = model
# 		product.is_model_deleted = False
# 		product.market_price = model.market_price

# 		if model.is_deleted:
# 			product.is_model_deleted = True
# 			#raise ValueError("product model is deleted: %s" % model_name)

# 		property_ids = []
# 		property_value_ids = []
# 		name = product.model_name
# 		if product.model_name != 'standard':
# 			for model_property_info in product.model_name.split('_'):
# 				property_id, property_value_id = model_property_info.split(':')
# 				property_ids.append(property_id)
# 				property_value_ids.append(property_value_id)

# 				id2property = dict([(property.id, {"id":property.id, "name":property.name}) for property in ProductModelProperty.objects.filter(id__in=property_ids)])
# 				for property_value in ProductModelPropertyValue.objects.filter(id__in=property_value_ids):
# 					id2property[property_value.property_id]['property_value'] = property_value.name
# 					id2property[property_value.property_id]['property_pic_url'] = property_value.pic_url
# 			product.custom_model_properties = id2property.values()
# 			product.custom_model_properties.sort(lambda x,y: cmp(x['id'], y['id']))
# 		else:
# 			product.custom_model_properties = None

# 		if product.stock_type == PRODUCT_STOCK_TYPE_UNLIMIT:
# 			product.stocks = -1

# 		return product.custom_model_properties


# 	#填充所有商品规格信息
# 	def fill_model(self):
# 		standard_model = self.fill_standard_model()

# 		if self.is_use_custom_model:
# 			self.custom_models = [model for model in ProductModel.objects.filter(product=self) if (model.name != 'standard') and (not model.is_deleted)]
# 		else:
# 			self.custom_models = []

# 		self.models = []
# 		self.models.append({
# 			"id": standard_model.id,
# 			"name": "standard",
# 			"original_price": self.price,
# 			"price": self.price,
# 			"weight": self.weight,
# 			"stock_type": self.stock_type,
# 			"stocks": self.stocks,
# 			"market_price": self.market_price
# 		})

# 		self.custom_properties = []
# 		self.product_model_properties = []
# 		recorded_model_property = set() #保存已记录的model property
# 		if len(self.custom_models) > 0:
# 			#获取系统所有property
# 			id2property = dict([(property.id, property) for property in ProductModelProperty.objects.filter(owner=self.owner_id, is_deleted=False)])
# 			properties = id2property.values()
# 			properties.sort(lambda x,y: cmp(x.id, y.id))
# 			for property in properties:
# 				self.custom_properties.append({
# 					"id": property.id,
# 					"name": property.name
# 				})
# 			self.custom_properties_json_str = json.dumps(self.custom_properties)

# 			property_ids = id2property.keys()
# 			id2value = dict([(value.id, value) for value in ProductModelPropertyValue.objects.filter(property_id__in=property_ids, is_deleted=False)])

# 			#获取系统所有<property, [values]>
# 			id2property = {}
# 			for property in properties:
# 				id2property[property.id] = {"id":property.id, "name":property.name, "values":[]}

# 			stock_custom_model_names = []	#无限库存或库存不为>0的custom_model_name集合
# 			property_value_ids = []
# 			for custom_model in self.custom_models:
# 				if custom_model.stock_type == 0 or custom_model.stocks > 0:
# 					stock_custom_model_names.append(str(custom_model.name))
# 				for model_property_info in custom_model.name.split('_'):
# 					property_id, property_value_id = model_property_info.split(':')
# 					property_value_ids.append(int(property_value_id))
# 			self.stock_custom_model_names = stock_custom_model_names
# 			for value in id2value.values():
# 				#增加该规格值是否属于该产品
# 				is_belong_product = (value.id in property_value_ids)
# 				id2property[value.property_id]['values'].append({
# 					"id": value.id,
# 					"name": value.name,
# 					"image": value.pic_url,
# 					"is_belong_product": is_belong_product
# 				})
# 			self.model_properties = id2property.values()
# 			self.model_properties.sort(lambda x,y: cmp(x['id'], y['id']))

# 			#获取商品关联的所有的model和property
# 			for custom_model in self.custom_models:
# 				if custom_model.name == 'standard':
# 					continue

# 				model_dict = {
# 					"id": custom_model.id,
# 					"name": custom_model.name,
# 					"original_price": custom_model.price,
# 					"price": custom_model.price,
# 					"weight": custom_model.weight,
# 					"stock_type": custom_model.stock_type,
# 					"stocks": custom_model.stocks,
# 					"market_price": custom_model.market_price
# 				}

# 				model_dict['property_values'] = []
# 				try:
# 					for model_property_info in custom_model.name.split('_'):
# 						property_id, property_value_id = model_property_info.split(':')
# 						model_dict['property_values'].append({
# 							"propertyId": property_id,
# 							"id": property_value_id,
# 							"name": id2value[int(property_value_id)].name
# 						})

# 						#记录商品的model property
# 						if not property_id in recorded_model_property:
# 							model_property = id2property[int(property_id)]
# 							self.product_model_properties.append(model_property)
# 							recorded_model_property.add(property_id)

# 					self.models.append(model_dict)
# 				except:
# 					fatal_msg = u"商品填充所有商品规格信息错误，商品id:{}, 错误的mall_product_model.id:{}, cause:\n{}".format(self.id, custom_model.id, unicode_full_stack())
# 					watchdog_fatal(fatal_msg)

# 		self.models_json_str = json.dumps(self.models)
# 		self.product_model_properties_json_str = json.dumps(self.product_model_properties)


# 	#add by bert at 17.0
# 	@staticmethod
# 	def can_update_by(owner_id, product_id):
# 		#当前owner下不还有商品，微众商城表里包含商品 这样的商品不能修改
# 		if Product.objects.filter(owner_id=owner_id, id=product_id).count() > 0:
# 			return True
# 		else:
# 			return False

# 	@staticmethod
# 	def can_update_weizoom_mall_button(user, product_id):
# 		# 商户访问商品时，
# 		# 微众商城表里包含商品, 并且已通过审核
# 		# 这样的商品 商户 不能改变页面 '是否加入微众商城' 值
# 		try:
# 			webapp_id = user.get_profile().webapp_id
# 			product = Product.objects.get(owner_id=user.id, id=product_id)
# 			wmall_has_other_products = WeizoomMallHasOtherMallProduct.objects.filter(product_id=product.id, webapp_id=webapp_id, is_checked=True)
# 			if wmall_has_other_products.count() > 0:
# 				return True
# 			else:
# 				return False
# 		except:
# 			return False

# 	@property
# 	def weizoom_mall(self):
# 		if hasattr(self, '_weizoom_mall'):
# 			return self._weizoom_mall
# 		else:
# 			try:
# 				if WeizoomMallHasOtherMallProduct.objects.filter(product_id=self.id).count() > 0:
# 					self._weizoom_mall = 1
# 				else:
# 					self._weizoom_mall = 0
# 				return self._weizoom_mall
# 			except:
# 				return 0

# 	# 是否有购买次商品权限
# 	#add by liupeiyu at 17.1
# 	def is_can_buy_by_product(self, request):
# 		if hasattr(request, 'webapp_user') and request.webapp_user:
# 			order_ids = [o.id for o in Order.objects.filter(webapp_user_id=request.webapp_user.id, webapp_id=request.user_profile.webapp_id)]
# 			count = OrderHasProduct.objects.filter(order_id__in=order_ids, product_id=self.id).count()
# 			if count > 0:
# 				self.is_can_buy_by_product = False
# 			else:
# 				self.is_can_buy_by_product = True
# 		else:
# 			self.is_can_buy_by_product = True

# 	def get_str_type(self):
# 		try:
# 			return PRODUCT_TYPE2TEXT[self.type]
# 		except:
# 			return ''

# 	# 如果规格有图片就显示，如果没有，使用缩略图
# 	def order_thumbnails_url(self):
# 		if hasattr(self, 'custom_model_properties') and self.custom_model_properties:
# 			for model in self.custom_model_properties:
# 				if model['property_pic_url']:
# 					return model['property_pic_url']

# 		return self.thumbnails_url

# 	# 是否免运费
# 	def is_free_postage(self):
# 		if self.postage_id > 0:
# 			return False

# 		return True
Product = new_mall_models.Product


#########################################################################
# ProductSwipeImage：商品轮播图片
#########################################################################
# class ProductSwipeImage(models.Model):
# 	product = models.ForeignKey(Product)
# 	url = models.CharField(max_length=256, default='')
# 	link_url = models.CharField(max_length=256, default='')
# 	created_at = models.DateTimeField(auto_now_add=True) #添加时间

# 	class Meta(object):
# 		db_table = 'mall_product_swipe_image'
# 		verbose_name = '商品轮播图'
# 		verbose_name_plural = '商品轮播图'
ProductSwipeImage = new_mall_models.ProductSwipeImage


#########################################################################
# ProductModelProperty：商品规格属性
#########################################################################
PRODUCT_MODEL_PROPERTY_TYPE_TEXT = 0
PRODUCT_MODEL_PROPERTY_TYPE_IMAGE = 1
# class ProductModelProperty(models.Model):
# 	owner = models.ForeignKey(User)
# 	name = models.CharField(max_length=256) #商品规格属性名
# 	type = models.IntegerField(default=PRODUCT_MODEL_PROPERTY_TYPE_TEXT) #属性类型
# 	is_deleted = models.BooleanField(default=False) #是否删除
# 	created_at = models.DateTimeField(auto_now_add=True) #添加时间

# 	class Meta(object):
# 		db_table = 'mall_product_model_property'
# 		verbose_name = '商品规格属性'
# 		verbose_name_plural = '商品规格属性'

# 	@property
# 	def values(self):
# 		return list(ProductModelPropertyValue.objects.filter(property=self, is_deleted=False))
ProductModelProperty = new_mall_models.ProductModelProperty


#########################################################################
# ProductModelPropertyValue：商品规格属性值
#########################################################################
# class ProductModelPropertyValue(models.Model):
# 	property = models.ForeignKey(ProductModelProperty, related_name='model_property_values')
# 	name = models.CharField(max_length=256) #商品名称
# 	pic_url = models.CharField(max_length=1024) #商品图
# 	is_deleted = models.BooleanField(default=False) #是否已删除
# 	created_at = models.DateTimeField(auto_now_add=True) #添加时间

# 	class Meta(object):
# 		db_table = 'mall_product_model_property_value'
# 		verbose_name = '商品规格属性值'
# 		verbose_name_plural = '商品规格属性值'
ProductModelPropertyValue = new_mall_models.ProductModelPropertyValue


#########################################################################
# ProductModel：商品规格
#########################################################################
# class ProductModel(models.Model):
# 	owner = models.ForeignKey(User)
# 	product = models.ForeignKey(Product)
# 	name = models.CharField(max_length=255, db_index=True) #商品规格名
# 	is_standard = models.BooleanField(default=True) #是否是标准规格
# 	price = models.FloatField(default=0.0) #商品价格
# 	market_price = models.FloatField(default=0.0) #商品市场价格
# 	weight = models.FloatField(default=0.0) #重量
# 	stock_type = models.IntegerField(default=PRODUCT_STOCK_TYPE_UNLIMIT)#0:无限 1:有限
# 	stocks = models.IntegerField(default=-1) #有限：数量
# 	is_deleted = models.BooleanField(default=False) #是否已删除
# 	created_at = models.DateTimeField(auto_now_add=True) #添加时间

# 	class Meta(object):
# 		db_table = 'mall_product_model'
# 		verbose_name = '商品规格属性'
# 		verbose_name_plural = '商品规格属性'
ProductModel = new_mall_models.ProductModel


#########################################################################
# ProductModelHasProperty: <商品规格，商品规格属性值>关系
#########################################################################
# class ProductModelHasPropertyValue(models.Model):
# 	model = models.ForeignKey(ProductModel)
# 	property_id = models.IntegerField(default=0)
# 	property_value_id = models.IntegerField(default=0)
# 	created_at = models.DateTimeField(auto_now_add=True) #添加时间

# 	class Meta(object):
# 		db_table = 'mall_product_model_has_property'
ProductModelHasPropertyValue = new_mall_models.ProductModelHasPropertyValue


#########################################################################
# CategoryHasProduct：<category, product>关系
#########################################################################
# class CategoryHasProduct(models.Model):
# 	product = models.ForeignKey(Product)
# 	category = models.ForeignKey(ProductCategory)

# 	class Meta(object):
# 		db_table = 'mall_category_has_product'
# 		verbose_name = '分类下的商品'
# 		verbose_name_plural = '分类下的商品'
CategoryHasProduct = new_mall_models.CategoryHasProduct


# MODULE END: product
# Termite GENERATED END: model


ORDER_STATUS_NOT = 0	#待支付：已下单，未付款
ORDER_STATUS_PAYED_SUCCESSED = 2	#已支付：已下单，已付款
ORDER_STATUS_PAYED_NOT_SHIP = 3#待发货：已付款，未发货
ORDER_STATUS_PAYED_SHIPED = 4#已发货：已付款，已发货
ORDER_STATUS_SUCCESSED = 5#已完成：自下单10日后自动置为已完成状态
ORDER_STATUS_CANCEL = 1 #已取消：取消订单
ORDER_BILL_TYPE_NONE = 0 #无发票
ORDER_BILL_TYPE_PERSONAL = 1 #个人发票
ORDER_BILL_TYPE_COMPANY = 2 #公司发票
STATUS2TEXT = {
	ORDER_STATUS_NOT: u'待支付',
	ORDER_STATUS_PAYED_SUCCESSED: u'已支付',
	ORDER_STATUS_PAYED_NOT_SHIP: u'待发货',
	ORDER_STATUS_PAYED_SHIPED: u'已发货',
	ORDER_STATUS_SUCCESSED: u'已完成',
	ORDER_STATUS_CANCEL: u'已取消',
}
ORDERSTATUS2TEXT = STATUS2TEXT
PAYMENT_INFO = u'下单'
DEFAULT_DATETIME = datetime.strptime('2000-01-01', '%Y-%m-%d')

THANKS_CARD_ORDER = 'thanks_card'	#感恩贺卡类型的订单

ORDER_TYPE2TEXT = {
	PRODUCT_DEFAULT_TYPE: u'普通订单',
	PRODUCT_DELIVERY_PLAN_TYPE: u'套餐订单',
	PRODUCT_TEST_TYPE: u'测试订单',
	THANKS_CARD_ORDER: u'贺卡订单',
	PRODUCT_INTEGRAL_TYPE: u'积分商品'
}
# ########################################################################
# # Order：订单
# #################t#######################################################
# class Order(models.Model):
# 	order_id = models.CharField(max_length=100) #订单号
# 	webapp_user_id = models.IntegerField() #WebApp用户的id
# 	webapp_id = models.CharField(max_length=20, verbose_name='店铺ID') #webapp
# 	buyer_name = models.CharField(max_length=100) # 购买人姓名
# 	buyer_tel = models.CharField(max_length=100) # 购买人电话
# 	ship_name = models.CharField(max_length=100) # 收货人姓名
# 	ship_tel = models.CharField(max_length=100) # 收货人电话
# 	ship_address = models.CharField(max_length=200) # 收货人地址
# 	area = models.CharField(max_length=100)
# 	status = models.IntegerField(default=ORDER_STATUS_NOT) # 订单状态
# 	order_source = models.CharField(max_length=100, default='weixin') #订单来源
# 	bill_type = models.IntegerField(default=ORDER_BILL_TYPE_NONE) #发票类型
# 	bill = models.CharField(max_length=100, default='') #发票信息
# 	remark = models.TextField() #备注
# 	product_price = models.FloatField(default=0.0) #商品金额
# 	coupon_id = models.IntegerField(default=0) #优惠券id，用于支持返还优惠券
# 	coupon_money = models.FloatField(default=0.0) #优惠券金额
# 	postage = models.FloatField(default=0.0) #运费
# 	integral = models.IntegerField(default=0) #积分
# 	integral_money = models.FloatField(default=0.0) #积分对应金额
# 	member_grade = models.CharField(max_length=50, default='') #会员等级
# 	member_grade_discount = models.IntegerField(default=100) #折扣
# 	member_grade_discounted_money = models.FloatField(default=0.0) #折扣金额
# 	final_price = models.FloatField(default=0.0) #最终总金额: (product_price + postage) - (coupon_money + weizoom_card_money + integral_money + )
# 	pay_interface_type = models.IntegerField(default=-1) #支付方式
# 	express_company_name = models.CharField(max_length=50, default='') #物流公司名称
# 	express_number = models.CharField(max_length=100) #快递单号
# 	leader_name = models.CharField(max_length=256) # 订单负责人
# 	customer_message = models.CharField(max_length=1024) #商家留言
# 	payment_time = models.DateTimeField(blank=True, default=DEFAULT_DATETIME)	#订单支付时间
# 	created_at = models.DateTimeField(auto_now_add=True) #添加时间
# 	type = models.CharField(max_length=50, default=PRODUCT_DEFAULT_TYPE)	#产品的类型
# 	integral_each_yuan = models.IntegerField(verbose_name='一元是多少积分', default=-1)
# 	reason = models.CharField(max_length=256, default='') #取消订单原因
# 	update_at = models.DateTimeField(auto_now=True)#订单信息更新时间 2014-11-11
# 	weizoom_card_money = models.FloatField(default=0.0) #微众卡抵扣金额
# 	promotion_money = models.FloatField(default=0.0) #优惠抵扣金额

# 	class Meta(object):
# 		db_table = 'mall_order'
# 		verbose_name = '订单'
# 		verbose_name_plural = '订单'

# 	#############################################################################
# 	# get_coupon: 获取定单使用的优惠券信息
# 	#############################################################################
# 	def get_coupon(self):
# 		if self.coupon_id == 0:
# 			return None
# 		else:
# 			coupon = coupon_model.Coupon.objects.get(id=self.coupon_id)
# 			return coupon

# 	#############################################################################
# 	# get_weizoom_card_id: 获取定单使用的微众卡的id
# 	#############################################################################
# 	def get_used_weizoom_card_id(self):
# 		if self.pay_interface_type == PAY_INTERFACE_WEIZOOM_COIN:
# 			from market_tools.tools.weizoom_card import models as weizoom_card_model
# 			weizoom_card_id = weizoom_card_model.WeizoomCardHasOrder.objects.get(order_id=self.order_id).card_id
# 			weizoom_card_number = weizoom_card_model.WeizoomCard.objects.get(id=weizoom_card_id).weizoom_card_id
# 			return weizoom_card_id, weizoom_card_number
# 		else:
# 			return None, None

# 	@staticmethod
# 	def fill_payment_time(orders):
# 		order_ids = [order.order_id for order in orders]
# 		order2paylog = dict([(pay_log.order_id, pay_log) for pay_log in OrderOperationLog.objects.filter(order_id__in = order_ids, action = '支付')])
# 		for order in orders:
# 			if order2paylog.has_key(order.order_id):
# 				order.payment_time = order2paylog[order.order_id].created_at
# 			else:
# 				order.payment_time = ''

# 	#############################################################################
# 	# get_orders_by_coupon_ids: 通过优惠券id获取订单列表
# 	#############################################################################
# 	@staticmethod
# 	def get_orders_by_coupon_ids(coupon_ids):
# 		if len(coupon_ids) == 0:
# 			return None
# 		else:
# 			return list(Order.objects.filter(coupon_id__in=coupon_ids))
# 	@property
# 	def get_pay_interface_name(self):
# 		return PAYTYPE2NAME.get(self.pay_interface_type, u'')

# 	@property
# 	def get_str_area(self):
# 		from tools.regional import views as regional_util
# 		if self.area:
# 			return regional_util.get_str_value_by_string_ids(self.area)
# 		else:
# 			return ''

# 	# 订单金额
# 	def get_total_price(self):
# 		return self.member_grade_discounted_money + self.postage

# 	# 支付金额
# 	# 1、如果是本店的订单，就显示 支付金额
# 	# 2、如果是商城下的单，显示  订单金额
# 	def get_final_price(self, webapp_id):
# 		if self.webapp_id == webapp_id:
# 			return self.final_price
# 		else:
# 			return self.get_total_price()

# 	# 订单使用积分
# 	# 1、如果是本店的订单，返回使用积分
# 	# 2、如果是商城下的单，返回空
# 	def get_use_integral(self, webapp_id):
# 		if self.webapp_id == webapp_id:
# 			return self.integral
# 		else:
# 			return ''

# 	@property
# 	def get_products(self):
# 		return OrderHasProduct.objects.filter(order=self)

# 	@staticmethod
# 	def get_order_has_price_number(order):
# 		numbers = OrderHasProduct.objects.filter(order=order).aggregate(Sum("total_price"))
# 		number = 0
# 		if numbers["total_price__sum"] is not None:
# 			number = numbers["total_price__sum"]

# 		return number

# 	@staticmethod
# 	def get_order_has_product(order):
# 		relations = list(OrderHasProduct.objects.filter(order=order))
# 		product_ids = [r.product_id for r in relations]
# 		return Product.objects.filter(id__in=product_ids)

# 	@staticmethod
# 	def get_order_has_product_number(order):
# 		numbers = OrderHasProduct.objects.filter(order=order).aggregate(Sum("number"))
# 		number = 0
# 		if numbers["number__sum"] is not None:
# 			number = numbers["number__sum"]
# 		return number

# 	def get_status_text(self):
# 		return STATUS2TEXT[self.status]

# 	#add by bert at member_4.0
# 	@staticmethod
# 	def get_orders_final_price_sum(webapp_user_ids):
# 		numbers = Order.objects.filter(webapp_user_id__in=webapp_user_ids, status__gte=ORDER_STATUS_PAYED_SUCCESSED).aggregate(Sum("final_price"))
# 		number = 0
# 		if numbers["final_price__sum"] is not None:
# 			number = numbers["final_price__sum"]
# 		return number

# 	@staticmethod
# 	def get_pay_numbers(webapp_user_ids):
# 		return Order.objects.filter(webapp_user_id__in=webapp_user_ids, status__gte=ORDER_STATUS_PAYED_SUCCESSED).count()

# 	# @staticmethod
# 	# def pay_days_in(webapp_user_ids, days):
# 	# 	date_day = datetime.today()-timedelta(days=int(days))
# 	# 	return Order.objects.filter(webapp_user_id__in=webapp_user_ids, status__gte=ORDER_STATUS_PAYED_SUCCESSED, payment_time__gte=date_day).count()

# 	@staticmethod
# 	def get_webapp_user_ids_pay_times_greater_than(webapp_id, pay_times):
# 		list_info = Order.objects.filter(webapp_id=webapp_id, status__gte=ORDER_STATUS_PAYED_SUCCESSED).values('webapp_user_id').annotate(dcount=Count('webapp_user_id'))
# 		webapp_user_ids = []
# 		if list_info:
# 			for vlaue in list_info:
# 				if vlaue['dcount'] >= int(pay_times):
# 					webapp_user_ids.append(vlaue['webapp_user_id'])
# 		return webapp_user_ids

# 	@staticmethod
# 	def get_webapp_user_ids_pay_days_in(webapp_id, days):
# 		date_day = datetime.today()-timedelta(days=int(days))
# 		return [order.webapp_user_id for order in Order.objects.filter(webapp_id=webapp_id, status__gte=ORDER_STATUS_PAYED_SUCCESSED, payment_time__gte=date_day)]

# def belong_to(webapp_id):
# 	weizoom_mall_order_ids = WeizoomMallHasOtherMallProductOrder.get_order_ids_for(webapp_id)
# 	return Order.objects.filter(Q(webapp_id=webapp_id)|Q(order_id__in=weizoom_mall_order_ids))
# Order.objects.belong_to  = belong_to
#from django.db.models import signals
#def after_save_order(instance, created, **kwargs):
#	print '>>>>>>>>>>>>>>>>>>>>> after_save_order <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
#	print kwargs
Order = new_mall_models.Order


#signals.post_save.connect(after_save_order, sender=Order, dispatch_uid = "mall.after_save_order")

#added by chuter
########################################################################
# OrderPaymentInfo: 订单支付信息
########################################################################
# class OrderPaymentInfo(models.Model):
# 	order = models.ForeignKey(Order)
# 	transaction_id = models.CharField(max_length=32) #交易号
# 	appid = models.CharField(max_length=64) #公众平台账户的AppId
# 	openid = models.CharField(max_length=100) #购买用户的OpenId
# 	out_trade_no = models.CharField(max_length=100) #该平台中订单号

# 	class Meta(object):
# 		db_table = 'mall_order_payment_info'
# 		verbose_name = '订单支付信息'
# 		verbose_name_plural = '订单支付信息'
OrderPaymentInfo = new_mall_models.OrderPaymentInfo

# ########################################################################
# # OrderHasProduct:订单对应商品
# ########################################################################
# class OrderHasProduct(models.Model):
# 	order = models.ForeignKey(Order)
# 	product = models.ForeignKey(Product, related_name='product')
# 	product_name = models.CharField(max_length=256) #商品名
# 	product_model_name = models.CharField(max_length=256, default='') #商品规格名
# 	price = models.FloatField() # 商品单价
# 	total_price = models.FloatField() # 订单价格
# 	is_shiped = models.IntegerField(default=0) # 是否出货
# 	number = models.IntegerField(default=1) # 商品数量
# 	created_at = models.DateTimeField(auto_now_add=True) #添加时间
# 	promotion_id = models.IntegerField(default=0) #促销信息id
# 	promotion_money = models.FloatField(default=0.0) #促销抵扣金额

# 	class Meta(object):
# 		db_table = 'mall_order_has_product'
# 		verbose_name = '购物车'
# 		verbose_name_plural = '购物车'

# 	#填充特定的规格信息
# 	@property
# 	def get_specific_model(self):
# 		if hasattr(self, '_product_specific_model'):
# 			return self._product_specific_model
# 		else:
# 			try:
# 				self._product_specific_model = self.product.fill_specific_model(self.product_model_name)
# 				return self._product_specific_model
# 			except:
# 				return None

# 	# 如果规格有图片就显示，如果没有，使用缩略图
# 	@property
# 	def order_thumbnails_url(self):
# 		if hasattr(self, '_order_thumbnails_url'):
# 			return self._order_thumbnails_url
# 		else:
# 			if self.get_specific_model:
# 				for model in self.get_specific_model:
# 					if model['property_pic_url']:
# 						self._order_thumbnails_url = model['property_pic_url']
# 						return self._order_thumbnails_url
# 			# 没有图片使用商品的图片
# 			self._order_thumbnails_url = self.product.thumbnails_url
# 			return self._order_thumbnails_url
OrderHasProduct = new_mall_models.OrderHasProduct


UNSHIPED = 0
SHIPED = 1
########################################################################
# OrderHasDeliverTime: 订单对应配送套餐配送时间表
########################################################################
# class OrderHasDeliveryTime(models.Model):
# 	order = models.ForeignKey(Order)
# 	express_company_name = models.CharField(max_length=50, default='') #物流公司名称
# 	express_number = models.CharField(max_length=100) #快递单号
# 	leader_name = models.CharField(max_length=256) # 订单负责人
# 	status = models.IntegerField(default=UNSHIPED)
# 	delivery_date = models.DateField(default = DEFAULT_DATETIME)	#配送日期

# 	class Meta(object):
# 		db_table = 'mall_order_has_delivery_time'
# 		verbose_name = '配送时间'
# 		verbose_name_plural = '配送时间'
OrderHasDeliveryTime = new_mall_models.OrderHasDeliveryTime


IMG_TYPE = 0	#图片
VIDEO_TYPE = 1 	#视频
########################################################################
# ThanksCardOrder:	感恩贺卡订单
########################################################################
# class ThanksCardOrder(models.Model):
# 	order = models.ForeignKey(Order)	#订单
# 	thanks_secret = models.CharField(max_length=100, default='')	#感恩密码
# 	card_count = models.IntegerField(default=0)	#生成贺卡个数
# 	listen_count = models.IntegerField(default=0)	#收听次数
# 	is_used = models.BooleanField(default=False) #是否已经使用
# 	title = models.CharField(max_length=50)
# 	content = models.TextField() #贺卡内容
# 	type = models.IntegerField(default=IMG_TYPE)	#贺卡附件类型
# 	att_url = models.CharField(max_length=1024)	#附件地址
# 	member_id = models.IntegerField(default=0)	#会员的id
# 	created_at = models.DateTimeField(auto_now_add=True) #添加时间

# 	class Meta(object):
# 		db_table = 'mall_thanks_card_order'
# 		verbose_name = '感恩贺卡订单'
# 		verbose_name_plural = '感恩贺卡订单'
ThanksCardOrder = new_mall_models.ThanksCardOrder

# ########################################################################
# # OrderOperationLog:订单操作日志
# ########################################################################
# class OrderOperationLog(models.Model):
# 	order_id = models.CharField(max_length=50)
# 	remark = models.TextField()
# 	action = models.CharField(max_length=50)
# 	operator = models.CharField(max_length=50)
# 	created_at = models.DateTimeField(auto_now_add=True) #添加时间

# 	class Meta(object):
# 		db_table = 'mall_order_operation_log'
# 		verbose_name = '订单后台操作日志'
# 		verbose_name_plural = '订单后台操作日志'
OrderOperationLog = new_mall_models.OrderOperationLog


########################################################################
# OrderStatusLog:订单状态日志
########################################################################
# class OrderStatusLog(models.Model):
# 	order_id = models.CharField(max_length=50)
# 	from_status = models.IntegerField()
# 	to_status = models.IntegerField()
# 	remark = models.TextField()
# 	operator = models.CharField(max_length=50)
# 	created_at = models.DateTimeField(auto_now_add=True) #添加时间

# 	class Meta(object):
# 		db_table = 'mall_order_status_log'
# 		verbose_name = '订单状态日志'
# 		verbose_name_plural = '订单状态日志'
OrderStatusLog = new_mall_models.OrderStatusLog


# Termite GENERATED START: model
# MODULE START: PostageConfig
#########################################################################
# PostageConfig：运费配置
#########################################################################
# class PostageConfig(models.Model):
# 	owner = models.ForeignKey(User)
# 	name = models.CharField(max_length=256) #名称
# 	first_weight = models.FloatField(default=0.0) #首重
# 	first_weight_price = models.FloatField(default=0.0) #首重价格
# 	is_enable_added_weight = models.BooleanField(default=True) #是否启用续重机制
# 	added_weight = models.CharField(max_length=256) #续重
# 	added_weight_price = models.CharField(max_length=256, default='0') #续重价格
# 	display_index = models.IntegerField(default=1, db_index=True) #显示的排序
# 	is_used = models.BooleanField(default=False) #是否启用
# 	is_system_level_config = models.BooleanField(default=False) #是否是系统创建的不可修改的配置
# 	created_at = models.DateTimeField(auto_now_add=True) #添加时间

# 	class Meta(object):
# 		db_table = 'mall_postage_config'
# 		verbose_name = '运费配置'
# 		verbose_name_plural = '运费配置'

# 	def get_special_configs(self):
# 		return PostageConfigSpecial.objects.filter(postage_config=self)
PostageConfig = new_mall_models.PostageConfig

#########################################################################
# PostageConfigSpecial：运费特殊配置
#########################################################################
# class PostageConfigSpecial(models.Model):
# 	owner = models.ForeignKey(User)
# 	postage_config = models.ForeignKey(PostageConfig)
# 	first_weight_price = models.FloatField(default=0.0) #首重价格
# 	added_weight_price = models.CharField(max_length=256) #续重价格
# 	created_at = models.DateTimeField(auto_now_add=True) #添加时间

# 	class Meta(object):
# 		db_table = 'mall_postage_config_special'
# 		verbose_name = '运费特殊配置'
# 		verbose_name_plural = '运费特殊配置'

# 	def get_special_has_provinces(self):
# 		return PostageConfigSpecialHasProvince.objects.filter(postage_config_special=self)

# 	def get_provinces_array(self):
# 		provinces = []
# 		for special_has_provinces in self.get_special_has_provinces():
# 			provinces.append({'id': special_has_provinces.province.id, 'name': special_has_provinces.province.name})
# 		return provinces
PostageConfigSpecial = new_mall_models.SpecialPostageConfig

#########################################################################
# PostageConfigSpecialHasProvince：运费特殊配置对应省份
#########################################################################
# from tools.regional.models import Province
# class PostageConfigSpecialHasProvince(models.Model):
# 	owner = models.ForeignKey(User)
# 	postage_config = models.ForeignKey(PostageConfig)
# 	postage_config_special = models.ForeignKey(PostageConfigSpecial)
# 	province = models.ForeignKey(Province)
# 	created_at = models.DateTimeField(auto_now_add=True) #添加时间

# 	class Meta(object):
# 		db_table = 'mall_postage_config_special_has_province'
# 		verbose_name = '运费特殊配置对应省份'
# 		verbose_name_plural = '运费特殊配置对应省份'
PostageConfigSpecialHasProvince = new_mall_models.PostageConfigSpecialHasProvince
# MODULE END: postagesettings
# Termite GENERATED END: model


#########################################################################
# ShoppingCart：购物车
#########################################################################
class ShoppingCart(models.Model):
	webapp_user_id = models.IntegerField(default=0) #WebApp用户
	product = models.ForeignKey(Product) #商品
	product_model_name = models.CharField(max_length=125) #商品规格名
	count = models.IntegerField(default=1) #商品数量
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = 'mall_shopping_cart'
		verbose_name = '购物车'
		verbose_name_plural = '购物车'


#########################################################################
# PurchaseDailyStatistics：每日购买统计
#########################################################################
class PurchaseDailyStatistics(models.Model):
	webapp_id = models.CharField(max_length=20, verbose_name='店铺ID') #webapp
	webapp_user_id = models.IntegerField() #WebApp用户的id
	order_id = models.CharField(max_length=100) #订单号
	order_price = models.FloatField(default=0.0) #订单金额
	date = models.CharField(max_length=50) #购买日期
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = 'mall_purchase_daily_statistics'
		verbose_name = '购买统计'
		verbose_name_plural = '购买统计'


#########################################################################
# PayInterface：支付方式
#########################################################################
PAY_INTERFACE_ALIPAY = 0
PAY_INTERFACE_TENPAY = 1
PAY_INTERFACE_WEIXIN_PAY = 2
PAY_INTERFACE_COD = 9
PAY_INTERFACE_PREFERENCE = 10
###########################
#ADD BY BERT  AT 16
###########################
PAY_INTERFACE_WEIZOOM_COIN = 3

PAYTYPE2LOGO = {
	PAY_INTERFACE_ALIPAY: '/standard_static/img/mockapi/alipay.png',
	PAY_INTERFACE_TENPAY: '/standard_static/img/mockapi/tenpay.png',
	PAY_INTERFACE_WEIXIN_PAY: '/standard_static/img/mockapi/weixin_pay.png',
	PAY_INTERFACE_COD: '/standard_static/img/mockapi/cod.png',
	PAY_INTERFACE_WEIZOOM_COIN: '/standard_static/img/mockapi/wzcoin.png',
}
PAYTYPE2NAME = {
	-1: u'',
	PAY_INTERFACE_PREFERENCE: u'优惠抵扣',
	PAY_INTERFACE_ALIPAY: u'支付宝',
	PAY_INTERFACE_TENPAY: u'财付通',
	PAY_INTERFACE_WEIXIN_PAY: u'微信支付',
	PAY_INTERFACE_COD: u'货到付款',
	PAY_INTERFACE_WEIZOOM_COIN: u"微众卡支付"
}
VALID_PAY_INTERFACES = [PAY_INTERFACE_WEIXIN_PAY, PAY_INTERFACE_ALIPAY, PAY_INTERFACE_COD, PAY_INTERFACE_WEIZOOM_COIN]
ONLINE_PAY_INTERFACE = [PAY_INTERFACE_WEIXIN_PAY, PAY_INTERFACE_ALIPAY, PAY_INTERFACE_WEIZOOM_COIN, PAY_INTERFACE_TENPAY]
class PayInterface(models.Model):
	owner = models.ForeignKey(User)
	type = models.IntegerField() #支付接口类型
	description = models.CharField(max_length=50) #描述
	is_active = models.BooleanField(default=True) #是否启用
	related_config_id = models.IntegerField(default=0) #各种支付方式关联配置信息的id
	created_at = models.DateTimeField(auto_now_add=True) #创建日期

	class Meta(object):
		db_table = 'mall_pay_interface'
		verbose_name = '支付方式'
		verbose_name_plural = '支付方式'

	def pay(self, order, webapp_owner_id):
		if PAY_INTERFACE_ALIPAY == self.type:
			return '/webapp/alipay/?woid={}&order_id={}&related_config_id={}'.format(webapp_owner_id, order.order_id, self.related_config_id)
		elif PAY_INTERFACE_TENPAY == self.type:
			from account.models import UserProfile
			user_profile = UserProfile.objects.get(user_id=webapp_owner_id)
			call_back_url = "http://{}/tenpay/mall/pay_result/get/{}/{}/".format(user_profile.host, webapp_owner_id, self.related_config_id)
			notify_url = "http://{}/tenpay/mall/pay_notify_result/get/{}/{}/".format(user_profile.host, webapp_owner_id, self.related_config_id)
			pay_submit = TenpaySubmit(self.related_config_id, order, call_back_url, notify_url)
			tenpay_url = pay_submit.submit()

			return tenpay_url
		elif PAY_INTERFACE_COD == self.type:
			return './?woid={}&module=mall&model=pay_result&action=get&pay_interface_type={}&order_id={}'.format(webapp_owner_id, PAY_INTERFACE_COD, order.order_id)
		elif PAY_INTERFACE_WEIXIN_PAY == self.type:
			return '/webapp/wxpay/?woid={}&order_id={}&pay_id={}&showwxpaytitle=1'.format(webapp_owner_id, order.order_id, self.id)
		elif PAY_INTERFACE_WEIZOOM_COIN == self.type:
			return './?woid={}&module=mall&model=weizoompay_order&action=pay&pay_interface_type={}&pay_interface_id={}&order_id={}'.format(webapp_owner_id, PAY_INTERFACE_WEIZOOM_COIN, self.id, order.order_id)
		else:
			return ''

	def parse_pay_result(self, request):
		error_msg = ''

		if PAY_INTERFACE_ALIPAY == self.type:
			order_id = request.GET.get('out_trade_no', None)
			trade_status = request.GET.get('result', '')
			is_trade_success = ('success' == trade_status.lower())
		elif PAY_INTERFACE_TENPAY == self.type:
			trade_status = int(request.GET.get('trade_status', -1))
			is_trade_success = (0 == trade_status)
			error_msg = request.GET.get('pay_info', '')
			order_id = request.GET.get('out_trade_no', None)
		elif PAY_INTERFACE_COD == self.type:
			is_trade_success = True
			order_id = request.GET.get('order_id')
		elif PAY_INTERFACE_WEIXIN_PAY == self.type:
			is_trade_success = True
			order_id = request.GET.get('order_id')
		else:
			pass

		#兼容改价
		try:
			order_id = order_id.split('-')[0]
		except:
			pass

		return {
			'is_success': is_trade_success,
			'order_id': order_id,
			'error_msg': error_msg
		}

	def parse_notify_result(self, request):
		error_msg = ''
		if PAY_INTERFACE_ALIPAY == self.type:
			config = UserAlipayOrderConfig.objects.get(id=self.related_config_id)
			notify =  AlipayNotify(request, config)
		elif PAY_INTERFACE_TENPAY == self.type:
			notify = TenpayNotify(request)
		elif PAY_INTERFACE_WEIXIN_PAY == self.type:
			notify = WxpayNotify(request)
		else:
			notify = None

		if notify:
			order_id = notify.get_payed_order_id()
			is_trade_success = notify.is_pay_succeed()
			error_msg = notify.get_pay_info()
			reply_response = notify.get_reply_response()
			order_payment_info = notify.get_order_payment_info()
		else:
			order_id = ''
			is_trade_success = False
			error_msg = ''
			reply_response = ''
			order_payment_info = None
		
		#兼容改价
		try:
			order_id = order_id.split('-')[0]
		except:
			pass
		
		return {
			'order_id': order_id,
			'is_success': is_trade_success,
			'error_msg': error_msg,
			'reply_response': reply_response,
			'order_payment_info': order_payment_info
		}

	def get_str_name(self):
		return PAYTYPE2NAME[self.type]



import time
from account.models import UserWeixinPayOrderConfig
from core.wxapi import get_weixin_api
from core.wxapi.weixin_api import WeixinApiError
from core.wxapi.api_pay_delivernotify import PayDeliverMessage
from weixin.user.models import get_mpuser_access_token_by_appid

@receiver(mall_signals.post_ship_order, sender=Order)
def notify_weixin_pay_after_ship_order(order, **kwargs):
	if order.pay_interface_type != PAY_INTERFACE_WEIXIN_PAY:
		#对非微信支付的其它支付方式不进行任何处理
		return

	try:
		order_payment_info = OrderPaymentInfo.objects.get(order=order)
	except:
		fatal_msg = u"对微信支付的订单({})获取对应的支付信息失败, cause:\n{}".format(order.id, unicode_full_stack())
		watchdog_fatal(fatal_msg)
		return

	mpuser_access_token = get_mpuser_access_token_by_appid(order_payment_info.appid)
	if mpuser_access_token is None:
		fatal_msg = u"对微信支付的订单({})获取对应公众号授权信息失败, cause:\n{}".format(order_payment_info.id, unicode_full_stack())
		watchdog_fatal(fatal_msg)
		return

	try:
		weixin_pay_config = UserWeixinPayOrderConfig.objects.get(app_id=mpuser_access_token.app_id)
	except:
		fatal_msg = u"对微信支付的订单({})获取对应支付配置信息失败, cause:\n{}".format(order_payment_info.id, unicode_full_stack())
		watchdog_fatal(fatal_msg)
		return

	weixin_api = get_weixin_api(mpuser_access_token)
	post_message = PayDeliverMessage(
		mpuser_access_token.app_id,
		weixin_pay_config.paysign_key,
		order_payment_info.openid,
		order_payment_info.transaction_id,
		order_payment_info.out_trade_no,
		int(time.time()),
		1, #发货状态，1 表明成功，0 表明失败，失败时需要在 deliver_msg 填上失败原因
		'',
		)

	try:
		result = weixin_api.create_deliverynotify(post_message, True)
	except WeixinApiError, api_error:
		fatal_msg = u"调用微信发货通知接口失败，失败信息:\n{}".format(api_error.__unicode__())
		watchdog_fatal(fatal_msg)
	except:
		fatal_msg = u"调用微信发货通知接口失败, cause:\n{}".format(unicode_full_stack())
		watchdog_fatal(fatal_msg)

import signal_handler

#########################################################################
# WeizoomMall: 微众商城用户
#########################################################################
class WeizoomMall(models.Model):
	webapp_id = models.CharField(max_length=20, verbose_name='webapp id', db_index=True, unique=True)
	is_active = models.BooleanField(default=True, verbose_name='是否微众商城')
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = 'weizoom_mall'
		verbose_name = '微众商城用户'
		verbose_name_plural = '微众商城用户'

	@staticmethod
	def is_weizoom_mall(webapp_id):
		if WeizoomMall.objects.filter(webapp_id=webapp_id).count() > 0:
			return WeizoomMall.objects.filter(webapp_id=webapp_id)[0].is_active
		else:
			return False

#########################################################################
# WeizoomMallHasOtherMallProduct: 微众商城用户共享其它商家的商品
#########################################################################
class WeizoomMallHasOtherMallProduct(models.Model):
	weizoom_mall = models.ForeignKey(WeizoomMall)
	webapp_id = models.CharField(max_length=20, verbose_name='店铺ID') #webapp
	is_checked = models.BooleanField(default=False, verbose_name='是否审核通过') #是否审核通过
	product_id = models.IntegerField(default=-1, verbose_name='商品ID') #商品id
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = 'weizoom_mall_has_other_mall_product'
		verbose_name = '微众商城用户共享其它商家的商品'
		verbose_name_plural = '微众商城用户共享其它商家的商品'

#########################################################################
# WeizoomMallHasOtherMallProduct: 微众商城产生的其它商户商品的订单信息
#########################################################################
class WeizoomMallHasOtherMallProductOrder(models.Model):
	weizoom_mall = models.ForeignKey(WeizoomMall)
	webapp_id = models.CharField(max_length=20, verbose_name='店铺ID') # 商品对应店铺ID
	order_id = models.CharField(max_length=256) #订单号
	product_id = models.IntegerField(default=-1, verbose_name='商品ID') #商品id
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = 'weizoom_mall_has_other_mall_product_order'
		verbose_name = '微众商城产生的其它商户商品的订单信息'
		verbose_name_plural = '微众商城产生的其它商户商品的订单信息'

	@staticmethod
	def create(webapp_id, product_id, order):
		if WeizoomMall.objects.filter(webapp_id=webapp_id).count() > 0:
			weizoom_mall = WeizoomMall.objects.filter(webapp_id=webapp_id)[0]
			if WeizoomMallHasOtherMallProduct.objects.filter(weizoom_mall=weizoom_mall, product_id=product_id).count() > 0:
				partner_webapp_id = WeizoomMallHasOtherMallProduct.objects.filter(weizoom_mall=weizoom_mall, product_id=product_id)[0].webapp_id
				WeizoomMallHasOtherMallProductOrder.objects.get_or_create(
						weizoom_mall=weizoom_mall,
						webapp_id=partner_webapp_id,
						order_id=order.order_id,
						product_id=product_id
					)
	@staticmethod
	def get_order_ids_for(webapp_id):
		return [weizoom_mall_order.order_id for weizoom_mall_order in WeizoomMallHasOtherMallProductOrder.objects.filter(webapp_id=webapp_id)]

	@staticmethod
	def get_orders_weizoom_mall_for_other_mall(webapp_id):
		return [weizoom_mall_order.order_id for weizoom_mall_order in WeizoomMallHasOtherMallProductOrder.objects.filter(weizoom_mall__webapp_id=webapp_id)]



class UserHasOrderFilter(models.Model):
	"""
	用户对应的订单筛选条件
	"""
	owner = models.ForeignKey(User)
	filter_name = models.CharField(max_length=1024, verbose_name='名称')
	filter_value = models.CharField(max_length=1024, verbose_name='筛选条件')
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

	class Meta(object):
		db_table = 'user_has_order_filter'
		verbose_name = '用户对应的订单筛选条件'
		verbose_name_plural = '用户对应的订单筛选条件'

	@staticmethod
	def create(user, filter_name, filter_value):
		return UserHasOrderFilter.objects.create(
			owner = user,
			filter_name = filter_name,
			filter_value = filter_value
		)

	# value ： status:5^4^3|pay_interface_type:2|type:object|source:0
	#
	# 订单状态：status ()
	# 支付方式：pay_interface_type (支付宝0，财付通1，微信支付2，微众卡支付3，货到付款9，优惠抵扣10)
	# 来源： source (商户1，本店0)
	# 订单类型：type (普通object，套餐delivery，测试test)
	# return 查询参数的dict，和source的值
	@staticmethod
	def get_filter_params_by_value(value):
		str_param = value.strip()
		params = None
		source = None
		if len(value) > 0:
			params = dict()
			items = str_param.split('|')
			for item in items:
				try:
					attr = item.split(':')
					if attr[0] == 'source':
						source = int(attr[1])
					else:
						values = attr[1].split('^')
						if len(values) > 1:
							params[attr[0]+'__in'] = values
						else:
							params[attr[0]] = attr[1]
				except:
					pass

		return params, source
