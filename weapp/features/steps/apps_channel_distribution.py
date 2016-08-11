# -*- coding: utf-8 -*-
import json
from behave import *
from mall.promotion.models import CouponRule
from modules.member.models import MemberGrade, MemberTag, Member
from test import bdd_util
import logging
from market_tools.tools.distribution.models import ChannelDistributionQrcodeSettings
from utils.string_util import byte_to_hex


@When(u'{user}扫描渠道二维码"{qrcode_name}"')
def step_impl(context, user, qrcode_name):
	qrcode = ChannelDistributionQrcodeSettings.objects.get(bing_member_title=qrcode_name)
	owner_id = qrcode.owner
	
	
    # 模拟收到的消息
    openid = '%s_%s' % (webapp_user_name, owner.username)
    url = '/simulator/api/mp_user/qr_subscribe/?version=2'
    data = {
        "timestamp": "1402211023857",
        "webapp_id": webapp_id,
        "ticket": ticket,
        "from_user": openid
    }
    response = context.client.post(url, data)
    response_data = json.loads(response.content)
    context.qa_result = response_data


@When(u'{user}扫描带渠道二维码"{qrcode_name}"于{scan_qrcode_time}')
def step_impl(context, user, qrcode_name, scan_qrcode_time):
	context.execute_steps(u'when %s扫描带参数二维码"%s"' % (user, qrcode_name))
	scan_qrcode_time = ChannelDistributionQrcodeSettings.objects.get()
	relation = ChannelQrcodeHasMember
