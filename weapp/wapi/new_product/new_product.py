# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from account.models import UserProfile
from core import api_resource, paginator
from core import dateutil
from mall import models as mall_models
from wapi.decorators import param_required
import logging

import cache


class AddedCategoryProduct(api_resource.ApiResource):
	app = 'new_product'
	resource = 'new_product'

	@param_required([])
	def get(args):
		"""
		添加和移除商品分组里的商品（新品速递）
		"""

		# 【微众商城】帐号:weshop,用于测试的帐号devceshi
		owner = User.objects.get(username='weshop')
		# 使得webapp_cache.py能够有user_profile
		cache.request.user_profile = UserProfile.objects.get(user=owner)

		# 获取今天之前的两周的开始时间
		start_date = dateutil.get_previous_date('today', 14)
		end_date = dateutil.get_today()

		start_time = start_date + ' 00:00:00'
		end_time = end_date + ' 23:59:59'

		# 获取首次上架时间为两周内的
		product_pools = mall_models.ProductPool.objects.filter(woid=owner.id, sync_at__gte=start_time, sync_at__lte=end_time, status=mall_models.PP_STATUS_ON)

		pool_product_ids = [pp.product_id for pp in product_pools]

		# 获取商品的信息
		product_id2product_name = {p.id: p.name for p in mall_models.Product.objects.filter(id__in=pool_product_ids)}

		# 获取商品分组，若没有该分组则新建分组
		product_category = mall_models.ProductCategory.objects.filter(owner_id=owner.id, name=u'新品速递')

		if product_category.count() <= 0:
			product_category = mall_models.ProductCategory.objects.create(
				owner=owner,
				name=u'新品速递'
			)
			category_id = product_category.id
		else:
			category_id = product_category[0].id

		# 获取商品分组里的商品
		category_product_ids = [chp.product_id for chp in mall_models.CategoryHasProduct.objects.filter(category_id=category_id)]

		add_product_ids = set(pool_product_ids) - set(category_product_ids)
		del_product_ids = set(category_product_ids) - set(pool_product_ids)


		# 添加商品到新品速递分组
		add_product_list = []
		for add_p_id in add_product_ids:
			add_product_list.append(mall_models.CategoryHasProduct(
				product_id=add_p_id,
				category_id=category_id
			))
			logging.info(u'添加商品:id:{},name:{}'.format(add_p_id, product_id2product_name.get(add_p_id)))
		mall_models.CategoryHasProduct.objects.bulk_create(add_product_list)
		add_num = len(add_product_list)

		# 将商品移除新品速递分组
		mall_models.CategoryHasProduct.objects.filter(product_id__in=del_product_ids).delete()
		del_num = len(del_product_ids)
		for del_p_id in del_product_ids:
			logging.info(u'移除商品:id:{},name:{}'.format(del_p_id, product_id2product_name.get(del_p_id)))

		return {
			"result": {
				"add_num": add_num,
				"del_num": del_num
			}
		}
