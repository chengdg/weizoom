# -*- coding: utf-8 -*-
"""@package pay.weixin.api.api_pay_queryorder
统一支付API

HTTP请求方式: POST

请求Url
https://api.mch.weixin.qq.com/mmpaymkttransfers/sendredpack
是否需要证书
是（证书及使用说明详见商户证书）
请求方式
POST

操作步骤:

 1. 获得api请求地址
 2. 获得请求结果  注:异常信息统交给WeixinPayApi
 3. 格式化请求结果
 4. 格式化POST数据

参数信息:
id | 是 | 用户在商户appid下的唯一标识 |

举例:

	<xml>
			<sign></sign>
            <mch_billno></mch_billno>
            <mch_id></mch_id>
            <wxappid></wxappid>
            <nick_name></nick_name>
            <send_name></send_name>
            <re_openid></re_openid>
            <total_amount></total_amount>
            <min_value></min_value>
            <max_value></max_value>
            <total_num></total_num>
            <wishing></wishing>
            <client_ip></client_ip>
            <act_name></act_name>
            <act_id></act_id>
            <remark></remark>
            <logo_imgurl></logo_imgurl>
            <share_content></share_content>
            <share_url></share_url>
            <share_imgurl></share_imgurl>
            <nonce_str></nonce_str>
        </xml>
"""

__author__ = 'bert'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import random
import string
import time
import api_settings

from urllib import quote  
import xml.etree.ElementTree as ET  
  
try:  
    import pycurl  
    from cStringIO import StringIO  
except ImportError:  
    pycurl = None  

from sign import md5_sign
 
#from utils.url_helper import complete_get_request_url

SSLCERT_PATH = "./apiclient_cert.pem"  
SSLKEY_PATH = "./apiclient_key.pem"  

class CurlClient(object):
	"""使用Curl发送请求"""
	def __init__(self):
		self.curl = pycurl.Curl()
		self.curl.setopt(pycurl.SSL_VERIFYHOST, False)
		self.curl.setopt(pycurl.SSL_VERIFYPEER, False)
		#设置不输出header
		self.curl.setopt(pycurl.HEADER, False)

	def get(self, url, second=30):
		return self.postXmlSSL(None, url, second=second, cert=False, post=False)

	def postXml(self, xml, url, second=30):
		"""不使用证书"""
		return self.postXmlSSL(xml, url, second=second, cert=False, post=True)
		

	def postXmlSSL(self, xml, url, second=30, cert=True, post=True):
		"""使用证书"""
		self.curl.setopt(pycurl.URL, url)
		self.curl.setopt(pycurl.TIMEOUT, second)
		#设置证书
		#使用证书：cert 与 key 分别属于两个.pem文件
		#默认格式为PEM，可以注释
		if cert:
			self.curl.setopt(pycurl.SSLKEYTYPE, "PEM")
			self.curl.setopt(pycurl.SSLKEY, SSLKEY_PATH)
			self.curl.setopt(pycurl.SSLCERTTYPE, "PEM")
			self.curl.setopt(pycurl.SSLCERT, SSLKEY_PATH)
		#post提交方式
		if post:
			self.curl.setopt(pycurl.POST, True)
			self.curl.setopt(pycurl.POSTFIELDS, xml)
		buff = StringIO()
		self.curl.setopt(pycurl.WRITEFUNCTION, buff.write)

		self.curl.perform()
		return buff.getvalue()


POST_XML_DATA = """<xml><sign>%s</sign><mch_billno>%s</mch_billno><mch_id>%s</mch_id><wxappid>%s</wxappid><nick_name>%s</nick_name><send_name>%s</send_name><re_openid>%s</re_openid><total_amount>%s</total_amount><min_value>%s</min_value><max_value>%s</max_value><total_num>%s</total_num><wishing>%s</wishing><client_ip>%s</client_ip><act_name>%s</act_name><remark>%s</remark><nonce_str>%s</nonce_str></xml>"""

