# -*- coding: utf-8 -*-

__author__ = 'chuter'

class TenpayConfig(object):
	"""
	财付通支付配置信息
	"""

	def __init__(self):
		raise NotImplementedError

	#合作商户号
	partner = "1218210701"

	#密钥
	key = "03096f335a76f90444b96ec76a93a427"

	#字符编码格式 目前支持  utf-8
	input_charset = "UTF-8"

	#签名方式，默认为MD5
	sign_type = "MD5"