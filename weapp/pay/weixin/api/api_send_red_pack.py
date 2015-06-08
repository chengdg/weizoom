# -*- coding: utf-8 -*-
"""@package api.mch.weixin.qq.com
发红包API
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
from BeautifulSoup import BeautifulSoup 
from sign import md5_sign

import httplib
import urllib2
HOST = 'api.mch.weixin.qq.com'
API_URL = '/mmpaymkttransfers/sendredpack'
 
import platform
sysstr = platform.system()
if sysstr !="Windows":
	SSLCERT_PATH = "/weapp/web/weapp/pay/weixin/api/apiclient_cert.pem"  
	SSLKEY_PATH = "/weapp/web/weapp/pay/weixin/api/apiclient_key.pem"  
else:
	SSLCERT_PATH = "D://weapp_project//web//weapp//pay//weixin//api//apiclient_cert.pem"
	SSLKEY_PATH = "D://weapp_project//web//weapp//pay//weixin//api//apiclient_key.pem"

class RedPackMessage(object):
	def __init__(self, mch_id, appid, nick_name, send_name, openid, total_amount, min_value, max_value, total_num, wishing, client_ip, act_name, remark, api_key):
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
		sign_str += 'key=' + api_key
		print sign_str
		self.sign = md5_sign(sign_str)
		package_list['sign'] = self.sign
		self.package_list = package_list

	def arrayToXml(self):  
		"""array转xml"""  
		xml = ["<xml>"]  
		for k, v in self.package_list.iteritems():   
			xml.append("<{0}><![CDATA[{1}]]></{0}>".format(k, v))  
		xml.append("</xml>")  
		return "".join(xml)

	def post_data(self, key_file, cert_file):
		xml = self.arrayToXml()
		print xml
		headers = { 
	            'Content-type'   : 'text/xml; charset=\"UTF-8\"',
	            'Content-length' : len(xml),
	          }
		conn = httplib.HTTPSConnection(HOST, key_file=SSLKEY_PATH, cert_file = SSLCERT_PATH)
		conn.request("POST", API_URL, body=xml.encode('utf8'), headers=headers)
		response = conn.getresponse()
		return response.read()

def test():
	red_pack_msg = RedPackMessage(
		'1231154002',
		'wx9fefd1d7a80fbe41',
		u'微众传媒',
		u'微众传媒',
		'oucARuLTgL5_Q9ru7P0twY9WiOJE',
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
	result = red_pack_msg.post_data(SSLKEY_PATH, SSLCERT_PATH)
	#xml = red_pack_msg.arrayToXml()
	# print result
	result = BeautifulSoup(result)
	print result
	return_code = result.return_code.text
	return_msg = result.return_msg.text
	print return_code
	print return_msg
	

# if __name__ == "__main__":
#     test()

