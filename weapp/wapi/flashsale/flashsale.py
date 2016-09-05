# -*- coding: utf-8 -*-
import json

from datetime import datetime

from django.contrib import auth
from django.contrib.auth.models import User

from account.models import UserProfile
from core import api_resource, paginator
from core import dateutil
from mall.models import Product
from wapi.decorators import param_required

from mall.promotion import models as promotion_models

import cache

from apps.customerized_apps.group import models as group_models

class Flashsale(api_resource.ApiResource):
	app = 'flashsale'
	resource = 'flashsale'

	@param_required([])
	def get(args):
		"""
		创建限时抢购
		@param product_infos = [{
			"supplier_name":"sdf",
			"product_name": "sdfs",
			"flash_price":"200",
			"to_time": "2016/9/10"
		}]

		owner = models.ForeignKey(User)
		limit_period = models.IntegerField(default=0) #限购周期
		promotion_price = models.FloatField(default=0.0) #限购价格
		count_per_purchase = models.IntegerField(default=1) #单人限购数量每次
		count_per_period = models.IntegerField(default=0)
		"""

		product_infos = json.loads(args.get('product_infos', '[]'))
		#【微众商城】帐号
		owner = User.objects.get(username='weshop')
		#使得webapp_cache.py能够有user_profile
		cache.request.user_profile = UserProfile.objects.get(user=owner)

		product_names = []
		product_name2count = {}
		for product_info in product_infos:
			product_name = product_info.get('product_name')
			product_names.append(product_name)
			if not product_name2count.has_key(product_name):
				product_name2count[product_name] = 1
			else:
				product_name2count[product_name] += 1

		products = Product.objects.filter(owner_id=owner.id, name__in=product_names)

		product_name2product_id = {product.name: product.id for product in products}

		#已经配置过促销活动的商品
		product_id2promotion_id = {psp.product_id: psp.promotion_id for psp in promotion_models.ProductHasPromotion.objects.filter(product_id__in=product_name2product_id.values())}

		#已经配置过促销活动的商品，在进行中并且不能同时参加的活动
		product_id2type = {}
		for p in promotion_models.Promotion.objects.filter(owner_id=owner.id, status=promotion_models.PROMOTION_STATUS_STARTED, id__in=product_id2promotion_id.values()):
			if p.type in [promotion_models.PROMOTION_TYPE_FLASH_SALE, promotion_models.PROMOTION_TYPE_PREMIUM_SALE, promotion_models.PROMOTION_TYPE_COUPON]:
				for product_id, promotion_id in product_id2promotion_id.items():
					if p.id == promotion_id:
						product_id2type[product_id] = p.type

		# 过滤参团的商品
		group_records = group_models.Group.objects(owner_id=owner.id, status__lte=1)
		product_id2record = dict([(record.product_id, record) for record in group_records])

		result = []
		for product_info in product_infos:
			product_id = product_name2product_id.get(product_info["product_name"])
			if product_name2count[product_info["product_name"]] > 1:
				result.append({
					"result": "配置失败，该商品名称重复"
				})
			else:
				if product_id:
					if product_id2type.get(product_id):
						display_name = promotion_models.PROMOTION2TYPE[product_id2type.get(product_id)]["display_name"]
						result.append({
							"result": "配置失败，该商品参加过【%s】活动" % display_name
						})
					else:
						if product_id2record.get(product_id):
							result.append({
								"result": "配置失败，该商品参加过【团购】活动" #% product_id2record.get(product_id).name
							})
						else:
							try:
								limit_period = product_info.get('limit_period', 0)
								promotion_price = product_info.get('flash_price', 0.0)
								count_per_purchase = product_info.get('count_per_purchase', 9999999)
								count_per_period = int(product_info.get('count_per_period', 0))

								flash_sale = promotion_models.FlashSale.objects.create(
									owner=owner,
									limit_period=limit_period,
									promotion_price=promotion_price,
									count_per_purchase=count_per_purchase,
									count_per_period=count_per_period
								)
								# now = datetime.today()
								# start_date = args.get('start_date', '2000-01-01 00:00')
								# start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M')

								# 开始时间默认今天
								start_date = dateutil.get_today()
								# 当前实现了Promotion.update信号捕获更新缓存，因此数据插入时状态为活动未开始
								'''
									owner = models.ForeignKey(User)
									name = models.CharField(max_length=256) #活动名
									promotion_title = models.CharField(max_length=256) #促销标题
									status = models.IntegerField(default=PROMOTION_STATUS_NOT_START) #促销状态
									start_date = models.DateTimeField() #开始日期
									end_date = models.DateTimeField() #结束日期
									type = models.IntegerField() #促销类型
									detail_id = models.IntegerField(default=0) #促销数据id
									member_grade_id = models.IntegerField(default=0) #会员等级
									created_at = models.DateTimeField(auto_now_add=True) #添加时间
								'''
								name = product_info.get('product_name', '')
								promotion_title = product_info.get('promotion_title', '')
								member_grade_id = product_info.get('member_grade', 0)
								to_time = product_info.get('to_time', '2000/1/1')

								end_date = dateutil.get_date_string(to_time.replace('/', '-'))

								# 默认状态为开始
								status = promotion_models.PROMOTION_STATUS_STARTED
								promotion = promotion_models.Promotion.objects.create(
									owner=owner,
									type=promotion_models.PROMOTION_TYPE_FLASH_SALE,
									name=name,
									promotion_title=promotion_title,
									status=status,
									member_grade_id=member_grade_id,
									start_date=start_date,
									end_date=end_date,
									detail_id=flash_sale.id
								)

								promotion_models.ProductHasPromotion.objects.create(
									product_id=product_id,
									promotion=promotion
								)
								result.append({
									"result": "配置成功！"
								})
							except Exception, e:
								print e, "error"
								result.append({
									"result": "配置失败，原因%s" % e
								})
				else:
					result.append({
						"result": "配置失败，商品名称错误"
					})

		return {
			"result": result
		}
