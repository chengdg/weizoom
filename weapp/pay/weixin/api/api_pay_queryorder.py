# -*- coding: utf-8 -*-
"""@package pay.weixin.api.api_pay_queryorder
查询订单API

HTTP请求方式: POST

URL: `http://api.weixin.qq.com/pay/orderquery?access_token=xxxxxx`

操作步骤:

 1. 获得api请求地址
 2. 获得请求结果  注:异常信息统交给WeixinPayApi
 3. 格式化请求结果
 4. 格式化POST数据

参数信息:

| 参数  | 必需 | 说明 |
| :----------- | :---: | :-------------------------------------------- |
| appid      | 是	    | 公众号appid    |
| package | 是 | 询订单的关键信息数据，包含第三方唯一订单号out_trade_no、财付通商户身份标识partner（即前文所述的partnerid） 、签名sign |
| timestamp | 是 | linux时间戳  |
| app_signature | 是 | 根据支付签名（paySign）生成方法中所讲的签名方式生成的，参加签名字段为:appid、appkey、package、timestamp |
| sign_method | 是 | 签名方法 |

举例:

	{
	"appid" : "wwwwb4f85f3a797777",
	"package" : "out_trade_no=11122&partner=1900090055&sign=4e8d0df3da0c3d0df38f"
	"timestamp" : "1369745073" 
	"app_signature" : 53cca9d47b883bd4a5c85a9300df3da0cb48565c",：appid, appkey, package, timestamp生成的签名
	"sign_method" : "sha1"
	}
	
使用方法:

	weixin_api = get_weixin_api(mpuser_access_token)
	post_message = QueryOrderMessage(
		appid 是公众平台账户的 AppId
		package 是查询订单的关键信息数据，包含第三方唯一订单号out_trade_no、财付通商户身份标识partner（即前文所述的partnerid） 、签名sign
		timestamp 是linux时间戳
		app_signature 是根据支付签名（paySign）生成方法中所讲的签名方式生成的，参加签名字段为：appid、appkey、package、timestamp
		sign_method 是签名方法
		)
	result = weixin_api.query_order(post_message, True) #True 失败重试请求api False 失败后不重试

	api:返回结果
		微信公众平台在校验 ok之后，会返回数据表明是否通知成功，例如：
		{"errcode":0,"errmsg":"ok"}
		a.如果有异常，会在 errcode 和 errmsg 描述出来，如果成功 errcode 就为 0
		b.如果不包含 errcode 则是 访问api异常 异常信息会存到watchdog error级别
		
	if result.has_key('errcode'):
		errcode = result['errcode']
		...    
"""

__author__ = 'slzhu'

import time
import json
import random
import string
import api_settings

from sign import md5_sign, sha1_sign
 
from utils.url_helper import complete_get_request_url

class QueryOrderMessage(object):
	##########################################################
	#app_id 微信公众号 AppId(app_id)
	#partner_id 合作商户Id(partner_id)
	#partner_key 合作商户秘钥(partner_key)
	#out_trade_no 订单号
	##########################################################
	def __init__(self, app_id, partner_id, partner_key, out_trade_no):
		if app_id == None or app_id == '':
			raise ValueError(u'app_id con not be none or ""')

		if partner_id == None or partner_id == '':
			raise ValueError(u'partner_id con not be none or ""')
		
		if partner_key == None or partner_key == '':
			raise ValueError(u'partner_key con not be none or ""')

		if out_trade_no == None or out_trade_no == '':
			raise ValueError(u'out_trade_no con not be none or ""')
		
		self.app_id = app_id
		self.partner_id = partner_id
		self.partner_key = partner_key
		self.out_trade_no = out_trade_no


class QueryOrderV2Message(QueryOrderMessage):
	##########################################################
	#app_key 支付专用签名串(paysign_key)
	#sign_method 是签名方法
	##########################################################
	def __init__(self, app_id, app_key, partner_id, partner_key, out_trade_no, sign_method='md5'):
		QueryOrderMessage.__init__(self, app_id, partner_id, partner_key, out_trade_no)

		if app_key == None or app_key == '':
			raise ValueError(u'app_key con not be none or ""')

		self.app_key = app_key
		self.sign_method = sign_method
		self.timestamp = str(int(time.time()))
		
		sign = md5_sign("out_trade_no=%s&partner=%s" % (self.out_trade_no, self.partner_id), self.partner_key)
		self.package = "out_trade_no=%s&partner=%s&sign=%s" % (self.out_trade_no, self.partner_id, sign)
		self.app_signature = sha1_sign("appid=%s&appkey=%s&package=%s&timestamp=%s" % (self.app_id, self.app_key, self.package, self.timestamp))
	
	def get_message_json_str(self):
		return json.dumps({"appid" : self.app_id, "app_signature":self.app_signature, "package":self.package, "timestamp":self.timestamp, "sign_method":self.sign_method})
	

class QueryOrderV3Message(QueryOrderMessage):
	def __init__(self, app_id, partner_id, partner_key, out_trade_no):
		QueryOrderMessage.__init__(self, app_id, partner_id, partner_key, out_trade_no)

		self.nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 32))
		self.sign = md5_sign("appid=%s&mch_id=%s&nonce_str=%s&out_trade_no=%s" % (self.app_id, self.partner_id, self.nonce_str, self.out_trade_no), self.partner_key)
	
	def get_message_json_str(self):
		WEIXIN_XML = u"""<xml><appid>%s</appid><mch_id>%s</mch_id><nonce_str><![CDATA[%s]]></nonce_str><sign><![CDATA[%s]]></sign><out_trade_no>%s</out_trade_no></xml>"""
		post_xml_data = WEIXIN_XML % (self.app_id, self.partner_id, self.nonce_str, self.sign, self.out_trade_no)
		
		return post_xml_data


QUERY_ORDER_MSG_URI = 'pay/orderquery'
class WeixinPayQueryOrderApi(object):
	
	def get_get_request_url_and_api_info(self, access_token=None, is_for='json', varargs=()):
		if len(varargs) >= 3 or len(varargs) == 0:
			raise ValueError(u'WeixinPayQueryOrderApi.get_get_request_url error, param illegal')
		if access_token is None:
			raise ValueError(u'WeixinPayQueryApi get_get_request_url_and_api_info：access_token is None')
		return self._complete_weixin_api_get_request_url(access_token, is_for), u'查询订单api'

	def parse_response(self, api_response):
		return api_response

	###############################################################################
	#	args 参数：args = custom_msg_instance
	###############################################################################
	def parese_post_param_json_str(self, args):
		
		if isinstance(args[0], QueryOrderMessage) is False:
			raise ValueError(u'WeixinPayQueryOrderApi param QueryOrderMessage illegal')			

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