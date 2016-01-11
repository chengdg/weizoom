# -*- coding: utf-8 -*-

__author__ = 'paco bert'

import json
from utils.url_helper import complete_get_request_url
import api_settings
from util import *
from custom_message import build_custom_message_json_str, TextCustomMessage
from core.wxpay.sign import sha1_sign

""""
	发货通知api:
	http请求方式: POST
	http://api.weixin.qq.com/pay/delivernotify?access_token=xxxxxx
	1.获得api请求地址

	2.获得请求结果  注：异常信息统交给WeixinApi

	3.格式化请求结果

	4.格式化post数据
	{
	"appid" : wwwwb4f85f3a797777",
	"openid" : oX99MDgNcgwnz3zFN3DNmo8uwa"
	"transid" : 111112222233333","transid" 
	"out_trade_no" : 555666uuu",
	"deliver_timestamp" :'时间戳 这里的时间戳是生成app_signature 时使用的时间戳'
	"deliver_status" : 1",
	"deliver_msg":'ok'
	 "app_signature" : 53cca9d47b883bd4a5c85a9300df3da0cb48565c",：appid, openid, transid, out_trade_no, deliver_timestamp, sign_method, deliver_status,deliver_msg生成的签名
	"sign_method" : sha1"
	}

	
	*使用方法：
	weixin_api = get_weixin_api(mpuser_access_token)
	post_message = PayDeliverMessage(
		appid 是公众平台账户的 AppId；
		appkey 支付专用签名串 appkey:
		openid 是购买用户的 OpenId;
		transid 是交易单号；
		out_trade_no 单号;
		deliver_timestamp 是发货时间戳，这里指得是 linux 时间戳;
		deliver_status 是发货状态，1 表明成功，0 表明失败，失败时需要在 deliver_msg 填上失败原因；
		deliver_msg是发货状态信息，失败时可以填上 UTF8 编码的错误提示信息，比如“该商品已退款”；
		)
	result = weixin_api.create_deliverynotify(post_message, True) #True 失败重试请求api False 失败后不重试

	api：返回结果
		微信公众平台在校验 ok 之后，会返回数据表明是否通知成功，例如：
		{"errcode":0,"errmsg":"ok"}
		a.如果有异常，会在 errcode 和 errmsg 描述出来，如果成功 errcode 就为 0
		b.如果不包含 errcode 则是 访问api异常 异常信息会存到watchdog error级别
		
	if result.has_key('errcode'):
		errcode = result['errcode']
		...    
"""

class PayDeliverMessage(object):
	##########################################################
	#appid 是公众平台账户的 AppId；
	#appkey 是公众平台账户的 appkey:
	#openid 是购买用户的 OpenId;
	#transid 是交易单号；
	#out_trade_no 单号;
	#deliver_timestamp 是发货时间戳，这里指得是 linux 时间戳;
	#deliver_status 是发货状态，1 表明成功，0 表明失败，失败时需要在 deliver_msg 填上失败原因；
	#deliver_msg是发货状态信息，失败时可以填上 UTF8 编码的错误提示信息，比如“该商品已退款”；
	##########################################################
	def __init__(self, appid, appkey, openid, transid, out_trade_no,deliver_timestamp, deliver_status='1',deliver_msg='ok'):
		if appid == None or appid == '':
			raise ValueError(u'appid con not be none or ""')

		if appkey == None or appkey == '':
			raise ValueError(u'appkey con not be none or ""')

		if openid == None or openid == '':
			raise ValueError(u'openid con not be none or ""')

		if transid == None or transid == '':
			raise ValueError(u'transid con not be none or ""')
		
		if out_trade_no == None or out_trade_no == '':
			raise ValueError(u'out_trade_no con not be none or ""')

		# if app_signature == None or app_signature == '':
		# 	raise ValueError(u'app_signature con not be none or ""')

		# if sign_method == None or sign_method == '':
		# 	raise ValueError(u'sign_method con not be none or ""')

		self.appid = appid
		self.appkey = appkey
		self.openid = openid
		self.transid = transid
		self.deliver_timestamp = deliver_timestamp
		self.out_trade_no = out_trade_no
		self.sign_method = 'sha1'
		self.deliver_status = deliver_status
		self.deliver_msg = deliver_msg

		self.app_signature = sha1_sign(appid, appkey, openid, transid, out_trade_no, deliver_timestamp, deliver_status, deliver_msg)

	def get_message_json_str(self):
		return json.dumps({"appid" : self.appid, "deliver_timestamp":self.deliver_timestamp, "openid" : self.openid, "transid":self.transid, "out_trade_no":self.out_trade_no,"app_signature":self.app_signature,"sign_method":self.sign_method,"deliver_status":self.deliver_status,"deliver_msg":self.deliver_msg})


PAY_DELIVERNOTIFY_MSG_URI = 'pay/delivernotify'
class WeixinPayDeliverNotifyApi(object):

	def get_get_request_url_and_api_info(self, mpuser_access_token=None, varargs=()):
		if len(varargs) >= 3 and len(varargs) == 0:
			raise ValueError(u'WeixinPayDeliverNotifyApi.get_get_request_url error, param illegal')

		if mpuser_access_token is None:
			raise ValueError(u'WeixinPayDeliverNotifyApi get_get_request_url_and_api_info：mpuser_access_token is None')
		return self._complete_weixin_api_get_request_url(mpuser_access_token), u'发货通知api'

	def parse_response(self, api_response):
		return api_response

	###############################################################################
	#	args 参数：args =（sendto_openid, custom_msg_instance	
	###############################################################################
	def parese_post_param_json_str(self, args):
		
		if isinstance(args[0], PayDeliverMessage) is False:
			raise ValueError(u'WeixinPayDeliverNotifyApi param PayDeliverMessage illegal')			

		return args[0].get_message_json_str()

	def request_method(self):
		return api_settings.API_POST

	def _complete_weixin_api_get_request_url(self, mpuser_access_token):
		param_dict = {}
		param_dict['access_token'] = mpuser_access_token.access_token
		return complete_get_request_url(
				api_settings.WEIXIN_API_PROTOCAL, 
				api_settings.WEIXIN_API_DOMAIN,
				PAY_DELIVERNOTIFY_MSG_URI,
				param_dict
				)

	def is_retry(self, args):
		if len(args) == 2:
			return True if args[1] is True else False
		return False