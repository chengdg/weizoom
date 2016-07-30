# -*- coding: utf-8 -*-
from __future__ import absolute_import
import time
import urllib
import urllib2
import json
import datetime
from django.conf import settings

from core.jsonresponse import create_response
from core import common_util
from watchdog.utils import *
from core.exceptionutil import full_stack, unicode_full_stack
from core.alipay.alipay_submit import *
from modules.member.models import *
from modules.member.util import *
from mall.models import *
from mall import models as mall_models
from mall import module_api as mall_api
from mall import signals as mall_signals
from account.models import *
from account.views import save_base64_img_file_local_for_webapp,save_upload_mobile_pic
from . import request_util
from . import utils
from core.send_order_email_code import *
from market_tools.tools.coupon import util as coupon_util

from webapp.handlers import event_handler_util
from webapp import cache_util
from cache import webapp_cache

def product_stocks(request):
	"""
	获取单个商品各个规格的实时库存
	"""
	product_id = request.GET.get('product_id', None)
	model_ids = request.GET.get('model_ids', None)
	need_member_info = request.GET.get('need_member_info', False)

	#改为从缓存读取库存数据 duhao 2015-08-13
	# response = create_response(200)
	# if product_id:
	# 	response.data = cache_util.get_product_stocks_from_cache(product_id)
	# elif model_ids:
	# 	response.data = cache_util.get_product_stocks_from_cache(model_ids, True)
	# else:
	# 	return create_response(500).get_response()

	# return response.get_response()

	result_data = dict()

	if product_id:
		models = ProductModel.objects.filter(product_id=product_id, is_deleted=False)
	elif model_ids:
		model_ids = model_ids.split(",")
		models = ProductModel.objects.filter(id__in=model_ids, is_deleted=False)
	else:
		models = []

	response = create_response(200)

	for model in models:
		model_data = dict()
		model_data["stocks"] = model.stocks
		model_data["stock_type"] = model.stock_type
		result_data[model.id] = model_data

	# 代码来自 get_member_product_info(request) mall/module_api.py
	if need_member_info == '1':
		member_info_data = mall_api.get_member_product_info_dict(request)
		result_data = dict(result_data, **member_info_data)


	response.data = result_data
	return response.get_response()


def products_stocks(request):
	"""
	获取商品实时库存
	"""
	product_ids = request.POST.get('product_ids', None)
	model_ids = request.POST.get('model_ids', None)

	result_data = dict()
	if product_ids and model_ids:
		product_ids = product_ids.split('_')
		model_ids = model_ids.split('_')
		if len(product_ids) == len(model_ids):
			models = ProductModel.objects.filter(id__in=model_ids)
			for model in models:
				if str(model.product_id) in product_ids:
					model_data = dict()
					model_data["stocks"] = str(model.stocks),
					model_data["stock_type"] = str(model.stock_type),
					result_data['%s-%s' % (model.product_id, model.id)] = model_data

	response = create_response(200)
	response.data = result_data
	return response.get_response()


def pay_order(request):
	"""
	订单支付api, 获取【支付跳转路径】
	避免使用，直接通过save_order方法返回【支付跳转路径】
	"""
	order_to_pay = None
	#profile = request.user_profile
	#webapp_user = request.webapp_user

	order_id = request.POST.get('order_id', None)
	if order_id is None:
		response = create_response(400)
		response.errMsg = u'订单不存在'
		return response.get_response()

	try:
		order_to_pay = Order.objects.get(id=order_id)
	except:
		response = create_response(500)
		response.errMsg = u'获取订单失败'
		response.innerErrMsg = full_stack()
		return response.get_response()

	interface_id = int(request.POST.get('interface_id', 0))
	if interface_id == 0:
		#没有指定interface id, 根据interface type获取
		pay_interface = PayInterface.objects.get(owner_id=request.webapp_owner_id, type=request.POST['interface_type'])
	else:
		pay_interface = PayInterface.objects.get(id=interface_id)

	pay_url = pay_interface.pay(order_to_pay, request.webapp_owner_id)
	if pay_url:
		response = create_response(200)
		response.data.url = pay_url
	else:
		response = create_response(500)
		response.errMsg = u'支付失败'
		#stack = unicode_full_stack()
		response.innerErrMsg = full_stack()

	return response.get_response()


WAIT_BUYER_PAY = 'WAIT_BUYER_PAY'
WAIT_SELLER_SEND_GOODS='WAIT_SELLER_SEND_GOODS'
TRADE_FINISHED = 'TRADE_FINISHED'
TRADE_CLOSED = 'TRADE_CLOSED'
WAIT_BUYER_CONFIRM_GOODS = 'WAIT_BUYER_CONFIRM_GOODS'


