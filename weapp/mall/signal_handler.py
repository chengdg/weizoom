# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import random
import math

from django.conf import settings
from django.dispatch import Signal
from django.dispatch.dispatcher import receiver
from django.db.models import signals as django_model_signals
from django.db.models import Q

from mall import signals as mall_signals
from mall import postage_calculator as mall_postage_calculator
from models import *
from webapp.models import Workspace
from account.models import UserProfile
from watchdog.utils import watchdog_alert, watchdog_fatal, watchdog_warning, watchdog_error, watchdog_info
from core.exceptionutil import unicode_full_stack
from market_tools.tools.delivery_plan.models import DeliveryPlan
from core.common_util import ignore_exception
from tools.express.express_poll import ExpressPoll
from webapp.modules.mall.utils import get_product_member_discount

#############################################################################################
# post_update_product_model_property_handler: post_update_product_model_property的handler
#############################################################################################
@receiver(mall_signals.post_update_product_model_property, sender=ProductModelProperty)
def post_update_product_model_property_handler(model_property, request, **kwargs):
	try:
		#获得更新后的property:value集合
		updated_property_values = set()
		for property_value in ProductModelPropertyValue.objects.filter(property=model_property, is_deleted=False):
			updated_property_values.add(property_value.id)

		#获取value已经被删除的model
		invalid_models = set()
		for relation in ProductModelHasPropertyValue.objects.filter(property_id=model_property.id):
			if relation.property_id != model_property.id:
				continue

			if not relation.property_value_id in updated_property_values:
				invalid_models.add(relation.model_id)

		#获得这些model关联的product
		product_ids = set(list(ProductModel.objects.filter(id__in=invalid_models).values_list('product_id', flat=True)))

		#删除这一批model
		ProductModel.objects.filter(id__in=invalid_models).update(is_deleted=True)

		#如果只剩standard model，下架商品
		for product_id in product_ids:
			if ProductModel.objects.filter(product_id=product_id, is_deleted=False).count() <= 1:
				Product.objects.filter(id=product_id).update(shelve_type=PRODUCT_SHELVE_TYPE_OFF)
				#from module_api import remove_product_from_all_shopping_cart
				#remove_product_from_all_shopping_cart(product_id=product_id)
	except:
		alert_message = u"post_update_product_model_property_handler处理失败, cause:\n{}".format(unicode_full_stack())
		if hasattr(request, 'user'):
			watchdog_alert(alert_message, type='WEB', user_id=str(request.user.id))
		else:
			watchdog_alert(alert_message, type='WEB')


#############################################################################################
# pre_delete_product_model_property: pre_delete_product_model_property的handler
#############################################################################################
@receiver(mall_signals.pre_delete_product_model_property, sender=ProductModelProperty)
def pre_delete_product_model_property_handler(model_property, request, **kwargs):
	try:
		#获取property已经被删除的model
		invalid_models = set()
		for relation in ProductModelHasPropertyValue.objects.filter(property_id=model_property.id):
			if relation.property_id != model_property.id:
				continue

			invalid_models.add(relation.model_id)

		#获得这些model关联的product
		product_ids = set(list(ProductModel.objects.filter(id__in=invalid_models).values_list('product_id', flat=True)))

		#删除这一批model
		ProductModel.objects.filter(id__in=invalid_models).update(is_deleted=True)

		#下架商品
		#for product_id in product_ids:
		Product.objects.filter(id__in=product_ids).update(shelve_type=PRODUCT_SHELVE_TYPE_OFF)
		#from module_api import remove_product_from_all_shopping_cart
		#remove_product_from_all_shopping_cart(product_id=product_id)
	except:
		if settings.DEBUG:
			raise
		else:
			alert_message = u"pre_delete_product_model_property_handler处理失败, cause:\n{}".format(unicode_full_stack())
			if hasattr(request, 'user'):
				watchdog_alert(alert_message, type='WEB', user_id=str(request.user.id))
			else:
				watchdog_alert(alert_message, type='WEB')


