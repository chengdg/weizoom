# -*- coding: utf-8 -*-
"""@package pay.weixin.api.api_pay_queryorder
统一支付API

HTTP请求方式: POST

URL: `https://api.mch.weixin.qq.com/pay/unifiedorder`

操作步骤:

 1. 获得api请求地址
 2. 获得请求结果  注:异常信息统交给WeixinPayApi
 3. 格式化请求结果
 4. 格式化POST数据

参数信息:

| 参数  | 必需 | 说明 |
| :----------- | :---: | :-------------------------------------------- |
| appid      | 是	    | 公众号appid    |
| mch_id | 是 | 微信支付分配的商户号 |
| nonce_str | 是 | 32位随机字符串  |
| sign | 是 | 签名 |
| body | 是 | 商品描述 |
| out_trade_no | 是 | 商户系统内部的订单号,32个字符内、可包含字母 |
| total_fee | 是 | 订单总金额，单位为分，不能带小数点 |
| spbill_create_ip | 是 | 订单生成的机器IP |
| notify_url | 是 | 接收微信支付成功通知 |
| trade_type | 是 | JSAPI |
| openid | 是 | 用户在商户appid下的唯一标识 |

举例:

	<xml>
	<appid>微信分配的公众账号ID</appid>
	<mch_id>微信支付分配的商户号</mch_id>
	<nonce_str><![CDATA[32位随机字符串]]></nonce_str>
	<sign><![CDATA[签名]]></sign>
	<body><![CDATA[商品描述]]></body>
	<out_trade_no>商户系统内部的订单号,32个字符内、可包含字母</out_trade_no>
	<total_fee>订单总金额，单位为分，不能带小数点</total_fee>
	<spbill_create_ip>订单生成的机器IP</spbill_create_ip>
	<notify_url>接收微信支付成功通知</notify_url>
	<trade_type>JSAPI</trade_type>
	<openid>用户在商户appid下的唯一标识</openid>
	</xml>
"""

__author__ = 'slzhu'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import random
import string
import api_settings

from sign import md5_sign
 
from utils.url_helper import complete_get_request_url

UNIFIED_ORDER_XML = u"""<xml><appid>%s</appid><mch_id>%s</mch_id><nonce_str><![CDATA[%s]]></nonce_str><sign><![CDATA[%s]]></sign><body><![CDATA[%s]]></body><out_trade_no>%s</out_trade_no><total_fee>%s</total_fee><spbill_create_ip>%s</spbill_create_ip><notify_url>%s</notify_url><trade_type>JSAPI</trade_type><openid>%s</openid></xml>"""

class UnifiedOrderMessage(object):
	def __init__(self, appid, mch_id, partner_key, out_trade_no, total_fee, spbill_create_ip, notify_url, openid, body=''):
		if appid == None or appid == '':
			raise ValueError(u'appid con not be none or ""')

		if mch_id == None or mch_id == '':
			raise ValueError(u'mch_id con not be none or ""')
		
		if partner_key == None or partner_key == '':
			raise ValueError(u'partner_key con not be none or ""')

		if out_trade_no == None or out_trade_no == '':
			raise ValueError(u'out_trade_no con not be none or ""')
		
		if total_fee == None or total_fee == '':
			raise ValueError(u'total_ffee con not be none or ""')
		
		if spbill_create_ip == None or spbill_create_ip == '':
			raise ValueError(u'spbill_create_ip con not be none or ""')
		
		if notify_url == None or notify_url == '':
			raise ValueError(u'notify_url con not be none or ""')
		
		if openid == None or openid == '':
			raise ValueError(u'openid con not be none or ""')
		
		self.appid = appid
		self.mch_id = mch_id
		self.partner_key = partner_key
		self.out_trade_no = out_trade_no
		self.total_fee = total_fee
		self.spbill_create_ip = spbill_create_ip
		self.notify_url = notify_url
		self.openid = openid
		self.body = body

		self.nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 32))
		
		package_list = {
			'trade_type':'JSAPI',
			'appid': appid,
			'body':body.encode('utf8'),
			'mch_id':mch_id,
			'nonce_str':self.nonce_str,
			'notify_url':notify_url,
			'openid':openid,
			'out_trade_no':out_trade_no,
			'spbill_create_ip':spbill_create_ip,
			'total_fee':total_fee
		}
		key_list = sorted(package_list.keys())
		sign_str = u''
		for key in key_list:
			sign_str += u"%s=%s&" % (key, package_list[key])
		sign_str += 'key=' + partner_key
		self.sign = md5_sign(sign_str)
	
	def get_message_json_str(self):
		post_xml_data = UNIFIED_ORDER_XML % (self.appid, self.mch_id, self.nonce_str, self.sign, self.body, self.out_trade_no, self.total_fee, self.spbill_create_ip, self.notify_url, self.openid)
		
		return post_xml_data


QUERY_ORDER_MSG_URI = 'pay/unifiedorder'
class WeixinPayUnifiedOrderApi(object):
	
	def get_get_request_url_and_api_info(self, access_token=None, is_for='xml', varargs=()):
		if len(varargs) >= 3 or len(varargs) == 0:
			raise ValueError(u'WeixinPayUnifiedOrderApi.get_get_request_url error, param illegal')
		if access_token is None:
			raise ValueError(u'WeixinPayUnifiedOrderApi get_get_request_url_and_api_info：access_token is None')
		return self._complete_weixin_api_get_request_url(access_token, is_for), u'统一支付接口api'

	def parse_response(self, api_response):
		return api_response

	###############################################################################
	#	args 参数：args = custom_msg_instance
	###############################################################################
	def parese_post_param_json_str(self, args):
		
		if isinstance(args[0], UnifiedOrderMessage) is False:
			raise ValueError(u'WeixinPayUnifiedOrderApi param UnifiedOrderMessage illegal')			

		return args[0].get_message_json_str()

	def request_method(self):
		return api_settings.API_POST

	def _complete_weixin_api_get_request_url(self, access_token, is_for):
		param_dict = {}
		param_dict['access_token'] = access_token
		if is_for == 'json':
			domain = api_settings.WEIXIN_API_DOMAIN
		else:
			domain = api_settings.WEIXIN_API_V3_DOMAIN
		return complete_get_request_url(
				api_settings.WEIXIN_API_PROTOCAL, 
				domain,
				QUERY_ORDER_MSG_URI,
				param_dict
				)