# -*- coding: utf-8 -*-
import json

from datetime import date, datetime

from BeautifulSoup import BeautifulSoup
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required
from account.models import UserWeixinPayOrderConfig
from core import resource
from core import paginator
from core.exceptionutil import unicode_full_stack
from core.jsonresponse import create_response
from mall.models import PayInterface
from market_tools.tools.template_message.module_api import send_apps_template_message
from modules.member import models as member_models
import models as app_models

PAY_INTERFACE_WEIXIN_PAY = 2 #支付方式为微信支付

class GroupGranter(resource.Resource):
	app = 'apps/group'
	resource = 'group_granter'

	@login_required
	def api_get(request):
		group_id = request.GET.get('group_id', None)
		member_id = request.GET.get('member_id', None)
		response = create_response(500)
		if not group_id or not member_id:
			response.errMsg = u'活动信息出错,请重试~'
			return response.get_response()
		group_relation = app_models.GroupRelations.objects(id=group_id)
		if group_relation.count() <=0:
			response.errMsg = u'不存在该团购'
			return response.get_response()
		else:
			group_relation = group_relation.first()
		owner_id = group_relation.owner_id
		member_info = app_models.GroupDetail.objects(relation_belong_to=group_id, member_id=member_id, msg_api_status=False)
		if member_info.count() <= 0:
			response.errMsg = u'没有必要给该会员发送模板消息'
			return response.get_response()
		else:
			member_info = member_info.first()
		member_senders_info = member_info.msg_api_failed_members_info
		if not send_apps_template_message(owner_id, member_senders_info):
			response.errMsg = u'发送模板消息失败'
			return response.get_response()
		else:
			response = create_response(200)
			return response.get_response()