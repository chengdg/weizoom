# -*- coding: utf-8 -*-

__author__ = 'chuter'

class WxpayConfig(object):
	"""
	微信支付配置信息
	"""

	def __init__(self):
		raise NotImplementedError

	#合作商户号
	partner = "1218640801"

	app_id = "wxe4d695b586d21dba"

	pay_signkey = "EBLl1cqAe1Smk1a4xbYnVdnaB2SJWegsrc1PyVPKWm6NCGOXphtFw7ybn9YWePP45Cyw1vYKR7Zb3HgELVAnQpHjhXRldOehntBW68XCvwnCTS9ShshLoZ0OK2zmCTnB"

	#密钥
	partner_key = "3afdaddb1d2de50caf0db8423da7a6cb"

	#字符编码格式 目前支持  utf-8
	input_charset = "UTF-8"

	#签名方式，默认为MD5
	sign_type = "MD5"