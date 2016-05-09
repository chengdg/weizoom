# -*- coding: utf-8 -*-
import json

from datetime import date, datetime
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required
# from apps.customerized_apps.red_packet.m_red_packet import reset_member_helper_info,reset_re_subscribed_member_helper_info
from core import resource
from core import paginator
from core.exceptionutil import unicode_full_stack
from core.jsonresponse import create_response
from modules.member import models as member_models
import models as app_models
import export
from mall import export as mall_export
from modules.member.models import Member
from utils.string_util import byte_to_hex
import os

from watchdog.utils import watchdog_error
from weapp import settings

FIRST_NAV = mall_export.MALL_PROMOTION_AND_APPS_FIRST_NAV
COUNT_PER_PAGE = 20

class RebateParticipances(resource.Resource):
	app = 'apps/rebate'
	resource = 'rebate_participances'

	@login_required
	def get(request):
		"""
		响应GET
		"""
		has_data = app_models.RebateParticipance.objects(belong_to=request.GET['id']).count()

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': mall_export.get_promotion_and_apps_second_navs(request),
			'second_nav_name': mall_export.MALL_APPS_SECOND_NAV,
			'third_nav_name': mall_export.MALL_APPS_REBATE_NAV,
			'has_data': has_data,
			'record_id': request.GET['id']
		})

		return render_to_response('rebate/templates/editor/rebate_participances.html', c)

	@staticmethod
	def get_datas(request):
		member_status = request.GET.get('status', '-1')
		webapp_id = request.user_profile.webapp_id
		member_ids = []
		if member_status != '-1':
			members = member_models.Member.objects.filter(webapp_id=webapp_id,status = member_status)
			temp_ids = [member.id for member in members]
			member_ids = temp_ids  if temp_ids else [-1]
		start_time = request.GET.get('start_time', '')
		end_time = request.GET.get('end_time', '')
		id = request.GET.get('id',0)
		#导出
		export_id = request.GET.get('export_id',0)
		if id:
			belong_to = id
		else:
			belong_to = export_id

		# rebate_info = app_models.Rebate.objects.get(id=belong_to)

		params = {'belong_to': belong_to}

		if member_ids:
			params['member_id__in'] = member_ids
		if start_time:
			params['created_at__gte'] = start_time
		if end_time:
			params['created_at__lte'] = end_time

		datas = app_models.RebateParticipance.objects(**params).order_by('-created_at')

		#进行分页
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		cur_page = int(request.GET.get('page', '1'))
		if not export_id:
			pageinfo, datas = paginator.paginate(datas, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

		tmp_member_ids = []
		for data in datas:
			tmp_member_ids.append(data.member_id)
		members = member_models.Member.objects.filter(id__in=tmp_member_ids)
		member_id2member = {member.id: member for member in members}

		items = []
		for data in datas:
			cur_member = member_id2member.get(data.member_id, None)
			if cur_member:
				try:
					name = cur_member.username.decode('utf8')
				except:
					name = cur_member.username_hexstr
			else:
				name = u'未知'

			items.append({
				'id': str(data.id),
				'member_id': data.member_id,
				'belong_to': data.belong_to,
				'participant_name': member_id2member[data.member_id].username_size_ten if member_id2member.get(data.member_id) else u'未知',
				'username': name,
				'participant_icon': member_id2member[data.member_id].user_icon if member_id2member.get(data.member_id) else '/static/img/user-1.jpg',
				'created_at': data.created_at.strftime("%Y-%m-%d %H:%M:%S"),
			})

		if export_id:
			return items
		else:
			return pageinfo, items

	@login_required
	def api_get(request):
		"""
		响应API GET
		"""
		pageinfo, items = RebateParticipances.get_datas(request)
		response_data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': '-id',
			'data': {}
		}
		response = create_response(200)
		response.data = response_data
		return response.get_response()

class RedPacketParticipances_Export(resource.Resource):
	'''
	批量导出
	'''
	app = 'apps/rebate'
	resource = 'rebate_participances_export'

	@login_required
	def api_get(request):
		"""
		分析导出
		"""
		export_id = request.GET.get('export_id',0)
		download_excel_file_name = u'拼红包详情.xls'
		excel_file_name = 'red_packet_details_'+datetime.now().strftime('%H_%M_%S')+'.xls'
		dir_path_suffix = '%d_%s' % (request.user.id, date.today())
		dir_path = os.path.join(settings.UPLOAD_DIR, dir_path_suffix)

		if not os.path.exists(dir_path):
			os.makedirs(dir_path)
		export_file_path = os.path.join(dir_path,excel_file_name)
		#Excel Process Part
		try:
			import xlwt
			datas =RebateParticipances.get_datas(request)
			fields_pure = []
			export_data = []

			#from sample to get fields4excel_file
			fields_pure.append(u'会员id')
			fields_pure.append(u'用户名')
			fields_pure.append(u'红包金额')
			fields_pure.append(u'已获取金额')
			fields_pure.append(u'红包状态')
			fields_pure.append(u'系统发放状态')
			fields_pure.append(u'参与时间')

			#processing data
			num = 0
			for data in datas:
				export_record = []
				member_id = data["member_id"]
				participant_name = data["username"]
				red_packet_money = data["red_packet_money"]
				current_money = data["current_money"]
				red_packet_status = data["red_packet_status"] if data["red_packet_status_text"] == u'已结束' else ''
				is_already_paid = data["is_already_paid"] if data["red_packet_status_text"] == u'已结束' else ''
				created_at = data["created_at"]

				export_record.append(member_id)
				export_record.append(participant_name)
				export_record.append(red_packet_money)
				export_record.append(current_money)
				export_record.append(red_packet_status)
				export_record.append(is_already_paid)
				export_record.append(created_at)
				export_data.append(export_record)
			#workbook/sheet
			wb = xlwt.Workbook(encoding='utf-8')
			ws = wb.add_sheet('id%s'%export_id)
			header_style = xlwt.XFStyle()

			##write fields
			row = col = 0
			for h in fields_pure:
				ws.write(row,col,h)
				col += 1

			##write data
			if export_data:
				row = 1
				lens = len(export_data[0])
				for record in export_data:
					row_l = []
					for col in range(lens):
						record_col= record[col]
						if type(record_col)==list:
							row_l.append(len(record_col))
							for n in range(len(record_col)):
								data = record_col[n]
								try:
									ws.write(row+n,col,data)
								except:
									#'编码问题，不予导出'
									print record
									pass
						else:
							try:
								ws.write(row,col,record[col])
							except:
								#'编码问题，不予导出'
								print record
								pass
					if row_l:
						row = row + max(row_l)
					else:
						row += 1
				try:
					wb.save(export_file_path)
				except Exception, e:
					print 'EXPORT EXCEL FILE SAVE ERROR'
					print e
					print '/static/upload/%s/%s'%(dir_path_suffix,excel_file_name)
			else:
				ws.write(1,0,'')
				wb.save(export_file_path)
			response = create_response(200)
			response.data = {'download_path':'/static/upload/%s/%s'%(dir_path_suffix,excel_file_name),'filename':download_excel_file_name,'code':200}
		except Exception, e:
			error_msg = u"导出文件失败, cause:\n{}".format(unicode_full_stack())
			watchdog_error(error_msg)
			response = create_response(500)
			response.innerErrMsg = unicode_full_stack()

		return response.get_response()
