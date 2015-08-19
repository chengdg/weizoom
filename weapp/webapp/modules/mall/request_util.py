# -*- coding: utf-8 -*-
from __future__ import absolute_import
import time
from datetime import datetime
import json
import copy

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response
# jz 2015-08-11
# from django.contrib.auth.decorators import login_required, permission_required
# from django.contrib.auth.models import User, Group, Permission
# from django.contrib import auth
# from django.contrib import messages
# from core.jsonresponse import JsonResponse, create_response
# from core.dateutil import get_today
from core.exceptionutil import unicode_full_stack
from mall.module_api import check_product_review_overdue

from watchdog.utils import watchdog_info, watchdog_error
from mall.models import *
from mall import models as mall_models
from mall import signals as mall_signals
from mall import module_api as mall_api
from . import utils
from webapp.modules.mall import util as mall_util
from modules.member import util as member_util
from modules.member import member_settings
from modules.member.models import *
from account.models import *
from mall.promotion import models as coupon_model
from market_tools.tools.delivery_plan import models as delivery_plan_model
from market_tools.tools.weizoom_card import models as weizoom_card_model
from mall.promotion import models as promotion_models

from tools.regional.models import City, Province, District
from tools.regional.views import get_str_value_by_string_ids
from core.send_order_email_code import *
from watchdog.utils import *
import mall.signal_handler
from webapp import util as webapp_util

from cache import webapp_cache

page_title = u'微众商城'


########################################################################
#      PAGE FOR TESTING - 测试用页面
#
# list_coupons: 显示"优惠券"页面
########################################################################
# jz 2015-08-10
# def list_coupons(request):
# 	profile = request.user_profile
# 	coupons = list(coupon_model.Coupon.objects.filter(owner=profile.user, member_id=0))

# 	c = RequestContext(request, {
# 		'is_hide_weixin_option_menu': True,
# 		'page_title': u'【测试】优惠券列表',
# 		'coupons': coupons
# 	})
# 	return render_to_response('%s/coupons.html' % request.template_dir, c)


########################################################################
# get_productcategory: 显示“商品分类”页面
########################################################################
# jz 2015-08-10
# def get_productcategory(request):
# 	category_id = request.GET['rid']

# 	try:
# 		product = Product.objects.get(id=product_id)
# 	except:
# 		product = {'is_deleted': True}

# 	#获得swipe image
# 	swipe_images = []
# 	swipe_images.append({
# 		"url": product.pic_url,
# 		"caption": '',
# 		"link_url": '#'
# 	})

# 	#获得购物车数量
# 	shopping_cart_product_nums = mall_api.get_shopping_cart_product_nums(request.webapp_user)

# 	#获得运费
# 	# product.postage_config, product.postage = mall_util.get_postage_for_weight(request.webapp_owner_id, product.weight)

# 	c = RequestContext(request, {
# 		'is_hide_weixin_option_menu': True,
# 		'page_title': u'商品分类',
# 		'swipe_images': swipe_images,
# 		'swipe_image_count': len(swipe_images),
# 		'swipe_images_json': json.dumps(swipe_images),
# 		'product': product,
# 		'shopping_cart_product_nums': shopping_cart_product_nums,
# 		'is_enable_get_coupons': settings.IS_IN_TESTING
# 	})
# 	return render_to_response('%s/product_detail.html' % request.template_dir, c)


########################################################################
# list_products: 显示"商品列表"页面
########################################################################
def list_products(request):
	# 得到会员对应的折扣
	# discount = get_member_discount(member)

	category_id = int(request.GET.get('category_id', 0))

	category, products = webapp_cache.get_webapp_products(request.user_profile, request.is_access_weizoom_mall, category_id)
	product_categories = webapp_cache.get_webapp_product_categories(request.user_profile, request.is_access_weizoom_mall)

	for p in products:
		if p.promotion:
			p.promotion_js = json.dumps(p.promotion)

	has_category = False
	if len(product_categories) > 0:
		has_category = True
	c = RequestContext(request, {
		'page_title': u'商品列表(%s)' % (category.name if hasattr(category, 'name') else category['name']),
		'products': products,
		'category': category,
		'is_deleted_data': category.is_deleted if hasattr(category, 'is_deleted') else False,
		#'shopping_cart_product_nums': mall_api.get_shopping_cart_product_nums(request.webapp_user),
		'product_categories': product_categories,
		'has_category': has_category,
		'hide_non_member_cover': True
	})
	if hasattr(request, 'is_return_context'):
		return c
	if request.user.is_weizoom_mall:
		return render_to_response('%s/products.html' % request.template_dir, c)
	else:
		return render_to_response('%s/products_original.html' % request.template_dir, c)


#added by chuter
# jz 2015-08-10
# def _get_has_deleted_product_response(request, webapp_user, product):
# 	#获得购物车数量
# 	shopping_cart_product_nums = mall_api.get_shopping_cart_product_nums(webapp_user)

# 	c = RequestContext(request, {
# 		'swipe_images': None,
# 		'swipe_image_count': 0,
# 		'swipe_images_json': '{}',
# 		'product': product,
# 		'shopping_cart_product_nums': shopping_cart_product_nums,
# 		'is_enable_get_coupons': settings.IS_IN_TESTING
# 	})
# 	return render_to_response('%s/product_detail.html' % request.template_dir, c)


########################################################################
# get_product: 显示“商品详情”页面
########################################################################
def get_product(request):
	product_id = request.GET['rid']
	webapp_user = request.webapp_user

	member_grade_id = request.member.grade_id if request.member else None
	# 检查置顶评论是否过期
	check_product_review_overdue(product_id)
	product = mall_api.get_product_detail(request.webapp_owner_id, product_id, webapp_user, member_grade_id)
	# jz 2015-08-10
	#product.fill_model()

	if product.is_deleted:
		c = RequestContext(request, {
			'is_deleted_data': True
		})
		return render_to_response('%s/product_detail.html' % request.template_dir, c)

	if product.promotion:
		product.promotion['is_active'] = product.promotion_model.is_active
	jsons = [{
		"name": "models",
		"content": product.models
	}, {
		'name': 'priceInfo',
		'content': product.price_info
	}, {
		'name': 'promotion',
		'content': product.promotion
	}]
	#获得运费计算因子
	# jz 2015-08-10
	#postage_factor = mall_util.get_postage_factor(request.webapp_owner_id, product=product)

	###################################################
	non_member_followurl = None
	if request.user.is_weizoom_mall:
		product.is_can_buy_by_product(request)
		otherProfile = UserProfile.objects.get(user_id=product.owner_id)
		otherSettings = OperationSettings.objects.get(owner=otherProfile.user)
		if otherSettings.weshop_followurl.startswith('http://mp.weixin.qq.com'):
			non_member_followurl = otherSettings.weshop_followurl

			# liupeiyu 记录点击关注信息
			non_member_followurl = './?woid={}&module=mall&model=concern_shop_url&action=show&product_id={}&other_owner_id={}'.format(request.webapp_owner_id, product.id, product.owner.id)

	request.should_hide_footer = True

	usable_integral = request.member.integral if request.member else 0
	use_integral = request.member.integral if request.member else 0

	is_non_member = True if request.member else False

	c = RequestContext(request, {
		'page_title': product.name,
		'product': product,
		'jsons': jsons,
		'is_deleted_data': product.is_deleted if hasattr(product, 'is_deleted') else False,
		# jz 2015-08-10
		# 'is_enable_get_coupons': settings.IS_IN_TESTING,
		'model_property_size': len(product.product_model_properties),
		# jz 2015-08-10
		# 'postage_factor': json.dumps(product.postage_factor),
		'hide_non_member_cover': True,
		'non_member_followurl': non_member_followurl,
		'price_info': product.price_info,
		'usable_integral': usable_integral,
		'use_integral': use_integral,
		'is_non_member': is_non_member,
		'per_yuan': request.webapp_owner_info.integral_strategy_settings.integral_each_yuan,
		#add by bert 增加分享时显示信息
		'share_page_desc': product.name,
		'share_img_url': product.thumbnails_url
	})

	if hasattr(request, 'is_return_context'):
		return c, product
	else:
		return render_to_response('%s/product_detail.html' % request.template_dir, c)


