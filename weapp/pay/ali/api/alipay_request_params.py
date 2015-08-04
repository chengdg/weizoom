# -*- coding: utf-8 -*-

__author__ = 'chuter'

class AlipayRequestParams(object):
	"""
	支付宝支付请求中的参数定义
	"""
	def __init__(self):
		raise NotImplementedError

	SIGN = 'sign'
	SIGN_TYPE = 'sign_type'
	SERVICE = 'service'
	V = 'v'
	SEC_ID = 'sec_id'
	NOTIFY_DATA = 'notify_data'
	FORMAT = 'format'
	REQ_ID = 'req_id'
	NOTIFY_URL = 'notify_url'
	CALL_BACK_URL = 'call_back_url'
	MERCHANT_URL = 'merchant_url'
	SELLER_EMAIL = 'seller_email'
	OUT_TRADE_NO = 'out_trade_no'
	SUBJECT = 'subject'
	TOTAL_FEE = 'total_fee'
	REQ_DATA = 'req_data'
	RES_DATA = 'res_data'
	INPUT_CHARSET = '_input_charset'
	PARTNER = 'partner'

	#返回结果和通知接口
	TRADE_RESULT = 'trade_mode' #交易模式，1为即使到账
	TRADE_STATE = 'trade_state' #交易状态，0:交易成功
	NOTIFY_ID = 'notify_id' #通知校验ID。唯一识别通知内容。重发相同内容的通知时，该值不变


