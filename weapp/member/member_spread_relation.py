#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required

from core.jsonresponse import create_response
from core import paginator
from core import resource

from modules.member.models import *
from mall.models import *

COUNT_PER_PAGE = 20

class MemberSpreadRelation(resource.Resource):
	app = 'member'
	resource = 'member_spread_relation'

	@login_required
	def api_get(request):
		cur_page = int(request.GET.get('page', 1))
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		sort_attr = request.GET.get('sort_attr', '-id')

		member_id = request.GET.get('member_id')

		member_type = request.GET.get('member_type', 'valid')

		total_order_money = 0
		total_cash_money = 0

		if member_type == 'valid': #星级会员

			ty_members = TengyiMember.objects.filter(recommend_by_member_id=member_id).order_by(sort_attr)
			member_ids = [ty.member_id for ty in ty_members]
			member_id2info = {m.id: m for m in Member.objects.filter(id__in=member_ids)}

			member_count = len(member_ids)

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

				total_order_money += order.product_price
				total_cash_money += order.final_price

			ty_member_id2relation = {ty.member_id: ty for ty in TengyiMemberRelation.objects.filter(member_id__in=member_ids)}

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
					'created_at': ty_member.created_at.strftime('%Y/%m/%d'),
					'scan_at': ty_member_id2relation[member_id].created_at.strftime('%Y/%m/%d'),
					'order_money': member_id2order_info[member_id]['order_money'] if member_id2order_info.get(member_id) else 0,
					'cash_money': member_id2order_info[member_id]['cash_money'] if member_id2order_info.get(member_id) else 0,
				})

		else: #预备会员
			valid_member_ids = [t.member_id for t in TengyiMember.objects.all()]
			ty_members = TengyiMemberRelation.objects.filter(recommend_by_member_id=member_id).exclude(member_id__in=valid_member_ids)
			member_ids = [ty.member_id for ty in ty_members]
			member_id2info = {m.id: m for m in Member.objects.filter(id__in=member_ids)}

			member_count = len(member_ids)
			pageinfo, ty_members = paginator.paginate(ty_members, cur_page, count_per_page,
													  query_string=request.GET.get('query', None))

			items = []
			for ty_member in ty_members:
				member_id = ty_member.member_id
				items.append({
					'member_id': member_id,
					'member_name': member_id2info[member_id].username_for_html,
					'member_icon': member_id2info[member_id].user_icon,
					'scan_at': ty_member.created_at.strftime('%Y/%m/%d'),
				})

		response = create_response(200)
		response.data = {
			'member_type': member_type,
			'member_count': member_count,
			'total_order_money': total_order_money,
			'total_cash_money': total_cash_money,
			'items': items,
			'sortAttr': sort_attr,
			'pageinfo': paginator.to_dict(pageinfo),
		}

		return response.get_response()