########################################################################
# get_order_list: 获取订单列表
########################################################################
def get_order_list(request):
    type = int(request.GET.get('type', -1))
    orders = mall_api.get_orders(request)

    status = {
        -1: u'全部订单列表',
        0: u'待支付',
        3: u'待发货',
        4: u'待收货',
        5: u'待评价',
    }

    c = RequestContext(request, {
        'is_hide_weixin_option_menu': True,
        'page_title': status[type],
        'orders': orders,
        'hide_non_member_cover': True,
        'status_type': type
    })
    return render_to_response('%s/order_list.html' % request.template_dir, c)


########################################################################
# pay_order: 支付订单页面
########################################################################
def pay_order(request):
	webapp_user = request.webapp_user
	# jz 2015-08-10
	# is_delivery_plan = 0
	# delivery_plan = None
	# has_delivery_times = None
	try:
		order_id = request.GET['order_id']
		order_id = order_id.split('-')[0]
		order = mall_api.get_order(webapp_user, order_id, True)
		if not order:
			error_msg = u'pay_order:订单({})不存在'.format(order_id)
			watchdog_error(error_msg, db_name=settings.WATCHDOG_DB)
			raise Http404(error_msg)
	except:
		if settings.DEBUG:
			raise
		else:
			error_msg = u'pay_order:异常, cause:\n{}'.format(unicode_full_stack())
			watchdog_error(error_msg, db_name=settings.WATCHDOG_DB)
			raise Http404(u'订单不存在')
	red_envelope = request.webapp_owner_info.red_envelope
	if promotion_models.RedEnvelopeRule.can_show_red_envelope(order, red_envelope):
		order.red_envelope = red_envelope.id
		if promotion_models.RedEnvelopeToOrder.objects.filter(order_id=order.id).count():
			order.red_envelope_created = True

	# jz 2015-08-10
	# if (order.postage and int(order.postage) !=0) or (order.integral) or (order.coupon_id):
	# 	order.is_show_field = True
	# else:
	# 	order.is_show_field = False
	#获取订单包含商品
	# order_has_products = []
	# try:
	# 	# order_has_products = OrderHasProduct.objects.filter(order=order)
	# 	order.products = mall_api.get_order_products(order)
	# 	order.total_price = Order.get_order_has_price_number(order)
	# except:
	# 	error_msg = u'pay_order:获取订单包含商品异常, cause:\n{}'.format(unicode_full_stack())
	# 	watchdog_error(error_msg, db_name=settings.WATCHDOG_DB)
	# 	pass

	if order.status == ORDER_STATUS_PAYED_SHIPED and (datetime.today() - order.update_at).days >= 3:
		#订单发货后3天显示确认收货按钮
		if not hasattr(order, 'session_data'):
			order.session_data = dict()
		order.session_data['has_comfire_button'] = '1'

	order.has_promotion_saved_money = order.promotion_saved_money > 0

	request.should_hide_footer = True
	c = RequestContext(request, {
		'page_title': u'订单支付',
		'order': order,
		'order_status_info': STATUS2TEXT[order.status],
		'pay_interface': PAYTYPE2NAME[order.pay_interface_type],
		'error_msg': None,
		'is_in_testing': settings.IS_IN_TESTING,
		'is_hide_weixin_option_menu': True,
		# jz 2015-08-10
		# 'is_delivery_plan': is_delivery_plan,
		# 'delivery_plan': delivery_plan,
		# 'has_delivery_times': has_delivery_times,
		#'order_has_products': order_has_products,
		# 'is_support_thanks_card': is_support_thanks_card,
		# 'thanks_cards': thanks_cards,
		'hide_non_member_cover': True,
		'is_show_success': request.GET.get('isShowSuccess', False)
	})
	if hasattr(request, 'is_return_context'):
		return c
	else:
		return render_to_response('%s/order_detail.html' % request.template_dir, c)

#added by chuter
def __record_order_payment_info(order, pay_result):
	if (order is None) or (pay_result is None):
		return None

	payment_info = pay_result.get('order_payment_info', None)
	if payment_info is None:
		return None

	try:
		return OrderPaymentInfo.objects.create(
			order = order,
			transaction_id = payment_info.transaction_id,
			appid = payment_info.appid,
			openid = payment_info.openid,
			out_trade_no = payment_info.out_trade_no
			)
	except:
		error_msg = u"记录订单({})对应的支付结果信息失败，cause:\n{}".format(order.id, unicode_full_stack())
		watchdog_error(error_msg, db_name=settings.WATCHDOG_DB)

		return None

