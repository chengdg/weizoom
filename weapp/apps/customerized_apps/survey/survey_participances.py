# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.conf import settings
from datetime import datetime, date
import os
from apps.customerized_apps.survey.m_survey import Msurvey
from core import resource
from core import paginator
from core.exceptionutil import unicode_full_stack
from core.jsonresponse import create_response
from modules.member import models as member_models
import models as app_models
from mall import export
from utils.string_util import byte_to_hex
from watchdog.utils import watchdog_error

FIRST_NAV = export.MALL_PROMOTION_AND_APPS_FIRST_NAV
COUNT_PER_PAGE = 20

class surveyParticipances(resource.Resource):
	app = 'apps/survey'
	resource = 'survey_participances'
	
	@login_required
	def get(request):
		"""
		响应GET
		"""
		has_data = app_models.surveyParticipance.objects(belong_to=request.GET['id']).count()
		
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_promotion_and_apps_second_navs(request),
			'second_nav_name': export.MALL_APPS_SECOND_NAV,
            'third_nav_name': export.MALL_APPS_SURVEY_NAV,
			'has_data': has_data,
			'activity_id': request.GET['id'],
		});
		
		return render_to_response('survey/templates/editor/survey_participances.html', c)
	
	@staticmethod
	def get_datas(request):
		name = request.GET.get('participant_name', '')
		webapp_id = request.user_profile.webapp_id
		member_ids = []
		if name:
			hexstr = byte_to_hex(name)
			members = member_models.Member.objects.filter(webapp_id=webapp_id,username_hexstr__contains=hexstr)
			temp_ids = [member.id for member in members]
			member_ids = temp_ids  if temp_ids else [-1]
		# webapp_user_ids = [webapp_user.id for webapp_user in member_models.WebAppUser.objects.filter(member_id__in=member_ids)]
		start_time = request.GET.get('start_time', '')
		end_time = request.GET.get('end_time', '')
		params = {'belong_to':request.GET['id']}
		if member_ids:
			params['member_id__in'] = member_ids
		if start_time:
			params['created_at__gte'] = start_time
		if end_time:
			params['created_at__lte'] = end_time
		datas = app_models.surveyParticipance.objects(**params).order_by('-id')
		
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
		pageinfo, datas = surveyParticipances.get_datas(request)

		tmp_member_ids = []
		for data in datas:
			tmp_member_ids.append(data.member_id)
		members = member_models.Member.objects.filter(id__in=tmp_member_ids)
		member_id2member = {member.id: member for member in members}
		
		items = []
		for data in datas:
			items.append({
				'id': str(data.id),
				'participant_name': member_id2member[data.member_id].username_truncated if member_id2member.get(data.member_id) else u'未知',
				'participant_icon': member_id2member[data.member_id].user_icon if member_id2member.get(data.member_id) else '/static/img/user-1.jpg',
				'created_at': data.created_at.strftime("%Y-%m-%d %H:%M:%S")
			})
		response_data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': 'id',
			'data': {}
		}
		response = create_response(200)
		response.data = response_data
		return response.get_response()		

class surveyParticipances_Export(resource.Resource):
	'''
	批量导出
	'''
	app = 'apps/survey'
	resource = 'survey_participances-export'
	@login_required
	def api_get(request):
		"""
		详情导出

		字段顺序:序号，用户名，创建时间，选择1，选择2……问题1，问题2……快照1，快照2……
		"""
		export_id = request.GET.get('export_id')

		excel_file_name = 'survey_details_'+datetime.now().strftime('%H_%M_%S')+'.xls'
		dir_path_suffix = '%d_%s' % (request.user.id, date.today())
		dir_path = os.path.join(settings.UPLOAD_DIR, dir_path_suffix)

		if not os.path.exists(dir_path):
			os.makedirs(dir_path)
		export_file_path = os.path.join(dir_path,excel_file_name)
		download_excel_file_name = u'用户调研详情.xls'

		#Excel Process Part
		try:
			import xlwt
			item_data_list = Msurvey.get_surveyparticipance_datas(request)

			fields_raw = []
			#from sample to get fields4excel_file
			fields_raw.append(u'编号')
			fields_raw.append(u'用户名')
			fields_raw.append(u'提交时间')

			if item_data_list:
				sample_datas = item_data_list[0]['items']
				for sample_data in sample_datas:
					fields_raw.append(sample_data['item_name'])

			#workbook/sheet
			wb = xlwt.Workbook(encoding='utf-8')
			ws = wb.add_sheet('id%s'%export_id)
			header_style = xlwt.XFStyle()

			##write fields
			row = col = 0
			for h in fields_raw:
				ws.write(row,col,h)
				col += 1

			##write data
			if item_data_list:
				row = num = 0
				for item_data in item_data_list:
					row += 1
					num += 1
					ws.write(row,0,num)
					ws.write(row,1,item_data['name'])
					ws.write(row,2,item_data['created_at'])
					col = 3
					items = item_data['items']
					add_row_num = []
					for item in items:
						item_values = item['item_value']
						add_row_list_num = 0
						if type(item_values) == list and len(item_values) > 1:
							for item_value in item_values:
								ws.write(row+add_row_list_num,col,item_value)
								add_row_list_num += 1
						else:
							if item_values:
								ws.write(row,col,item_values)
							else:
								ws.write(row,col,'')
							row += 1
						add_row_num.append(add_row_list_num)
						col += 1
					row = row + max(add_row_num)
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
		except:
			error_msg = u"导出文件失败, cause:\n{}".format(unicode_full_stack())
			watchdog_error(error_msg)
			response = create_response(500)
			response.innerErrMsg = unicode_full_stack()

		return response.get_response()