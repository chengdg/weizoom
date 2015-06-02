# -*- coding: utf-8 -*-

__author__ = 'chuter'


import hashlib

#===================================================
# md5_sign : 使用MD5的签名字符串
#===================================================
def md5_sign(text, key=None):
	if key == None:
		sign_source = "{}".format(text)
	else:
		sign_source = "{}&key={}".format(text, key)
	return hashlib.md5(sign_source).hexdigest().upper()


def sha1_sign(text, key=None):
	if key == None:
		sign_source = "{}".format(text)
	else:
		sign_source = "{}&key={}".format(text, key)
	return hashlib.sha1(sign_source).hexdigest()