########################################################################
# get_pay_result: 支付结果，在支付宝完成支付后支付宝访问
# 携带的参数中主要使用：
# out_trade_no 订单号
########################################################################
def get_pay_result(request):
	'''
	# jz 2015-08-10
	order_id = request.GET.get('out_trade_no', None)
	trade_status = request.GET.get('result', '')
	is_trade_success = TRADE_SUCCESS == trade_status.lower()
	'''
	webapp_owner_id = request.webapp_owner_id
	type = request.GET['pay_interface_type']
	related_config_id = request.GET.get('related_config_id', 0)

	# 同步支付结果开始时间
	get_pay_result_start_time = int(time.time() * 1000)

	# jz 2015-08-10
	# pay_interface = PayInterface.objects.get(owner_id=webapp_owner_id, type=type, related_config_id=related_config_id)
	# if not pay_interface:
	# 	msg = '支付方式(owner_id={},type={},related_config_id={})不存在'.format(webapp_owner_id, type, related_config_id)
	# 	error_msg = u'weixin pay, stage:[get_pay_result], result:{}, exception:\n{}'.format(msg, msg)
	# 	watchdog_error(error_msg)
	# 	raise Http404(error_msg)
	pay_interface = PayInterface()
	pay_interface.type = int(type)
	pay_result = pay_interface.parse_pay_result(request)

	try:
		watchdog_info(u'weixin pay, stage:[get_pay_result], result:支付同步通知{}'.format(pay_result))
	except:
		pass

	is_trade_success = pay_result['is_success']
	order_id = pay_result['order_id']

	webapp_user = request.webapp_user
	webapp_id = request.user_profile.webapp_id

	order = None
	if order_id:
		order, pay_result = mall_api.pay_order(webapp_id, webapp_user, order_id, is_trade_success, pay_interface.type)
		if not order:
			msg = '订单({})不存在'.format(order_id)
			error_msg = u'weixin pay, stage:[get_pay_result], result:{}, exception:\n{}'.format(msg, msg)
			watchdog_error(error_msg)
			raise Http404(error_msg)
		if pay_result:
			#request.webapp_user.complete_payment(request)
			mall_signals.post_pay_order.send(sender=Order, order=order, request=request)

	if order is None:
		raise Http404(u'订单%s不存在' % order_id)

	if order.coupon_id:
		try:
			coupons = coupon_model.Coupon.objects.filter(id=order.coupon_id)
			if coupons.count() > 0:
				coupon = coupons[0]
				order.coupon_id = coupon.coupon_rule.name
		except:
			error_msg = u'weixin pay, stage:[get_pay_result], result:获取优惠券异常, exception:\n{}'.format(unicode_full_stack())
			watchdog_error(error_msg)
			pass

	#获取感恩贺卡密码
	# jz 2015-08-10
	# is_support_thanks_card = False
	# thanks_cards = []
	# try:
	# 	thanks_card_orders = ThanksCardOrder.objects.filter(order_id=order.id)
	# 	if thanks_card_orders:
	# 		is_support_thanks_card = True
	# 		for thanks_card_order in thanks_card_orders:
	# 			thanks_card = {}
	# 			thanks_card['id'] = thanks_card_order.id
	# 			thanks_card['thanks_secret'] = thanks_card_order.thanks_secret
	# 			thanks_card['is_used'] = thanks_card_order.is_used
	# 			thanks_cards.append(thanks_card)
	# except:
	# 	error_msg = u'weixin pay, stage:[get_pay_result], result:获取感恩贺卡密码异常, exception:\n{}'.format(unicode_full_stack())
	# 	watchdog_error(error_msg)
	# 	pass
	#对于已取消的订单, 不展示感恩贺卡
	#if order.status == ORDER_STATUS_CANCEL:
	# is_support_thanks_card = False
	# thanks_cards = []

	# is_delivery_plan = False
	# if order.type == PRODUCT_DELIVERY_PLAN_TYPE:
	# 	is_delivery_plan = True
	#确定是否显示运费、积分、优惠券等信息
	if (order.postage and int(order.postage) !=0) or (order.integral) or (order.coupon_id):
		order.is_show_field = True
	else:
		order.is_show_field = False

	request.should_hide_footer = True

	#是否显示支付成功
	if is_trade_success and order.status == ORDER_STATUS_PAYED_NOT_SHIP: #支付成功
		is_show_success = True
	else:
		is_show_success = False

	#是否提示用户领红包
	is_show_red_envelope = False
	red_envelope_rule_id = 0

	red_envelope = request.webapp_owner_info.red_envelope
	if promotion_models.RedEnvelopeRule.can_show_red_envelope(order, red_envelope):
		# 是可以显示分享红包按钮
		is_show_red_envelope = True
		red_envelope_rule_id = red_envelope.id

	#获取订单包含商品
	order_has_products = OrderHasProduct.objects.filter(order=order)

	# 更新order信息
	#order = Order.objects.get(id=order.id)

	# 同步支付结果结束时间
	get_pay_result_end_time = int(time.time() * 1000)
	msg = u'weixin pay, stage:[get pay result], order_id:{}, consumed:{}ms'.format(order_id, (get_pay_result_end_time - get_pay_result_start_time))
	watchdog_info(msg)

	# 记录支付结束时间
	pay_end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
	msg = u'weixin pay, stage:[end], order_id:{}, time:{}'.format(order_id, pay_end_time)
	watchdog_info(msg)

	c = RequestContext(request, {
		'is_hide_weixin_option_menu': True,
		'page_title': u'支付结果',
		'order': order,
		'order_status_info': STATUS2TEXT[order.status],
		'order_has_products': order_has_products,
		'is_in_testing' : settings.IS_IN_TESTING,
		# jz 2015-08-10
		# 'is_support_thanks_card': is_support_thanks_card,
		# 'thanks_cards': thanks_cards,
		# 'is_delivery_plan': is_delivery_plan,
		'hide_non_member_cover': True,
		'is_show_success': is_show_success,
		'is_show_red_envelope': is_show_red_envelope,
		'red_envelope_rule_id': red_envelope_rule_id
	})
	if hasattr(request, 'is_return_context'):
		return c
	else:
		if order.status == ORDER_STATUS_PAYED_NOT_SHIP:
			return render_to_response('%s/success.html' % request.template_dir, c)
		else:
			return render_to_response('%s/order_detail.html' % request.template_dir, c)


########################################################################
# get_pay_result_success: 支付结果，成功页面
########################################################################
def get_pay_result_success(request):
	order_id = request.GET.get('order_id', None)
	try:
		order = Order.objects.get(order_id=order_id)
	except:
		raise Http404(u'订单%s不存在' % order_id)

	#是否提示用户领红包
	is_show_red_envelope = False
	red_envelope_rule_id = 0
	coupon_rule = None

	red_envelope = request.webapp_owner_info.red_envelope
	if promotion_models.RedEnvelopeRule.can_show_red_envelope(order, red_envelope):
		# 是可以显示分享红包按钮
		is_show_red_envelope = True
		red_envelope_rule_id = red_envelope.id

	c = RequestContext(request, {
		'is_hide_weixin_option_menu': True,
		'page_title': u'支付结果',
		'order': order,
		'is_show_red_envelope': is_show_red_envelope,
		'red_envelope_rule_id': red_envelope_rule_id
	})
	if hasattr(request, 'is_return_context'):
		return c
	else:
		return render_to_response('%s/success.html' % request.template_dir, c)


