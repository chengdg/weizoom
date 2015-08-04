# -*- coding: utf-8 -*-

__author__ = 'liupeiyu'

import sys
import unittest

if __name__ == '__main__':
	sys.path.insert(0, '../../')
	sys.path.insert(0, '../')

from test import test_env_with_db as test_env

from account.models import *
from core.weibo.weibo_authorize import WeiboAuthorize
from core.weibo.weibo_access_token import WeiboAccessToken
from core.weibo.weibo_token_info import WeiboTokenInfo
from core.weibo.weibo_user_info import WeiboUserInfo
from core.weibo.weibo_config import WeiboConfig
import urllib
import urllib2
from account.social_account.models import UserSocialLoginConfig


class WeiboUtilTest(unittest.TestCase):
	def setUp(self):
		self.user_profile = UserProfile.objects.get(shop_name='3180')
		try:
			UserSocialLoginConfig.objects.create(owner=self.user_profile.user, weibo_app_key='', weibo_app_secret='',
				qq_app_id='qq_app_id11', qq_app_key='qq_app_key22')
		except:
			pass
		self.request_test = RequestInfo
		self.request_test.user_profile = self.user_profile


	def test_get_authorize_url(self):
		weibo = WeiboAuthorize(self.request_test)
		url = weibo.get_Http_authorize_url()
		print 'test_get_authorize_url'
		print url
		self.assertTrue(True)

	def test_get_access_token(self):
		weibo = WeiboAccessToken(self.request_test, 'code123')
		result = u'{ "access_token":"SlAV32hkKG", "remind_in ":3600, "expires_in":3600 } '
		data = weibo._parse_result(result)
		print 'test_get_access_token'
		print data
		print data.get('access_token')
		self.assertEquals('SlAV32hkKG', data.get('access_token'))

	def test_get_token_info(self):
		access_token = 'SlAV32hkKG'
		weibo = WeiboTokenInfo(self.request_test, access_token)
		result = '''{
	       "uid": 1073880650,
	       "appkey": 1352222456,
	       "scope": null,
	       "create_at": 1352267591,
	       "expire_in": 157679471
	    }'''
		data = weibo._parse_result(result)
		print 'test_get_token_info'
		print data
		print data.get('uid')
		self.assertEquals(1073880650, data.get('uid'))

	def test_get_user_info(self):
		access_token = 'SlAV32hkKG'
		uid = '1073880650'
		social_account = Social
		social_account.token= access_token
		social_account.openid = uid

		weibo = WeiboUserInfo(self.request_test.user_profile, social_account)
		result = u'''{"id": 1073880650,
			    "screen_name": "zaku",
			    "name": "zaku",
			    "province": "11",
			    "city": "5",
			    "location": "北京 朝阳区",
			    "description": "人生五十年，乃如梦如幻；有生斯有死，壮士复何憾。",
			    "url": "http://blog.sina.com.cn/zaku",
			    "profile_image_url": "http://tp1.sinaimg.cn/1404376560/50/0/1",
			    "domain": "zaku",
			    "gender": "m",
			    "followers_count": 1204,
			    "friends_count": 447,
			    "statuses_count": 2908,
			    "favourites_count": 0,
			    "created_at": "Fri Aug 28 00:00:00 +0800 2009",
			    "following": false,
			    "allow_all_act_msg": false,
			    "geo_enabled": true,
			    "verified": false,
			    "status": {
			        "created_at": "Tue May 24 18:04:53 +0800 2011",
			        "id": 11142488790,
			        "text": "我的相机到了。",
			        "source": "<a href='http://weibo.com' rel='nofollow'>新浪微博</a>",
			        "favorited": false,
			        "truncated": false,
			        "in_reply_to_status_id": "",
			        "in_reply_to_user_id": "",
			        "in_reply_to_screen_name": "",
			        "geo": null,
			        "mid": "5610221544300749636",
			        "annotations": [],
			        "reposts_count": 5,
			        "comments_count": 8
			    },
			    "allow_all_comment": true,
			    "avatar_large": "http://tp1.sinaimg.cn/1404376560/180/0/1",
			    "verified_reason": "",
			    "follow_me": false,
			    "online_status": 0,
			    "bi_followers_count": 215}'''
		data = weibo._parse_result(result)
		print 'test_get_user_info'
		print data.get('name')
		self.assertEquals('zaku', data.get('name'))

class RequestInfo():
	def __init__(self):
		pass

class Social():
	def __init__(self):
		pass

if __name__ == '__main__':
	test_env.start_test_withdb()