# def __check_product_shelve_type(products):
# 	"""
# 	__check_product_shelve_type: 检查是否有商品被下架
# 	"""
# 	off_shelve_products = []
# 	for product in products:
# 		if product.shelve_type == PRODUCT_SHELVE_TYPE_OFF:
# 			off_shelve_products.append(product)

# 	return off_shelve_products

def save_order(request):
	"""保存订单
	"""
	profile = request.user_profile
	webapp_id = profile.webapp_id
	webapp_user = request.webapp_user
	webapp_owner_id = request.webapp_owner_id
	ship_name = request.POST['ship_name']
	ship_address = request.POST['ship_address']
	ship_tel = request.POST['ship_tel']
	# ship_id = request.POST.get('ship_id', None)  # never used ???
	order_type = request.POST.get('order_type', PRODUCT_DEFAULT_TYPE)
	pay_interface = request.POST.get('xa-choseInterfaces', '-1')

	refueling_order = request.POST.get('refueling_order', '')

	# 获取地址信息
	area = request.POST.get('area', '')
	# 获取发票信息
	if 'is_use_bill' in request.POST:
		bill_type = request.POST.get('bill_type', ORDER_BILL_TYPE_NONE)
		bill = request.POST.get('bill', '')
	else:
		bill_type = ORDER_BILL_TYPE_NONE
		bill = ''
	if not bill:
		bill_type = ORDER_BILL_TYPE_NONE

	# 获取用户留言信息
	customer_message = request.POST.get('message', '')

	# 获取购买的商品集合
	products = utils.get_products(request)
	# 发送下单检查信号
	fake_order = common_util.Object("order")
	fake_order.products = products
	fake_order.product_groups = mall_api.group_product_by_promotion(request, products)
	signal_responses = mall_signals.check_order_related_resource.send(sender=mall_signals, pre_order=fake_order, args=request.REQUEST, request=request)
	http_response = common_util.check_failed_signal_response(signal_responses)
	if http_response:
		return http_response

	order = None
	pay_url = None
	try:
		#保存订单信息
		order_info = {
			'products': products,
			'product_groups': fake_order.product_groups,
			'ship_name': ship_name,
			'ship_address': ship_address,
			'ship_tel': ship_tel,
			'area': area,
			'bill_type': bill_type,
			'bill': bill,
			'customer_message': customer_message,
			'type': order_type,
			'fake_order': fake_order,
			'pay_interface': pay_interface,
		}
		order = mall_api.save_order(webapp_id, webapp_owner_id, webapp_user, order_info, request)
		if order.final_price > 0 and pay_interface != '-1':
			# 处理 支付跳转路径
			# pay_interface = PayInterface.objects.get(owner_id=request.webapp_owner_id, type=pay_interface)
			pay_interface = filter(
				lambda x: x.type == int(pay_interface),
				request.webapp_owner_info.pay_interfaces)[0]
			pay_url = pay_interface.pay(order, webapp_owner_id)

		#删除购物车中的商品
		if request.POST.get('is_order_from_shopping_cart', 'false') == 'true':
			for product in products:
				if hasattr(product.model, 'name'):
					mall_api.remove_product_from_shopping_cart(webapp_user, product.id, product.model.name)
				else:
					mall_api.remove_product_from_shopping_cart(webapp_user, product.id, product.model['name'])

		#调用post_save_order service
		request.event_data = event_handler_util.extract_data(request, {
			'order_order_id': order.order_id
		})
		event_handler_util.handle(request, 'post_save_order')


		try:
			mall_api.create_mall_order_from_shared(request, order.id)
		except:
			pass

	except Exception, e:
		stack = unicode_full_stack()
		watchdog_error(stack, 'mall')
		data = dict()
		data['msg'] = u'创建订单失败，请稍后重试'
		data['exception'] = stack
		response = create_response(500)
		response.data = data
		return response.get_response()

	try:
		#加油集赞订单支付
		if refueling_order and '_79' in refueling_order:
			refueling_id = refueling_order.split('_')[0]
			MemberRefuelingHasOrder.objects.create(member_refueling_id=refueling_id, order_id=order.id)
			order.final_price = 79
			order.save()
	except:
		stack = unicode_full_stack()
		watchdog_error(stack, 'mall')

	if order:
		data = {
			'order_id' : order.order_id,
			'id' : order.id,
			'final_price' : round(order.final_price, 2)
		}
		if pay_url:
			data['pay_url'] = pay_url

	response = create_response(200)
	response.data = data
	return response.get_response()


