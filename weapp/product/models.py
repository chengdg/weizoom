# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

#########################################################################
# Product：配置后的Weapp产品
#########################################################################
PRODUCT_FOOTER_WEIZOOM = 0
PRODUCT_FOOTER_WEIHUTONG = 1
PRODUCT_FOOTERS = [
	{'name': u'微众', 'value': PRODUCT_FOOTER_WEIZOOM}, 
	{'name': u'微互通', 'value': PRODUCT_FOOTER_WEIHUTONG}
]
class Product(models.Model):
	name = models.CharField(max_length=100, default='')
	max_mall_product_count = models.IntegerField(default=7) #可添加的最大的商城商品个数
	price = models.FloatField(default=0.0) #价格
	webapp_modules = models.TextField(default='') #webapp模块，以英文逗号','分隔
	market_tool_modules = models.TextField(default='') #营销工具模块，以英文逗号','分隔
	footer = models.IntegerField(default=PRODUCT_FOOTER_WEIZOOM) #footer类型
	remark = models.TextField(default='') #备注
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'weapp_product'
		verbose_name = 'WeApp产品'
		verbose_name_plural = 'WeApp产品'


#########################################################################
# UserHasProduct：<User, Product>关系
#########################################################################
class UserHasProduct(models.Model):
	owner = models.ForeignKey(User)
	product = models.ForeignKey(Product)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'weapp_user_has_product'
