# -*- coding: utf-8 -*-

# from django.contrib.auth.models import User
# from account.models import UserOrderNotifySettings, UserProfile
# from django.conf import settings
# from core.exceptionutil import unicode_full_stack
# from watchdog.utils import watchdog_error, watchdog_notice, watchdog_info
# from core.sendmail import sendmail

# zhaolei 2015-11-18
# def _get_order_status_url_and_content_described(order, user_profile, is_pay=False):
# 	try:
# 		content_described = None
# 		if user_profile.webapp_template == 'wine':
# 			content_described = u'东方特酱%s订单'
# 		if user_profile.webapp_template == 'rice':
# 			content_described = u'响水骄子%s订单'
# 		if user_profile.webapp_template == 'tour':
# 			content_described = u'开封旅游%s订单'
# 		if user_profile.webapp_template == 'weapp':
# 			content_described = u'微众商城%s订单'
# 		if content_described:
# 			if is_pay:
# 				content_described = content_described % u'付款'
# 			else:
# 				content_described = content_described % u'新增'
# 		bill = ''
# 		bill_type = ''
# 		try:
# 			if order.bill_type:
# 				if int(order.bill_type) == 0:
# 					bill_type = u'个人，'
# 				else:
# 					bill_type = u'公司，'
# 				bill = bill_type + order.bill
# 		except:
# 			pass
# 		return content_described, u'订单号：<a href="http://%s/m/%s/pay_order/%s/%s/">%s</a>。  发票：%s' % (settings.DOMAIN, user_profile.webapp_template, user_profile.weapp_id, order.order_id ,order.order_id, bill)
# 	except:
# 		return None,None
#
# def _send_email(order, user_order_notify_setting, content_described, order_status_href, order_status_url, is_pay=False):
# 	black_list = user_order_notify_setting.black_list.split(',')
#
# 	# if order.order_source in black_list:
# 	# 	return
#
# 	try:
# 		if is_pay:
# 			order_list = user_order_notify_setting.pay_email_list.split(',')
# 		else:
# 			order_list = user_order_notify_setting.create_email_list.split(',')
# 		for email in order_list:
# 			if is_pay:
# 				watchdog_info(email)
# 			sendmail(email, content_described, order_status_href)
# 	except:
# 		watchdog_notice(u'发送qq邮件时异常，订单号：%s, 异常信息:\n%s' % (order.order_id, unicode_full_stack()))
#