@receiver(mall_signals.post_pay_order, sender=Order)
def post_pay_order_handler(order, request, **kwargs):
	try:
		#支付完成之后的webapp_user操作
		if hasattr(request, 'webapp_user'):
			request.webapp_user.complete_payment(request, order)
		#更新order的payment_time字段
		dt = datetime.now()
		payment_time = dt.strftime('%Y-%m-%d %H:%M:%S')
		Order.objects.filter(order_id=order.order_id).update(payment_time = payment_time)
		#发送模板消息
		try:
			from market_tools.tools.template_message.module_api import send_order_template_message
			send_order_template_message(order.webapp_id, order.id, 0)
		except:
			alert_message = u"post_pay_order_handler 发送模板消息失败, cause:\n{}".format(unicode_full_stack())
			watchdog_warning(alert_message)

		try:
			"""
				增加异步消息：修改会员消费次数和金额,平均客单价
			"""
			from modules.member.tasks import update_member_pay_info
			order.payment_time = payment_time
			update_member_pay_info(order)
		except:
			alert_message = u"post_pay_order_handler 修改会员消费次数和金额,平均客单价, cause:\n{}".format(unicode_full_stack())
			watchdog_warning(alert_message)
	except:
		alert_message = u"post_pay_order_handler处理失败, cause:\n{}".format(unicode_full_stack())
		if hasattr(request, 'user'):
			watchdog_alert(alert_message, type='WEB', user_id=str(request.user.id))
		else:
			watchdog_alert(alert_message, type='WEB')

	try:
		for relation in OrderHasProduct.objects.filter(order_id=order.id):
			product_id = relation.product_id
			count = relation.number
			if ProductSales.objects.filter(product_id=product_id).count() > 0:
				ProductSales.objects.filter(product_id=product_id).update(sales = F('sales') + count)
			else:
				ProductSales.objects.create(
					product_id = product_id,
					sales = count
				)
	except:
		if settings.DEBUG:
			raise
		else:
			alert_message = u"post_pay_order_handler处理失败, cause:\n{}".format(unicode_full_stack())
			if hasattr(request, 'user'):
				watchdog_alert(alert_message, type='WEB', user_id=str(request.user.id))
			else:
				watchdog_alert(alert_message, type='WEB')

	# try:
	# 	order_has_products = OrderHasProduct.objects.filter(order_id=order.id)
	# 	is_thanks_card_order = False
	# 	for order_has_product in order_has_products:
	# 		product = Product.objects.get(id = order_has_product.product_id)
	# 		if product.is_support_make_thanks_card:
	# 			is_thanks_card_order = True
	# 			for i in range(order_has_product.number):	#购买几个商品创建几个密码
	# 				secret = __gen_thanks_card_secret()
	# 				member_id = 0	#bdd测试不支持request.member
	# 				if request.member:
	# 					member_id = request.member.id
	# 				ThanksCardOrder.objects.create(
	# 					order_id= order.id,
	# 					thanks_secret= secret,
	# 					card_count= 0,
	# 					listen_count= 0,
	# 					is_used= False,
	# 					title='',
	# 					content='',
	# 					type=IMG_TYPE,
	# 					att_url='',
	# 					member_id=member_id)
	# 		if is_thanks_card_order:
	# 			Order.objects.filter(order_id=order.order_id).update(type = THANKS_CARD_ORDER)
	# except:
	# 	alert_message = u"post_pay_order_handler 生成感恩密码失败, cause:\n{}".format(unicode_full_stack())
	# 	if hasattr(request, 'user'):
	# 		watchdog_alert(alert_message, type='WEB', user_id=str(request.user.id))
	# 	else:
	# 		watchdog_alert(alert_message, type='WEB')

#############################################################################################
# create_delivery_product_handler: 创建一个与DeliveryPlan关联的product一模一样的product,
# 并将deliveryPlan关联新创建的product
# 该设计有个问题,没有考虑到规格以及规格的变动
#############################################################################################
@receiver(mall_signals.create_delivery_product, sender = DeliveryPlan)
def create_delivery_product_handler(delivery_plan, **keyword):
	try:
		product_id = delivery_plan.product_id
		product = Product.objects.get(id = product_id)

		#创建type=delivery的product
		delivery_product = Product.objects.create(
			owner_id = product.owner_id,
			name = delivery_plan.name,
			physical_unit = product.physical_unit,
			introduction = product.introduction,
			thumbnails_url = product.thumbnails_url,
			pic_url = product.pic_url,
			detail = product.detail,
			remark = product.remark,
			stock_type = 0,	#库存无限

			shelve_type = product.shelve_type,
			shelve_start_time = product.shelve_start_time,
			shelve_end_time = product.shelve_end_time,

			price = delivery_plan.price,	#价格
			type = 'delivery'
		)
		#将delivery_plan的product_id更新为delivery_product的id
		delivery_plan.product_id = delivery_product.id
		delivery_plan.save()

		#保持关联轮播图
		swipe_images = ProductSwipeImage.objects.filter(product_id = product_id)
		for swipe_image in swipe_images:
			ProductSwipeImage.objects.create(
				product = delivery_product,
				url = swipe_image.url
			)

		#创建ProductModel
		ProductModel.objects.create(
			owner_id = delivery_product.owner_id,
			product_id = delivery_product.id,
			name = 'standard',
			is_standard = 1,
			price = delivery_plan.price,
			stock_type = delivery_product.stock_type
			)
		#TODO: 确定是否不需要商品规格
	except:
		alert_message = u"create_delivery_product_handler处理失败, cause:\n{}".format(unicode_full_stack())
		watchdog_fatal(alert_message, type='WEB')


########################################################################
# __gen_thanks_card_secret: 生成感恩密码
########################################################################
def __gen_thanks_card_secret():
	secret = random.randint(1000000, 9999999)
	if ThanksCardOrder.objects.filter(thanks_secret=secret).count() > 0:
		return __gen_thanks_card_secret()
	else:
		return secret

#############################################################################################
# cancel_order_handler: 取消订单后触发的动作
# 1、重置该订单的感恩密码
# 2、删除订单统计表中的数据
#############################################################################################
@receiver(mall_signals.cancel_order, sender=Order)
def cancel_order_handler(order, **kwargs):
	from market_tools.tools.weizoom_card import module_api as weizoom_card_module_api
	from mall.promotion import models as promotion_models
	try:
		# 返还微众卡
		weizoom_card_module_api.return_weizoom_card_money(order)

		# 返还优惠券
		if order.coupon_id and order.coupon_id > 0:
			coupons = promotion_models.Coupon.objects.filter(id = order.coupon_id)
			if len(coupons) > 0:
				coupons.update(status = promotion_models.COUPON_STATUS_UNUSED)
				promotion_models.CouponRule.objects.filter(id = coupons[0].coupon_rule_id).update(use_count = F('use_count') - 1)
	except:
		alert_message = u"cancel_order_handler处理失败, cause:\n{}".format(unicode_full_stack())
		watchdog_fatal(alert_message, type='WEB')

	# 2、删除订单统计表中的数据
	PurchaseDailyStatistics.objects.filter(order_id=order.order_id).delete()


