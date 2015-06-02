# -*- coding: utf-8 -*-
from datetime import datetime
import random

from django.dispatch import Signal
from django.dispatch.dispatcher import receiver
from django.db.models import signals as django_model_signals

from webapp.modules.mall import signals as mall_signals
#import webapp.modules.mall.signals as mall_signals
from .models import *
from webapp.models import Workspace
from account.models import UserProfile
from watchdog.utils import watchdog_alert, watchdog_fatal, watchdog_warning, watchdog_error, watchdog_info
from core.exceptionutil import unicode_full_stack
from market_tools.tools.delivery_plan.models import  DeliveryPlan
from market_tools.tools.template_message.module_api import send_order_template_message
from core.common_util import ignore_exception

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
# @receiver(mall_signals.pre_delete_product_model_property, sender=ProductModelProperty)
# def pre_delete_product_model_property_handler(model_property, request, **kwargs):
# 	try:
# 		#获得更新后的property:value集合
# 		updated_property_values = set()
# 		for property_value in ProductModelPropertyValue.objects.filter(property=model_property, is_deleted=False):
# 			updated_property_values.add(property_value.id)

# 		#获取property已经被删除的model
# 		invalid_models = set()
# 		for relation in ProductModelHasPropertyValue.objects.filter(property_id=model_property.id):
# 			if relation.property_id != model_property.id:
# 				continue

# 			invalid_models.add(relation.model_id)

# 		#获得这些model关联的product
# 		product_ids = set(list(ProductModel.objects.filter(id__in=invalid_models).values_list('product_id', flat=True)))
		
# 		#删除这一批model
# 		ProductModel.objects.filter(id__in=invalid_models).update(is_deleted=True)

# 		#下架商品
# 		for product_id in product_ids:
# 			Product.objects.filter(id=product_id).update(shelve_type=PRODUCT_SHELVE_TYPE_OFF)
# 			from module_api import remove_product_from_all_shopping_cart
# 			remove_product_from_all_shopping_cart(product_id=product_id)
# 	except:
# 		alert_message = u"pre_delete_product_model_property_handler处理失败, cause:\n{}".format(unicode_full_stack())
# 		if hasattr(request, 'user'):
# 			watchdog_alert(alert_message, type='WEB', user_id=str(request.user.id))
# 		else:
# 			watchdog_alert(alert_message, type='WEB')

@receiver(mall_signals.post_pay_order, sender=Order)
def post_pay_order_handler(order, request, **kwargs):
	try:
		#支付完成之后的webapp_user操作
		request.webapp_user.complete_payment(request, order)
		#更新order的payment_time字段
		dt = datetime.now()
		payment_time = dt.strftime('%Y-%m-%d %H:%M:%S')
		Order.objects.filter(order_id=order.order_id).update(payment_time = payment_time)
		#发送模板消息
		try:
			send_order_template_message(order.webapp_id, order.id, 0)
		except:
			alert_message = u"post_pay_order_handler 发送模板消息失败, cause:\n{}".format(unicode_full_stack())
			watchdog_warning(alert_message)
	except:
		alert_message = u"post_pay_order_handler处理失败, cause:\n{}".format(unicode_full_stack())
		if hasattr(request, 'user'):
			watchdog_alert(alert_message, type='WEB', user_id=str(request.user.id))
		else:
			watchdog_alert(alert_message, type='WEB')

	try:
		order_has_products = OrderHasProduct.objects.filter(order_id=order.id)
		is_thanks_card_order = False
		for order_has_product in order_has_products:
			product = Product.objects.get(id = order_has_product.product_id)
			if product.is_support_make_thanks_card:
				is_thanks_card_order = True
				for i in range(order_has_product.number):	#购买几个商品创建几个密码
					secret = __gen_thanks_card_secret()
					member_id = 0	#bdd测试不支持request.member
					if request.member:
						member_id = request.member.id
					ThanksCardOrder.objects.create(
						order_id= order.id,
						thanks_secret= secret,
						card_count= 0,
						listen_count= 0,
						is_used= False,
						title='',
						content='',
						type=IMG_TYPE,
						att_url='',
						member_id=member_id)
			if is_thanks_card_order:
				Order.objects.filter(order_id=order.order_id).update(type = THANKS_CARD_ORDER)
	except:
		alert_message = u"post_pay_order_handler 生成感恩密码失败, cause:\n{}".format(unicode_full_stack())
		if hasattr(request, 'user'):
			watchdog_alert(alert_message, type='WEB', user_id=str(request.user.id))
		else:
			watchdog_alert(alert_message, type='WEB')

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
from market_tools.tools.weizoom_card import module_api as weizoom_card_module_api
@receiver(mall_signals.cancel_order, sender=Order)
def cancel_order_handler(order, **kwargs):
	try:
		thanks_card_orders = ThanksCardOrder.objects.filter(order_id=order.id)
		for thanks_card_order in thanks_card_orders:
			thanks_card_order.thanks_secret = __gen_thanks_card_secret()
			thanks_card_order.is_used=False
			thanks_card_order.content=''
			thanks_card_order.att_url=''
			thanks_card_order.card_count=0
			thanks_card_order.listen_count=0
			thanks_card_order.save()
	except:
		alert_message = u"cancel_order_handler处理失败, cause:\n{}".format(unicode_full_stack())
		watchdog_fatal(alert_message, type='WEB')

	try:
		weizoom_card_module_api.return_weizoom_card_money(order)
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
