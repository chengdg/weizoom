#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required

from core.jsonresponse import create_response
from core import resource

from modules.member.models import *
from mall.models import *
from utils.string_util import byte_to_hex

COUNT_PER_PAGE = 20

class MemberSpreadExport(resource.Resource):
	app = 'member'
	resource = 'member_spread_export'

	@login_required
	def api_get(request):

		ty_members = TengyiMember.objects.all()
		member_id2_valid = {ty.member_id: ty for ty in ty_members}

		member_ids = [ty.member_id for ty in ty_members]
		member_id2info = {m.id: m for m in Member.objects.filter(id__in=member_ids)}

		webapp_user_id2member_id = {w.id: w.member_id for w in WebAppUser.objects.filter(member_id__in=member_ids)}

		orders = Order.objects.filter(webapp_user_id__in=webapp_user_id2member_id.keys())

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

		ty_member_id2referees = {}
		for relation in TengyiMemberRelation.objects.filter(recommend_by_member_id__in=member_ids):
			re_by_id = relation.recommend_by_member_id
			member_id = relation.member_id
			member_info = {
				'member_id': member_id,
				'scan_at': relation.created_at.strftime("%Y-%m-%d %H:%M:%S"),
				'created_at': member_id2_valid[member_id].created_at.strftime("%Y-%m-%d %H:%M:%S") if member_id in member_ids else u'预备会员'
			}
			if not ty_member_id2referees.has_key(re_by_id):
				ty_member_id2referees[re_by_id] = {
					'total': 1,
					'valid': 0,
					'referees': [member_info]
				}

			else:
				ty_member_id2referees[re_by_id]['total'] += 1
				ty_member_id2referees[re_by_id]['referees'].append(member_info)

			if member_id in member_ids:
				ty_member_id2referees[re_by_id]['valid'] += 1

		name = request.GET.get('name')
		level = int(request.GET.get('level', -1))
		start_time = request.GET.get('start_time')
		end_time = request.GET.get('end_time')
		webapp_id = request.user_profile.webapp_id

		if name:
			hexstr = byte_to_hex(name)
			ty_members = ty_members.filter(member_id__in=[m.id for m in Member.objects.filter(webapp_id=webapp_id, username_hexstr__contains=hexstr)])

		if level in [1,2]:
			ty_members = ty_members.filter(level=level)

		if start_time and end_time:
			ty_members = ty_members.filter(created_at__range=[start_time, end_time])

		ty_members = ty_members.order_by('-id')

		try:
			import os, xlwt
			excel_file_name = 'member_spread_relations.xls'
			excel_file_path = os.path.join(settings.UPLOAD_DIR, excel_file_name)
			wb = xlwt.Workbook(encoding='utf-8')
			ws = wb.add_sheet(u'订单详情')

			fields_cn = [u'会员id', u'会员名称', u'星级', u'本人成为星级会员时间', u'推荐人id',
						 u'推荐人名称', u'推荐会员数', u'星级会员数', u'推荐会员id', u'扫码时间', u'成为星级会员时间']

			row = col = 0
			for content in fields_cn:
				ws.write(row, col, content)
				col += 1

			for ty_member in ty_members:
				row += 1
				col = 0
				member_id = ty_member.member_id
				items = [
					member_id,
					member_id2info[member_id].username_for_html,
					u'一星' if ty_member.level == 1 else u'二星',
					ty_member.created_at.strftime('%Y/%m/%d'),
				  	ty_member.recommend_by_member_id,
					member_id2info[ty_member.recommend_by_member_id].username_for_html if ty_member.recommend_by_member_id != 0 else u'管理员',
					ty_member_id2referees[member_id]['total'] if ty_member_id2referees.get(member_id) else 0,
					ty_member_id2referees[member_id]['valid'] if ty_member_id2referees.get(member_id) else 0,
					'',#推荐会员id
					'',#扫码时间
					''#成为星级会员时间
				]
				for item in items:
					ws.write(row, col, item)
					col += 1

				referees = ty_member_id2referees[member_id]['referees'] if ty_member_id2referees.get(member_id) else []
				for referee in referees:
					sub_col = 0
					sub_items = ['', '', '', '', '', '', '', '', referee['member_id'], referee['scan_at'], referee['created_at']]
					row += 1
					for sub_item in sub_items:
						ws.write(row, sub_col, sub_item)
						sub_col += 1

			wb.save(excel_file_path)
			response = create_response(200)
			response.data = {
				'filename': u'星级会员推广关系.xls',
				'download_path': '/static/upload/%s' % excel_file_name
			}
		except:
			response = create_response(500)
			response.innerErrMsg = unicode_full_stack()
			response.errMsg = u'上传出错'

		return response.get_response()

