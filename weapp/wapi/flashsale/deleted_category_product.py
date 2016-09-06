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

class DeletedCategoryProduct(api_resource.ApiResource):
	app = 'flashsale'
	resource = 'deleted_category_product'

	@param_required([])
	def get(args):
		"""
		删除商品分组里的商品
		@param category_name: u'限时抢购'
		"""

		#商品分组的名称
		category_name = args.get('category_name', u'')
		#【微众商城】帐号:weshop,用于测试的帐号devceshi
		owner = User.objects.get(username='devceshi')
		#使得webapp_cache.py能够有user_profile
		cache.request.user_profile = UserProfile.objects.get(user=owner)

		#获取商品分组
		product_category = mall_models.ProductCategory.objects.filter(name=category_name)

		result = []
		if product_category.count() > 0:
			# 获取限时抢购已结束,已删除,已失效的活动promotion_models.PROMOTION_STATUS_FINISHED, promotion_models.PROMOTION_STATUS_DELETED, promotion_models.PROMOTION_STATUS_DISABLE
			# 获取进行中和未开始的的限时抢购的活动promotion_models.PROMOTION_STATUS_NOT_START, promotion_models.PROMOTION_STATUS_STARTED
			promotions = promotion_models.Promotion.objects.filter(
				owner_id=owner.id,
				type=promotion_models.PROMOTION_TYPE_FLASH_SALE
			)
			promotion_id2status = {p.id: p.status for p in promotions}
			product_has_promotions = promotion_models.ProductHasPromotion.objects.filter(promotion_id__in=promotion_id2status.keys()).order_by('id')
			product_ids = set()
			for php in product_has_promotions:
				promotion_id = php.promotion_id
				if promotion_id2status.get(promotion_id) in [promotion_models.PROMOTION_STATUS_FINISHED, promotion_models.PROMOTION_STATUS_DELETED, promotion_models.PROMOTION_STATUS_DISABLE]:
					product_ids.add(php.product_id)
				else:
					if php.product_id in product_ids:
						product_ids.remove(php.product_id)
			category_has_products = mall_models.CategoryHasProduct.objects.filter(category_id=product_category[0].id, product_id__in=product_ids)
			product_id2product_name = {p.id: p.name for p in mall_models.Product.objects.filter(id__in=product_ids)}

			for chp in category_has_products:
				chp.delete()
				result.append({
					"product_id": chp.product_id,
					"product_name": product_id2product_name.get(chp.product_id, u''),
					"result": u'移除分组成功！'
				})
		else:
			result.append({
				"product_id": 0,
				"product_name": u'',
				"result": u'【%s】未找到该商品分组' % category_name
			})

		return {
			"result": result
		}