########################################################################
# get_shopping_cart_product_ids: 获取购物车中商品id集合
########################################################################
def get_shopping_cart_product_ids(request):
	ids = mall_api.get_shopping_cart_product_ids(request.webapp_user)

	response = create_response(200)
	response.data.ids = ids
	return response.get_response()


########################################################################
# add_shopping_cart: 将商品加入购物车
########################################################################
def add_shopping_cart(request):
	product_id = request.POST['product_id']
	product_model_name = request.POST.get('product_model_name', 'standard');
	count = int(request.POST.get('count', 0))
	mall_api.add_product_to_shopping_cart(request.webapp_user, product_id, product_model_name, count)

	response = create_response(200)
	response.data.shopping_cart_product_nums = mall_api.get_shopping_cart_product_nums(request.webapp_user)
	return response.get_response()


########################################################################
# delete_shopping_cart: 删除购物车内容
########################################################################
def delete_shopping_cart(request):
	shopping_cart_item_ids = request.POST.get('shopping_cart_item_ids', '').split(',')
	# print '***************************'
	# print request.POST
	# print shopping_cart_item_ids
	mall_api.remove_shopping_cart_items(request.webapp_user, shopping_cart_item_ids)
	'''
	product_ids = request.POST.get('product_ids', None)
	if product_ids:
		product_ids = product_ids.split('_')

	product_model_names = request.POST.get('product_model_names',  None)
	if product_model_names:
		if '$' in product_model_names:
			product_model_names = product_model_names.split('$')
		else:
			product_model_names = product_model_names.split('%24')

	# product_id = request.POST['product_id']
	# product_model_name = request.POST.get('product_model_name', 'standard')
	for i in range(0, len(product_ids)):
		mall_api.remove_product_from_shopping_cart(request.webapp_user, product_ids[i], product_model_names[i])
	'''
	return create_response(200).get_response()


########################################################################
# update_shopping_cart: 更新购物车内容
########################################################################
def update_shopping_cart(request):
	update_info = json.loads(request.POST['update_info'])
	mall_api.update_shopping_cart(request.webapp_user, update_info)
	return create_response(200).get_response()


########################################################################
# clear_shopping_cart_invalid_products: 清空购物车中的无效商品
########################################################################
def clear_shopping_cart_invalid_products(request):
	shopping_cart_item_ids = request.POST.get('shopping_cart_item_ids', '').split(',')
	mall_api.clear_shopping_cart_invalid_products(request.webapp_user, shopping_cart_item_ids)
	return create_response(200).get_response()


from market_tools.tools.weizoom_card import mobile_api_views
def check_weizoom_card(request):
	return mobile_api_views.check_weizoom_card(request)


########################################################################
# update_order_status: 修改订单的状态
########################################################################
def update_order_status(request):
	order_id = request.POST.get('order_id', 0)
	action = request.POST.get('action', '')
	if not order_id or action == '':
		response = create_response(500)
		response.errMsg = u'webapp中修改订单失败'
		return response.get_response()

	try:
		order = Order.objects.get(id=order_id)
		mall_api.update_order_status(request.user, action, order)
		response = create_response(200)
	except:
		response = create_response(500)
		response.errMsg = u'webapp中修改订单失败'
		response.innerErrMsg = full_stack()
		notify_message = u"webapp中修改订单状态失败, order_id:{}, action:{}, cause:\n{}".format(order_id, action, unicode_full_stack())
		watchdog_error(notify_message)

	return response.get_response()


