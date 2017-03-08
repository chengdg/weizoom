#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from django.contrib.auth.decorators import login_required

from core.jsonresponse import create_response
from core import paginator
from core import resource

from modules.member.models import *
from mall.models import *

COUNT_PER_PAGE = 20

class MemberSpreadRebate(resource.Resource):
	app = 'member'
	resource = 'member_spread_rebate'

	@login_required
	def api_get(request):
		cur_page = int(request.GET.get('page', 1))
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		sort_attr = request.GET.get('sort_attr', '-id')

		member_id = request.GET.get('member_id')

		rebate_type = request.GET.get('rebate_type', 'self')
		cur_month = datetime.now().month
		month = int(request.GET.get('month', cur_month))

		cur_month_rebate_member_count = 0
		cur_month_rebate_money = 0


		if rebate_type == 'self': #自己购买返利
			logs = TengyiRebateLog.objects.filter(member_id=member_id, is_self_order=True, is_exchanged=True)
			pageinfo, ty_members = paginator.paginate(logs, cur_page, count_per_page, query_string=request.GET.get('query', None))

			items = []
			for log in logs:
				items.append({
					'rebate_money': log.rebate_money,
					'rebate_time': log.exchanged_at.strftime('%Y/%m/%d')
				})
		else: #被推荐人返利
			logs = TengyiRebateLog.objects.filter(member_id=member_id, is_self_order=False, is_exchanged=True, exchanged_at__month=month)
			pageinfo, ty_members = paginator.paginate(logs, cur_page, count_per_page,
													  query_string=request.GET.get('query', None))
			cur_month_rebate_member_count = len(set([l.supply_member_id for l in logs]))

			member_ids = [ty.supply_member_id for ty in logs]
			member_id2info = {m.id: m for m in Member.objects.filter(id__in=member_ids)}

			items = []
			for log in logs:
				cur_month_rebate_money += log.rebate_money
				items.append({
					'supplier_id': log.supply_member_id,
					'supplier_name': member_id2info[log.supply_member_id].username_for_html,
					'supplier_icon': member_id2info[log.supply_member_id].user_icon,
					'rebate_money': log.rebate_money,
					'rebate_time': log.exchanged_at.strftime('%Y/%m/%d')
				})

		response = create_response(200)
		response.data = {
			'cur_month_rebate_member_count': cur_month_rebate_member_count,
			'cur_month_rebate_money': cur_month_rebate_money,
			'cur_month': month,
			'items': items,
			'sortAttr': sort_attr,
			'pageinfo': paginator.to_dict(pageinfo),
		}

		return response.get_response()

