# -*- coding: utf-8 -*-

from mall.models import *
from django.contrib.auth.models import Group, User

def pay(pay_interface, order, webapp_owner_id):
	if PAY_INTERFACE_ALIPAY == pay_interface.type:
		from account.models import UserProfile
		user_profile = UserProfile.objects.get(user_id=webapp_owner_id)
		call_back_url = "http://{}/alipay/mall/pay_result/get/{}/{}/".format(user_profile.host, webapp_owner_id, pay_interface.related_config_id)
		notify_url = "http://{}/alipay/mall/pay_notify_result/get/{}/{}/".format(user_profile.host, webapp_owner_id, pay_interface.related_config_id)

		pay_submit = AlipaySubmit(pay_interface.related_config_id, order, call_back_url, notify_url)
		alipay_url = pay_submit.submit()

		return alipay_url
	elif PAY_INTERFACE_TENPAY == pay_interface.type:
		from account.models import UserProfile
		user_profile = UserProfile.objects.get(user_id=webapp_owner_id)
		call_back_url = "http://{}/tenpay/mall/pay_result/get/{}/{}/".format(user_profile.host, webapp_owner_id, pay_interface.related_config_id)
		notify_url = "http://{}/tenpay/mall/pay_notify_result/get/{}/{}/".format(user_profile.host, webapp_owner_id, pay_interface.related_config_id)
		pay_submit = TenpaySubmit(pay_interface.related_config_id, order, call_back_url, notify_url)
		tenpay_url = pay_submit.submit()

		return tenpay_url
	elif PAY_INTERFACE_COD == pay_interface.type:
		return './?woid={}&module=apps:weshop:mall2&model=pay_result&action=get&pay_interface_type={}&order_id={}'.format(webapp_owner_id, PAY_INTERFACE_COD, order.order_id)
	elif PAY_INTERFACE_WEIXIN_PAY == pay_interface.type:
		return '/webapp/wxpay/?woid={}&order_id={}&pay_id={}&callback_module=apps:weshop:mall2&showwxpaytitle=1'.format(webapp_owner_id, order.order_id, pay_interface.id)
	# jz 2015-10-09
	# elif PAY_INTERFACE_WEIZOOM_COIN == pay_interface.type:
	# 	return './?woid={}&module=mall&model=weizoompay_order&action=pay&pay_interface_type={}&pay_interface_id={}&order_id={}'.format(webapp_owner_id, PAY_INTERFACE_WEIZOOM_COIN, pay_interface.id, order.order_id)
	else:
		return ''