import urllib2
import urllib
import json
import hashlib
from BeautifulSoup import BeautifulSoup
from weixin.user.models import ComponentAuthedAppid
def get_openid(request):
	code = request.POST.get('code', '')
	appid = request.POST.get('appid', '')
	#secret = request.POST.get('secret', '')

	# data = {
	# 	'appid': appid,
	# 	'secret': secret,
	# 	'code': code,
	# 	'grant_type': 'authorization_code'
	# }

	component_authed_appid = ComponentAuthedAppid.objects.filter(authorizer_appid=appid, user_id=request.user_profile.user_id)[0]
	component_info = component_authed_appid.component_info
	component_access_token = component_info.component_access_token

	data = {
		'appid': appid,
		#'secret': weixin_mp_user_access_token.app_secret,
		'code': code,
		'grant_type': 'authorization_code',
		'component_appid': component_info.app_id,
		'component_access_token': component_access_token
	}
	url = 'https://api.weixin.qq.com/sns/oauth2/component/access_token'

	try:
		req = urllib2.urlopen(url, urllib.urlencode(data))
		response_data = req.read()
		response_data = eval(response_data)
		if response_data.has_key('openid'):
			response = create_response(200)
			response.data = response_data
		else:
			req = urllib2.urlopen(url, urllib.urlencode(data))
			response_data = req.read()
			response_data = eval(response_data)
			if response_data.has_key('openid'):
				response = create_response(200)
				response.data = response_data
			else:
				response = create_response(201)
				response.data = response_data

		watchdog_info(u"openid获取信息: \n{}".format(response_data), db_name=settings.WATCHDOG_DB)
		return response.get_response()
	except:
		error_msg = u"get_openid异常, cause:\n{}".format(unicode_full_stack())
		watchdog_error(error_msg, db_name=settings.WATCHDOG_DB)
		response = create_response(500)
		response.data['exception'] = error_msg
		return response.get_response()
	# code = request.POST.get('code', '')
	# appid = request.POST.get('appid', '')
	# secret = request.POST.get('secret', '')

	# data = {
	# 	'appid': appid,
	# 	'secret': secret,
	# 	'code': code,
	# 	'grant_type': 'authorization_code'
	# }


	# try:
	# 	url = 'https://api.weixin.qq.com/sns/oauth2/access_token?'
	# 	req = urllib2.urlopen(url, urllib.urlencode(data))
	# 	response_data = req.read()
	# 	response_data = eval(response_data)
	# 	if response_data.has_key('openid'):
	# 		response = create_response(200)
	# 		response.data = response_data
	# 	else:
	# 		response = create_response(201)
	# 		response.data = response_data

	# 	watchdog_info(u"openid获取信息: \n{}".format(response_data), db_name=settings.WATCHDOG_DB)
	# 	return response.get_response()
	# except:
	# 	error_msg = u"get_openid异常, cause:\n{}".format(unicode_full_stack())
	# 	watchdog_error(error_msg, db_name=settings.WATCHDOG_DB)
	# 	response = create_response(500)
	# 	response.data['exception'] = error_msg
	# 	return response.get_response()


WEIXIN_XML = u"""<xml><appid>%s</appid><mch_id>%s</mch_id><nonce_str><![CDATA[%s]]></nonce_str><sign><![CDATA[%s]]></sign><body><![CDATA[%s]]></body><out_trade_no>%s</out_trade_no><total_fee>%s</total_fee><spbill_create_ip>%s</spbill_create_ip><notify_url>%s</notify_url><trade_type>JSAPI</trade_type><openid>%s</openid></xml>"""
SUCCESS = "SUCCESS"
FALI = "FAIL"

