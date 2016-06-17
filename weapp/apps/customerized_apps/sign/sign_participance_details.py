# -*- coding: utf-8 -*-
import json
from datetime import datetime, timedelta,date
import calendar
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required
from core import resource
from core import paginator
from core.jsonresponse import create_response
from modules.member import models as member_models
import models as app_models
import export
from modules.member.models import Member
from utils.string_util import hex_to_byte, byte_to_hex

FIRST_NAV = 'apps'
COUNT_PER_PAGE = 30

class SignParticipances(resource.Resource):
	app = 'apps/sign'
	resource = 'sign_participance_details'

	@login_required
	def api_get(request):
		"""
		签到详情查看
		"""
		member_id = request.GET.get('member_id', None)
		belong_to = request.GET.get('belong_to', None)
		if member_id and belong_to:
			items = app_models.SignDetails.objects(belong_to=belong_to, member_id=int(member_id)).order_by('-created_at')

			#进行分页
			count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
			cur_page = int(request.GET.get('page', '1'))
			pageinfo, items = paginator.paginate(items, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
			sign_member_ids = [item.member_id for item in items]
			member_id2info = {m.id: {'is_subscribed': m.is_subscribed, 'member_name': m.username_for_html} for m in Member.objects.filter(id__in=sign_member_ids)}
			returnDataList = []
			for t in items:
				prize_str = u''
				if t['prize'].get('integral', None):
					prize_str += u'积分+%s' % str(t['prize']['integral'])
				if t['prize'].get('coupon', None):
					if t['prize']['coupon']['id']:
						prize_str += u'%s' % str(t['prize']['coupon']['name'])
				returnDataDict = {
					"member_id": t.member_id,
					"member_name": member_id2info[t.member_id]['member_name'],
					"created_at": t.created_at.strftime("%Y.%m.%d %H:%M:%S"),
					"type": t.type,
					"prize": prize_str
				}
				returnDataList.append(returnDataDict)
		else:
			returnDataList = []
		response = create_response(200)
		response.data.items = returnDataList
		response.data.pageinfo = paginator.to_dict(pageinfo)
		return response.get_response()
