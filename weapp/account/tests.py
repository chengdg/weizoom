# jz 2015-10-10
# """
# This file demonstrates writing tests using the unittest module. These will pass
# when you run "manage.py test".

# Replace this with more appropriate tests for your application.
# """

# from django.test import TestCase
# from django.test.client import Client
# from django.db import connection
# from django.conf import settings

# from core.jsonresponse import decode_json_str
# from templatetags.account_filter import *
# from account.models import *
# from message.models import Session, WeixinUser

# class AccountTest(TestCase):
# 	def setUp(self):
# 		self.client = Client()

# 	#获取response对象中的json数据
# 	def get_json(self, response):
# 		#去掉头部信息，截取返回的json字符串
# 		data_str = str(response).split('\n\n')[1].strip()
# 		#解析json字符串，返回json对象
# 		return decode_json_str(data_str)


# 	def test_1_account(self):
# 		settings.MODE = 'deploy' #设置MODE为deploy，防止session自动显示

# 		#test用户登录
# 		self.client.login(username='test', password='test')

# 		# 没有绑定账号， 进入绑定公众账号界面
# 		response = self.client.get('/account/mp/')
# 		self.assertEquals('account-mp', response.context['nav_name'])
# 		self.assertFalse(response.context['mp_user'])

# 		# 绑定公众账号
# 		# 创建用户登录信息
# 		data = {
# 			'username': 'robert',
# 			'password': 'weizoom',
# 		    'access_token': 'robert_474',
# 		    'cookie': 'cert=robert;slave_user=12eqweqqe2321qweqwe;slave_sid=adderd9700080afa',
# 		    'fakeId': 'robert_1369963462474'
# 		}
# 		response = self.client.post('/account/api/weixin_mp_user_login_info/create/', data)
# 		self.assertEquals(200, response.status_code)

# 		# 已绑定账号， 跳转预览设置界面
# 		response = self.client.get('/account/mp/')
# 		self.assertEquals(302, response.status_code)

# 		# 进入预览设置界面
# 		response = self.client.get('/account/preview_info/')
# 		self.assertEquals('account-mp', response.context['nav_name'])
# 		preview_info = response.context['preview_user']
# 		self.assertTrue(preview_info)
# 		self.assertEquals('robert', preview_info.name)
# 		self.assertEquals('/static/img/user-1.jpg', preview_info.image_path)

# 		# 修改预览信息
# 		self.client.post('/account/api/preview_user/update/',
# 						{'id': preview_info.id, 'name': u'预览信息', 'pic_url': '/static/img/100.jpg'})

# 		# 获取信息
# 		response = self.client.get('/account/api/preview_info/get/')
# 		data = self.get_json(response)['data']
# 		self.assertEquals(u'预览信息', data['name'])
# 		self.assertEquals('/static/img/100.jpg', data['image_path'])

# 		#
# 		# 2. 测试首页
# 		#
# 		user = User.objects.get(username='test')
# 		user_profile = UserProfile.objects.get(user=user)
# 		user_profile.is_mp_registered = True
# 		user_profile.save()

# 		#没有todo
# 		response = self.client.get('/')
# 		self.assertFalse(response.context['has_todo'])
# 		self.assertEquals(0, len(response.context['todos']))
# 		self.assertEquals(0, response.context['todo_count'])

# 		#发送消息
# 		self.client.logout()
# 		self.client.post('/simulator/api/weixin/send/', {'weixin_user_name':'zhouxun', 'shop_name':'3180', 'content':'msg11', 'weixin_user_fakeid':'zhouxun'})
# 		self.client.post('/simulator/api/weixin/send/', {'weixin_user_name':'yaochen', 'shop_name':'3180', 'content':'msg21', 'weixin_user_fakeid':'yaochen'})
# 		self.client.post('/simulator/api/weixin/send/', {'weixin_user_name':'yaochen', 'shop_name':'3180', 'content':'msg22', 'weixin_user_fakeid':'yaochen'})
# 		self.client.post('/simulator/api/weixin/send/', {'weixin_user_name':'yangmi', 'shop_name':'3180', 'content':'msg31', 'weixin_user_fakeid':'yangmi'})
# 		self.client.post('/simulator/api/weixin/send/', {'weixin_user_name':'yangmi', 'shop_name':'3180', 'content':'msg32', 'weixin_user_fakeid':'yangmi'})
# 		self.client.post('/simulator/api/weixin/send/', {'weixin_user_name':'yangmi', 'shop_name':'3180', 'content':'msg33', 'weixin_user_fakeid':'yangmi'})
# 		self.client.get('/message/api/session/enable/?id=1')
# 		self.client.get('/message/api/session/enable/?id=3')

# 		#验证todo出现
# 		self.client.login(username='test', password='test')
# 		response = self.client.get('/')
# 		self.assertTrue(response.context['has_todo'])
# 		self.assertEquals(1, len(response.context['todos']))
# 		self.assertEquals(1, response.context['todo_count'])
# 		todo = response.context['todos'][0]
# 		self.assertEquals(u'收到4条新消息', todo['text'])
# 		self.assertEquals('/message/', todo['url'])

# 		#访问message列表后，todo消失
# 		self.client.get('/message/')
# 		response = self.client.get('/')
# 		self.assertFalse(response.context['has_todo'])
# 		self.assertEquals(0, len(response.context['todos']))
# 		self.assertEquals(0, response.context['todo_count'])

# 		#再次发送消息，todo出现
# 		self.client.logout()
# 		self.client.post('/simulator/api/weixin/send/', {'weixin_user_name':'zhouxun', 'shop_name':'3180', 'content':'msg13', 'weixin_user_fakeid':'zhouxun'})
# 		self.client.login(username='test', password='test')
# 		response = self.client.get('/')
# 		self.assertTrue(response.context['has_todo'])
# 		self.assertEquals(1, len(response.context['todos']))
# 		self.assertEquals(1, response.context['todo_count'])
# 		todo = response.context['todos'][0]
# 		self.assertEquals(u'收到1条新消息', todo['text'])
# 		self.assertEquals('/message/', todo['url'])

# from test.app_test_suites_loader import *
# from account_util_tests import AccountUtilTest

# test_cases = [
# 	AccountTest,
# 	AccountUtilTest,
# ]

# def suite():
# 	test_suites_in_cur_file = build_test_suite_from(test_cases)
# 	test_suites_in_all_others = load_testsuits_from_app('account')

# 	test_suites_in_all_others.addTests(test_suites_in_cur_file)
# 	return test_suites_in_all_others