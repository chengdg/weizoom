# -*- coding: utf-8 -*-

__author__ = 'bert'

WEIXIN_API_PROTOCAL = 'https'
WEIXIN_API_DOMAIN = 'api.weixin.qq.com'
WEIXIN_API_V3_DOMAIN = 'api.mch.weixin.qq.com'

API_GET= 'get'
API_POST= 'post'

API_CLASSES = {
	'query_order': 'pay.weixin.api.api_pay_queryorder.WeixinPayQueryOrderApi',
	'get_unifiedorder': 'pay.weixin.api.api_pay_unifiedorder.WeixinPayUnifiedOrderApi',
	'get_openid': 'pay.weixin.api.api_pay_openid.WeixinPayOpenidApi',
}