########################################################################
# get_pay_notify_result : 支付宝异步 回调接口
########################################################################
def get_pay_notify_result(request):
	profile = request.user_profile
	webapp_user = request.webapp_user
	webapp_id = request.user_profile.webapp_id

	type = request.GET['pay_interface_type']
	related_config_id = request.GET.get('related_config_id', 0)

	pay_interface = PayInterface.objects.get(type=type, related_config_id=related_config_id)
	if not pay_interface:
		msg = '支付方式(type={},related_config_id={})不存在'.format(type, related_config_id)
		error_msg = u'weixin pay, stage:[get_pay_notify_result], result:{}, exception:\n{}'.format(msg, msg)
		watchdog_error(error_msg)
		raise Http404(error_msg)
	pay_notify_result = pay_interface.parse_notify_result(request)
	is_trade_success = pay_notify_result['is_success']
	order_id = pay_notify_result['order_id']
	error_msg = pay_notify_result['error_msg']
	reply_response = pay_notify_result['reply_response']

	order = None
	if order_id:
		order, pay_result = mall_api.pay_order(webapp_id, webapp_user, order_id, is_trade_success, pay_interface.type)

		if not order:
			msg = '订单({})不存在'.format(order_id)
			error_msg = u'weixin pay, stage:[get_pay_notify_result], result:{}, exception:\n{}'.format(msg, msg)
			watchdog_error(error_msg)
			raise Http404(u'订单%s不存在' % order_id)

		if pay_result:
			#added by chuter
			#记录订单对应的支付结果信息
			__record_order_payment_info(order, pay_notify_result)

			# jz 2015-08-10
			#request.webapp_user.complete_payment(request)
			mall_signals.post_pay_order.send(sender=Order, order=order, request=request)
	try:
		watchdog_info(u'weixin pay, stage:[get_pay_notify_result], result:支付异步通知{}'.format(pay_notify_result))
	except:
		pass

	return HttpResponse(reply_response, 'text/html;charset=utf-8')


def show_shopping_cart(request):
	'''显示购物车详情
	'''
	product_groups, invalid_products = mall_api.get_shopping_cart_products(request)
	product_groups = _sorted_product_groups_by_promotioin(product_groups)

	# json化的商品促销信息
	for product_group in product_groups:
		product_group['promotion_js'] = json.dumps(product_group['promotion'])

	request.should_hide_footer = True
	jsons = [{
		"name": "productGroups",
		"content": __format_product_group_price_factor(product_groups)
	}]

	c = RequestContext(request, {
		'is_hide_weixin_option_menu': True,
		'page_title': u'购物车',
		'product_groups': product_groups,
		'invalid_products': invalid_products,
		'jsons': jsons,
		'discount': get_member_discount_percentage(request)
	})
	return render_to_response('%s/shopping_cart.html' % request.template_dir, c)


def _sorted_product_groups_by_promotioin(product_groups):
	'''
	按商品促销信息排序，先按促销id升序排，再按促销类型升序排，无促销信息的排到后面
	供获取订单商品、显示购物车详情调用
	'''
	product_groups = sorted(product_groups, cmp=lambda x, y: \
		cmp(x['promotion']['id'] if x['promotion'] else 0, y['promotion']['id'] if y['promotion'] else 0 ))
	product_groups = sorted(product_groups, cmp=lambda x, y: \
		cmp(x['promotion']['type'] if x['promotion'] else 9, y['promotion']['type'] if y['promotion'] else 9 ))
	return product_groups


########################################################################
# edit_order: 编辑订单
########################################################################
def edit_order(request):
	products = utils.get_products(request)

	product = products[0]

	webapp_user = request.webapp_user
	webapp_owner_id = request.webapp_owner_id

	#创建order对象
	order = mall_api.create_order(webapp_owner_id, webapp_user, product)
	order.product_groups = mall_api.group_product_by_promotion(request, products)

	#测试订单，修改价钱和订单类型
	# jz 2015-08-10
	# type = request.GET.get('type', '')
	# order = mall_api.update_order_type_test(type, order)
	#获得运费计算因子
	#postage_factor = order.used['postage_config'].factor
	# delivery_plan_id = request.REQUEST.get('delivery_plan_id', '')
	# delivery_dates = request.REQUEST.get('delivery_dates', '')

	#获得运费配置，支持前端修改数量、优惠券等后实时计算运费
	postage_factor = product.postage_config['factor']

	#获取积分信息
	integral_info = webapp_user.integral_info
	integral_info['have_integral'] = (integral_info['count'] > 0)

	#获取优惠券
	coupons, limit_coupons = __fill_coupons_for_edit_order(webapp_user, products)

	#获取订单中用户的可用积分
	order.usable_integral = mall_api.get_order_usable_integral(order, integral_info)

	#获取商城配置
	mall_config = request.webapp_owner_info.mall_data['mall_config']#MallConfig.objects.get(owner_id=webapp_owner_id)
	use_ceiling = request.webapp_owner_info.integral_strategy_settings.use_ceiling

	request.should_hide_footer = True

	jsons = [{
		"name": "postageFactor",
		"content": postage_factor
	}, {
		"name": "integralInfo",
		"content": integral_info
	}, {
		"name": "productGroups",
		"content": __format_product_group_price_factor(order.product_groups)
	}]

	c = RequestContext(request, {
		'is_hide_weixin_option_menu': True,
		'page_title': u'编辑订单',
		'order': order,
		'mall_config': mall_config,
		'integral_info': integral_info,
		'coupons': coupons,
		'limit_coupons': limit_coupons,
		# jz 2015-08-10
		# 'is_delivery_plan': 1 if product.type == 'delivery' else 0,	#通过该类型判断商品是配送套餐还是其他商品
		# 'delivery_plan_id': delivery_plan_id,	#配送套餐id
		# 'delivery_dates': delivery_dates,	#配送套餐计划,
		'hide_non_member_cover': True,
		'use_ceiling': use_ceiling,
		'jsons': jsons
	})
	if hasattr(request, 'is_return_context'):
		return c
	return render_to_response('%s/edit_order.html' % request.template_dir, c)

def __fill_coupons_for_edit_order(webapp_user, products):
	coupons = webapp_user.coupons
	limit_coupons = []
	result_coupons = []
	today = datetime.today()

	product_ids = []
	total_price = 0
	productIds2price = dict()
	for product in products:
		product_ids.append(product.id)
		product_total_price = product.price * product.purchase_count
		total_price += product_total_price
		if not productIds2price.get(product.id):
			productIds2price[product.id] = 0
		productIds2price[product.id] += product_total_price
	for coupon in coupons:
		valid = coupon.valid_restrictions
		limit_id = coupon.limit_product_id

		if coupon.start_date > today:
			#兼容历史数据
			if coupon.status == promotion_models.COUPON_STATUS_USED:
				coupon.display_status = 'used'
			else:
				coupon.display_status = 'disable'
			limit_coupons.append(coupon)
		elif coupon.status != promotion_models.COUPON_STATUS_UNUSED:
			# 状态不是未使用
			if coupon.status == promotion_models.COUPON_STATUS_USED:
				# 状态是已使用
				coupon.display_status = 'used'
			else:
				# 过期状态
				coupon.display_status = 'overdue'
			limit_coupons.append(coupon)
		elif coupon.limit_product_id > 0 and \
			(product_ids.count(limit_id) == 0 or valid > productIds2price[limit_id]) or\
			valid > total_price or\
			coupon.provided_time >= today:
			# 1.订单没有限定商品
			# 2.订单金额不足阈值
			# 3.优惠券活动尚未开启
			coupon.display_status = 'disable'
			limit_coupons.append(coupon)
		else:
			result_coupons.append(coupon)

	return result_coupons, limit_coupons

