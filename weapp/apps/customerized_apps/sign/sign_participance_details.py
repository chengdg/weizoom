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
from core import dateutil

from mall.promotion import models as promotion_models

FIRST_NAV = 'apps'
COUNT_PER_PAGE = 15

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
			#最近90天
			total_days, low_date, cur_date, high_date = dateutil.get_date_range(dateutil.get_today(), str(89), 0)
			date_list = dateutil.get_date_range_list(low_date,cur_date)

			#进行分页
			count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
			cur_page = int(request.GET.get('page', '1'))
			date_list.reverse()
			pageinfo, date_list = paginator.paginate(date_list, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

			start_date = low_date.strftime("%Y-%m-%d %H:%M:%S")
			#现在的时间
			end_date = cur_date.strftime("%Y-%m-%d 23:59:59")

			items = app_models.SignDetails.objects(belong_to=belong_to, member_id=int(member_id),created_at__gte=start_date,created_at__lte=end_date).order_by('-created_at')

			sign_member_ids = [item.member_id for item in items]
			member_id2info = {m.id: {'is_subscribed': m.is_subscribed, 'member_name': m.username_for_html} for m in Member.objects.filter(id__in=sign_member_ids)}
			returnDataList = []
			time2prize = {}
			coupon_ids = []
			for t in items:
				if t['prize'].get('coupon', None):
					if t['prize']['coupon']['id']:
						coupon_ids.append(t['prize']['coupon']['id'])
			coupon_id2name = {c.id: c.name for c in promotion_models.CouponRule.objects.filter(id__in=coupon_ids)}

			for item in items:
				prize_str = u''
				if item['prize'].get('integral', None):
					prize_str += u'积分+%s<br/>' % str(item['prize']['integral'])
				if item['prize'].get('coupon', None):
					if item['prize']['coupon']['id']:
						prize_str += u'%s<br/>' % coupon_id2name.get(item['prize']['coupon']['id'],'')
				time2prize[item.created_at.strftime("%Y.%m.%d")] = {
					"created_at": item.created_at.strftime("%Y.%m.%d %H:%M:%S"),
					"created_at_f": item.created_at.strftime("%Y-%m-%d %H:%M:%S"),
					"prize": prize_str,
					"status": 1
				}
			for date_d in date_list:
				date_ymd = date_d.strftime("%Y.%m.%d")
				if time2prize.get(date_ymd,None):
					returnDataList.append(time2prize[date_ymd])
				else:
					returnDataList.append({
						"created_at": date_d.strftime("%Y.%m.%d %H:%M:%S"),
						"created_at_f": date_d.strftime("%Y-%m-%d %H:%M:%S"),
						"prize": "",
						"status": 0
					})
		else:
			returnDataList = []
		response = create_response(200)
		response.data.items = returnDataList
		response.data.pageinfo = paginator.to_dict(pageinfo)
		return response.get_response()
