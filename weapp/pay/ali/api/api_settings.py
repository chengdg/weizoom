# -*- coding: utf-8 -*-

__author__ = 'bert'


TRADE_CREATE_SERVICE = 'alipay.wap.trade.create.direct'
AUTH_AND_EXECUTE_SERVICE = 'alipay.wap.auth.authAndExecute'

FORMAT = 'xml'
V = '2.0'

ALIPAY_GATEWAY = 'http://wappaygw.alipay.com/service/rest.htm'

API_GET= 'get'
API_POST= 'post'

API_CLASSES = {
	'get_token': 'pay.ali.api.api_pay_token.AliPayTokenApi',
}