def get_wixin_pay_package(request):
	import sys
	reload(sys)
	sys.setdefaultencoding('utf-8')
	appid = request.POST.get('appid', '').strip()
	mch_id = request.POST.get('mch_id', '').strip()
	nonce_str = request.POST.get('nonce_str', '')
	body = request.POST.get('body', '')
	out_trade_no = request.POST.get('out_trade_no', '')
	total_fee = request.POST.get('total_fee', '')
	spbill_create_ip = request.POST.get('spbill_create_ip', '')
	notify_url = request.POST.get('notify_url', '')
	openid = request.POST.get('openid', '')
	tenant_key = request.POST.get('key', '')

	try:
		if appid == '' or mch_id == '' or nonce_str == '' or out_trade_no == '' or total_fee == '' or spbill_create_ip == '' or notify_url == '' or openid == '':
			error_msg = u'get_wixin_pay_package: 缺少必要参数'
			watchdog_error(error_msg, db_name=settings.WATCHDOG_DB)
			response = create_response(201)
			return response.get_response()
		#创建 sign
		package_list = {'trade_type':'JSAPI','appid': appid, 'body':body.encode('utf8') , 'mch_id':mch_id, 'nonce_str':nonce_str,'notify_url':notify_url,'openid':openid,'out_trade_no':out_trade_no,'spbill_create_ip':spbill_create_ip, 'total_fee':total_fee}
		key_list = sorted(package_list.keys())
		sing_str = u''
		for key in key_list:
			sing_str = sing_str + (u"%s=%s&" % (key, package_list[key]))

		sign_str = sing_str + 'key=' + tenant_key
		m = hashlib.md5()
		m.update(sign_str)
		sign = m.hexdigest().upper()

		#填充xml
		post_xml_data = WEIXIN_XML % (appid, mch_id, nonce_str, sign, body, out_trade_no, total_fee, spbill_create_ip, notify_url, openid)
		data = {}
		try:
			#发送POST请求
			url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
			cookies = urllib2.HTTPCookieProcessor()
			opener = urllib2.build_opener(cookies)
			request = urllib2.Request(
				url = url,
				headers = {'Content-Type' : 'text/xml'},
				data = post_xml_data.encode('utf8'))

			response_data = opener.open(request).read()
			response_data = BeautifulSoup(response_data)
			if response_data.result_code and response_data.return_code:
				result_code = response_data.result_code.text.upper()
				return_code = response_data.return_code.text.upper()
				time_stamp = str(int(time.time()))
				if result_code == SUCCESS and return_code == SUCCESS:
					data['nonce_str'] = response_data.nonce_str.text
					data['prepay_id'] = response_data.prepay_id.text
					pay_sign_args_dict = {'appId': appid, 'timeStamp': time_stamp, 'nonceStr':data['nonce_str'],'package=prepay_id': data['prepay_id'], 'signType': 'MD5'}
					pay_sign_args_keys = sorted(pay_sign_args_dict.keys())
					pay_sign = ''
					for key in pay_sign_args_keys:
						pay_sign = pay_sign + ("%s=%s&" % (key, pay_sign_args_dict[key]))
					pay_sign = pay_sign + 'key='+tenant_key
					m_pay = hashlib.md5()
					m_pay.update(pay_sign)
					pay_sign = m_pay.hexdigest()

					data['pay_sign'] = pay_sign.upper()
					data['time_stamp'] = time_stamp

					watchdog_info(u"get_wixin_pay_package获取信息: \n{}".format(data), db_name=settings.WATCHDOG_DB)
					response = create_response(200)
				else:
					watchdog_error("get_wixin_pay_package失败, cause:\n{}".format(response_data), db_name=settings.WATCHDOG_DB)
					response = create_response(201)
			else:
				response = create_response(201)
		except:
			error_msg = u"get_wixin_pay_package异常, cause:\n{}".format(unicode_full_stack())
			watchdog_error(error_msg, db_name=settings.WATCHDOG_DB)
			response = create_response(201)

		response.data = data
		return response.get_response()

	except:
		error_msg = u"get_wixin_pay_package异常, cause:\n{}".format(unicode_full_stack())
		watchdog_error(error_msg, db_name=settings.WATCHDOG_DB)
		response = create_response(201)
		response.data = data
		return response.get_response()


def _get_coupons_to_json(coupons):
	data = []
	for coupon in coupons:
		item = dict()
		item['id'] = coupon.id
		item['coupon_id'] = coupon.coupon_id
		item['coupon_rule_name'] = coupon.coupon_rule.name
		item['status'] = coupon.status
		item['member_id'] = coupon.member_id
		item['provided_time'] = coupon.provided_time.strftime('%Y-%m-%d')
		item['expired_time'] = coupon.expired_time.strftime('%Y-%m-%d')
		item['money'] = coupon.money
		item['is_manual_generated'] = coupon.is_manual_generated
		data.append(item)

	return data


########################################################################
# is_can_use_coupon: 是否可以使用该优惠券
########################################################################
def is_can_use_coupon(request):
	coupon_id = request.POST.get('coupon_coupon_id', None)
	product_ids = request.POST.get('product_ids', None)
	product_prices = request.POST.get('product_price', None)
	original_prices = request.POST.get('original_price', None)
	product_id2price = request.POST.get('product_id2price', None)
	if product_id2price:
		product_id2price = json.loads(product_id2price)

	if product_ids and product_prices:
		product_ids = product_ids.split('_')
		product_prices = [float(price) for price in product_prices.split('_')]
		original_prices = [float(price) for price in original_prices.split('_')]

	response = create_response(200)
	msg, coupon = coupon_util.has_can_use_by_coupon_id(coupon_id, request.webapp_owner_id, product_prices, product_ids, request.member.id, original_prices=original_prices, product_id2price=product_id2price)
	if coupon:
		response.data = {
			'id': coupon_id,
			'money': str(coupon.money),
			'productid': coupon.coupon_rule.limit_product_id
		}
	else:
		response.data = {'msg': msg,'id': 0}
	return response.get_response()


