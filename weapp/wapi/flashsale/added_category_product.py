# -*- coding: utf-8 -*-
import json

from datetime import datetime

from django.contrib import auth
from django.contrib.auth.models import User

from account.models import UserProfile
from core import api_resource, paginator
from core import dateutil
from mall import models as mall_models
from wapi.decorators import param_required

from mall.promotion import models as promotion_models

import cache

from apps.customerized_apps.group import models as group_models

class AddedCategoryProduct(api_resource.ApiResource):
	app = 'flashsale'
	resource = 'added_category_product'

	@param_required([])
	def get(args):
		"""
		添加商品分组里的商品
		@param category_name: u'限时抢购'
		"""

		#商品分组的名称
		products = json.loads(args.get('products', u''))
		#【微众商城】帐号:weshop,用于测试的帐号devceshi
		owner = User.objects.get(username='devceshi')
		#使得webapp_cache.py能够有user_profile
		cache.request.user_profile = UserProfile.objects.get(user=owner)

		product_names = []
		for p in products:
			product_name = p["result"].encode("utf-8")
			if product_name.startswith(u'配置成功'):
				product_names.append(p["product_name"])

		#获取商品
		produt_name2product_id = {p.name: p.id for p in mall_models.Product.objects.filter(name__in=product_names)}

		#获取商品分组
		result = []
		product_category = mall_models.ProductCategory.objects.filter(name=u'限时抢购')
		if product_category.count() > 0:
			for p in products:
				product_name = p["product_name"]
				product_id = produt_name2product_id.get(product_name)
				if product_id:
					mall_models.CategoryHasProduct.objects.create(
						product_id=product_id,
						category_id=product_category[0].id
					)
					result.append({
						"result": "配置成功！"
					})
				else:
					result.append({
						"result": "配置失败！限时抢购操作失败"
					})
		else:
			result.append({
				"result": "配置失败！未找到【限时抢购】的商品分组"
			})

		return {
			"result": result
		}