def __format_product_group_price_factor(product_groups):
	factors = []
	for product_group in product_groups:
		product_factors = []
		for product in product_group['products']:
			product_factors.append({
				"id": product.id,
				"model": product.model_name,
				"count": product.purchase_count,
				"price": product.price,
				"original_price": product.original_price,
				"weight": product.weight,
				"active_integral_sale_rule": getattr(product, 'active_integral_sale_rule', None),
				"postageConfig": product.postage_config if hasattr(product, 'postage_config') else {}
			})

		factor = {
			'id': product_group['id'],
			'uid': product_group['uid'],
			'products': product_factors,
			'promotion': product_group['promotion'],
			'promotion_type': product_group['promotion_type'],
			'promotion_result': product_group['promotion_result'],
			'integral_sale_rule': product_group['integral_sale_rule'],
			'can_use_promotion': product_group['can_use_promotion']
		}
		factors.append(factor)

	return factors


def get_member_discount(request):
	"""返回与会员等级相关的折扣

	Return:
	  fload: 如果用户是会员返回对应的折扣， 否这不打折返回1.00

	"""
	if hasattr(request, 'member') and request.member:
		member_grade_id = request.member.grade_id
		member_grades = request.webapp_owner_info.member_grades
		member_grade = filter(lambda x: x.id == member_grade_id, member_grades)[0]

		return member_grade.shop_discount / 100.00
	else:
		return 1.0


def get_member_discount_percentage(request):
	"""返回与会员等级相关的折扣

	Return:
	  fload: 如果用户是会员返回对应的折扣， 否这不打折返回100

	"""
	if hasattr(request, 'member') and request.member:
		member_grade_id = request.member.grade_id
		member_grades = request.webapp_owner_info.member_grades
		member_grade = filter(lambda x: x.id == member_grade_id, member_grades)[0]

		return member_grade.shop_discount
	else:
		return 100


def edit_shopping_cart_order(request):
	"""编辑从购物车产生的订单
	"""
	webapp_user = request.webapp_user
	webapp_owner_id = request.webapp_owner_id
	products = utils.get_products(request)
	buf = []

	for product in products:
		buf.append({
			"name": product.name,
			"purchase_count": product.purchase_count,
			"model": product.model['name']
		})

	# 没有选择商品，跳转回购物车
	if len(products) == 0:
		url = request.META.get('HTTP_REFERER','/workbench/jqm/preview/?woid={}&module=mall&model=shopping_cart&action=show'.format(webapp_owner_id))
		return HttpResponseRedirect(url)

	order = mall_api.create_shopping_cart_order(webapp_owner_id, webapp_user, products)
	order.product_groups = mall_api.group_product_by_promotion(request, products)

	#获得运费配置，支持前端修改数量、优惠券等后实时计算运费
	postage_factor = None
	for product in products:
		if product.postage_type == POSTAGE_TYPE_CUSTOM:
			postage_factor = product.postage_config['factor']
			break
		postage_factor = product.postage_config['factor']

	#获取积分信息
	integral_info = webapp_user.integral_info
	integral_info['have_integral'] = (integral_info['count'] > 0)

	#获取优惠券
	coupons, limit_coupons = __fill_coupons_for_edit_order(webapp_user, products)

	#获取订单中用户的可用积分
	order.usable_integral = mall_api.get_order_usable_integral(order, integral_info)

	#获取商城配置
	mall_config = request.webapp_owner_info.mall_data['mall_config'] # MallConfig.objects.get(owner_id=webapp_owner_id)
	use_ceiling = request.webapp_owner_info.integral_strategy_settings.use_ceiling

	jsons = [{
		"name": "postageFactor",
		"content": postage_factor
	}, {
		"name": "integralInfo",
		"content": integral_info
	}, {
		"name": "productGroups",
		"content": __format_product_group_price_factor(order.product_groups)
	}]

	request.should_hide_footer = True
	c = RequestContext(request, {
		'is_hide_weixin_option_menu': True,
		'page_title': u'购物车订单编辑',
		'order': order,
		'mall_config': mall_config,
		'coupons': coupons,
		'limit_coupons': limit_coupons,
		'postage_factor': json.dumps(postage_factor),
		'integral_info': integral_info,
		'is_order_from_shopping_cart': True,
		'use_ceiling': use_ceiling,
		'jsons': jsons
	})
	return render_to_response('%s/edit_order.html' % request.template_dir, c)


########################################################################
# list_pay_interfaces: 显示支付方式列表
########################################################################
def list_pay_interfaces(request):
	webapp_owner_id = request.webapp_owner_id
	order_id = request.GET.get('order_id', 0)

	# 获取该订单的支付方式
	pay_interfaces = mall_api.get_order_pay_interfaces(webapp_owner_id, request.webapp_user, order_id)

	for pay_interface in pay_interfaces:
		pay_interface.pay_logo = PAYTYPE2LOGO[pay_interface.type]
		pay_interface.name = PAYTYPE2NAME[pay_interface.type]

	request.should_hide_footer = True

	#add by bert at 17.0 针对微众商城的用户直接跳转到微众卡支付页面不显示支付列表
	if request.user.is_weizoom_mall is False:
		c = RequestContext(request, {
			'is_hide_weixin_option_menu': True,
			'page_title': u'支付列表',
			'order_id': request.GET['order_id'],
			'pay_interfaces': pay_interfaces,
			'hide_non_member_cover': True
		})
		return render_to_response('%s/pay_interfaces.html' % request.template_dir, c)
	else:
		order_id = request.GET.get('order_id', -1)

		try:
			order = Order.objects.get(id=order_id)
		except:
			raise Http404(u'订单%s不存在' % order_id)

		page_url = 'http://%s%s?%s' % (request.META['HTTP_HOST'], request.path, request.META['QUERY_STRING'])
		c = RequestContext(request, {
			'order_id': order.order_id,
			'is_in_weixin': request.user.is_from_weixin,
			'page_url': page_url,
			'page_title': u'支付列表',
			'is_hide_weixin_option_menu': True,
			'hide_non_member_cover': True
		})

		response = render_to_response('mall/templates/webapp/default/pay_weizoonpay_order.html', c)
		return response


########################################################################
# pay_alipay_order: 处理支付宝订单
########################################################################
def pay_alipay_order(request):
	page_url = 'http://%s%s?%s' % (request.META['HTTP_HOST'], request.path, request.META['QUERY_STRING'])
	request.should_hide_footer = True
	c = RequestContext(request, {
		'order_id': request.GET['order_id'],
		'pay_interface_id': request.GET['pay_interface_id'],
		'is_in_weixin': request.user.is_from_weixin,
		'page_url': page_url
	})

	response = render_to_response('%s/pay_alipay_order.html' % request.template_dir, c)
	if not request.user.is_from_weixin:
		#不是从微信来的访问，设置cookie：sct
		sct = member_settings.SOCIAL_ACCOUNT_TOKEN_SESSION_KEY
		response.set_cookie(sct, request.GET['sct'], max_age=60*60*24*365)

	return response


