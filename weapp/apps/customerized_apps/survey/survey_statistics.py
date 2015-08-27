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

class surveyStatistics(resource.Resource):
	app = 'apps/survey'
	resource = 'survey_statistics'

	@login_required
	def get(request):
		"""
		响应GET
		"""
		if 'id' in request.GET:
			survey_id =request.GET['id']
			all_participances = app_models.surveyParticipance.objects(belong_to=survey_id)
			total_count = all_participances.count()

			q_vote ={}
			result_list = []

			for participance in all_participances:
				termite_data = participance.termite_data
				for k in sorted(termite_data.keys()):
					value = termite_data[k]
					if value['type'] == 'appkit.selection':
						if not q_vote.has_key(k):
							q_vote[k] = {
								'type': 'appkit.selection',
								'value': [value['value']]
							}
						else:
							q_vote[k]['value'].append(value['value'])
					if value['type'] == 'appkit.qa':
						if not q_vote.has_key(k):
							q_vote[k] = {
								'type': 'appkit.qa',
								'value': [value['value']],

							}
						else:
							q_vote[k]['value'].append(value['value'])

			for k,v in q_vote.items():
				a_isSelect = {}
				result = {}
				count = len(v['value'])
				value_list = []
				v_a = {}
				for title_value in v['value']:
					if v['type'] == 'appkit.selection':
						v_a = title_value
						for a_k,a_v in title_value.items():
							if not a_isSelect.has_key(a_k):
								a_isSelect[a_k] = 0
							if a_v['isSelect'] == True:
								a_isSelect[a_k] += 1
				for a_k in sorted(v_a.keys()):
					value ={}
					value['name'] = a_k.split('_')[1]
					value['count'] = a_isSelect[a_k]
					value['per'] =  '%d%s' % (a_isSelect[a_k]*100/float(count),'%')
					value_list.append(value)
				title_name = k.split('_')[1]
				result['title'] = title_name
				result['title_'] = k
				result['count'] = count
				question_list = []
				# if v['type'] == 'appkit.qa':
				# 	for question in v['value']:
				# 		question_list.append(question)


				result['values'] = value_list if v['type'] == 'appkit.selection' else question_list
				result['type'] = v['type']
				result_list.append(result)

			project_id = 'new_app:survey:%s' % request.GET.get('related_page_id', 0)
		else:
			total_count = 0
			result_list = None
			project_id = 'new_app:survey:0'
			survey_id = 0

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_customerized_apps(request),
			'second_nav_name': 'surveies',
			'titles': result_list,
			'total_count': total_count,
			'project_id': project_id,
			'survey_id':survey_id

		})

		return render_to_response('survey/templates/editor/survey_statistics.html', c)

class question(resource.Resource):
	app = 'apps/survey'
	resource = 'question'

	@login_required
	def api_get(request):
		"""
		响应API GET
		"""
		survey_id =request.GET['id']
		question_title = request.GET['question_title']
		all_participances = app_models.surveyParticipance.objects(belong_to=survey_id)

		result_list = []

		for participance in all_participances:
			termite_data = participance.termite_data
			for k in sorted(termite_data.keys()):
				if question_title == k :
					value = termite_data[k]
					if value['type'] == 'appkit.qa':
						result_list.append({
							'content': value['value'],
							'created_at':participance['created_at'].strftime('%Y-%m-%d')
						})

		#进行分页
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		cur_page = int(request.GET.get('page', '1'))
		pageinfo, datas = paginator.paginate(result_list, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

		items = []
		for data in datas:
			items.append(data)
		response_data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': 'id',
			'data': {}
		}
		response = create_response(200)
		response.data = response_data
		return response.get_response()

