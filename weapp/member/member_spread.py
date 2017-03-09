#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from core.jsonresponse import create_response
from core import paginator
from core import resource

from modules.member.models import *
from mall.models import *
import export

COUNT_PER_PAGE = 20

class MemberSpread(resource.Resource):
	app = 'member'
	resource = 'member_spread'

	@login_required
	def get(request):
		c = RequestContext(request, {
			'first_nav_name': export.MEMBER_FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': export.MEMBER_SPREAD,
		})

		return render_to_response('member/editor/member_spread.html', c)

	@login_required
	def api_get(request):
		cur_page = int(request.GET.get('page', 1))
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		sort_attr = request.GET.get('sort_attr', '-id')

		webapp_id = request.user_profile.webapp_id

		name = request.GET.get('name')
		level = int(request.GET.get('level', -1))
		start_time = request.GET.get('start_time')
		end_time = request.GET.get('end_time')

		ty_members = TengyiMember.objects.all()
		if name:
			hexstr = byte_to_hex(name)
			member_ids = [m.id for m in Member.objects.filter(webapp_id=webapp_id, username_hexstr__contains=hexstr)]
			ty_members = ty_members.filter(member_id__in=member_ids)

		if level in [1,2]:
			ty_members = ty_members.filter(level=level)

		if start_time and end_time:
			ty_members = ty_members.filter(created_at__range=[start_time, end_time])

		ty_members = ty_members.order_by(sort_attr)

		member_ids = [ty.member_id for ty in ty_members]
		member_id2info = {m.id: m for m in Member.objects.filter(id__in=member_ids)}

		webapp_user_id2member_id = {w.id: w.member_id for w in WebAppUser.objects.filter(member_id__in=member_ids)}

		orders = Order.objects.filter(webapp_user_id__in=webapp_user_id2member_id.values())

		member_id2order_info = {}

		for order in orders:
			member_id = webapp_user_id2member_id[order.webapp_user_id]
			if not member_id2order_info.has_key(member_id):
				member_id2order_info[member_id] = {
					'order_money': order.product_price,
					'cash_money': order.final_price
				}
			else:
				member_id2order_info[member_id]['order_money'] += order.product_price
				member_id2order_info[member_id]['cash_money'] += order.final_price

		print member_ids
		print '====================='
		print member_id2order_info
		print '======================='

		ty_member_id2spread_count = {}
		for relation in TengyiMemberRelation.objects.filter(recommend_by_member_id__in=member_ids):
			re_by_id = relation.recommend_by_member_id
			if not ty_member_id2spread_count.has_key(re_by_id):
				ty_member_id2spread_count[re_by_id] = 1
			else:
				ty_member_id2spread_count[re_by_id] += 1

		pageinfo, ty_members = paginator.paginate(ty_members, cur_page, count_per_page, query_string=request.GET.get('query', None))

		items = []
		for ty_member in ty_members:
			member_id = ty_member.member_id
			items.append({
				'member_id': member_id,
				'member_name': member_id2info[member_id].username_for_html,
				'member_icon': member_id2info[member_id].user_icon,
				'level': ty_member.level,
				'level_text': u'一星' if ty_member.level == 1 else u'二星',
				'recommend_by': member_id2info[ty_member.recommend_by_member_id].username_for_html if ty_member.recommend_by_member_id != 0 else u'管理员',
				'spread_count': ty_member_id2spread_count.get(member_id, 0),
				'order_money': member_id2order_info[member_id]['order_money'] if member_id2order_info.get(member_id) else 0,
				'cash_money': member_id2order_info[member_id]['cash_money'] if member_id2order_info.get(member_id) else 0,
				'created_at': ty_member.created_at.strftime('%Y/%m/%d')
			})

		response = create_response(200)
		response.data = {
			'items': items,
			'sortAttr': sort_attr,
			'pageinfo': paginator.to_dict(pageinfo),
		}

		return response.get_response()