#############################################################################################
# 检查商品是否已下架
#############################################################################################
#@receiver(mall_signals.check_order_related_resource, sender=mall_signals)
@ignore_exception
def check_order_related_resource_handler(order, args, request, **kwargs):
	#检查是否有商品已下架
	products = order.products
	off_shelve_products = [product for product in products if product.shelve_type == PRODUCT_SHELVE_TYPE_OFF]
	if len(off_shelve_products) > 0:
		if len(off_shelve_products) == len(products):
			#所有商品下架，返回商品列表页
			return {
				'success': False,
				'data': {
					'msg': u'商品已下架<br/>2秒后返回商城首页',
					'redirect_url': '/workbench/jqm/preview/?module=mall&model=products&action=list&category_id=0&workspace_id=mall&woid=%s' % request.user_profile.user_id
				}
			}
		else:
			return {
				'success': False,
				'data': {
					'msg': u'有商品已下架<br/>2秒后返回购物车<br/>请重新下单',
					'redirect_url': '/workbench/jqm/preview/?module=mall&model=shopping_cart&action=show&workspace_id=mall&woid=%s' % request.user_profile.user_id
				}
			}
	else:
		return {
			'success': True
		}


#############################################################################################
# workspace_post_save_handler: save homepage workspace之后的handler
# 1、将workspace的id存储在user profile中
# TODO: 将其放入webapp/signal_handler.py中
#############################################################################################
@receiver(django_model_signals.post_save, sender=Workspace)
def workspace_post_save_handler(instance, created, **kwargs):
	if created:
		if instance.inner_name == 'home_page':
			UserProfile.objects.filter(user_id=instance.owner_id).update(homepage_workspace_id=instance.id)


def _get_province_id_by_area(area):
	"""
	根据area：2_2_22 , 来获取省份id(2)
	"""
	if area and len(area.split('_')):
		return area.split('_')[0]
	return 0


@receiver(mall_signals.pre_save_order, sender=mall_signals)
def postage_pre_save_order(pre_order, order, products, product_groups, **kwargs):
	"""计算订单运费
	"""
	postage_config = None
	for product in products:
		if product.postage_type == POSTAGE_TYPE_CUSTOM:
			postage_config = product.postage_config
			break

	province_id = _get_province_id_by_area(order.area)

	postage_calculator = mall_postage_calculator.PostageCalculator(postage_config)

	order.postage = postage_calculator.get_postage(products, province_id)
	order.final_price += order.postage


@receiver(mall_signals.pre_save_order, sender=mall_signals)
def coupon_pre_save_order(pre_order, order, products, product_groups, **kwargs):
	"""使用优惠券
	"""
	from mall.promotion import models as promotion_models

	if not pre_order.session_data.get('coupon', ''):
		return
	coupon = pre_order.session_data['coupon']

	order.coupon_id = coupon.id

	# 如果是通用优惠券
	if not coupon.coupon_rule.limit_product:
		# 会员折扣优惠的价格
		# cut = sum(map(lambda x: x.price*(1-x.member_discount)*x.purchase_count, products))

		# if order.final_price - cut < order.postage:
		# 	order.final_price = order.postage
		# else:
		# 	order.final_price -= cut
		order.final_price = sum(map(lambda x: x.price*x.purchase_count, products))
	else:
		limit_product_id = coupon.coupon_rule.limit_product_id
		final_price = sum(map(lambda x: x.price*x.purchase_count, products))
		limit_product = filter(lambda x: x.id == limit_product_id, products)
		lack_price = 0.0
		for p in limit_product:
			lack = (p.original_price - p.price) * p.purchase_count
			lack_price += lack
		final_price += lack_price
		order.final_price = final_price

	# 如果去掉优惠券价格后商品终价低于运费
	if order.final_price - coupon.money < order.postage:
		order.coupon_money = order.final_price - order.postage
		order.final_price = order.postage
	else:
		order.coupon_money = coupon.money
		order.final_price -= coupon.money

	coupon = promotion_models.Coupon.objects.filter(id=coupon.id)
	coupon_rule = promotion_models.CouponRule.objects.filter(id=coupon[0].coupon_rule_id)
	if not coupon[0].member_id:
		coupon_rule.update(remained_count=F('remained_count') - 1)
	coupon.update(status=promotion_models.COUPON_STATUS_USED)
	coupon_rule.update(use_count=F('use_count') + 1)


@receiver(mall_signals.check_order_related_resource, sender=mall_signals)
def check_coupon_for_order(pre_order, args, request, **kwargs):
	"""
	检查优惠券
	"""
	if not hasattr(pre_order, 'session_data'):
		pre_order.session_data = dict()

	fail_msg = {
		'success': False,
		'data': {
			'msg': u'',
			'redirect_url': '/workbench/jqm/preview/?module=mall&model=shopping_cart&action=show&workspace_id=mall&woid=%s' % request.user_profile.user_id
		}
	}
	is_use_coupon = (request.POST.get('is_use_coupon', 'false') == 'true')
	if is_use_coupon:
		coupon_id = request.POST.get('coupon_id', 0)
		order_price = [product.price * product.purchase_count for product in pre_order.products]
		product_ids = [str(product.id) for product in pre_order.products]

		from market_tools.tools.coupon import util as coupon_util
		msg, coupon = coupon_util.has_can_use_by_coupon_id(coupon_id, request.webapp_owner_id, order_price, product_ids, request.member.id)
		if coupon:
			pre_order.session_data['coupon'] = coupon
		else:
			fail_msg['data']['msg'] = msg
			return fail_msg
	return {
		'success': True
	}


