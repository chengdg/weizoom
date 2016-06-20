# -*- coding: utf-8 -*-
import json
from datetime import datetime
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
COUNT_PER_PAGE = 20

class SignParticipances(resource.Resource):
	app = 'apps/sign'
	resource = 'sign_participances'

	@login_required
	def get(request):
		"""
		响应GET
		"""
		has_data = app_models.SignParticipance.objects(belong_to=request.GET['id']).count()

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': "signs",
			'has_data': has_data,
			'activity_id': request.GET['id']
		})

		return render_to_response('sign/templates/editor/sign_participances.html', c)

	@staticmethod
	def get_datas(request):
		sort_attr = request.GET.get('sort_attr', '-latest_date')
		participant_name = request.GET.get('participant_name', '')
		webapp_id = request.user_profile.webapp_id

		datas = app_models.SignParticipance.objects(belong_to=request.GET['id'])

		if participant_name != '':
			hexstr = byte_to_hex(participant_name)
			members = member_models.Member.objects.filter(webapp_id=webapp_id,username_hexstr__contains=hexstr)
			temp_ids = [member.id for member in members]
			member_ids = temp_ids  if temp_ids else [-1]
			datas = datas.filter(member_id__in=member_ids)

		if 'total_integral' in sort_attr:
			datas = sorted(datas, lambda x,y: cmp(x.prize['integral'], y.prize['integral']), reverse=True if '-' in sort_attr else False)
		else:
			datas = datas.order_by(sort_attr)
		#进行分页
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		cur_page = int(request.GET.get('page', '1'))
		pageinfo, datas = paginator.paginate(datas, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

		return pageinfo, datas

	@login_required
	def api_get(request):
		"""
		响应API GET
		"""
		sort_attr = request.GET.get('sort_attr', '-latest_date')
		pageinfo, datas = SignParticipances.get_datas(request)

		member_ids = []
		for data in datas:
			member_ids.append(data.member_id)
		members = member_models.Member.objects.filter(id__in=member_ids)
		member_id2member = {member.id: member for member in members}

		items = []
		for data in datas:
			print len(data.prize['coupon'].split(',')),"data.prize['coupon']"
			coupon_count = len(data.prize['coupon'].split(','))
			items.append({
				'id': str(data.id),
				'belong_to': data.belong_to,
				'member_id': data.member_id,
				'participant_name': member_id2member[data.member_id].username_for_html if member_id2member.get(data.member_id) else u'未知',
				'participant_icon': member_id2member[data.member_id].user_icon if member_id2member.get(data.member_id) else '/static/img/user-1.jpg',
				'created_at': data.created_at.strftime("%Y/%m/%d %H:%M:%S"),
				'latest_date': data.latest_date.strftime("%Y/%m/%d %H:%M:%S") if data.latest_date else "",
				'total_count': data.total_count,
				'serial_count': data.serial_count,
				'top_serial_count': data.top_serial_count,
				'total_integral': data.prize['integral'],
				'coupon_count': coupon_count
			})
		response_data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': sort_attr,
			'data': {}
		}
		response = create_response(200)
		response.data = response_data
		return response.get_response()

class SignParticipancesDetail(resource.Resource):
	'''
	签到详情
	'''
	app = 'apps/sign'
	resource = 'sign_participance_detail'
	def get(request):
		"""
		响应GET
		"""
		member_id = request.GET.get('member_id', None)
		belong_to = request.GET.get('belong_to', None)
		if member_id and belong_to:
			items = app_models.SignDetails.objects(belong_to=belong_to, member_id=int(member_id)).order_by('-created_at')
			sign_member_ids = [item.member_id for item in items]
			member_id2info = {m.id: {'is_subscribed': m.is_subscribed, 'member_name': m.username_for_html} for m in Member.objects.filter(id__in=sign_member_ids)}
			returnDataList = []
			for t in items:
				prize_str = u''
				if t['prize'].get('integral', None):
					prize_str += u'积分奖励: %s <br>' % str(t['prize']['integral'])
				if t['prize'].get('coupon', None):
					prize_str += u'优惠券奖励: %s' % str(t['prize']['coupon']['name'])
				returnDataDict = {
					"member_id": t.member_id,
					"member_name": member_id2info[t.member_id]['member_name'],
					"created_at": t.created_at.strftime("%Y/%m/%d %H:%M"),
					"type": t.type,
					"prize": prize_str
				}
				returnDataList.append(returnDataDict)
			c = RequestContext(request, {
				'items': returnDataList,
				'errMsg': None
			})
		else:
			c = RequestContext(request, {
				'items': None,
				'errMsg': u'member_id或者belong_to不存在'
			})
		return render_to_response('sign/templates/editor/sign_participance_detail.html', c)
