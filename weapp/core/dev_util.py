# -*- coding: utf-8 -*-

__author__ = 'robert'


def print_cookies(client, msg):
	print '################# %s #####################' % msg
	if hasattr(client, 'cookies'):
		cookies = client.cookies
	else:
		cookies = client
	for cookie_value in cookies.values():
		print cookie_value.key, cookie_value.value
	print '##############################################'