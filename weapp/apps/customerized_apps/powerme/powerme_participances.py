# -*- coding: utf-8 -*-
import json
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
from mall import export as mall_export
from utils.string_util import byte_to_hex
import os
from weapp import settings

FIRST_NAV = mall_export.MALL_PROMOTION_AND_APPS_FIRST_NAV
COUNT_PER_PAGE = 20

class PowerMeParticipances(resource.Resource):
	app = 'apps/powerme'
	resource = 'powerme_participances'
	
	@login_required
	def get(request):
		"""
		响应GET
		"""
		has_data = app_models.PowerMeParticipance.objects(belong_to=request.GET['id']).count()
		
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': mall_export.get_promotion_and_apps_second_navs(request),
			'second_nav_name': mall_export.MALL_APPS_SECOND_NAV,
			'third_nav_name': mall_export.MALL_APPS_POWERME_NAV,
			'has_data': has_data,
			'activity_id': request.GET['id']
		});
		
		return render_to_response('powerme/templates/editor/powerme_participances.html', c)
	
	@staticmethod
	def get_datas(request):
		name = request.GET.get('participant_name', '')
		member_ids = []
		if name:
			members = member_models.Member.objects.filter(username_hexstr__contains = byte_to_hex(name))
			member_ids = [member.id for member in members]
		start_time = request.GET.get('start_time', '')
		end_time = request.GET.get('end_time', '')
		id = request.GET.get('id',0)
		#导出
		export_id = request.GET.get('export_id',0)
		if id:
			belong_to = id
		else:
			belong_to = export_id
		params = {'belong_to': belong_to,'has_join': True}
		if member_ids:
			params['member_id__in'] = member_ids
		if start_time:
			params['created_at__gte'] = start_time
		if end_time:
			params['created_at__lte'] = end_time
		datas = app_models.PowerMeParticipance.objects(**params).order_by('-power','created_at')

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
		#排名  导出时不适用
		ranking = (cur_page-1)*count_per_page
		for data in datas:
			ranking += 1
			items.append({
				'id': str(data.id),
				'ranking': ranking,
				'participant_name': member_id2member[data.member_id].username_size_ten if member_id2member.get(data.member_id) else u'未知',
				'username': member_id2member[data.member_id].username_for_html if member_id2member.get(data.member_id) else u'未知',
				'participant_icon': member_id2member[data.member_id].user_icon if member_id2member.get(data.member_id) else '/static/img/user-1.jpg',
				'power': data.power,
				'created_at': data.created_at.strftime("%Y-%m-%d %H:%M:%S")
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
		pageinfo, items = PowerMeParticipances.get_datas(request)
		response_data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': '-power',
			'data': {}
		}
		response = create_response(200)
		response.data = response_data
		return response.get_response()

class PowerMeParticipances_Export(resource.Resource):
	'''
	批量导出
	'''
	app = 'apps/powerme'
	resource = 'powerme_participances_export'

	@login_required
	def api_get(request):
		"""
		分析导出
		"""
		export_id = request.GET.get('export_id',0)
		download_excel_file_name = u'微助力详情.xls'
		excel_file_name = 'powerme_details.xls'
		export_file_path = os.path.join(settings.UPLOAD_DIR,excel_file_name)
		#Excel Process Part
		try:
			import xlwt
			datas = PowerMeParticipances.get_datas(request)
			fields_pure = []
			export_data = []

			#from sample to get fields4excel_file
			fields_pure.append(u'排名')
			fields_pure.append(u'用户名')
			fields_pure.append(u'助力值')
			fields_pure.append(u'参与时间')

			#processing data
			num = 0
			for data in datas:
				export_record = []
				num = num+1
				participant_name = data["username"]
				power = data["power"]
				created_at = data["created_at"]

				export_record.append(num)
				export_record.append(participant_name)
				export_record.append(power)
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
								ws.write(row+n,col,data)
						else:
							ws.write(row,col,record[col])
					if row_l:
						row = row + max(row_l)
					else:
						row += 1
				try:
					wb.save(export_file_path)
				except Exception, e:
					print 'EXPORT EXCEL FILE SAVE ERROR'
					print e
					print '/static/upload/%s'%excel_file_name
			else:
				ws.write(1,0,'')
				wb.save(export_file_path)
			response = create_response(200)
			response.data = {'download_path':'/static/upload/%s'%excel_file_name,'filename':download_excel_file_name,'code':200}
		except Exception, e:
			print e
			response = create_response(500)

		return response.get_response()

