# -*- coding: utf-8 -*-

__author__ = 'chuter'

class AlipayConfig(object):
	"""
	支付宝支付配置信息
	"""

	def __init__(self):
		raise NotImplementedError

	#合作身份者ID，以2088开头由16位纯数字组成的字符串
	partner = "2088011762225307"

	# 交易安全检验码，由数字和字母组成的32位字符串
	# 如果签名方式设置为“MD5”时，请设置该参数
	key = "82i3y2zodm1cp18nv57xj5uovurxlzbl"

	# 商户的私钥
	# 如果签名方式设置为“0001”时，请设置该参数
	private_key = ""

	# 支付宝的公钥
	# 如果签名方式设置为“0001”时，请设置该参数
	ali_public_key = ""

	# 字符编码格式 目前支持  utf-8
	input_charset = "utf-8"

	# 签名方式，选择项：0001(RSA)、MD5
	sign_type = "MD5"
	# 无线的产品中，签名方式为rsa时，sign_type需赋值为0001而不是RSA

	seller_email = 'dftejiang@163.com'