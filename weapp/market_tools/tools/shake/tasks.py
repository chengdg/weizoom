# -*- coding: utf-8 -*-

__author__ = 'bert'

import time
from datetime import datetime
from django.conf import settings
from django.db.models import F

from core.exceptionutil import unicode_full_stack

from core import emotion

from watchdog.utils import watchdog_fatal, watchdog_error, watchdog_info

from modules.member.models import *
from mall.models import *
from account.models import UserWeixinPayOrderConfig, UserProfile

from celery import task

from pay.weixin.api.api_send_red_pack import RedPackMessage
from BeautifulSoup import BeautifulSoup 
from weixin.user.models import *
from models import *

import platform
sysstr = platform.system()
if sysstr !="Windows":
	SSLCERT_PATH = "/weapp/web/weapp/pay/weixin/api/apiclient_cert.pem"  
	SSLKEY_PATH = "/weapp/web/weapp/pay/weixin/api/apiclient_key.pem"  
else:
	SSLCERT_PATH = "D://weapp_project//web//weapp//pay//weixin//api//apiclient_cert.pem"
	SSLKEY_PATH = "D://weapp_project//web//weapp//pay//weixin//api//apiclient_key.pem"
@task
def send_red_pack_task(detail_id, owner_id, member_id, record_id, ip):
	time.sleep(2)
	print '>>>>>>>>>>>>>>>>>>>>> in send_red_pack_task----', record_id
	shake_detail = ShakeDetail.objects.get(id=detail_id)
	record = ShakeRecord.objects.get(id=record_id)
	price = int(record.money * 100)
	openid = MemberHasSocialAccount.objects.filter(member_id=member_id)[0].account.openid
	print '>>>>>>>>>>>>>>>>>>>>> in send_red_pack_task',member_id, price, owner_id, ip, openid

	pay_interface = PayInterface.objects.get(type=PAY_INTERFACE_WEIXIN_PAY, owner_id=owner_id)
	weixin_pay_config = UserWeixinPayOrderConfig.objects.get(id=pay_interface.related_config_id)

	try:
		authed_appid = ComponentAuthedAppid.objects.filter(user_id=owner_id, authorizer_appid=weixin_pay_config.app_id, is_active=False)[0]
		info = ComponentAuthedAppidInfo.objects.filter(auth_appid=authed_appid, authorizer_appid=weixin_pay_config.app_id, is_active=False)[0]
		nick_name = info.nick_name
	except:
		nick_name = u'微众传媒'

	red = RedPackMessage(weixin_pay_config.partner_id, weixin_pay_config.app_id, nick_name,
		nick_name,openid,price,price,price,1, shake_detail.shake.wishing, ip,
		shake_detail.shake.name,
		shake_detail.shake.remark,
		weixin_pay_config.partner_key)
	result = red.post_data(SSLKEY_PATH, SSLCERT_PATH)
	xml = red.arrayToXml()
	#print result
	result = BeautifulSoup(result)
	return_code = result.return_code.text
	return_msg = result.return_msg.text
	if return_code == "SUCCESS":
		record.is_sended = True
	else:
		record.is_sended = False
	record.return_msg = return_msg
	record.return_code = return_code
	record.xml_msg = xml
	record.save()
	print return_msg
	print 'ok'
	