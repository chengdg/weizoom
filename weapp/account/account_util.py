# -*- coding: utf-8 -*-
"""
包括User和token互转的函数。

"""

#from django.contrib import auth
from django.contrib.auth.models import User
from utils.string_util import byte_to_hex, hex_to_byte

__author__ = 'chuter'

MAGIC_CODE = '*weizoom*'

def get_token_for_logined_user(user):
	"""
	根据已经登录的用户信息生成token串，可使用 get_logined_user_from_token(token)。

	@param user   登录用户信息

	@retval 据该token串解析出来对应登录后的用户信息。如果user信息非法直接返回None
	"""
	if (user is None) or (not isinstance(user, User)):
		return None

	encoded_str_with_userinfo = "{}_{}_{}".format(59, MAGIC_CODE, user.username)
	encoded_hex_str = byte_to_hex(encoded_str_with_userinfo)

	#进行字节码的混淆处理
	hex_byte_list = []
	for hex_byte in encoded_hex_str:
		hex_byte_list.append(hex_byte)
		hex_byte_list.append('0')
	return ''.join(hex_byte_list)


def get_logined_user_from_token(token, request_host='weixin.weizoom.com'):
	"""
	根据token串解析出来对应的登录后的用户信息

	与 `get_token_for_logined_user(user)` 为可逆操作。

	@param token

	@retval User对象
	"""
	if (token is None) or (not isinstance(token, str)\
		and not isinstance(token, unicode)):
		return None

	if (len(token) == 0) or (len(token) % 2 != 0):
		#token串的长度一定是偶数
		return None

	#进行token串(字节码串)的反混淆处理
	decoded_hex_byte_list = []
	max_index = len(token) - 1
	for index in xrange(0, max_index, 2):
		decoded_hex_byte_list.append(token[index])

	try:
		decoded_hex_str = ''.join(decoded_hex_byte_list)
		decoded_str = hex_to_byte(decoded_hex_str)

		#decoded_str格式为 ‘1_*weizoom*_test’，其中1为用户id(user.id)，
		#test为用户名称(user.username)
		userid_and_username = decoded_str.split("_{}_".format(MAGIC_CODE))
		if len(userid_and_username) != 2:
			return None

		userid = userid_and_username[0]
		username = userid_and_username[1]
		#进行userid和username的校验，即获取指定userid的User信息，
		#判断用户名信息是否匹配

		if 	request_host in ['weixin.weizoom.com', 'weapp.weizoom.com', 'dev.weapp.com', 'red.weapp.weizzz.com', 'weapp.dev.com']:
			user = User.objects.get(username = username)

			user.backend = 'django.contrib.auth.backends.ModelBackend'
			return user
		else:
			user = User.objects.get(id = int(userid))

			if user.username == username:
				user.backend = 'django.contrib.auth.backends.ModelBackend'
				return user
			else:
				return None
	except:
		#TODO 是否需要进行异常处理？？
		return None