########################################################################
# pay_weizoompay_order: 处理微众卡支付
########################################################################
def pay_weizoompay_order(request):
	page_url = 'http://%s%s?%s' % (request.META['HTTP_HOST'], request.path, request.META['QUERY_STRING'])
	request.should_hide_footer = True
	c = RequestContext(request, {
		'order_id': request.GET['order_id'],
		'is_in_weixin': request.user.is_from_weixin,
		'page_url': page_url,
		'is_hide_weixin_option_menu': True
	})

	response = render_to_response('%s/pay_weizoonpay_order.html' % request.template_dir, c)
	return response

from core import core_setting
def get_weizoompay_confirm(request):
	page_url = 'http://%s%s?%s' % (request.META['HTTP_HOST'], request.path, request.META['QUERY_STRING'])
	request.should_hide_footer = True
	auth_key = request.COOKIES.get(core_setting.WEIZOOM_CARD_AUTH_KEY, None)
	order_id = request.GET.get('order_id','-1')
	try:
		order = Order.objects.get(order_id = order_id)
	except:
		raise Http404(u'订单%s不存在' % order_id)

	card_id = request.GET.get('card_id', -1)

	if weizoom_card_model.WeizoomCard.objects.filter(id=card_id).count() > 0 and weizoom_card_model.WeizoomCardUsedAuthKey.is_can_pay(auth_key, card_id):
		weizoom_card =  weizoom_card_model.WeizoomCard.objects.get(id=card_id)
	else:
		c = RequestContext(request, {
			'order_id': order.order_id,
			'is_in_weixin': request.user.is_from_weixin,
			'page_url': page_url
			})
		return render_to_response('%s/pay_weizoonpay_order.html' % request.template_dir, c)

	is_can_pay = True if weizoom_card.money >= order.final_price else False

	c = RequestContext(request, {
		'is_in_weixin': request.user.is_from_weixin,
		'page_url': page_url,
		'weizoom_card': weizoom_card,
		'order': order,
		'is_can_pay':is_can_pay,
		'is_hide_weixin_option_menu': True
	})

	response = render_to_response('%s/weizoonpay_order_confirm.html' % request.template_dir, c)

	return response

def get_weizoomcard_change_intr(request):
	page_url = 'http://%s%s?%s' % (request.META['HTTP_HOST'], request.path, request.META['QUERY_STRING'])
	c = RequestContext(request, {
		'is_in_weixin': request.user.is_from_weixin,
		'page_url': page_url,
		'is_hide_weixin_option_menu': False
	})
	return render_to_response('%s/weizoomcard_change_intr.html' % request.template_dir, c)


########################################################################
# edit_address: 编辑收货地址信息
########################################################################
def edit_address(request):
	webapp_user = request.webapp_user
	webapp_owner_id = request.webapp_owner_id
	#隐藏底部导航条#
	request.should_hide_footer = True
	ship_info_id = request.GET.get('id', 0)
	if request.action == 'add':
		ship_info = None
	elif ship_info_id > 0:
		try:
			ship_info = ShipInfo.objects.get(id=ship_info_id)
		except:
			ship_info = None
	else:
		ship_info = webapp_user.ship_info

	c = RequestContext(request, {
		'is_hide_weixin_option_menu': True,
		'page_title': u'编辑收货地址',
		'ship_info': ship_info,
		'redirect_url_query_string': request.redirect_url_query_string
	})
	if hasattr(request, 'is_return_context'):
		return c
	return render_to_response('%s/order_address.html' % request.template_dir, c)


########################################################################
# show_concern_shop_url: 点击关注店铺
########################################################################
def show_concern_shop_url(request):
	redirect_url = request.META.get('HTTP_REFERER','')
	product_id = request.GET.get('product_id')
	other_owner_id = request.GET.get('other_owner_id')
	from_webapp_id = request.user_profile.webapp_id
	to_webapp_id = None

	# jz 2015-08-10
	# otherProduct = WeizoomMallHasOtherMallProduct.objects.filter(product_id=product_id, weizoom_mall__webapp_id=from_webapp_id, is_checked=True)
	# if otherProduct.count() > 0:
	# to_webapp_id = otherProduct[0].webapp_id
	otherProfile = UserProfile.objects.get(user_id=other_owner_id)
	otherSettings = OperationSettings.objects.get(owner_id = otherProfile.user)
	if otherSettings.weshop_followurl.startswith('http://mp.weixin.qq.com'):
		redirect_url = otherSettings.weshop_followurl
	else:
		redirect_url = otherSettings.non_member_followurl

	webapp_util.concern_shop_log(request.webapp_user.id, from_webapp_id, to_webapp_id, redirect_url, product_id)
	return HttpResponseRedirect(redirect_url)


########################################################################
# list_address: 收货地址信息列表
########################################################################
def list_address(request):
	webapp_user = request.webapp_user
	webapp_owner_id = request.webapp_owner_id
	#隐藏底部导航条#
	request.should_hide_footer = True
	c = RequestContext(request, {
		'is_hide_weixin_option_menu': True,
		'page_title': u'编辑收货地址',
		'redirect_url_query_string': request.redirect_url_query_string,
		'ship_infos': webapp_user.ship_infos,
	})
	return render_to_response('%s/list_address.html' % request.template_dir, c)


########################################################################
# add_address: 添加收货地址信息
########################################################################
def add_address(request):
	webapp_user = request.webapp_user
	webapp_owner_id = request.webapp_owner_id
	#隐藏底部导航条#
	request.should_hide_footer = True

	c = RequestContext(request, {
		'is_hide_weixin_option_menu': True,
		'page_title': u'编辑收货地址',
		'redirect_url_query_string': request.redirect_url_query_string
	})
	return render_to_response('%s/order_address.html' % request.template_dir, c)


########################################################################
# delete_address: 删除收货地址信息
########################################################################
def delete_address(request):
	ship_info_id = request.GET.get('id', 0)
	ShipInfo.objects.filter(id=ship_info_id).update(is_deleted=True)

	# 默认选中
	ship_infos = request.webapp_user.ship_infos
	selected_ships_count = ship_infos.filter(is_selected=True).count()
	if ship_infos.count() > 0 and selected_ships_count == 0:
		ship_info = ship_infos[0]
		ship_info.is_selected = True
		ship_info.save()

	# 显示地址列表
	return list_address(request)


########################################################################
# success_alert: 成功提示页面
########################################################################
def success_alert(request):
	webapp_user = request.webapp_user
	webapp_owner_id = request.webapp_owner_id
	#隐藏底部导航条#
	request.should_hide_footer = True
	is_pay_interface_cod = request.GET.get('is_pay_interface_cod', 0)

	c = RequestContext(request, {
		'is_hide_weixin_option_menu': True,
		'page_title': u'成功',
		'is_pay_interface_cod': is_pay_interface_cod
	})
	return render_to_response('%s/success.html' % request.template_dir, c)



########################################################################
# get_express_detail: 物流信息
########################################################################
def get_express_detail(request):
	webapp_user = request.webapp_user
	webapp_owner_id = request.webapp_owner_id
	#隐藏底部导航条#
	request.should_hide_footer = True
	order_id = request.GET.get('order_id', None)
	order = mall_api.get_order_by_id(order_id)
	c = RequestContext(request, {
		'is_hide_weixin_option_menu': True,
		'page_title': u'物流信息',
		'order': order
	})
	return render_to_response('%s/express_detail.html' % request.template_dir, c)


