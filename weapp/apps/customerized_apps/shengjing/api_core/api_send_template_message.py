# -*- coding: utf-8 -*-

__author__ = 'liupeiyu'

from django.conf import settings
from django.contrib.auth.models import User
from core.exceptionutil import full_stack, unicode_full_stack
from account.models import UserProfile
from modules.member import module_api as member_model_api
from modules.member.models import WebAppUser
from account.util import get_binding_weixin_mpuser, get_mpuser_accesstoken
from core.wxapi import get_weixin_api

from watchdog.utils import watchdog_warning, watchdog_error, watchdog_info
from api_params import ShengjingAPIParams
from api_config import ShengjingAPIConfig


class TemplateDetail(object):
	first = u'第一句话'
	remark = u'最后一句话'
	name = u'名称'
	date_time = u'2015-01-01 08:00:00'

	def __init__(self, first, remark, name, date_time, template_type):
		self.first = first
		self.remark = remark
		self.name = name
		self.date_time = date_time
		self.template_type = template_type
		

""""
	盛景发送服务取消通知
	调用用户信息api:
	http请求方式: POST
	https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=ACCESS_TOKEN
	
	1.获得api请求地址

	2.获得请求结果  注：异常信息统交给WeixinApi

	3.格式化请求结果

	4.格式化post数据
	  {
           "touser":"OPENID",
           "template_id":"ngqIpbwh8bUfcSsECmogfXcV14J0tQlEpBO27izEYtY",
           "url":"http://weixin.qq.com/download",
           "topcolor":"#FF0000",
           "data":{
                   "first": {
                       "value":"您好，您已成功消费。",
                       "color":"#0A0A0A"
                   },
                   "keynote1":{
                       "value":"巧克力",
                       "color":"#CCCCCC"
                   },
                   "keynote2": {
                       "value":"39.8元",
                       "color":"#CCCCCC"
                   },
                   "keynote3":{
                       "value":"2014年9月16日",
                       "color":"#CCCCCC"
                   },
                   "remark":{
                       "value":"欢迎再次购买。",
                       "color":"#173177"
                   }
           }
       }
		
	发货通知：
		{{first.DATA}} 

		快递公司：{{delivername.DATA}}
		快递单号：{{ordername.DATA}}
		 {{remark.DATA}}

"""
class ShengjingTemplateMessage(object):

	text_color = "#000000"

	def __init__(self, webapp_user_id, template_detail):
		self.template_detail = template_detail
		self.shengjing_params = ShengjingAPIParams()
		self.shengjing_config = ShengjingAPIConfig()
		self.webapp_user_id = webapp_user_id
		self.webapp_id = self.get_webapp_id()
		self.user = self.get_user()


	def get_webapp_id(self):
		return WebAppUser.objects.get(id=self.webapp_user_id).webapp_id


	def get_user(self):
		return UserProfile.objects.get(webapp_id=self.webapp_id).user


	def _get_openid(self):
		social_account = member_model_api.get_social_account(self.webapp_user_id)
		if social_account and social_account.openid:				
			return social_account.openid
		else:
			return None


	def _get_message_dict(self):
		openid = self._get_openid()
		if openid is None:
			return None

		template_data = dict()
		template_data['touser'] = openid
		template_data['template_id'] = self.shengjing_config.get_message_template_id(self.template_detail.template_type)
		template_data['url'] = ''
		template_data['topcolor'] = "#0000FF"
		template_data['data'] = self.__get_templeta_data(self.template_detail)
		return template_data


	def __get_templeta_data(self, message):		
		detail_data = {
			"first": {
				"value": message.first,
				"color": self.text_color
			},
			"remark": {
				"value": message.remark,
				"color": self.text_color
			},
			"keyword1": {
				"value": message.name,
				"color": self.text_color
			},
			"keyword2": {
				"value": message.date_time,
				"color": self.text_color
			}
		}
		return detail_data


	def _get_mpuser_access_token(self, user):
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

	def send_message(self):
		try:
			message = self._get_message_dict()
			if message is None:
				return False, u"message dict错误"

			mpuser_access_token = self._get_mpuser_access_token(self.user)
			weixin_api = get_weixin_api(mpuser_access_token)
			result = weixin_api.send_template_message(message, True)
			return True, result
		except:
			notify_message = u"shengjing发送模板消息异常, cause:\n{}".format(unicode_full_stack())
			watchdog_warning(notify_message, self.shengjing_params.WATCHDOG_TYPE_SHENGJING)
			return False, unicode_full_stack()

