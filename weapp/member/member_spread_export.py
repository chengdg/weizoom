#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required

from core.jsonresponse import create_response
from core import resource

from modules.member.models import *
from mall.models import *

COUNT_PER_PAGE = 20

class MemberSpreadExport(resource.Resource):
	app = 'member'
	resource = 'member_spread_export'

	@login_required
	def api_get(request):

		ty_members = TengyiMember.objects.all().order_by('-id')

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

		ty_member_id2spread_count = {}
		for relation in TengyiMemberRelation.objects.filter(recommend_by_member_id__in=member_ids):
			re_by_id = relation.recommend_by_member_id
			if not ty_member_id2spread_count.has_key(re_by_id):
				ty_member_id2spread_count[re_by_id] = 1
			else:
				ty_member_id2spread_count[re_by_id] += 1

		try:
			import os, xlwt
			excel_file_name = 'member_spread_relations.xls'
			excel_file_path = os.path.join(settings.UPLOAD_DIR, excel_file_name)
			wb = xlwt.Workbook(encoding='utf-8')
			ws = wb.add_sheet(u'订单详情')

			fields_cn = (
				[u'会员id', u'会员名称', u'星级', u'扫码时间', u'成为星级会员时间', u'推荐人id', u'推荐人名称', u'推荐会员数', u'星级会员数', u'推荐会员ids']
			)

			row = col = 0
			for content in fields_cn:
				ws.write(row, col, content)
				col += 1

			for ty_member in ty_members:
				row += 1
				member_id = ty_member.member_id
				item = [
					member_id,
					member_id2info[member_id].username_for_html,
					u'一星' if ty_member.level == 1 else u'二星',
					u'非扫码' if ty_member.recommend_by_member_id == 0 else 0,
					ty_member.created_at.strftime('%Y/%m/%d'),
				  	ty_member.recommend_by_member_id,
					member_id2info[ty_member.recommend_by_member_id].username_for_html if ty_member.recommend_by_member_id != 0 else u'管理员',
					ty_member_id2spread_count.get(member_id, 0),
					#
					#
				]

				ws.write(row, col, item)
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