########################################################################
# edit_order_review: 评论信息
########################################################################
def edit_order_review(request):
    products = utils.get_products(request)
    c = RequestContext(request,
                       {
                           'is_hide_weixin_option_menu': True,
                           'page_title': u'商品评价',
                           'products': products,
                       })
    return render_to_response('%s/review_create.html' % request.template_dir, c)


def _get_order_review_list(request,need_product_detail=False):
    '''
        得到会员已完成订单中所有未评价的商品列表的订单，
        或者已评价未晒图的订单

        PreCondition: webapp_user_id, member_id,
        PostCondition: orders

    '''

    webapp_user_id = request.webapp_user.id  # 游客身份
    member_id = request.member.id            # 会员身份

    # jz 2015-08-10
    # need_product_detail = request.GET.get("need_product_detail", False)
    #判断调用的页面是否需要产品信息
    # start

    # 得到会员的所有已完成的订单
    orders = Order.objects.filter(webapp_user_id=webapp_user_id, status=5)
    orderIds = [order.id for order in orders]
    orderHasProducts = OrderHasProduct.objects.filter(order_id__in=orderIds)
    totalProductIds = [orderHasProduct.product_id for orderHasProduct in orderHasProducts]

    orderId2orderHasProducts = dict()
    for orderHasProduct in orderHasProducts:
        if not orderId2orderHasProducts.get(orderHasProduct.order_id):
            orderId2orderHasProducts[orderHasProduct.order_id] = []
        orderId2orderHasProducts.get(orderHasProduct.order_id).append(orderHasProduct)

    orderHasProductIds = [orderHasProduct.id for orderHasProduct in orderHasProducts]
    ProductReviews = mall_models.ProductReview.objects.filter(order_has_product_id__in=orderHasProductIds)
    orderHasProductId2ProductReviews = dict()
    for ProductReview in ProductReviews:
        orderHasProductId2ProductReviews[ProductReview.order_has_product_id] = ProductReview

    allProductReviewPicture = mall_models.ProductReviewPicture.objects.filter(order_has_product_id__in= orderHasProductIds)
    ProductReviewPictureIds = [ProductReviewPicture.product_review_id for ProductReviewPicture in allProductReviewPicture]
    def _product_review_has_picture(product_review):
        '''
        评价是否有晒图
        '''


        if product_review.id in ProductReviewPictureIds:
            return True
        else:
            return False

    if need_product_detail:
        cache_products = webapp_cache.get_webapp_products_detail(request.webapp_owner_id, totalProductIds)
        cache_productId2cache_products = dict([(product.id, product) for product in cache_products])

        # 对于每个订单
        for order in orders:
            products = []             # 订单的所有未评价商品, 或者有评价未晒图
            order_is_reviewed = True  # 订单是否评价完成
            # 对于订单的每件商品
            for orderHasProduct in orderId2orderHasProducts[order.id]:
                # 如果商品有评价
                product_review = orderHasProductId2ProductReviews.get(orderHasProduct.id,False)
                product = copy.copy(cache_productId2cache_products[orderHasProduct.product_id]) #此处需要复制
                if product_review:
                    product.has_review = True
                    product_review_picture =  _product_review_has_picture(product_review)
                    # 如果评价有晒图
                    if product_review_picture:
                        order_is_reviewed = order_is_reviewed & True
                    # 评价无晒图
                    else:
                        order_is_reviewed = order_is_reviewed & False
                        product.order_has_product_id = orderHasProduct.id
                        product.has_picture = False
                        product.fill_specific_model(
                            orderHasProduct.product_model_name, cache_productId2cache_products[product.id].models)
                        product.product_model_name = product.custom_model_properties
                        products.append(product)
                # 商品无评价
                else:
                    order_is_reviewed = order_is_reviewed & False
                    product.order_has_product_id = orderHasProduct.id
                    product.has_review = False
                    product.fill_specific_model(
                        orderHasProduct.product_model_name, cache_productId2cache_products[product.id].models)
                    product.product_model_name = product.custom_model_properties

                    products.append(product)

                product.order_product_model_name = orderHasProduct.product_model_name

            order.products = products
            order.order_is_reviewed = order_is_reviewed
    else:
        ##############################################################################
        for order in orders:

            order_is_reviewed = True  # 订单是否评价完成
            # 对于订单的每件商品
            for orderHasProduct in orderId2orderHasProducts[order.id]:
                # 如果商品有评价
                product_review = orderHasProductId2ProductReviews.get(orderHasProduct.id,False)
                # product = dict() #此处需要复制
                if product_review:

                    product_review_picture =  _product_review_has_picture(product_review)
                    # 如果评价有晒图
                    if product_review_picture:
                        order_is_reviewed = order_is_reviewed & True
                    # 评价无晒图
                    else:
                        order_is_reviewed = order_is_reviewed & False

                # 商品无评价
                else:
                    order_is_reviewed = order_is_reviewed & False
            order.order_is_reviewed = order_is_reviewed

    return orders

########################################################################
# get_order_review_list: 会员订单中未评价订单列表
########################################################################
def get_order_review_list(request):
    '''
        得到会员已完成订单中所有未评价的商品列表的订单，
        或者已评价未晒图的订单

        Precondition: webapp_user
        PostCondition: RequestContext with the following context:
            {
                'orders': [
                    order,
                    order,],
                'is_hide_weixin_option_menu': ''
                'page_title': '',
            }

    '''

    orders = _get_order_review_list(request,need_product_detail=True)

    c = RequestContext(request,
                       {"orders": orders,
                        'is_hide_weixin_option_menu': True,
                        'page_title': u'待评价列表',
                        })
    return render_to_response(
        '%s/order_review_list.html' % request.template_dir, c)


########################################################################
# get_product_review_successful_page: 评论信息
########################################################################
def get_product_review_successful_page(request):
    c = RequestContext(request,
                       {'is_hide_weixin_option_menu': True,
                        'page_title': u'评论信息',
                        })
    return render_to_response(
        '%s/product_review_successful.html' % request.template_dir, c)


