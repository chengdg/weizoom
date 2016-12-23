# -*- coding: utf-8 -*-

__author__ = 'bert'

from dateutil import get_current_datetime

from django.conf import settings

from bdem import msgutil
from eaglet.core import watchdog

from weixin2 import models as weixin_models
from mall.promotion import models as mall_models


def send_mns_message(topic_name, message_name, data):
	msgutil.send_message(topic_name, message_name, data)

	message = u"send_mns_message, topic_name:{}, message_name:{}, data:{}".format(topic_name, message_name, data)
	watchdog.info(message)


def coupon_issuing_tmpl_compatible(tmpl_name):
	"""
	decorator
	为了兼容新旧消息模板，首先检测商家是否配置了新的tmpl_name，如果是的话，则采用新的阿里云消息机制，
	否则，使用旧的celery机制
	注：为了能够获取到商家的woid，所以，被装饰的函数第一个参数要求是CouponRule的实例
	:param tmpl_name: 新模板的消息名称
	"""
	def wrapper(func):
		def inner(*args, **kwargs):
			#判断是否配置了新的模版
			coupon_rule = args[0]
			woid = coupon_rule.owner_id
			member_id = args[1]


			if has_new_tmpl(woid, tmpl_name):
				all_member_noused_coupons = mall_models.Coupon.objects.filter(member_id=member_id,
																			  status=mall_models.COUPON_STATUS_UNUSED)
				total_money = 0
				for coupon in all_member_noused_coupons:
					total_money += coupon.money

				#商家配置了新的模板消息，则使用mns,并返回空函数
				send_weixin_template_msg({
					'user_id': woid,
					'member_id': member_id,
					'name': tmpl_name,
					'url': '',
					'items': {
						'keyword1': u'个人中心-我的优惠券',
						'keyword2': str(coupon_rule.money),
						'keyword3': str(total_money),
						'keyword4': get_current_datetime(),
					}
				})
				return empty_func()
			else:
				return func(*args, **kwargs)

		return inner
	return wrapper

def empty_func():
	pass

def has_new_tmpl(owner_id, tmpl_name):
	user_tmpls = weixin_models.UserTemplateSettings.objects.filter(owner_id=owner_id, title=tmpl_name, status=True)
	return user_tmpls.count() > 0


def send_weixin_template_msg(data):
	topic_name = 'test-weixin-topic'
	message_name = 'template_msg'
	data['test_env'] = settings.TEST_ENV

	send_mns_message(topic_name, message_name, data)