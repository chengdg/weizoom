# -*- coding: utf-8 -*-

__author__ = 'chuter'

class WxpayRequestParams(object):
	"""
	财付通支付请求中的参数定义
	"""
	def __init__(self):
		raise NotImplementedError

	
	SIGN_TYPE = 'sign_type' #签名类型，非必填，默认为MD5
	INPUT_CHARSET = 'input_charset' #字符编码，给必填，取值：GBK,UTF-8， 默认GBK

	#支付接口
	APPID = 'appid'
	TIMESTAMP = 'timestamp'
	NONCESTR = 'noncestr'
	PACKAGE = 'package'

	ATTACH = 'attach' #附加数据，原样返回
	BANK_TYPE = 'bank_bype' #银行类型，非必填，默认为“DEFAULT”-财付通支付中心
	BODY = 'body' #商品描述，必填
	ATTACH = 'attach' #附加数据，非必填，原样返回
	NOTIFY_URL = 'return_url' #支付完成后，接收微信通知支付结果的URL，255字符内
	PARTNER = 'partner' #签名方商户号，必填
	OUT_TRADE_NO = 'out_trade_no' #商户系统内部的订单号，必填，32个字符内，可包含字符
	TOTAL_FEE = 'total_fee' #订单总金额，单位为分，必填
	FEE_TYPE = 'fee_type' #现金支付币种，必填，取值1(人民币)，暂只支持1
	SPBILL_CREATE_IP = 'spbill_create_ip' #订单生成的机器IP，必填项，

	#返回结果和通知接口
	SIGN = 'sign' #签名，必填
	TRADE_MODE = 'trade_mode' #交易模式，1为即使到账
	TRADE_STATE = 'trade_state' #交易状态，0:交易成功
	PAY_INFO = 'pay_info' #支付结果信息，支付成功时为空
	NOTIFY_ID = 'notify_id' #支付结果通知id，据此可查询交易结果，2分钟内有效
	TRANSACTION_ID = 'transaction_id' #财付通交易号，28位长的数值
	TIME_END = 'time_end' #支付完成时间，格式为yyyymmddhhmmss
	OPENID = 'openid'
	IS_SUBSCRIBE = 'issubscribe'
	APP_SIGNATURE = 'appsignature'
	SIGN_METHOD = 'signmethod'