def get_product_review_list(request):
    '''
    得到商品评价列表
    '''
    member_id = request.GET.get('member_id', None)
    if member_id:
        # 得到某个会员的所有商品评价列表
        member_id = int(member_id)
        product_review_list = mall_models.ProductReview.objects.filter(
            member_id=member_id
        ).order_by('-id')

        # 对于每个商品评价得到对应的商品评价晒图
        product_review_ids = [i.id for i in product_review_list]
        product_picture_list = mall_models.ProductReviewPicture.objects.filter(
            product_review_id__in=product_review_ids
        )
        product_review_has_picture = {}
        for picture in product_picture_list:
            pp_id = picture.product_review_id
            if pp_id in product_review_has_picture:
                product_review_has_picture[pp_id].append(picture)
            else:
                product_review_has_picture[pp_id] = []
                product_review_has_picture[pp_id].append(picture)

        # 构造所需商品信息
        product_id_list = set([review.product_id for review in product_review_list])
        products = mall_models.Product.objects.filter(id__in=product_id_list)
        review_products = {}
        for product in products:
            review_products[product.id] = product

        # 构造商品评价列表
        for product_review in product_review_list:
            product_review.product = review_products.get(product_review.product_id)
            product_review.pictures = product_review_has_picture.get(product_review.id, None)

        c = RequestContext(request,
                           {'is_hide_weixin_option_menu': True,
                            'page_title': u'',
                            'product_review_list': product_review_list,
                            })
        return render_to_response(
            '%s/product_review_list.html' % request.template_dir, c)
    # 得到所有人的审批通过的商品评价列表
    else:
        product_review_list = mall_api.get_product_review(request)
        c = RequestContext(request,
                           {'is_hide_weixin_option_menu': True,
                            'page_title': u'',
                            'product_review_list': product_review_list,
                            })
        return render_to_response(
            '%s/product_review_all_user_list.html' % request.template_dir, c)


def create_product_review(request):
    '''
    为指定用户的指定订单的指定商品，创建评价
    '''

    # 判断订单是否评价过
    order_id = request.GET.get('order_id', None)
    product_model_name = request.GET.get('product_model_name', None)
    order_has_product_id = int(request.GET.get('order_has_product_id', None))
    product_id = request.GET.get('product_id', None)

    order_review_count = mall_models.OrderReview.objects.filter(
            owner_id=request.member.id,
            order_id=order_id,
        ).count()
    has_order_review = order_review_count > 0

    # 得到商品信息, 如果商品已不存在（下架..）, 返回404

    try:
        # order_has_product = mall_models.OrderHasProduct.objects.get(id=order_has_product_id)
        product = webapp_cache.get_webapp_product_detail(request.webapp_owner_id,product_id)
        product = product
        product.fill_specific_model(product_model_name, product.models)
    except ObjectDoesNotExist:
        return Http404

    #
    send_time = time.time()
    c = RequestContext(request,
                       {
                           'is_hide_weixin_option_menu': True,
                           'page_title': u'发表评价',
                           'order_id': order_id,
                           'has_order_review': has_order_review,
                           'order_has_product_id': order_has_product_id,
                           'product':product,
                           'created': False,
                           'send_time': send_time
                       })
    return render_to_response(
        '%s/product_review_create.html' % request.template_dir, c)


def update_product_review_picture(request):
    '''

    为product_review添加晒图
    Precondition: product_id

    '''
    # 得到商品信息

    order_id = request.GET.get('order_id', None)
    product_model_name = request.GET.get('product_model_name', None)
    order_has_product_id = int(request.GET.get('order_has_product_id', None))
    product_id = request.GET.get('product_id', None)
    # order_has_product = mall_models.OrderHasProduct.objects.get(id=order_has_product_id)

    product = webapp_cache.get_webapp_product_detail(request.webapp_owner_id,product_id)

    product.fill_specific_model(product_model_name, product.models)
    # 得到product_review
    send_time = time.time()
    try:
        product_review = mall_models.ProductReview.objects.get(order_has_product_id=order_has_product_id)
        c = RequestContext(request,
                            {
                                'is_hide_weixin_option_menu': True,
                                'page_title': u'追加晒图',
                                'order_has_product_id': order_has_product_id,
                                'order_id': order_id,
                                'product': product,
                                'product_review': product_review,
                                'send_time': send_time,
                                'created': True
                            })
        return render_to_response(
            '%s/product_review_create.html' % request.template_dir, c)
    except ObjectDoesNotExist:
        return Http404


def redirect_product_review(request):
    '''
    PreCondition: identify
    PostCondition:
        如果identify是True， 显示返回首页页面
        否则显示返回评价列表页面
    '''
    orders_is_reviewed = request.GET.get("identify", 'True')
    c = RequestContext(request,
                       {
                           'is_hide_weixin_option_menu': True,
                           'page_title': u'感谢您评价',
                           'orders_is_reviewed': orders_is_reviewed.upper(),
                       })
    return render_to_response(
        '%s/product_review_successful.html' % request.template_dir, c)


########################################################################
# edit_order: 编辑订单
########################################################################
def edit_refueling_order(request):
	refueling_id = request.GET.get('refueling_id', None)
	member_refueling = MemberRefueling.objects.get(id=refueling_id)
	products = utils.get_products(request)

	product = products[0]
	product.price = 79
	webapp_user = request.webapp_user
	webapp_owner_id = request.webapp_owner_id

	#创建order对象
	order = mall_api.create_order(webapp_owner_id, webapp_user, product)
	order.product_groups = mall_api.group_product_by_promotion(request, products)

	#测试订单，修改价钱和订单类型
	type = request.GET.get('type', '')
	order = mall_api.update_order_type_test(type, order)
	order.final_price = 79
	#获得运费计算因子
	#postage_factor = order.used['postage_config'].factor
	#获得运费配置，支持前端修改数量、优惠券等后实时计算运费
	postage_factor = product.postage_config['factor']
	#获取积分信息
	integral_info = webapp_user.integral_info
	integral_info['have_integral'] = (integral_info['count'] > 0)

	#获取优惠券
	coupons, limit_coupons = __fill_coupons_for_edit_order(webapp_user, products)

	#获取订单中用户的可用积分
	order.usable_integral = 0#mall_api.get_order_usable_integral(order, integral_info)

	#获取商城配置
	mall_config = request.webapp_owner_info.mall_data['mall_config']#MallConfig.objects.get(owner_id=webapp_owner_id)
	use_ceiling = request.webapp_owner_info.integral_strategy_settings.use_ceiling

	request.should_hide_footer = True
	# jz 2015-08-10
	# delivery_plan_id = request.REQUEST.get('delivery_plan_id', '')
	# delivery_dates = request.REQUEST.get('delivery_dates', '')


	jsons = [{
		"name": "postageFactor",
		"content": postage_factor
	}, {
		"name": "integralInfo",
		"content": integral_info
	}, {
		"name": "productGroups",
		"content": __format_product_group_price_factor(order.product_groups)
	}]
	refueling_order = '%s_79' % refueling_id
	c = RequestContext(request, {
		'is_hide_weixin_option_menu': True,
		'page_title': u'编辑订单',
		'order': order,
		'mall_config': mall_config,
		'integral_info': 0,
		'coupons': None,
		'limit_coupons': None,
		# jz 2015-08-10
		# 'is_delivery_plan': 1 if product.type == 'delivery' else 0,	#通过该类型判断商品是配送套餐还是其他商品
		# 'delivery_plan_id': delivery_plan_id,	#配送套餐id
		# 'delivery_dates': delivery_dates,	#配送套餐计划,
		'hide_non_member_cover': True,
		'use_ceiling': None,
		'jsons': jsons,
		'refueling_order': refueling_order
	})
	if hasattr(request, 'is_return_context'):
		return c
	return render_to_response('%s/edit_order.html' % request.template_dir, c)