########################################################################
# save_address: 保存地址
########################################################################
def save_address(request):
	webapp_user = request.webapp_user
	response = create_response(200)
	data = dict()
	try:
		ship_id = int(request.POST.get('ship_id', 0))
		ship_name = request.POST.get('ship_name', '')
		ship_address = request.POST.get('ship_address', '')
		ship_tel = request.POST.get('ship_tel', '')
		area = request.POST.get('area', '')

		#更新收货地址信息
		ship_id = webapp_user.update_ship_info(
			ship_id = ship_id,
			ship_name=ship_name,
			ship_address=ship_address,
			ship_tel=ship_tel,
			area=area
		)
	except:
		if settings.DEBUG:
			raise
		else:
			response = create_response(500)
			stack = unicode_full_stack()
			watchdog_error(stack)
			data['msg'] = u'保存收货信息失败，请稍后重试'
			data['exception'] = stack

	data['ship_name'] = ship_name
	data['ship_id'] = ship_id
	response.data = data
	return response.get_response()


########################################################################
# select_address: 选择地址
########################################################################
def select_address(request):
	webapp_user = request.webapp_user
	response = create_response(200)
	data = dict()
	ship_id = 0
	try:
		ship_id = int(request.POST.get('ship_id', 0))
		#更新收货地址信息
		ShipInfo.objects.filter(webapp_user_id=webapp_user.id).update(is_selected=False)
		ShipInfo.objects.filter(id=ship_id).update(is_selected=True)
	except:
		response = create_response(500)
		stack = unicode_full_stack()
		watchdog_error(stack)
		data['msg'] = u'保存收货信息失败，请稍后重试'
		data['exception'] = stack

	data['ship_id'] = ship_id
	data['msg'] = '默认收货地址设置成功'
	response.data = data
	return response.get_response()


def check_shopping_cart_products(request):
	"""
	检查商品是否满足"去结算"条件
	"""
	msg, products = utils.get_products(request)

	fake_order = common_util.Object("order")
	fake_order.products = products
	fake_order.product_groups = mall_api.group_product_by_promotion(request, products)
	signal_responses = mall_signals.check_pre_order_related_resource.send(sender=mall_signals, pre_order=fake_order, args=request.REQUEST, request=request)
	http_response = common_util.check_failed_signal_response(signal_responses)
	if http_response:
		return http_response

	return create_response(200).get_response()

def update_wishlist_product(request):
	"""
	更新商品收藏
	"""
	return mall_api.update_wishlist_product(request)

def check_product_in_wishlist(request):
	"""
	判断会员是否收藏了此商品
	"""
	return mall_api.check_product_in_wishlist(request)

def get_member_product_info(request):
	'''
	获取购物车的数量和检查商品是否已被收藏
	'''
	return mall_api.get_member_product_info(request)

# def get_product_detail(request):
# 	"""
# 	获取商品的介绍信息
# 	"""
# 	product_id = request.GET['product_id']
# 	webapp_user = request.webapp_user
# 	try:
# 		product = mall_api.get_product_detail(request.webapp_owner_id, product_id, webapp_user)
# 	except:
# 		return create_response(500).get_response()

# 	response = create_response(200)
# 	response.data = product.detail
# 	return response.get_response()


def get_review_status(request):
	'''
	得到个人中心待评价列表的状态，
	如果所有订单已完成晒图， 返回True
	否则返回 False
	'''
	# 得到个人中心的所用订单
	orders = request_util._get_order_review_list(request)
	# 如果订单都已经完成晒图
	result = True
	for order in orders:
		result = result & order.order_is_reviewed
	return result


