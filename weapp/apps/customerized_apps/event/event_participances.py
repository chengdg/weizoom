# -*- coding: utf-8 -*-
import json
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.conf import settings
from datetime import datetime, date
import os

from core import resource
from core import paginator
from core.jsonresponse import create_response
from modules.member import models as member_models
import models as app_models
from mall import export
import re
from utils.string_util import hex_to_byte, byte_to_hex
from watchdog.utils import watchdog_error
from core.exceptionutil import unicode_full_stack

FIRST_NAV = export.MALL_PROMOTION_AND_APPS_FIRST_NAV
COUNT_PER_PAGE = 20

ITEM_FOR_DISPLAY = {
	'phone': u'手机',
	'name': u'姓名',
	'email': u'邮箱',
	'qq':u'QQ号',
	'job':u'职位',
	'addr':u'地址'
}

class eventParticipances(resource.Resource):
	app = 'apps/event'
	resource = 'event_participances'
	
	@login_required
	def get(request):
		"""
		响应GET
		"""
		has_data = app_models.eventParticipance.objects(belong_to=request.GET['id']).count()
		
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_promotion_and_apps_second_navs(request),
			'second_nav_name': export.MALL_APPS_SECOND_NAV,
            'third_nav_name': export.MALL_APPS_EVENT_NAV,
			'has_data': has_data,
			'activity_id': request.GET['id']
		});
		
		return render_to_response('event/templates/editor/event_participances.html', c)
	
	@staticmethod
	def get_datas(request,is_pageinfo=True):
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
		datas = app_models.eventParticipance.objects(**params).order_by('-id')	

		if is_pageinfo:
			#进行分页
			count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
			cur_page = int(request.GET.get('page', '1'))
			pageinfo, datas = paginator.paginate(datas, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

		event_ids = []
		tmp_member_ids = []
		for data in datas:
			tmp_member_ids.append(data.member_id)
			event_ids.append(data.id)
		members = member_models.Member.objects.filter(id__in=tmp_member_ids)
		member_id2member = {member.id: member for member in members}

		event_participances = app_models.eventParticipance.objects(id__in=event_ids)
		event_id2item_data_list = {}
		for p in event_participances:
			termite_data = p.termite_data
			item_data_list = []
			for k in sorted(termite_data.keys()):
				v = termite_data[k]
				pureName = k.split('_')[1]
				item_data = {}
				if pureName in ITEM_FOR_DISPLAY:#判断是否是自定义的填写项
					item_data['item_name'] = ITEM_FOR_DISPLAY[pureName]
				else:
					item_data['item_name'] = pureName
				item_data['item_value'] = v['value']
				item_data_list.append(item_data)
			event_id2item_data_list[p.id] = item_data_list

		items = []
		for data in datas:
			cur_member = member_id2member.get(data.member_id,None)
			if cur_member:
				try:
					name = cur_member.username.decode('utf8')
				except:
					name = cur_member.username_hexstr
			items.append({
				'id': str(data.id),
				'name': name,
				'participant_name': member_id2member[data.member_id].username_truncated if member_id2member.get(data.member_id) else u'未知',
				'participant_icon': member_id2member[data.member_id].user_icon if member_id2member.get(data.member_id) else '/static/img/user-1.jpg',
				'created_at': data.created_at.strftime("%Y-%m-%d %H:%M:%S"),
				'informations': event_id2item_data_list[data.id]
			})
		if is_pageinfo:
			return pageinfo, items
		else:
			return items
	
	@login_required
	def api_get(request):
		"""
		响应API GET
		"""
		pageinfo, items = eventParticipances.get_datas(request)

		response_data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': 'id',
			'data': {}
		}
		response = create_response(200)
		response.data = response_data
		return response.get_response()		

class eventParticipances_Export(resource.Resource):
	'''
	批量导出
	'''
	app = 'apps/event'
	resource = 'event_participances-export'

	@login_required
	def api_get(request):
		"""
		详情导出

		字段顺序:序号，用户名，创建时间，选择1，选择2……问题1，问题2……快照1，快照2……
		"""
		export_id = request.GET.get('id')
		download_excel_file_name = u'活动报名详情.xls'
		excel_file_name = 'event_details_'+datetime.now().strftime('%H_%M_%S')+'.xls'
		dir_path_suffix = '%d_%s' % (request.user.id, date.today())
		dir_path = os.path.join(settings.UPLOAD_DIR, dir_path_suffix)

		if not os.path.exists(dir_path):
			os.makedirs(dir_path)
		export_file_path = os.path.join(dir_path,excel_file_name)

		#Excel Process Part
		try:
			import xlwt
			items = eventParticipances.get_datas(request,False)
			fields_raw = []

			#from sample to get fields4excel_file
			fields_raw.append(u'编号')
			fields_raw.append(u'用户名')
			fields_raw.append(u'提交时间')
			if items:
				sample_datas = items[0]['informations']
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
			if items:
				row = 0
				for item in items:
					row += 1
					ws.write(row,0,row)
					ws.write(row,1,item['name'])
					ws.write(row,2,item['created_at'])
					col = 3
					informations = item['informations']
					for data in informations:
						ws.write(row,col,data['item_value'])
						col += 1
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