@receiver(mall_signals.pre_save_order, sender=mall_signals)
def promotions_pre_save_order(pre_order, order, products, product_groups, **kwargs):
	"""执行促销，更新order.final_price, order.integral, order.integral_money.
	"""
	order.pre_yuan = pre_order.pre_yuan if hasattr(pre_order, 'pre_yuan') else 0
	for product_group in product_groups:
		promotion_result = product_group['promotion_result']
		if promotion_result:
			order.final_price -= promotion_result.get('final_saved_money', 0.000)

		if product_group['integral_sale_rule']:
			integral_sale_result = product_group['integral_sale_rule'].get('result', None)
			if integral_sale_result:
				use_integral = integral_sale_result['use_integral']
				if use_integral > 0:
					order.integral += use_integral
					order.integral_money += integral_sale_result['final_saved_money']
					order.final_price -= integral_sale_result['final_saved_money']
	if hasattr(pre_order, 'integral') and hasattr(pre_order, 'integral_money'):
		order.integral = pre_order.integral
		order.integral_money = pre_order.integral_money
		order.final_price -= pre_order.integral_money


def __fill_promotion_failed_reason(product_group, reason):
	if product_group.get('promotion_result', None):
		product_group['promotion_result']['failed_reason'] = reason
	else:
		pass
		# product_group['promotion_result'] = {
		# 	'can_use_promotion': False,
		# 	'reason': reason
		# }


def __check_integral(request, product_groups, data_detail, pre_order):
	"""检查积分应用、整单积分抵扣使用
	"""

	integralinfo = request.POST.get('group2integralinfo', None)
	count_per_yuan = request.webapp_owner_info.integral_strategy_settings.integral_each_yuan
	total_integral = 0
	if not integralinfo or integralinfo == '{}':
		if request.POST.get('orderIntegralInfo', None):
			# 整单抵扣
			# {"integral":100,"money":50}
			use_ceiling = request.webapp_owner_info.integral_strategy_settings.use_ceiling
			if use_ceiling < 0:
				return '积分抵扣尚未开启'
			orderIntegralInfo = json.loads(request.POST.get('orderIntegralInfo'))
			total_integral = orderIntegralInfo['integral']
			pre_order.integral = total_integral
			pre_order.integral_money = round(float(orderIntegralInfo['money']), 2)
			# 校验前台输入：积分金额不能大于使用上限、积分值不能小于积分金额对应积分值
			product_price = sum([product.price * product.purchase_count for product in pre_order.products])
			if (pre_order.integral_money - 1) > round(product_price * use_ceiling / 100, 2)\
				or (total_integral + 1) < (pre_order.integral_money * count_per_yuan):
				return '积分使用超限'
	else:
		#积分应用
		group2integralinfo = json.loads(integralinfo)
		group2integralsalerule = dict((group['uid'], group['integral_sale_rule']) for group in product_groups)
		uid2group = dict((group['uid'], group) for group in product_groups)
		for group_uid, integral_info in group2integralinfo.items():
			products = uid2group[group_uid]['products']
			if not group_uid in group2integralsalerule.keys() or not group2integralsalerule[group_uid]:
				for product in products:
					data_detail.append({
						'id': product.id,
						'model_name': product.model_name,
						'msg': '积分折扣已经过期',
						'short_msg': '已经过期'
					})
				continue
			use_integral = int(integral_info['integral'])
			# integral_info['money'] = integral_info['money'] *
			integral_money = round(float(integral_info['money']), 2) #round(1.0 * use_integral / count_per_yuan, 2)
			# 校验前台输入：积分金额不能大于使用上限、积分值不能小于积分金额对应积分值
			# 根据用户会员与否返回对应的商品价格
			# for product in products:
			# 	product.price = product.price * get_product_member_discount(product.member_discount, product)
			product_price = sum([product.price * product.purchase_count for product in products])
			integralsalerule = group2integralsalerule[group_uid]
			max_integral_price = round(product_price * integralsalerule['rule']['discount'] / 100, 2)

			if max_integral_price < (integral_money - 0.01) \
				or (integral_money * count_per_yuan) > (use_integral + 1):
				for product in products:
					data_detail.append({
							'id': product.id,
							'model_name': product.model_name,
							'msg': '使用积分不能大于促销限额',
							'short_msg': '积分应用',
						})

			integral_sale_rule = group2integralsalerule[group_uid]
			integral_sale_rule['result'] = {
				'final_saved_money': integral_money,
				'promotion_saved_money': integral_money,
				'use_integral': use_integral
			}
			total_integral += use_integral

	if total_integral > 0 and not request.webapp_user.can_use_integral(total_integral):
		return '积分不足'
	return None


