#coding: utf8
"""@package weapp.webapp.handlers.test
event_handler_util的测试脚本

"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weapp.settings')
#for path in sys.path: print(path)
import weapp.settings

def test_local_handle():
	# 测试本地情况的handle
	from webapp.handlers.event_handler_util import *
	args = {
		'GET': {'get1':'value1', 'get2':'value2'},
		'COOKIES': '<cookie>',
		'method': 'GET',
		'POST': {'post1': 'value1', 'post2': 'value2'},
		'data': {
			'app_id': '123',
			'user_id': '1234',
			'webppuser_id': '1234',
			'user_profile_id': '1234',
			'social_account_id': '1234',
			'member_id': '1234',
			'is_user_from_mobile_phone': False,
			'is_user_from_weixin': False,
			},
		'visit_data': '<visit_data>'
	}
	result = handle(args, 'example')
	print('result: {}'.format(result))

if __name__=="__main__":
	test_local_handle()
