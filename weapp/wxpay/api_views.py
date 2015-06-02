# -*- coding: utf-8 -*-

__author__ = 'chuter'

from django.http import HttpResponse

from models import PayWarningNotify, PayFeedback

from core.exceptionutil import unicode_full_stack
from core.wxpay.wxpay_warning import WxpayWarningNotify
from core.wxpay.wxpay_feedback import WxpayFeedback

from watchdog.utils import watchdog_warning

def create_pay_warning_notify(request):
	wxpay_warning_notify = WxpayWarningNotify(request)
	notify_post_data_soup = wxpay_warning_notify.get_notify_data_soup()

	if notify_post_data_soup is not None:
		try:
			warning_notify_record = PayWarningNotify.create_by_post_data_soup(notify_post_data_soup)
			warning_msg = u"微信支付告警通知, 通知id:{}".format(warning_notify_record.id)
		except:
			warning_msg = u"创建微信支付告警通知记录失败，告警通知:\n{}, cause:\n{}"\
				.format(notify_post_data_soup.__str__(), unicode_full_stack())
			watchdog_warning(warning_msg)

	return HttpResponse("success")

def create_pay_feedback(request):
	wxpay_feedback = WxpayFeedback(request)
	feedback_post_data_soup = wxpay_feedback.get_feedback_data_soup()

	if feedback_post_data_soup is not None:
		try:
			pay_feedback_record = PayFeedback.create_by_post_data_soup(feedback_post_data_soup)
			warning_msg = u"微信支付维权, 维权id:{}".format(pay_feedback_record.id)
		except:
			warning_msg = u"创建微信支付维权记录失败，维权信息:\n{}, cause:\n{}\n请求信息:\n{}"\
				.format(feedback_post_data_soup.__str__(), unicode_full_stack(), request.META)
			watchdog_warning(warning_msg)

	return HttpResponse("success")