class RedPackMessage(object):
	def __init__(self, mch_id, appid, nick_name, send_name, openid, total_amount, min_value, max_value, total_num, wishing, client_ip, act_name, remark, key):
		
		self.wxappid = appid
		self.mch_id = mch_id
		self.nick_name = nick_name

		self.send_name = send_name
		self.total_amount = total_amount
		self.client_ip = client_ip
		self.min_value = min_value
		self.openid = openid
		self.max_value = max_value
		self.total_num = total_num
		self.wishing = wishing
		self.act_name = act_name
		self.remark = remark

		self.mch_billno = "%s%s%s" % (mch_id,time.strftime("%Y%m%d%H%M%S", time.localtime()),  ''.join(random.sample(string.ascii_letters+string.digits, 4)))

		self.nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 32))
		
		package_list = {
			'nonce_str': self.nonce_str,
			'mch_billno':self.mch_billno,
			'mch_id': mch_id,
			'wxappid': appid,
			'nick_name': nick_name,
			'send_name': send_name,
			're_openid': openid,
			'total_amount': total_amount,
			'min_value': min_value,
			'max_value': max_value,
			'total_num': total_num,
			'wishing': wishing,
			'client_ip':client_ip,
			'act_name':act_name,
			'remark': remark
		}
		key_list = sorted(package_list.keys())
		sign_str = u''
		for key in key_list:
			sign_str += u"%s=%s&" % (key, package_list[key])
		sign_str += 'key=' + key
		self.sign = md5_sign(sign_str)
	
	def get_message_str(self):
		post_xml_data = POST_XML_DATA % (self.sign, 
			self.mch_billno,  self.mch_id,self.wxappid, self.nick_name, self.send_name, self.openid, self.total_amount, self.min_value, self.max_value, self.total_num, self.wishing, self.client_ip, self.act_name, self.remark, self.nonce_str)
		
		return post_xml_data

import httplib
import urllib2

PEM_FILE = '/path/certif.pem' # Renamed from PEM_FILE to avoid confusion
CLIENT_CERT_FILE = '/path/clientcert.p12' # This is your client cert!

# HTTPS Client Auth solution for urllib2, inspired by
# http://bugs.python.org/issue3466
# and improved by David Norton of Three Pillar Software. In this
# implementation, we use properties passed in rather than static module
# fields.
class HTTPSClientAuthHandler(urllib2.HTTPSHandler):
	def __init__(self, key, cert):
		urllib2.HTTPSHandler.__init__(self)
		self.key = key
		self.cert = cert
	def https_open(self, req):
		#Rather than pass in a reference to a connection class, we pass in
		# a reference to a function which, for all intents and purposes,
		# will behave as a constructor
		req.timeout = 300
		return self.do_open(self.getConnection, req)
	def getConnection(self, host):
		return httplib.HTTPSConnection(host, key_file=self.SSLKEY, cert_file=self.SSLCERT_PATH)




def test():
	red_pack_msg = RedPackMessage(
		'1231154002',
		'wx9fefd1d7a80fbe41',
		u'微众传媒',
		u'微众传媒',
		'openid',
		2,
		2,
		2,
		1,
		u'给你的红包',
		'192.168.1.221',
		u'现金红包活动',
		u'我是备注',
		'u89hjyh78ty7689u90ju8yh7yt87t76f'
		)
	xml = red_pack_msg.get_message_str()
	url = "https://api.mch.weixin.qq.com/mmpaymkttransfers/sendredpack"
	# curl_client = CurlClient()
	# x = curl_client.postXmlSSL(xml, url)
	# print xml
	cert_handler = HTTPSClientAuthHandler(PEM_FILE, CLIENT_CERT_FILE)
	opener = urllib2.build_opener(cert_handler)
	urllib2.install_opener(opener)
	# cookies = urllib2.HTTPCookieProcessor()
	request = urllib2.Request(
		url = url,
		headers = {'Content-Type' : 'text/xml'},
		data = xml.encode('utf8'))
	f = opener.open(request)
	print f





if __name__ == "__main__":
    test()



# QUERY_ORDER_MSG_URI = 'mmpaymkttransfers/sendredpack'
# class WeixinSendRedPackApi(object):
	
# 	def get_get_request_url_and_api_info(self, access_token=None, is_for='xml', varargs=()):
# 		if len(varargs) >= 3 or len(varargs) == 0:
# 			raise ValueError(u'WeixinPayUnifiedOrderApi.get_get_request_url error, param illegal')
# 		if access_token is None:
# 			raise ValueError(u'WeixinPayUnifiedOrderApi get_get_request_url_and_api_info：access_token is None')
# 		return self._complete_weixin_api_get_request_url(access_token, is_for), u'统一支付接口api'

# 	def parse_response(self, api_response):
# 		return api_response

# 	###############################################################################
# 	#	args 参数：args = custom_msg_instance
# 	###############################################################################
# 	def parese_post_param_json_str(self, args):
		
# 		if isinstance(args[0], UnifiedOrderMessage) is False:
# 			raise ValueError(u'WeixinPayUnifiedOrderApi param UnifiedOrderMessage illegal')			

# 		return args[0].get_message_json_str()

# 	def request_method(self):
# 		return api_settings.API_POST

# 	def _complete_weixin_api_get_request_url(self, access_token, is_for):
# 		param_dict = {}
# 		param_dict['access_token'] = access_token
# 		if is_for == 'json':
# 			domain = api_settings.WEIXIN_API_DOMAIN
# 		else:
# 			domain = api_settings.WEIXIN_API_V3_DOMAIN
# 		return complete_get_request_url(
# 				api_settings.WEIXIN_API_PROTOCAL, 
# 				domain,
# 				QUERY_ORDER_MSG_URI,
# 				param_dict
# 				)