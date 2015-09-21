# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import copy
import shutil
import random

from itertools import chain

from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db.models import Q, F

from core.jsonresponse import JsonResponse, create_response
from core.exceptionutil import full_stack, unicode_full_stack
from core import dateutil
from core.wxapi.weixin_api import *
from core.wxapi import get_weixin_api
from core.wxapi.weixin_api import WeixinApi

from tools.regional import views as regional_util
from tools.express import util as express_util


#from mall.models import Order,Product
from modules.member import module_api as member_model_api

from models import *

from core.wxapi import get_weixin_api
from account.util import get_binding_weixin_mpuser, get_mpuser_accesstoken
from account.models import UserProfile
from watchdog.utils import watchdog_warning, watchdog_error, watchdog_info


def get_template_message_by(owner, send_point):
	if MarketToolsTemplateMessageDetail.objects.filter(owner=owner, template_message__send_point=send_point, status=1).count() > 0:
		return MarketToolsTemplateMessageDetail.objects.filter(owner=owner, template_message__send_point=send_point, status=1)[0]
	else:
		return None

########################################################################
# send_template_message: 发送模板消息
########################################################################
def send_order_template_message(webapp_id, order_id, send_point):
	user_profile = UserProfile.objects.get(webapp_id=webapp_id)
	user = user_profile.user
	template_message = get_template_message_by(user, send_point)

	from mall.models import Order
	order =  Order.objects.get(id=order_id)

	if order and user_profile and template_message and template_message.template_id:
		mpuser_access_token = _get_mpuser_access_token(user)
		if mpuser_access_token:
			try:
				weixin_api = get_weixin_api(mpuser_access_token)

				message = _get_order_send_message_dict(user_profile, template_message, order, send_point)
				result = weixin_api.send_template_message(message, True)
				#_record_send_template_info(order, template_message.template_id, user)
				# if result.has_key('msg_id'):
				# 	UserSentMassMsgLog.create(user_profile.webapp_id, result['msg_id'], MESSAGE_TYPE_TEXT, content)
				return True
			except:
				notify_message = u"发送模板消息异常, cause:\n{}".format(unicode_full_stack())
				watchdog_warning(notify_message)
				return False
		else:
			return False

	return True

def _get_mpuser_access_token(user):
	mp_user = get_binding_weixin_mpuser(user)
	if mp_user:
		mpuser_access_token = get_mpuser_accesstoken(mp_user)
	else:
		return False

	if mpuser_access_token is None:
		return False

	if mpuser_access_token.is_active:
		return mpuser_access_token
	else:
		return None

def _get_order_send_message_dict(user_profile, template_message, order, send_point):
	template_data = dict()
	social_account = member_model_api.get_social_account(order.webapp_user_id)
	if social_account and social_account.openid:
		template_data['touser'] = social_account.openid
		template_data['template_id'] = template_message.template_id
		if user_profile.host.find('http') > -1:
			host ="%s/workbench/jqm/preview/" % user_profile.host
		else:
			host = "http://%s/workbench/jqm/preview/" % user_profile.host

		template_data['url'] = '%s?woid=%s&module=mall&model=order&action=pay&order_id=%s&workspace_id=mall&sct=%s' % (host, user_profile.user_id, order.order_id, social_account.token)

		template_data['topcolor'] = "#FF0000"
		detail_data = {}
		template_message_detail = template_message.template_message
		detail_data["first"] = {"value" : template_message.first_text, "color" : "#000000"}
		detail_data["remark"] = {"value" : template_message.remark_text, "color" : "#000000"}
		order.express_company_name =  u'%s快递' % express_util.get_name_by_value(order.express_company_name)
		if template_message_detail.attribute:
			attribute_data_list = template_message_detail.attribute.split(',')
			for attribute_datas in attribute_data_list:
				attribute_data = attribute_datas.split(':')
				key = attribute_data[0].strip()
				attr = attribute_data[1].strip()
				if attr == 'final_price' and getattr(order, attr):
					value = u'￥%s［实际付款］' % getattr(order, attr)
					detail_data[key] = {"value" : value, "color" : "#173177"}
				elif hasattr(order, attr):
					if attr == 'final_price':
						value = u'￥%s［实际付款］' % getattr(order, attr)
						detail_data[key] = {"value" : value, "color" : "#173177"}
					elif attr == 'payment_time':
						dt = datetime.now()
						payment_time = dt.strftime('%Y-%m-%d %H:%M:%S')
						detail_data[key] = {"value" : payment_time, "color" : "#173177"}
					else:
						detail_data[key] = {"value" : getattr(order, attr), "color" : "#173177"}
				else:
					if 'number' == attr:
						number = order.get_order_has_product_number(order)
						detail_data[key] = {"value" : number, "color" : "#173177"}

					if 'product_name' == attr:
						products = order.get_order_has_product(order)
						product_names =','.join([p.name for p in products])
						detail_data[key] = {"value" : product_names, "color" : "#173177"}
		template_data['data'] = detail_data
	return template_data


