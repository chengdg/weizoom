# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


#########################################################################
# Category: 分类
#########################################################################
class Category(models.Model):
	name = models.CharField(max_length=256)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'example_category'


#########################################################################
# Product: 商品
#########################################################################
class Product(models.Model):
	categories = models.ManyToManyField(Category, through='CategoryHasProduct')
	name = models.CharField(max_length=256)
	price = models.IntegerField(default=1)
	count = models.IntegerField(default=0)
	detail = models.CharField(max_length=256)

	class Meta(object):
		db_table = 'example_product'


#########################################################################
# CategoryHasProduct: <category, product>关系
#########################################################################
class CategoryHasProduct(models.Model):
	category = models.ForeignKey(Category)
	product = models.ForeignKey(Product)

	class Meta(object):
		db_table = 'example_category_has_product'


#########################################################################
# Order: 订单
#########################################################################
class Order(models.Model):
	product = models.ForeignKey(Product)
	receiver = models.CharField(max_length=256) #收货人
	price = models.IntegerField(default=1)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'example_order'