# -*- coding: utf-8 -*-

import json
import time
import string
import random
from datetime import date

from django.http import HttpResponse
from django.shortcuts import render

from BeautifulSoup import BeautifulSoup


def access_token(request):
    appid = request.GET.get('appid', None)
    secret = request.GET.get('secret', None)
    code = request.GET.get('code', None)
    grant_type = request.GET.get('grant_type', None)
    
    if appid == None or secret == None or code == None or grant_type == None:
        return HttpResponse(json.dumps({'errcode':40029, 'errmsg':'missing parameter'}), 'application/json; charset=utf-8')
    
    access_token = ''.join(random.sample(string.ascii_letters + string.digits, 32))
    expires_in = 7200
    refresh_token = ''.join(random.sample(string.ascii_letters + string.digits, 32))
    openid = ''.join(random.sample(string.ascii_letters + string.digits, 28))
    scope = 'snsapi_base'
    
    result = json.dumps({
        'access_token': access_token,
        'expires_in': expires_in,
        'refresh_token': refresh_token,
        'openid': openid,
        'scope': scope
    })
    
    return HttpResponse(result, 'charset=utf-8')


def pay_unifiedorder(request):
    if hasattr(request, 'raw_post_data'):
        post_data = request.raw_post_data
    else:
        post_data = request.body
    
    result_fail_template = """
        <xml>
        <return_code><![CDATA[FAIL]]></return_code>
        <return_msg><![CDATA[%s]]></return_msg>
        </xml>
    """
    _post_data_soup = BeautifulSoup(post_data)
    if not _post_data_soup.appid or (_post_data_soup.appid and _post_data_soup.appid.text == ''):
         return HttpResponse(result_fail_template % u'missing appid', 'charset=utf-8')

    if not _post_data_soup.mch_id or (_post_data_soup.mch_id and _post_data_soup.mch_id.text == ''):
        return HttpResponse(result_fail_template % u'missing mch_id', 'charset=utf-8')
 
    if not _post_data_soup.out_trade_no or (_post_data_soup.out_trade_no and _post_data_soup.out_trade_no.text == ''):
        return HttpResponse(result_fail_template % u'missing out_trade_no', 'charset=utf-8')
     
    if not _post_data_soup.total_fee or (_post_data_soup.total_fee and _post_data_soup.total_fee == ''):
        return HttpResponse(result_fail_template % u'missing total_fee', 'charset=utf-8')
     
    if not _post_data_soup.spbill_create_ip or (_post_data_soup.spbill_create_ip and _post_data_soup.spbill_create_ip == ''):
        return HttpResponse(result_fail_template % u'missing spbill_create_ip', 'charset=utf-8')
     
    if not _post_data_soup.notify_url or (_post_data_soup.notify_url and _post_data_soup.notify_url == ''):
        return HttpResponse(result_fail_template % u'missing notify_url', 'charset=utf-8')
     
    if not _post_data_soup.openid or (_post_data_soup.openid and _post_data_soup.openid == ''):
        return HttpResponse(result_fail_template % u'missing openid', 'charset=utf-8')
    
    if not _post_data_soup.trade_type or (_post_data_soup.trade_type and _post_data_soup.trade_type == ''):
        return HttpResponse(result_fail_template % u'missing trade_type', 'charset=utf-8')
    
    
    result_success_template = """
        <xml>
        <return_code><![CDATA[SUCCESS]]></return_code>
        <return_msg><![CDATA[OK]]></return_msg>
        <appid><![CDATA[%s]]></appid>
        <mch_id><![CDATA[%s]]></mch_id>
        <device_info><![CDATA[1000]]></device_info>
        <nonce_str><![CDATA[%s]]></nonce_str>
        <sign><![CDATA[%s]]></sign>
        <result_code><![CDATA[SUCCESS]]></result_code>
        <trade_type><![CDATA[JSAPI]]></trade_type>
        <prepay_id><![CDATA[%s]]></prepay_id>
        </xml>
    """
    appid = _post_data_soup.appid.text
    mch_id = _post_data_soup.mch_id.text
    nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))
    sign = ''.join(random.sample(string.ascii_letters + string.digits, 32))
    prepay_id = ''.join(random.sample(string.ascii_letters + string.digits, 36))
    
    return HttpResponse(result_success_template % (appid, mch_id, nonce_str, sign, prepay_id), 'charset=utf-8')