########################################################################
# create_product_review: 创建评论
########################################################################
def create_product_review(request):
	'''

	Precondition:
		json data like:
		{
		'product_score': '!None',
		'review_detail': '',
		'serve_score': '!None',
		'deliver_score': '!None',
		'process_score': '!None',
		}
	PostCondition:
		返回一个状态码, 表示是否创建成功

	'''
	if request.method == 'POST':
		# 规格化所需数据
		owner_id = int(request.webapp_owner_id)
		order_id = request.POST.get('order_id', None)
		member_id = int(request.member.id)
		product_id = int(request.POST.get('product_id', None))
		order_has_product_id = int(request.POST.get('order_has_product_id', None))

		send_time = request.POST.get('send_time', None)
		detal_time = request.POST.get('detal_time', None)

		request_length = request.META['CONTENT_LENGTH']

		if send_time and detal_time:
			send_time = float(send_time)
			detal_time = float(detal_time)
			send_time = send_time + detal_time
			total_seconds =  time.time() - send_time
			watchdog_info(u"order_has_product_id: %d, request time: %d, response time: %d, total_seconds: %d, total_size: %dkb" %
							(order_has_product_id, float(send_time), time.time(), total_seconds, int(request_length)//1024),
					  type="mall",
					  user_id=int(request.webapp_owner_id))

		data_dict = request.POST
		product_score = data_dict.get('product_score', None)
		review_detail = data_dict.get('review_detail', None)
		serve_score = data_dict.get('serve_score', None)
		deliver_score = data_dict.get('deliver_score', None)
		process_score = data_dict.get('process_score', None)
		picture_list = data_dict.get('picture_list', None)
		#创建订单评论
		order_review, created = mall_models.OrderReview.objects.get_or_create(
			order_id=order_id,
			owner_id=owner_id,
			member_id=member_id,
			serve_score=serve_score,
			deliver_score=deliver_score,
			process_score=process_score)

		# 创建商品评论
		product_review, created = mall_models.ProductReview.objects.get_or_create(
			member_id=member_id,
			order_review=order_review,
			order_id=order_id,
			owner_id=owner_id,
			product_id=product_id,
			order_has_product_id=order_has_product_id,
			product_score=product_score,
			review_detail=review_detail
		)
		response = create_response(200)
		response.data = get_review_status(request)
		if picture_list:
			for picture in list(eval(picture_list)):
				mall_models.ProductReviewPicture(
					product_review=product_review,
					order_has_product_id=order_has_product_id,
					att_url=picture
				).save()
				watchdog_info(u"create_product_review after save img  %s" %\
					(picture), type="mall", user_id=request.webapp_owner_id)

			watchdog_info(u"create_product_review end, order_has_product_id is %s" %\
				(order_has_product_id), type="mall", user_id=owner_id)
		return response.get_response()
	elif request.method == 'GET':
		return create_response(500).get_response()

def create_mobile_pic(request):
	basestr=request.POST.get('basestr',None)
	return save_upload_mobile_pic(request,basestr)

def update_product_review_picture(request):
	'''
	为指定商品评论添加晒图
	PreCondition: product_review_id, picture_list
	'''

	# 得到商品评论ID
	product_review_id = request.POST.get('product_review_id', None)
	order_has_product_id = int(request.POST.get('order_has_product_id', None))
	if product_review_id:
		product_review_id=int(product_review_id)

	send_time = request.POST.get('send_time', None)
	request_length = request.META['CONTENT_LENGTH']

	if send_time:
		total_seconds =  time.time()- float(send_time)
		watchdog_info(u"order_has_product_id: %d, request time: %d, response time: %d, total_seconds: %d, total_size: %dkb" %
						(order_has_product_id, float(send_time), time.time(), total_seconds, int(request_length)//1024), type="mall", user_id=int(request.webapp_owner_id))
	# 得到图片
	picture_list = request.POST.get('picture_list', None)
	# 为此商品评论创建贴图
	if picture_list:
		for picture in list(eval(picture_list)):
			mall_models.ProductReviewPicture(
				product_review_id=product_review_id,
				order_has_product_id=order_has_product_id,
				att_url=picture
			).save()
		# TODO 更好的实现，能触发缓存更新
		# mall_models.ProductReviewPicture.objects.bulk_create(picture_model_list)

		response = create_response(200)
		response.data = get_review_status(request)
		return response.get_response()


def init_ship_infos(request):
	ship_infos = list(request.webapp_user.ship_infos)
	items = {}
	for ship_info in ship_infos:
		data_dict = dict()
		data_dict['ship_id'] = ship_info.id
		data_dict['ship_name'] = ship_info.ship_name
		data_dict['ship_tel'] = ship_info.ship_tel
		data_dict['ship_address'] = ship_info.ship_address
		data_dict['area'] = ship_info.area
		try:
			data_dict['area_str'] = ship_info.get_str_area
		except:
			pass
		data_dict['is_selected'] = ship_info.is_selected
		items[ship_info.id] = data_dict
	return items

def init_sessionstorage(request):
	response = create_response(200)
	data = dict()
	data['ship_infos'] = init_ship_infos(request)
	response.data = data
	return response.get_response()


def delete_address(request):
	print('hereeee')
	ship_info_id = request.POST.get('id', 0)
	ShipInfo.objects.filter(id=ship_info_id).update(is_deleted=True)

	# 默认选中
	ship_infos = request.webapp_user.ship_infos
	selected_ships_count = ship_infos.filter(is_selected=True).count()
	if ship_infos.count() > 0 and selected_ships_count == 0:
		ship_info = ship_infos[0]
		ship_info.is_selected = True
		ship_info.save()
		selected_id = ship_info.id
	else:
		selected_id = 0
	print('selected_id...:', selected_id)
	# 显示地址列表
	response = create_response(200)
	data = dict()
	data['selected_id'] = selected_id
	response.data = data
	return response.get_response()


def log_js_analysis(request):
	def __get_from_request(key, value=None):
		if value:
			return False
		if key in request.META:
			value = request.META.get(key, None)
		elif key in request:
			value = request.get(key, None)
		else:
			# value_from_request = None
			return False
		message_list.append({key: value})
		return True

	response = create_response(200).get_response()
	if not request.is_ajax():
		return response

	message = ''
	message_list = []
	try:
		# 默认数据

		# api默认数据
		message_list.append({'analysis_name': request.POST.get('analysis_name', '')})

		# request默认数据
		"""
		HTTP_REFERER:发送请求的页面URL
		REMOTE_ADDR：用户IP
		HTTP_USER_AGENT：USER_AGENT
		"""
		request_default_info = ('HTTP_REFERER', 'REMOTE_ADDR', 'HTTP_USER_AGENT')
		for key in request_default_info:
			# message_dict[key] = request.META.get(key, None)
			__get_from_request(key)

		# weapp默认数据
		try:
			member_id = request.member.id
		except:
			member_id = '0'
		message_list.append({'member_id': member_id})

		# 处理content
		content = request.POST.get('content', '')
		try:
			for key, value in json.loads(content).items():
				if not __get_from_request(key, value):
					message_list.append({key: value})
		except ValueError:
			# 如果不是JSON对象，则以字符串判断
			message_list.append({'content': content})

		for item in message_list:
			message += '[%s]:%s\n' % (item.items()[0][0], item.items()[0][1])

		try:
			woid = request.webapp_owner_id
		except:
			woid = '0'
		watchdog_js_analysis(message, type='JS_Analysis', user_id=woid)
	except:
		# 即使出错，也返回200响应
		stack = unicode_full_stack()
		watchdog_error(stack)
	return response


def get_shopping_cart_count(request):
	
	if request.webapp_user:
		try:
			webapp_user_id = request.webapp_user.id
			shopping_cart = ShoppingCart.objects.filter(webapp_user_id=webapp_user_id)
			if shopping_cart.count() > 0:
				shopping_cart_count = shopping_cart.count()
			else:
				shopping_cart_count = 0
		except:
			notify_message = u"购物车数量函数出错，cause:\n{}".format(unicode_full_stack())
			watchdog_error(notify_message)
			shopping_cart_count = 0
		print shopping_cart_count
		response = create_response(200)
		response.data = {'count': shopping_cart_count}
		return response.get_response()
	else:
		notify_message = u"参数webapp_user_id确实或者错误！"
		watchdog_error(notify_message)
		response = create_response(200)
		response.data = {'count': 0}
		return response.get_response()

def get_member_subscribed_status(request):
	try:
		is_subscribed = request.member.is_subscribed
		response = create_response(200)
		response.data = {'is_subscribed': is_subscribed}
		return response.get_response()
	except:
		notify_message = u"获取会员状态失败，cause:\n{},{}".format(unicode_full_stack(), request.COOKIES)
		watchdog_error(notify_message)
		response = create_response(200)
		response.data = {'is_subscribed': True}
		return response.get_response()


def _set_empty_product_list():
	pass


def get_page_products(request):
	product_ids = request.GET.get('product_ids', '')
	category_id = int(request.GET.get('category_id', 0))

	products_data = []

	_, products = webapp_cache.get_webapp_products_new(request.user_profile, False, category_id)

	woid = request.user_profile.user_id
	if woid==1120:
		try:
			length = len(products)
		except:
			length = -1
		watchdog_info({
			'woid':woid,
			'type_products':str(type(products)),
			'length':length,
			'location':1
		})

	if product_ids:
		product_ids = map(lambda x: int(x), product_ids.split(','))
		products = filter(lambda x: x.id in product_ids, products)

	for product in products:

		products_data.append({
			"id": product.id,
			"name": product.name,
			"thumbnails_url": product.thumbnails_url,
			"display_price": product.display_price,
			"is_member_product": product.is_member_product,
			"promotion_js": json.dumps(product.promotion) if product.promotion else ""
		})


	if woid==1120:
		try:
			length = len(products_data)
		except:
			length = -1
		watchdog_info({
			'woid':woid,
			'type_products':str(type(products_data)),
			'length':length,
			'location':2
		})

	response = create_response(200)
	response.data = {'products': products_data}
	return response.get_response()
