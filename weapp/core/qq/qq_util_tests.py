# -*- coding: utf-8 -*-

__author__ = 'liupeiyu'

import sys
import unittest

if __name__ == '__main__':
	sys.path.insert(0, '../../')
	sys.path.insert(0, '../')

from test import test_env_with_db as test_env

from account.models import *
from core.qq.qq_authorize import QQAuthorize
from core.qq.qq_access_token import QQAccessToken
from core.qq.qq_open_id import QQOpenID
from core.qq.qq_user_info import QQUserInfo
from account.social_account.models import UserSocialLoginConfig

class QQUtilTest(unittest.TestCase):
	def setUp(self):
		pass

	def test_get_authorize_url(self):
		request = Social
		request.user_profile = None
		qq = QQAuthorize(request)
		url = qq.get_Http_authorize_url()
		print 'test_get_authorize_url'
		print url
		self.assertTrue(True)
#
#	def test_get_access_token(self):
#		qq = QQGetAccessToken(None, 'code123')
#		result = 'access_token=FE04AAACCE2&expires_in=7776000&refresh_token=88E4BE14'
#		data = qq._parse_result(result)
#		print 'test_get_access_token'
#		print data
#		print data.get('access_token')
#		self.assertEquals('FE04AAACCE2', data.get('access_token'))
#
#	def test_get_open_id(self):
#		access_token = 'FE04AAACCE2'
#		qq = QQGetOpenID(None, access_token)
#		result = 'callback( {"client_id":"YOUR_APPID","openid":"YOUR_OPENID"} );'
#		data = qq._parse_result(result)
#		print 'test_get_open_id'
#		print data
#		print data.get('openid')
#		print data.get('client_id')
#		self.assertEquals('YOUR_OPENID', data.get('openid'))

	def test_get_user_info(self):
		access_token = 'FE04AAACCE2'
		open_id = 'open_id'
		user_profile = UserProfile.objects.get(shop_name='3180')
		UserSocialLoginConfig.objects.create(owner=user_profile.user, weibo_app_key='', weibo_app_secret='',
		qq_app_id='qq_app_id11', qq_app_key='qq_app_key22')


		social_account = Social
		social_account.access_token= access_token
		social_account.openid = access_token
		qq = QQUserInfo(user_profile, social_account)
		result = '''{
   "ret":0,
   "msg":"",
   "nickname":"YOUR_NICK_NAME"
}'''
		data = qq._parse_result(result)
		print 'test_get_user_info'
		print data
		print data.get('nickname')
		self.assertEquals('YOUR_NICK_NAME', data.get('nickname'))

		print qq.qq_config.app_id
		print qq.qq_config.app_key


		from hashlib import md5
		content = 'abc'
		content_str = str(content)
		ciphertext = md5(content_str).hexdigest() #加密
		print ciphertext

		#from hashlib import md5
		#ciphertext_str=raw_input() #写入要解密的密文,如827ccb0eea8a706c4c34a16891f84e7b
		#MD5是不可逆的密码加密，可以说除了暴力破解外无法还原，但同样的输入加密出来的结果是一致的，因此要比较输入是否正确，只要比较一下加密后的结果即可，而Python中可以使用hashlib进行MD5加密，具体方法如下

		for i in xrange(100000):
			ciphertext_tmp = md5(str(i)).hexdigest()
			if ciphertext_tmp == ciphertext:
				print 'the password is %d' % i
				break

class Social():
	def __init__(self):
		pass

if __name__ == '__main__':
	test_env.start_test_withdb()