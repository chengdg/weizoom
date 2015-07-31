# -*- coding: utf-8 -*-

__author__ = 'bert'

from utils.uuid import uniqueid
from utils.string_util import byte_to_hex
from models import *

import member_settings
from member_info_util import get_request_member

from mall.models import Order

########################################################################
# get_uuid : 获取请求信息中包含的uuid信息
# 对于还没有与微站进行过绑定的用户，cookie中都会有uuid信息，用于记录
# 在绑定前在微站中进行的操作行为
########################################################################
def get_uuid(request):
	if hasattr(request, 'uuid') and request.uuid:
		return request.uuid

	return request.COOKIES.get(member_settings.UUID_SESSION_KEY, None)

def generate_uuid(request):
	return uniqueid()

def get_request_webapp_user_by_uuid(uuid, webapp_id):
	if (uuid is None) or (webapp_id is None):
		return None

	#update by bert at wechat_cache_1
	try:
		return WebAppUser.objects.filter(token=uuid, webapp_id=webapp_id)[0]
	except:
		return None

from core.alipay.alipay_notify import AlipayNotify
from core.wxpay.wxpay_notify import WxpayNotify
def get_request_webapp_user_by_member(request, is_create_when_not_exist=True):
	request_member = get_request_member(request)

	webapp_user = None
	member_id = 0
	if request_member:
		member_id = request_member.id
		try:
			webapp_user = WebAppUser.objects.filter(member_id=request_member.id, webapp_id=request.user_profile.webapp_id, father_id=0)[0]
		except:
			webapp_user = None
	elif ('/tenpay/mall/' in request.path) or ('/alipay/mall/' in request.path) or ('/wxpay/' in request.path) or ('/pay/' in request.path):
		order_id = request.REQUEST.get('out_trade_no', None)
		if order_id is None:
			order_id = request.REQUEST.get('order_id', None)		

		#added by chuter
		if (order_id is None) and ('/alipay/mall/pay_notify_result/') in request.path:
			#支付宝异步通知
			order_id = AlipayNotify.parse_order_id(request)
		
		if (order_id is None) and ('/wxpay/mall/pay_notify_result/') in request.path:
			#微信v3版支付异步通知
			notify = WxpayNotify(request)
			if notify:
				order_id = notify.get_payed_order_id()
		
		if order_id:
			#兼容改价
			order_id = order_id.split('-')[0]
			order = Order.objects.get(order_id=order_id)
			webapp_user = WebAppUser.objects.get(id=order.webapp_user_id)
			if webapp_user.member_id != 0:
				request.member = Member.objects.get(id=webapp_user.member_id)
	else:
		webapp_id = request.user_profile.webapp_id
		uuid = request.uuid

		try:
			webapp_user = WebAppUser.objects.get(token=uuid, member_id=0, webapp_id=webapp_id)
		except:
			webapp_user = None
		
	if is_create_when_not_exist and (not webapp_user):
		#未能识别任何已知的webapp user，创建一个新的
		if request.user_profile:
			if member_id > 0:
				uuid = str(member_id)
			else:
				assert (request.uuid)
				uuid = request.uuid

			webapp_id = request.user_profile.webapp_id
			webapp_user,_ = WebAppUser.objects.get_or_create(
					token = uuid,
					webapp_id = webapp_id,
					member_id = member_id
				)

	return webapp_user