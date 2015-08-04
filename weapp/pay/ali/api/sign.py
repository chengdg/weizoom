# -*- coding: utf-8 -*-

__author__ = 'chuter'


import hashlib

#===================================================
# md5_sign : 使用MD5的签名字符串
#===================================================
def md5_sign(text, key):
	sign_source = text + key
	return hashlib.md5(sign_source).hexdigest()