def _record_send_template_info(order, template_id, user):
	if order:
		member = member_model_api.get_member_by(order.webapp_user_id)
		if member:
			MarketToolsTemplateMessageSendRecord.objects.create(owner=user, template_id=template_id, member_id=member.id, order_id=order.order_id)



########################################################################
# send_weixin_template_message: 发送优惠劵模板消息
# webapp_owner_id : 55
# member_id: 2
# send_point: COUPON_ARRIVAL_NOTIFY/COUPON_EXPIRED_REMIND
#
#  	发送优惠劵的model格式
# model: {
# 	"coupon_store": u'全部可用',
# 	"coupon_rule": u'每笔订单满159元即可使用本卷' or u'不限'
# }
########################################################################
def send_weixin_template_message(webapp_owner_id, member_id, model, send_point):
	if _is_member_subscribed(member_id):
		# 会员已经取消关注
		return True

	user_profile = UserProfile.objects.get(user_id=webapp_owner_id)
	user = user_profile.user
	template_message = get_template_message_by(user_profile.user, send_point)
	if not template_message:
		return False
	template_message.send_point = send_point
	#return _get_send_message_dict(user_profile, member_id, model, template_message)

	if model and user_profile and template_message and template_message.template_id:
		mpuser_access_token = _get_mpuser_access_token(user)
		if mpuser_access_token:
			try:
				weixin_api = get_weixin_api(mpuser_access_token)

				message = _get_send_message_dict(user_profile, member_id, model, template_message)
				result = weixin_api.send_template_message(message, True)
				#_record_send_template_info(order, template_message.template_id, user)
				return True
			except:
				notify_message = u"发送模板消息异常, cause:\n{}".format(unicode_full_stack())
				watchdog_warning(notify_message)
				return False
		else:
			return False

	return True

## 会员是否取消关注
def _is_member_subscribed(member_id):
	member = member_model_api.get_member_by_id(id=member_id)
	if member and member.is_subscribed is True:
		return False

	return True


def _get_host(user_profile):
	if user_profile.host.find('http') > -1:
		host = user_profile.host
	else:
		host = "http://%s" % user_profile.host
	return host


def _get_send_message_dict(user_profile, member_id, model, template_message):
	template_data = dict()
	social_account = member_model_api.get_social_account_by_member_id(member_id)

	if social_account and social_account.openid:
		template_data['touser'] = social_account.openid
		template_data['template_id'] = template_message.template_id
		template_data['topcolor'] = "#FF0000"
		template_data['url'] = __get_template_url(template_message.send_point, user_profile, social_account, model)

		detail_data = {}
		detail_data["first"] = {"value" : template_message.first_text, "color" : "#000000"}
		detail_data["remark"] = {"value" : template_message.remark_text, "color" : "#000000"}

		customer_data = __get_detail_data_by_template(template_message.template_message, model)
		detail_data = dict(detail_data, **customer_data)

		template_data['data'] = detail_data
	return template_data

def __get_template_url(send_point, user_profile, social_account, model):
	host = _get_host(user_profile)
	if send_point == COUPON_ARRIVAL_NOTIFY or send_point == COUPON_EXPIRED_REMIND:
		return u'{}/workbench/jqm/preview/?module=market_tool:coupon&model=usage&action=get&workspace_id=market_tool:coupon&webapp_owner_id={}&project_id=0&sct={}'.format(host, user_profile.user.id, social_account.token)

	return u''

def __get_detail_data_by_template(template_message_detail, model):
	detail_data = dict()
	if template_message_detail.attribute:
		if template_message_detail.send_point == COUPON_ARRIVAL_NOTIFY:
			return __get_coupon_detail_data(template_message_detail.attribute, model)
		elif template_message_detail.send_point == COUPON_EXPIRED_REMIND:
			return __get_coupon_detail_data(template_message_detail.attribute, model)

	return detail_data


def __get_coupon_detail_data(attribute, model):
	detail_data = dict()

	attribute_data_list = attribute.split(',')
	for attribute_datas in attribute_data_list:
		attribute_data = attribute_datas.split(':')
		key = attribute_data[0].strip()
		attr = attribute_data[1].strip()

		value = u'{}'.format(model.get(attr))
		detail_data[key] = {"value" : value, "color" : "#173177"}

	return detail_data