@receiver(mall_signals.check_pre_order_related_resource, sender=mall_signals)
def check_promotions_for_pre_order(pre_order, args, request, **kwargs):
	"""
	检查促销活动是否可接受
	"""
	from mall.promotion import models as promotion_models
	fail_msg = {
		'success': False,
		'data': {
			'msg': u'',
			'redirect_url': '/workbench/jqm/preview/?module=mall&model=shopping_cart&action=show&workspace_id=mall&woid=%s' % request.user_profile.user_id
		}
	}
	data_detail = []
	"""
	促销不可接受数据

	data_detail = [{
		'id': 商品id,
		'model_name': 规格信息
		'short_msg': 不接受原因，4字以内,
		'msg': 不接受原因
	}]
	"""
	product_groups = pre_order.product_groups
	today = datetime.today()
	# 赠品所需数量
	id2premium_count = dict()
	id2flashsale = dict()
	for product_group in product_groups:
		promotion = product_group['promotion']
		if not promotion:
			first_product = product_group['products'][0]
			if hasattr(first_product, 'used_promotion_id') and int(getattr(first_product, 'used_promotion_id')) != 0:
				for product in product_group['products']:
					data_detail.append({
						'id': product.id,
						'msg': '该活动已经过期',
						'model_name': product.model_name,
						'short_msg': '已经过期',
						'inner_step': 1
					})
				__fill_promotion_failed_reason(product_group, "promotion == null and first_product.used_promotion_id, 活动过期0")
				continue
			else:
				__fill_promotion_failed_reason(product_group, 'no promotion')
				continue

		first_product = product_group['products'][0]
		if first_product.used_promotion_id == 0:
			__fill_promotion_failed_reason(product_group, 'first_product.used_promotion_id == 0')
			#不使用促销
			continue

		if promotion['type'] == promotion_models.PROMOTION_TYPE_COUPON:
			__fill_promotion_failed_reason(product_group, 'promotion is coupon')
			# 优惠券不检查
			continue

		if promotion['id'] != first_product.used_promotion_id:
			#商品携带的“促销活动”与商品当前关联的促销活动不一致，意味着商品携带的促销活动已结束
			for product in product_group['products']:
				data_detail.append({
					'id': product.id,
					'msg': '该活动已经过期',
					'model_name': product.model_name,
					'short_msg': '已经过期',
					'inner_step': 2
				})
			__fill_promotion_failed_reason(product_group, "promotion['id'] != first_product.used_promotion_id, 活动过期1")
			continue

		if promotion['status'] == promotion_models.PROMOTION_STATUS_NOT_START or\
			datetime.strptime(promotion['start_date'], '%Y-%m-%d %H:%M:%S') > today:
			for product in product_group['products']:
				data_detail.append({
						'id': product.id,
						'model_name': product.model_name,
						'msg': '该活动尚未开始',
						'short_msg': '尚未开始'
					})
			__fill_promotion_failed_reason(product_group, "活动未开始")
			continue

		if promotion['status'] > promotion_models.PROMOTION_STATUS_STARTED or\
			datetime.strptime(promotion['end_date'], '%Y-%m-%d %H:%M:%S') < today:
			for product in product_group['products']:
				data_detail.append({
						'id': product.id,
						'model_name': product.model_name,
						'msg': '该活动已经过期',
						'short_msg': '已经过期',
						'inner_step': 3
					})
			__fill_promotion_failed_reason(product_group, "活动过期2")
			continue
		if promotion['member_grade_id'] > 0 and promotion['member_grade_id'] != request.member.grade_id:
			for product in product_group['products']:
				data_detail.append({
						'id': product.id,
						'msg': '您的会员等级不满足促销条件',
						'model_name': product.model_name,
						'short_msg': '活动等级'
					})
			__fill_promotion_failed_reason(product_group, "会员等级不满足促销条件")
			continue

		detail = promotion['detail']

		if promotion['type'] == promotion_models.PROMOTION_TYPE_FLASH_SALE:
			# 限时抢购
			product = product_group['products'][0]
			promotion_id = promotion['id']

			#检查是否超过了限购周期的限制
			if int(detail['limit_period']) in (-1, 0):
				pass
			else:
				delta = datetime.today() - timedelta(days=detail['limit_period'])
				purchase_records = OrderHasPromotion.objects.filter(
					Q(webapp_user_id=request.webapp_user.id) &
					Q(promotion_id=promotion_id) &
					Q(created_at__gte=delta) &
					~Q(order__status=ORDER_STATUS_CANCEL)
				)
				# 限购周期内已购买过商品
				if purchase_records.count() > 0:  #
					data_detail.append({
						'id': product.id,
						'model_name': product.model_name,
						'msg': '在限购周期内不能多次购买',
						'short_msg': '限制购买'
					})
					continue

			if promotion_id in id2flashsale:
				flash_sale = id2flashsale[promotion_id]
				flash_sale['total_count'] = flash_sale['total_count'] + product.purchase_count
				flash_sale['product'].append(product)
			else:
				id2flashsale[promotion_id] = {
					'count_per_purchase': promotion['detail']['count_per_purchase'],
					'total_count': product.purchase_count,
					'product': [product]
				}

			product_group['promotion_result'] = {
				'promotion_saved_money': (product.price - detail['promotion_price']) * product.purchase_count,
				'promotioned_product_price': detail['promotion_price']
			}
			#用抢购价替换商品价格
			product.price = detail['promotion_price']
		# elif promotion['type'] == promotion_models.PROMOTION_TYPE_INTEGRAL_SALE:
		# 	# 积分应用
		# 	product = product_group['products'][0]
		# 	#由于冒号':'不是一个有效的dom selector，所以在前端，':'被替换成了'-'
		# 	_product_model_name = product.model['name'].replace(':', '-')
		# 	is_use_integral = request.POST.get('is_use_integral_%s_%s' % (product.id, _product_model_name), None)
		# 	if is_use_integral and is_use_integral == 'on':
		# 		# 用户页面勾选积分
		# 		use_integral = int(request.POST.get('integral_%s_%s' % (product.id, _product_model_name), 0))
		# 		if use_integral > 0:
		# 			if not promotion['detail']['is_permanant_active']:
		# 				# 积分不是永久有效，需要验证积分活动开始结束时间
		# 				if promotion['status'] == promotion_models.PROMOTION_STATUS_NOT_START or\
		# 					datetime.strptime(promotion['start_date'], '%Y-%m-%d %H:%M:%S') > today:
		# 					for product in product_group['products']:
		# 						data_detail.append({
		# 								'id': product.id,
		# 								'model_name': product.model_name,
		# 								'msg': '该活动尚未开始',
		# 								'short_msg': '尚未开始'
		# 							})
		# 					continue
		# 				if promotion['status'] > promotion_models.PROMOTION_STATUS_STARTED or\
		# 					datetime.strptime(promotion['end_date'], '%Y-%m-%d %H:%M:%S') < today:
		# 					for product in product_group['products']:
		# 						data_detail.append({
		# 								'id': product.id,
		# 								'model_name': product.model_name,
		# 								'msg': '该活动已经过期',
		# 								'short_msg': '已经过期',
		# 								'inner_step': 4
		# 							})
		# 					continue
		# 			# 用户页面计算积分大于零
		# 			count_per_yuan = request.webapp_user.integral_info['count_per_yuan']
		# 			limit_count = product.total_price * ((detail['discount']+0.0) / 100) * count_per_yuan
		# 			if limit_count >= use_integral:
		# 				integral_money = round(1.0 * use_integral / count_per_yuan, 2)
		# 				product_group['promotion_result'] = {
		# 					'final_saved_money': integral_money,
		# 					'promotion_saved_money': integral_money,
		# 					'use_integral': use_integral
		# 				}
		# 			else:
		# 				fail_msg['data']['msg'] = '使用积分不能大于促销限额'
		# 				data_detail.append({
		# 					'id': product.id,
		# 					'model_name': product.model_name,
		# 					'msg': fail_msg['data']['msg'],
		# 					'short_msg': '积分应用',
		# 				})
		# 				# return fail_msg
		elif promotion['type'] == promotion_models.PROMOTION_TYPE_PRICE_CUT:
			total_price = 0.0
			for product in product_group['products']:
				total_price += product.price * product.purchase_count

			if total_price < detail['price_threshold']:
				#订单金额小于满减阈值
				continue

			if detail['is_enable_cycle_mode']:
				# 循环满减
				count = int(total_price / float(detail['price_threshold']))
				final_saved_money = count * float(detail['cut_money'])
			else:
				final_saved_money = float(detail['cut_money'])

			product_group['promotion_result']['final_saved_money'] = final_saved_money
			product_group['promotion_result']['promotion_saved_money'] = final_saved_money
		elif promotion['type'] == promotion_models.PROMOTION_TYPE_PREMIUM_SALE:
			# 买赠
			total_purchase_count = 0
			for product in product_group['products']:
				total_purchase_count += product.purchase_count

			detail = product_group['promotion']['detail']
			if total_purchase_count >= detail['count']:
				#确定赠送轮数
				if detail['is_enable_cycle_mode']:
					premium_round_count = total_purchase_count / detail['count']
				else:
					premium_round_count = 1

				premium_products = []
				# for i in range(premium_count):
				for premium_product in detail['premium_products']:
					premium_products.append({
						"id": premium_product['id'],
						"name": premium_product['name'],
						"bar_code": premium_product['id'],
						"price": premium_product['current_used_model']['price'],
						"count": premium_product['premium_count'],
						"thumbnails_url": premium_product['thumbnails_url'],
						"forcing_submit": request.POST.get("forcing_submit", None),
					})

					# 检查赠品库存
					if request.POST.get("forcing_submit", None):
						continue
					if id2premium_count.has_key(premium_product['id']):
						id2premium_count[premium_product['id']] += premium_product['premium_count']
					else:
						id2premium_count[premium_product['id']] = premium_product['premium_count']
				product_group['promotion_result'] = {
					'premium_products': premium_products
				}
			else:
				product_group['promotion_result'] = None

	# 检查赠品库存
	if len(id2premium_count) > 0:
		# 主商品中有赠品于的情况
		mastproductid2count = dict()
		for product in pre_order.products:
			if id2premium_count.has_key(product.id):
				id2premium_count[product.id] += product.purchase_count
				mastproductid2count[product.id] = product.purchase_count

		productids = [productid for productid, count in id2premium_count.items()]
		products = []
		for productid in productids:
			products.append(Product(id=productid))

		Product.fill_model_detail(0, products, productids)
		for product in products:
			model = product.standard_model
			if model['stock_type'] != PRODUCT_STOCK_TYPE_LIMIT:
				continue
			elif model['stocks'] < id2premium_count[product.id]:
				# 库存不足 TODO 去掉读取数据库
				product = Product.objects.get(id=product.id)
				msg = '库存不足'
				if model['stocks'] <= 0:
					msg = '已赠完'
				data_detail.append({
					'id': product.id,
					'msg': msg,
					'short_msg': msg,
					'name': product.name,
					'pic_url': product.thumbnails_url,
					'stocks': model['stocks'] - mastproductid2count[product.id] if product.id in mastproductid2count else 0,
					'need_stocks': id2premium_count[product.id]
				})

	#检查限时抢购
	if len(id2flashsale) > 0:
		for promotion_id, flash_sale in id2flashsale.items():
			if flash_sale['count_per_purchase'] < flash_sale['total_count']:
				for product in flash_sale['product']:
					fail_msg['data']['msg'] = '限购%d件' % flash_sale['count_per_purchase']
					data_detail.append({
						'id': product.id,
						'model_name': product.model_name,
						'msg': fail_msg['data']['msg'],
						'short_msg': fail_msg['data']['msg'],
					})

	#检查积分应用
	msg = __check_integral(request, product_groups, data_detail, pre_order)
	if msg:
		fail_msg['data']['msg'] = msg
	if len(data_detail) > 0 or fail_msg['data']['msg'] != '':
		fail_msg['data']['detail'] = data_detail
		return fail_msg

	return {
		'success': True
	}
