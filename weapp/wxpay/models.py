# -*- coding: utf-8 -*-

__author__ = 'chuter'

from django.db import models

#===============================================================================
# WebAppUser: WebApp的用户
#===============================================================================
class PayWarningNotify(models.Model):
	appid = models.CharField(max_length=64)
	error_type = models.IntegerField()
	description = models.TextField()
	alarm_content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True) #创建时间

	class Meta(object):
		db_table = 'wxpay_warning_notify'
		verbose_name = '微信支付告警通知'
		verbose_name_plural = '微信支付告警通知'

	@staticmethod
	def create_by_post_data_soup(post_data_soup):
		if post_data_soup is None:
			return None

		return PayWarningNotify.objects.create(
			appid = post_data_soup.appid.text,
			error_type = int(post_data_soup.errortype.text),
			description = post_data_soup.description.text,
			alarm_content = post_data_soup.alarmcontent.text
			)

class PayFeedback(models.Model):
	appid = models.CharField(max_length=64)
	openid = models.CharField(max_length=64)
	feedback_id = models.CharField(max_length=64) #投诉单号
	reason = models.TextField()
	detail_xml = models.TextField()

	class Meta(object):
		db_table = 'wxpay_feedback'
		verbose_name = '微信支付维权信息'
		verbose_name_plural = '微信支付维权信息'

	@staticmethod
	def create_by_post_data_soup(post_data_soup):
		if post_data_soup is None:
			return None

		return PayFeedback.objects.create(
			appid = post_data_soup.appid.text,
			openid = post_data_soup.openid.text,
			feedback_id = post_data_soup.feedbackid.text,
			reason = post_data_soup.reason.text,
			detail_xml = post_data_soup.__str__()
			)