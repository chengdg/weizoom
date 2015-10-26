# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import json

import factory

from django.contrib.auth import models as auth_models

from account.models import *
from mall import models as webapp_models
from modules.member import models as member_models

###############################################################################################
# UserFactory
###############################################################################################
USERNAME2FIRSTNAME = {
	'zhouxun': u'周迅',
	'yangmi': u'杨幂',
	'bigs': u'大S',
	'yaochen': u'姚晨',
	'zhangbozhi': u'张柏芝',
	'likaifu': u'李开复',
	'leijun': u'雷军',
	'shiyuzhu': u'史玉柱',
	'mayun': u'马云',
}

class UserFactory(factory.django.DjangoModelFactory):
	FACTORY_FOR = auth_models.User
	FACTORY_DJANGO_GET_OR_CREATE = ('username',)

	username = factory.Sequence(lambda n: 'test%d' % n)
	first_name = factory.LazyAttribute(lambda obj: USERNAME2FIRSTNAME[obj.username] if obj.username in USERNAME2FIRSTNAME else obj.username)
	is_staff = True
	password = factory.PostGenerationMethodCall('set_password', 'test')

	# @factory.post_generation
	# def bala(self, create, extracted, **kwargs):
	# 	pass


class ProductCategoryFactory(factory.django.DjangoModelFactory):
	"""
	ProductCategoryFactory
	"""
	FACTORY_FOR = webapp_models.ProductCategory
	FACTORY_DJANGO_GET_OR_CREATE = ('name',)

	@factory.post_generation
	def update_created_at(self, create, extracted, **kwargs):
		if not create:
			return

		new_created_at = datetime.strptime('2014-06-01 00:00:00', '%Y-%m-%d %H:%M:%S') + timedelta(seconds=self.id)
		self.created_at = new_created_at
		self.save()


###############################################################################################
# mall: ProductFactory
###############################################################################################
from mall.models import PRODUCT_SHELVE_TYPE_ON, PRODUCT_STOCK_TYPE_UNLIMIT
class ProductFactory(factory.django.DjangoModelFactory):
	FACTORY_FOR = webapp_models.Product
	FACTORY_DJANGO_GET_OR_CREATE = ('name',)

	physical_unit = u"包"
	price = 11.0
	weight = 5.0
	thumbnails_url = "/standard_static/test_resource_img/hangzhou1.jpg"
	pic_url = "/standard_static/test_resource_img/hangzhou1.jpg"
	introduction = u"product的简介"
	detail = u"product的详情"
	shelve_type = PRODUCT_SHELVE_TYPE_ON
	stock_type = PRODUCT_STOCK_TYPE_UNLIMIT
	stocks = 0

	@factory.post_generation
	def update_created_at(self, create, extracted, **kwargs):
		if not create:
			return


###############################################################################################
# mall: ProductSwipeImageFactory
###############################################################################################
class ProductSwipeImageFactory(factory.django.DjangoModelFactory):
	FACTORY_FOR = webapp_models.ProductSwipeImage

	url = "/standard_static/test_resource_img/hangzhou1.jpg"
	link_url = "/standard_static/test_resource_img/hangzhou1.jpg"


###############################################################################################
# mall: CategoryHasProductFactory
###############################################################################################
class CategoryHasProductFactory(factory.django.DjangoModelFactory):
	FACTORY_FOR = webapp_models.CategoryHasProduct


###############################################################################################
# MemberTag: MemberTagFactory
###############################################################################################
class MemberTagFactory(factory.django.DjangoModelFactory):
	FACTORY_FOR = member_models.MemberTag
	FACTORY_DJANGO_GET_OR_CREATE = ('name',)

	@factory.post_generation
	def update_created_at(self, create, extracted, **kwargs):
		if not create:
			return

		new_created_at = datetime.strptime('2014-06-01 00:00:00', '%Y-%m-%d %H:%M:%S') + timedelta(seconds=self.id)
		self.created_at = new_created_at
		self.save()


###############################################################################################
# Order: OrderFactory
###############################################################################################
from mall.models import ORDER_STATUS_NOT
class OrderFactory(factory.django.DjangoModelFactory):
	FACTORY_FOR = webapp_models.Order
	FACTORY_DJANGO_GET_OR_CREATE = ('order_id',)

	order_id = '00001' #订单号
	webapp_id = '3180' #webapp
	buyer_name = u'购买人' # 购买人姓名
	buyer_tel = u'1511235636' # 购买人电话
	ship_name = u'收货人' # 收货人姓名
	ship_tel = u'1333333333' # 收货人电话
	ship_address = u'东路' # 收货人地址
	area = u'1'
	status = ORDER_STATUS_NOT # 订单状态
	product_price = 1.0 #商品金额
	final_price = 1.0 #最终总金额
	# express_company_name = models.CharField(max_length=50, default='') #物流公司名称
	# express_number = models.CharField(max_length=100) #快递单号
	# leader_name = models.CharField(max_length=256) # 订单负责人
	# customer_message = models.CharField(max_length=1024) #商家留言
	# payment_time = models.DateTimeField(blank=True, default=DEFAULT_DATETIME)	#订单支付时间
	# created_at = models.DateTimeField(auto_now_add=True) #添加时间
	# type = models.CharField(max_length=50, default=PRODUCT_DEFAULT_TYPE)	#产品的类型

	@factory.post_generation
	def update_created_at(self, create, extracted, **kwargs):
		if not create:
			return

		new_created_at = datetime.strptime('2014-10-15 00:00:00', '%Y-%m-%d %H:%M:%S') + timedelta(seconds=self.id)
		self.created_at = new_created_at
		self.save()
		