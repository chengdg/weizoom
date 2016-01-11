# -*- coding: utf-8 -*-
"""TODO 逐步作废，移动到 .utils.py中
"""
import time


# from core.alipay.alipay_submit import *

from account.models import UserProfile
from modules.member.models import *
from mall.models import *
from modules.member.models import WebAppUser
from account.models import *
from mall.models import *

# from tools.regional.views import get_str_value_by_string_ids
# from core.send_order_email_code import *



def get_postage_for_weight(weight, postage_config, special_factor=None):
	"""
	获得指定运费模板、商品重量对应的运费
	"""
	if special_factor:
		# 有特殊运费
		if weight <= postage_config.first_weight:
			return float('%.2f' % special_factor.get('firstWeightPrice'))

		if not postage_config.is_enable_added_weight:
			return float('%.2f' % special_factor.get('firstWeightPrice'))

		price = special_factor.get('firstWeightPrice')
		weight = weight - postage_config.first_weight

		added_weight_count = 1
		added_weight = float(postage_config.added_weight)
		added_weight_price = float(special_factor.get('addedWeightPrice'))
	else:
		if weight <= postage_config.first_weight:
			return float('%.2f' % postage_config.first_weight_price)

		if not postage_config.is_enable_added_weight:
			return float('%.2f' % postage_config.first_weight_price)

		price = postage_config.first_weight_price
		weight = weight - postage_config.first_weight

		added_weight_count = 1
		added_weight = float(postage_config.added_weight)
		added_weight_price = float(postage_config.added_weight_price)

	while True:
		weight = float('%.2f' % weight) - float('%.2f' % added_weight)
		if weight <= 0:
			break
		else:
			added_weight_count += 1
	added_price = added_weight_count * added_weight_price
	return float('%.2f' % (price + added_price))


def get_postage_for_products(postage_configs, products, province_id=0):
	"""
	获得一批商品的运费
	"""
	# 获取postage config
	if len(products) == 1:
		if products[0].type == PRODUCT_INTEGRAL_TYPE:
			postage_config = filter(lambda c: c.is_system_level_config, postage_configs)[0]
		else:
			postage_config = filter(lambda c: c.is_used, postage_configs)[0]
	else:
		postage_config = filter(lambda c: c.is_used, postage_configs)[0]

	total_weight = 0.0
	for product in products:
		if product.postage_id > 0:
			total_weight += float(product.weight) * product.purchase_count

	factor = postage_config.factor
	if province_id > 0:
		special_factor = factor.get('special_factor', None)
		if special_factor:
			province_special_factor = special_factor.get('province_{}'.format(province_id))
			if province_special_factor:
				return get_postage_for_weight(total_weight, postage_config, province_special_factor)

	return get_postage_for_weight(total_weight, postage_config)


def get_postage_for_all_models(webapp_owner_id, product, postage_config=None):
	"""
	获得商品的所有规格的运费
	商品详情页面调用，暂时不用
	"""
	if not postage_config:
		if product.type == PRODUCT_INTEGRAL_TYPE:
			# 1、积分商品 免运费
			postage_configs = PostageConfig.objects.filter(owner_id=webapp_owner_id, is_system_level_config=True)
		else:
			# 2、普通商品
			postage_configs = PostageConfig.objects.filter(owner_id=webapp_owner_id, is_used=True)

		if postage_configs.count() > 0:
			postage_config = postage_configs[0]
		else:
			return None

	for model in product.models:
		if model["price"] == 0:
			model["postage"] = 0.0
		else:
			_, model["postage"] = get_postage_for_weight(webapp_owner_id, model['weight'], postage_config)

	return postage_config


########################################################################
# _update_default_postage_config: 修改运费默认配置
# 当改owner_id下的运费没有默认使用的
# 将‘免运费’设置为启用
########################################################################
def _update_default_postage_config(webapp_owner_id):
	postages = PostageConfig.objects.filter(owner_id=webapp_owner_id)
	if postages.filter(is_used=True).count() == 0:
		postages.filter(is_system_level_config=True).update(is_used=True)





