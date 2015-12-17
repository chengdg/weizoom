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
		datas = app_models.eventParticipance.objects(**params).order_by('-id')	
		
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
		pageinfo, datas = eventParticipances.get_datas(request)

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
			items.append({
				'id': str(data.id),
				'participant_name': member_id2member[data.member_id].username_size_ten if member_id2member.get(data.member_id) else u'未知',
				'participant_icon': member_id2member[data.member_id].user_icon if member_id2member.get(data.member_id) else '/static/img/user-1.jpg',
				'created_at': data.created_at.strftime("%Y-%m-%d %H:%M:%S"),
				'informations': event_id2item_data_list[data.id]
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
		export_id = request.GET.get('export_id')
		trans2zh = {u'phone':u'手机',u'email':u'邮箱',u'name':u'姓名',u'tel':u'电话',u'qq':u'QQ号',u'job':u'职位',u'addr':u'地址'}

		# app_name = eventParticipances_Export.app.split('/')[1]
		# excel_file_name = ('%s_id%s_%s.xls') % (app_name,export_id,datetime.now().strftime('%Y%m%d%H%m%M%S'))
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
			name = request.GET.get('participant_name', '')
			webapp_id = request.user_profile.webapp_id
			member_ids = []
			if name:
				hexstr = byte_to_hex(name)
				members = member_models.Member.objects.filter(webapp_id=webapp_id,username_hexstr__contains=hexstr)
				temp_ids = [member.id for member in members]
				member_ids = temp_ids  if temp_ids else [-1]
			start_time = request.GET.get('start_time', '')
			end_time = request.GET.get('end_time', '')
			params = {'belong_to':request.GET['export_id']}
			if member_ids:
				params['member_id__in'] = member_ids
			if start_time:
				params['created_at__gte'] = start_time
			if end_time:
				params['created_at__lte'] = end_time
			data = app_models.eventParticipance.objects(**params).order_by('-id')

			fields_raw = []
			fields_pure = []
			export_data = []

			#from sample to get fields4excel_file
			fields_raw.append(u'编号')
			fields_raw.append(u'用户名')
			fields_raw.append(u'提交时间')
			if data:
				sample = data[0]
				fields_selec = []
				fields_qa= []
				fields_textlist = []

				sample_tm = sample['termite_data']
				for item in sorted(sample_tm.keys()):
					if sample_tm[item]['type']=='appkit.qa':
						if item in fields_qa:
							pass
						else:
							fields_qa.append(item)
					if sample_tm[item]['type']=='appkit.selection':
						if item in fields_selec:
							pass
						else:
							fields_selec.append(item)
					if sample_tm[item]['type'] in['appkit.textlist', 'appkit.shortcuts']:
						if item in fields_textlist:
							pass
						else:
							fields_textlist.append(item)
				fields_raw = fields_raw + fields_selec + fields_qa + fields_textlist


			for field in fields_raw:
				if '_' in field:
					purename = field.split('_')[1]
					if purename in trans2zh:
						fields_pure.append(trans2zh[purename])
					else:
						fields_pure.append(purename)
				else:
					fields_pure.append(field)

			#username(member_id)
			member_ids = []
			for record in data:
				member_ids.append(record['member_id'])
			members = member_models.Member.objects.filter(id__in=member_ids)
			member_id2member = {member.id: member for member in members}
			#processing data
			num = 0
			for record in data:
				selec =[]
				qa = []
				shortcuts =[]
				export_record = []

				num = num+1
				cur_member = member_id2member.get(record['member_id'], None)
				if cur_member:
					try:
						name = cur_member.username.decode('utf8')
					except:
						name = cur_member.username_hexstr
				else:
					name = u'未知'
				create_at = record['created_at'].strftime("%Y-%m-%d %H:%M:%S")

				for s in fields_selec:
					s_i = record[u'termite_data'][s][u'value']
					for i in s_i:
						if s_i[i]['isSelect'] == True:
							selec.append(i.split('_')[1])
				for s in fields_qa:
					s_v = record[u'termite_data'][s][u'value']
					qa.append(s_v)
				for s in fields_textlist:
					s_v = record[u'termite_data'][s][u'value']
					shortcuts.append(s_v)

				# don't change the order
				export_record.append(num)
				export_record.append(name)
				export_record.append(create_at)

				for item in selec:
					export_record.append(item)
				for item in qa:
					export_record.append(item)
				for item in shortcuts:
					export_record.append(item)

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
				row = 0
				lens = len(export_data[0])
				for record in export_data:
					row +=1
					for col in range(lens):
						try:
							ws.write(row,col,record[col])
						except:
							#'编码问题，不予导出'
							print record
							pass
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