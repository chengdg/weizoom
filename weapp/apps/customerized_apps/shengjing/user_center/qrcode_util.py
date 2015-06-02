# -*- coding: utf-8 -*-

from django.contrib.auth.models import User, Group, Permission
from django.db.models import F

import time

from core.wxapi.weixin_api import *
from core.wxapi import get_weixin_api
from core.wxapi.weixin_api import WeixinApi
from core.wxapi.api_create_qrcode_ticket import QrcodeTicket

from core.exceptionutil import full_stack, unicode_full_stack

from watchdog.utils import watchdog_fatal, watchdog_error

from modules.member.models import Member, MemberGrade, BRING_NEW_CUSTOMER_VIA_QRCODE, SOURCE_MEMBER_QRCODE, MemberFollowRelation
from account.util import get_binding_weixin_mpuser, get_mpuser_accesstoken

from market_tools.tools.member_qrcode.models import *



def __get_qrcode(user_id):
	try:
		user = User.objects.get(id=user_id)
	except:
		notify_msg = u"微信会员二维码__get_qrcode errror :id={}cause:\n{}".format(user_id, unicode_full_stack())
		watchdog_error(notify_msg)
		return None, None
	
	mp_user = get_binding_weixin_mpuser(user)
	if mp_user:
		mpuser_access_token = get_mpuser_accesstoken(mp_user)
	else:
		return None, None

	if mpuser_access_token is None:
		return None, None

	if mpuser_access_token.is_active:
		weixin_api = get_weixin_api(mpuser_access_token)
		try:
			ticket = None
			qrcode_ticket = weixin_api.create_qrcode_ticket(int(user.id))
			try:
				ticket = qrcode_ticket.ticket
			except:
				ticket = None
				
			#qcrod_info = weixin_api.get_qrcode(ticket)
			if ticket:
				return ticket, 604000
			else:
				return None, None
		except:
			notify_msg = u"微信会员二维码__get_qrcode errror :id={}cause:\n{}".format(user_id, unicode_full_stack())
			watchdog_error(notify_msg, 'WEB', user_id)
			return None, None
		
	else:
		return None, None


###########################################################
#get_member_qrcode : 获取微站下的会员二维码
###########################################################
def get_member_qrcode(user_id, member_id):
	try:
		from django.db import connection, transaction
		cursor = connection.cursor()
		cursor.execute('update market_tool_member_qrcode set expired_second = expired_second - (%d - created_time) where is_active = 1;' % (int(time.time())))
		cursor.execute('update market_tool_member_qrcode set is_active = 0 where expired_second <= 0;')
		transaction.commit_unless_managed()
	except:
		notify_msg = u"微信会员二维码get_member_qrcode execute sql errror cause:\n{}".format(unicode_full_stack())
		watchdog_fatal(notify_msg)
		pass
			
	try:
		viper_spreads = MemberQrcode.objects.filter(member_id=member_id, expired_second__gt=850, is_active=1)
		if viper_spreads.count() > 0:
			return viper_spreads[0].ticket, viper_spreads[0].expired_second
		else:
			ticket, expired_second = __get_qrcode(user_id)
			if ticket:
				MemberQrcode.objects.create(owner_id=user_id, member_id=member_id, ticket=ticket, created_time=int(time.time()), expired_second=expired_second)
				return ticket, expired_second
			else:
				return None, None
	except:
		notify_msg = u"微信会员二维码get_member_qrcode execute sql errror cause:\n{}".format(unicode_full_stack())
		watchdog_fatal(notify_msg)
		return None, None


###########################################################
#get_qcrod_url : 二维码url路径
###########################################################
weixin_qcrod_url = 'https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=%s'
def get_qcrod_url(ticket):
	return 	weixin_qcrod_url % ticket