mall_signals.check_order_related_resource.connect(check_promotions_for_pre_order, sender=mall_signals, dispatch_uid = "check_order_related_resource:check_promotions_for_pre_order")


@receiver(mall_signals.check_pre_order_related_resource, sender=mall_signals)
def check_stocks_for_pre_order(pre_order, args, request, **kwargs):
	"""
	检查商品库存是否满足下单条件
	@todo 改为基于redis的并发安全的实现
	"""
	from mall import module_api as mall_api

	fail_msg = {
		'success': False,
		'data': {
			'msg': u'有商品库存不足<br/>2秒后返回购物车<br/>请重新下单',
			'redirect_url': '/workbench/jqm/preview/?module=mall&model=shopping_cart&action=show&workspace_id=mall&woid=%s' % request.user_profile.user_id,
			'detail': []
		}
	}
	products = pre_order.products
	mall_api.fill_realtime_stocks(products)
	for product in products:
		for model in product.models:
			if product.model_name == model['name']:
				product.stock_type = model['stock_type']
				product.stocks = model['stocks']
				if model.get('is_deleted', True):
					fail_msg['data']['detail'].append({
						'id': product.id,
						'model_name': product.model_name,
						'msg': '有商品规格已删除，请重新下单',
						'short_msg': '已删除'
					})

		if product.stock_type == PRODUCT_STOCK_TYPE_LIMIT and product.purchase_count > product.stocks:
			if product.stocks == 0:
				fail_msg['data']['detail'].append({
					'id': product.id,
					'model_name': product.model_name,
					'msg': '有商品已售罄，请重新下单',
					'short_msg': '已售罄'
				})
			else:
				fail_msg['data']['detail'].append({
					'id': product.id,
					'model_name': product.model_name,
					'msg': '有商品库存不足，请重新下单',
					'short_msg': '库存不足'
				})
	if len(fail_msg['data']['detail']) > 0:
		return fail_msg
	return {
		'success': True
	}