class surveyStatistics_Export(resource.Resource):
	'''
	批量导出
	'''
	app = 'apps/survey'
	resource = 'survey_statistics-export'

	@login_required
	def api_get(request):
		"""
		不同类型分页统计
		"""
		export_id = request.GET.get('export_id')
		trans2zh = {u'phone':u'手机',u'email':u'邮箱',u'name':u'姓名',u'tel':u'电话'}

		app_name = surveyStatistics_Export.app.split('/')[1]
		excel_file_name = ('%s_%s.xls') % (app_name,datetime.now().strftime('%Y%m%d%H%m%M%S'))
		export_file_path = os.path.join(settings.UPLOAD_DIR,excel_file_name)

		#Excel Process Part
		try:
			import xlwt
			data = app_models.surveyParticipance.objects(belong_to=export_id)
			# total = data.count()
			termite_data = [ item['termite_data'] for item in data]

			#select sheet
			select_data = {}
			select_static ={}
			qa_data = {}
			qa_static = {}
			for record in termite_data:
				for s_i in record:
					if record[s_i]['type']=='appkit.selection':
						select_data[s_i]=record[s_i]
					if record[s_i]['type']=='appkit.qa':
						qa_data[s_i]=record[s_i]
			#analaysis

				#select 是问题
				#select_data[select]是字典内容
				#select_data[select]['value']选项字典{u'08_QA1': {u'isSelect': False, u'type': u'radio'}, u'10_QA3': {u'isSelect': False, u'type': u'radio'}, u'09_QA2': {u'isSelect': True, u'type': u'radio'}}
				#select_data[select]['value']->item选项
				#select_data[select]['value'][item]['isSelect'] 选项结果 True/False
			for select in select_data:
				for item in select_data[select]['value']:
					if select not in select_static:
						select_static[select]={}
					if item not in select_static[select]:
						select_static[select][item] = 0
					if select_data[select]['value'][item]['isSelect'] == True:
						select_static[select][item] += 1

			print select_static
			print '----------------'
			print 'here'


			# fields_raw = []
			# fields_pure = []
			# export_data = []
            #
			# #from sample to get fields4excel_file
			# fields_raw.append(u'编号')
			# fields_raw.append(u'用户名')
			# fields_raw.append(u'提交时间')
			# sample = data[0]
            #
			# fields_selec = []
			# fields_qa= []
			# fields_shortcuts = []
            #
			# sample_tm = sample['termite_data']
            #
			# for item in sample_tm:
			# 	if sample_tm[item]['type']=='appkit.qa':
			# 		if item in fields_qa:
			# 			pass
			# 		else:
			# 			fields_qa.append(item)
			# 	if sample_tm[item]['type']=='appkit.selection':
			# 		if item in fields_selec:
			# 			pass
			# 		else:
			# 			fields_selec.append(item)
			# 	if sample_tm[item]['type']=='appkit.shortcuts':
			# 		if item in fields_shortcuts:
			# 			pass
			# 		else:
			# 			fields_shortcuts.append(item)
			# fields_raw = fields_raw + fields_selec + fields_qa + fields_shortcuts
            #
            #
			# for field in fields_raw:
			# 	if '_' in field:
			# 		purename = field.split('_')[1]
			# 		if purename in trans2zh:
			# 			fields_pure.append(trans2zh[purename])
			# 		else:
			# 			fields_pure.append(purename)
			# 	else:
			# 		fields_pure.append(field)
            #
			# #username(webapp_user_id/member_id)
			# webapp_id_list = map(long,[record['webapp_user_id'] for record in data ])#大
			# #测试：member里的id好像和webapp_id不一样
			# members = member_models.Member.objects.filter(webapp_id__in = webapp_id_list)#小
			# webapp_id2name ={}
			# for member in members:
			# 	w_id = long(member.webapp_id)
			# 	if w_id not in webapp_id2name:
			# 		webapp_id2name[w_id] = member.username
			# 	else:
			# 		webapp_id2name[w_id] = member.username
			# for item in webapp_id_list:
			# 	if item not in webapp_id2name:
			# 		webapp_id2name[item] = u"非会员"
            #
			# #processing data
			# num = 0
			# for record in data:
			# 	selec =[]
			# 	qa = []
			# 	shortcuts =[]
			# 	export_record = []
            #
			# 	num = num+1
			# 	name = webapp_id2name[record['webapp_user_id']]
			# 	create_at = record['created_at'].strftime("%Y-%m-%d %H:%M:%S")
            #
			# 	for s in fields_selec:
			# 		s_i = record[u'termite_data'][s][u'value']
			# 		for i in s_i:
			# 			if s_i[i]['isSelect'] == True:
			# 				selec.append(i.split('_')[1])
			# 	for s in fields_qa:
			# 		s_v = record[u'termite_data'][s][u'value']
			# 		qa.append(s_v)
			# 	for s in fields_shortcuts:
			# 		s_v = record[u'termite_data'][s][u'value']
			# 		shortcuts.append(s_v)
            #
			# 	# don't change the order
			# 	export_record.append(num)
			# 	export_record.append(name)
			# 	export_record.append(create_at)
            #
			# 	for item in selec:
			# 		export_record.append(item)
			# 	for item in qa:
			# 		export_record.append(item)
			# 	for item in shortcuts:
			# 		export_record.append(item)
            #
			# 	export_data.append(export_record)

			# #workbook/sheet
			# wb = xlwt.Workbook(encoding='utf-8')
			# ws = wb.add_sheet('id%s'%export_id)
			# header_style = xlwt.XFStyle()
            #
			# ##write fields
			# row = col = 0
			# for h in fields_pure:
			# 	ws.write(row,col,h)
			# 	col += 1
            #
			# ##write data
			# row = 0
			# lens = len(export_data[0])
			# for record in export_data:
			# 	row +=1
			# 	for col in range(lens):
			# 		ws.write(row,col,record[col])
			# try:
			# 	wb.save(export_file_path)
			# except:
			# 	print 'EXPORT EXCEL FILE SAVE ERROR'
			# 	print '/static/upload/%s'%excel_file_name

			response = create_response(200)
			# response.data = {'download_path':'/static/upload/%s'%excel_file_name,'filename':excel_file_name,'code':200}
		except:
			response = create_response(500)

		return response.get_response()