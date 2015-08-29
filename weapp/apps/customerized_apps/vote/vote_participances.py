# -*- coding: utf-8 -*-
import json
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.conf import settings
from datetime import datetime
import os

from core import resource
from core import paginator
from core.jsonresponse import create_response
from modules.member import models as member_models
import models as app_models
from weixin2 import export

FIRST_NAV = 'apps'
COUNT_PER_PAGE = 20

class voteParticipances(resource.Resource):
	app = 'apps/vote'
	resource = 'vote_participances'
	
	@login_required
	def get(request):
		"""
		响应GET
		"""
		has_data = app_models.voteParticipance.objects(belong_to=request.GET['id']).count()
		
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_customerized_apps(request),
			'second_nav_name': "votes",
			'has_data': has_data,
			'activity_id': request.GET['id']
		})
		
		return render_to_response('vote/templates/editor/vote_participances.html', c)
	
	@staticmethod
	def get_datas(request):
		name = request.GET.get('participant_name', '')
		if name:
			members = member_models.Member.get_by_username(name)
		else:
			members = member_models.Member.get_members(request.user_profile.webapp_id)
		member_ids = [member.id for member in members]
		webapp_user_ids = [webapp_user.id for webapp_user in member_models.WebAppUser.objects.filter(member_id__in=member_ids)]
		start_time = request.GET.get('start_time', '')
		end_time = request.GET.get('end_time', '')
		params = {'belong_to':request.GET['id']}
		if webapp_user_ids:
			params['webapp_user_id__in'] = webapp_user_ids
		if start_time:
			params['created_at__gte'] = start_time
		if end_time:
			params['created_at__lte'] = end_time
		datas = app_models.voteParticipance.objects(**params).order_by('-id')
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
		pageinfo, datas = voteParticipances.get_datas(request)
		
		webappuser2datas = {}
		webapp_user_ids = set()
		for data in datas:
			webappuser2datas.setdefault(data.webapp_user_id, []).append(data)
			webapp_user_ids.add(data.webapp_user_id)
			data.participant_name = u'未知'
			data.participant_icon = '/static/img/user-1.jpg'
		
		webappuser2member = member_models.Member.members_from_webapp_user_ids(webapp_user_ids)
		if len(webappuser2member) > 0:
			for webapp_user_id, member in webappuser2member.items():
				for data in webappuser2datas.get(webapp_user_id, ()):
					data.participant_name = member.username_for_html
					data.participant_icon = member.user_icon
		
		items = []
		for data in datas:
			items.append({
				'id': str(data.id),
				'participant_name': data.participant_name,
				'participant_icon': data.participant_icon,
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

class voteParticipances_Export(resource.Resource):
	'''
	批量导出
	'''
	app = 'apps/vote'
	resource = 'vote_participances-export'

	@login_required
	def api_get(request):
		"""
		详情导出

		字段顺序:序号，用户名，创建时间，选择1，选择2……问题1，问题2……快照1，快照2……
		"""
		export_id = request.GET.get('export_id')
		trans2zh = {u'phone':u'手机',u'email':u'邮箱',u'name':u'姓名',u'tel':u'电话'}

		app_name = voteParticipances_Export.app.split('/')[1]
		excel_file_name = ('%s_id%s_%s.xls') % (app_name,export_id,datetime.now().strftime('%Y%m%d%H%m%M%S'))
		export_file_path = os.path.join(settings.UPLOAD_DIR,excel_file_name)

		#Excel Process Part
		try:
			import xlwt
			data = app_models.voteParticipance.objects(belong_to=export_id)
			fields_raw = []
			fields_pure = []
			export_data = []

			#from sample to get fields4excel_file
			fields_raw.append(u'编号')
			fields_raw.append(u'用户名')
			fields_raw.append(u'提交时间')
			sample = data[0]

			fields_selec = []
			fields_qa= []
			fields_shortcuts = []

			sample_tm = sample['termite_data']

			for item in sample_tm:
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
				if sample_tm[item]['type']=='appkit.shortcuts':
					if item in fields_shortcuts:
						pass
					else:
						fields_shortcuts.append(item)
			fields_raw = fields_raw + fields_selec + fields_qa + fields_shortcuts


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
			member_ids = [record['member_id'] for record in data ]
			members = member_models.Member.objects.filter(id__in = member_ids)
			member_id2name ={}
			for member in members:
				m_id = member.id
				if member.is_subscribed == True:
					u_name = member.username
				else:
					u_name = u'非会员'
				if m_id not in member_id2name:
					member_id2name[m_id] = u_name
				else:
					member_id2name[m_id] = u_name
			#processing data
			num = 0
			for record in data:
				selec =[]
				selec_v =[]
				qa = []
				shortcuts =[]
				export_record = []

				num = num+1
				name = member_id2name[record['member_id']]
				create_at = record['created_at'].strftime("%Y-%m-%d %H:%M:%S")

				for s in fields_selec:
					s_i = record[u'termite_data'][s][u'value']
					for i in s_i:
						if s_i[i]['isSelect'] == True:
							selec_v.append(i.split('_')[1])
					selec.append(selec_v)
				for s in fields_qa:
					s_v = record[u'termite_data'][s][u'value']
					qa.append(s_v)
				for s in fields_shortcuts:
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
			print export_data
			if export_data:
				row = 0
				lens = len(export_data[0])
				for record in export_data:
					row +=1
					for col in range(lens):
						if type(record[col]) == list and len(record[col])>=2:
							ws.write(row,col,u",".join(record[col]))
						else:
							ws.write(row,col,record[col])
				try:
					wb.save(export_file_path)
				except:
					print 'EXPORT EXCEL FILE SAVE ERROR'
					print '/static/upload/%s'%excel_file_name

			response = create_response(200)
			response.data = {'download_path':'/static/upload/%s'%excel_file_name,'filename':excel_file_name,'code':200}
		except:
			response = create_response(500)

		return response.get_response()