mall_signals.check_order_related_resource.connect(check_stocks_for_pre_order, sender=mall_signals, dispatch_uid = "check_order_related_resource:check_stocks_for_pre_order")


@receiver(mall_signals.check_pre_order_related_resource, sender=mall_signals)
def check_deleted_product_for_pre_order(pre_order, args, request, **kwargs):
	"""
	检查商品是否已被删除
	"""
	products = pre_order.products
	for product in products:
		if product.is_model_deleted or product.is_deleted:
			return {
				'success': False,
				'data': {
					'msg': u'有商品已被删除<br/>2秒后返回购物车<br/>请重新下单',
					'redirect_url': '/workbench/jqm/preview/?module=mall&model=shopping_cart&action=show&workspace_id=mall&woid=%s' % request.user_profile.user_id,
					'detail': [{
						'id': product.id,
						'model_name': product.model_name,
						'msg': '有商品已被删除，请重新下单',
						'short_msg': '已删除'
					}]
				}
			}

	return {
		'success': True
	}
mall_signals.check_order_related_resource.connect(check_deleted_product_for_pre_order, sender=mall_signals, dispatch_uid = "check_order_related_resource:check_deleted_product_for_pre_order")


@receiver(mall_signals.check_pre_order_related_resource, sender=mall_signals)
def check_shelve_type_for_pre_order(pre_order, args, request, **kwargs):
	"""
	检查商品是否已下架
	"""
	products = pre_order.products
	off_shelve_products = [product for product in products if not product.is_model_deleted and not product.is_deleted and product.shelve_type != PRODUCT_SHELVE_TYPE_ON]
	if len(off_shelve_products) > 0:
		data_detail = []
		for off_shelve_product in off_shelve_products:
			data_detail.append({
					'id': off_shelve_product.id,
					'msg': '商品已下架, 请重新下单',
					'model_name': product.model_name,
					'short_msg': '已下架'
				})
		if len(off_shelve_products) == len(products):
			#所有商品下架，返回商品列表页
			return {
				'success': False,
				'data': {
					'msg': u'商品已下架<br/>2秒后返回商城首页',
					'redirect_url': '/workbench/jqm/preview/?module=mall&model=products&action=list&category_id=0&workspace_id=mall&woid=%s' % request.user_profile.user_id,
					'detail': data_detail
				}
			}
		else:
			return {
				'success': False,
				'data': {
					'msg': u'有商品已下架<br/>2秒后返回购物车<br/>请重新下单',
					'redirect_url': '/workbench/jqm/preview/?module=mall&model=shopping_cart&action=show&workspace_id=mall&woid=%s' % request.user_profile.user_id,
					'detail': data_detail
				}
			}
	else:
		return {
			'success': True
		}
mall_signals.check_order_related_resource.connect(check_shelve_type_for_pre_order, sender=mall_signals, dispatch_uid = "check_order_related_resource:check_shelve_type_for_pre_order")


@receiver(mall_signals.post_save_order, sender=mall_signals)
def weizoom_card_log_for_order(order, webapp_user, **kwargs):
	"""
	记录微众卡日志
	"""
	from market_tools.tools.weizoom_card import module_api as weizoom_card_api
	from market_tools.tools.weizoom_card import models as weizoom_card_model
	if not order.session_data.has_key('weizoom_card'):
		return
	for card in order.session_data['weizoom_card']:
		weizoom_card_api.create_weizoom_card_log(
			order.session_data['webapp_owner_id'],
			order.order_id,
			weizoom_card_model.WEIZOOM_CARD_LOG_TYPE_BUY_USE,
			card.id,
			card.use_price)


