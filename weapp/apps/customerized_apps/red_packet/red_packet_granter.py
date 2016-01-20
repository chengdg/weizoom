# -*- coding: utf-8 -*-
import json

from datetime import date, datetime
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required
# from apps.customerized_apps.powerme.m_powerme import clear_non_member_power_info
from account.models import UserWeixinPayOrderConfig
from core import resource
from core import paginator
from core.exceptionutil import unicode_full_stack
from core.jsonresponse import create_response
from mall.models import PayInterface
from modules.member import models as member_models
import models as app_models
import export
from mall import export as mall_export
from modules.member.models import Member, MemberHasSocialAccount
from pay.weixin.api.api_send_red_pack import RedPackMessage
from utils.string_util import byte_to_hex
import os

from watchdog.utils import watchdog_error
from weapp import settings
from weixin.user.models import ComponentAuthedAppid, ComponentAuthedAppidInfo

PAY_INTERFACE_WEIXIN_PAY = 2 #支付方式为微信支付

class RedPacketGranter(resource.Resource):
	app = 'apps/red_packet'
	resource = 'red_packet_granter'
	
	@login_required
	def api_put(request):
		"""
		发红包
		@return:
		"""
		record_id = request.POST.get('id', None)
		member_id = request.POST.get('member_id', None)
		response = create_response(500)
		if not record_id or not member_id:
			response.errMsg = u'活动信息出错,请重试~'
			return response.get_response()

		record = app_models.RedPacket.objects(id=record_id)
		if record.count() <=0:
			response.errMsg = u'不存在该活动'
			return response.get_response()
		else:
			record = record.first()
		owner_id = record.owner_id

		member_info = app_models.RedPacketParticipance.objects(belong_to=record_id, member_id=member_id)
		if member_info.count() <=0:
			response.errMsg = u'用户信息出错: %s' % member_id
			return response.get_response()
		else:
			member_info = member_info.first()

		#获取该member_id的固定openid
		openid = MemberHasSocialAccount.objects.filter(member_id=member_id)[0].account.openid
		#获取商户的支付配置信息
		pay_interface = PayInterface.objects.get(type=PAY_INTERFACE_WEIXIN_PAY, owner_id=owner_id)
		weixin_pay_config = UserWeixinPayOrderConfig.objects.get(id=pay_interface.related_config_id)

		authed_appid = ComponentAuthedAppid.objects.filter(user_id=owner_id, authorizer_appid=weixin_pay_config.app_id, is_active=True)[0]
		appid_info = ComponentAuthedAppidInfo.objects.filter(auth_appid=authed_appid)[0]
		nick_name = appid_info.nick_name

		# red = RedPackMessage(weixin_pay_config.partner_id, weixin_pay_config.app_id, nick_name,
		# 	nick_name,openid,price,price,price,1, shake_detail.shake.wishing, ip,
		# 	shake_detail.shake.name,
		# 	shake_detail.shake.remark,
		# 	weixin_pay_config.partner_key)