@receiver(mall_signals.post_save_order, sender=mall_signals)
def post_save_order_handler_for_integral(order, webapp_user, **kwargs):
	"""
	订单保存后，更新webapp user的积分值
	"""
	webapp_user.use_integral(order.integral)


@receiver(mall_signals.post_save_order, sender=mall_signals)
def post_save_order_handler_for_product_sales(order, webapp_user, product_groups, **kwargs):
	"""
	订单保存后，赠品库存
	"""
	from mall.promotion import models as promotion_models
	for product_group in product_groups:
		promotion = product_group['promotion']
		if not promotion or promotion['type'] != promotion_models.PROMOTION_TYPE_PREMIUM_SALE:
			continue
		if product_group['promotion_result'] and 'premium_products' in product_group['promotion_result']:
			for product in product_group['promotion_result']['premium_products']:
				productModel = ProductModel.objects.filter(product_id=product['id'], name='standard');
				if len(productModel) != 1:
					# 多规格商品，前台配置错误不处理库存
					continue
				product_model = productModel[0]
				if product_model.stock_type == PRODUCT_STOCK_TYPE_LIMIT:
					if product_model.stocks < product['count']:
						product['count'] = product_model.stocks
					if product['count'] > 0:
						ProductModel.objects.filter(id=productModel[0].id).update(stocks = F('stocks') - product['count'])


@receiver(mall_signals.pre_save_order, sender=mall_signals)
def weizoom_card_pre_save_order(pre_order, order, products, product_groups, **kwargs):
	"""扣除微众卡金额
	"""
	order.weizoom_card_money = 0
	if not pre_order.session_data.has_key('weizoom_card'):
		return
	cards = pre_order.session_data['weizoom_card']
	from market_tools.tools.weizoom_card import module_api as weizoom_card_api
	for card in cards:
		use_price = weizoom_card_api.use_weizoom_card(card, order.final_price)
		order.final_price -= use_price
		order.weizoom_card_money += use_price
		card.use_price = use_price
	order.session_data['weizoom_card'] = cards


@receiver(mall_signals.check_order_related_resource, sender=mall_signals)
def check_weizoom_card_for_order(pre_order, args, request, **kwargs):
	"""
	检查微众卡是否可用
	"""
	if not hasattr(pre_order, 'session_data'):
		pre_order.session_data = dict()
	from market_tools.tools.weizoom_card import module_api as weizoom_card_api
	card_name = request.POST.get('card_name', '')
	card_pass = request.POST.get('card_pass', '')

	card_passes = card_pass.split(',')
	card_names = card_name.split(',')
	fail_msg = {
			'success': False,
			'data': {
				'msg': None,
				'redirect_url': '/workbench/jqm/preview/?module=mall&model=shopping_cart&action=show&workspace_id=mall&woid=%s' % request.user_profile.user_id
			}
		}
	if len(card_passes) > 0:
		if len(card_passes) > 11:
			fail_msg['data']['msg'] = '微众卡只能使用十张'
			return fail_msg
		if len(set(card_names)) != len(card_passes):
			fail_msg['data']['msg'] = '该微众卡已经添加'
			return fail_msg
		card_index = 0
 		pre_order.session_data['weizoom_card'] = []
	 	for card_name in card_names:
	 		msg = None
	 		if len(card_passes) > card_index and len(card_name) > 0:
	 			msg, weizoom_card = weizoom_card_api.check_weizoom_card(card_name, card_passes[card_index], request.webapp_owner_id)
		 		if msg:
		 			fail_msg['data']['msg'] = msg
					return fail_msg
				else:
					pre_order.session_data['weizoom_card'].append(weizoom_card)
			card_index += 1
	return {
		'success': True
	}


@receiver(mall_signals.post_ship_send_request_to_kuaidi, sender=Order)
def send_request_to_kuaidi(order, **kwargs):
	"""
	向快递100发送订阅请求
	"""
	if settings.IS_UNDER_BDD:
		# BDD 暂时不测试快递100信息
		return
	from tools.express.express_poll import ExpressPoll
	print u'------------ send_request_to_kuaidi order.status:{}'.format(order.status)
	# if order.status == ORDER_STATUS_PAYED_SHIPED:
	is_success = ExpressPoll(order).get_express_poll()
	print u'----------- send_request_to_kuaidi: {}'.format(is_success)



#############################################################################################
# post_update_product_model_property_handler: post_update_product_model_property的handler
#############################################################################################
@receiver(mall_signals.products_not_online, sender=Product)
def products_not_online_handler_for_promotions(product_ids, request, **kwargs):
	from mall.promotion import models as promotion_models
	from webapp.handlers import event_handler_util
	disable_coupon = False
	shelve_type = request.POST.get('shelve_type')
	if shelve_type and shelve_type == 'delete':
		disable_coupon = True

	target_promotion_ids = []
	promotionIds =[relation.promotion_id for relation in promotion_models.ProductHasPromotion.objects.filter(
		product_id__in=product_ids)]
	for promotion in promotion_models.Promotion.objects.filter(id__in=promotionIds):
		if promotion.type != promotion_models.PROMOTION_TYPE_COUPON:
			target_promotion_ids.append(str(promotion.id))
		elif disable_coupon:
			promotion.status = promotion_models.PROMOTION_STATUS_DISABLE
			promotion.save()
			promotion_models.CouponRule.objects.filter(id=promotion.detail_id).update(is_active=False)

	if len(target_promotion_ids) > 0:
		event_data = {
			"id": ','.join(target_promotion_ids)
		}
		event_handler_util.handle(event_data, 'finish_promotion')
