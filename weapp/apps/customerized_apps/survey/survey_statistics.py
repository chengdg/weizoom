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
from mall import export

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
			total_participance = all_participances.count()

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
					if value['type'] == 'appkit.uploadimg':
						if not q_vote.has_key(k):
							q_vote[k] = {
								'type': 'appkit.uploadimg',
								'value': [value['value']],
							}
						else:
							q_vote[k]['value'].append(value['value'])

			for k in sorted(q_vote.keys()):
				a_isSelect = {}
				result = {}
				count = len(q_vote[k]['value'])
				total_count = 0
				value_list = []
				v_a = {}
				title_type = u''
				for title_value in q_vote[k]['value']:
					if q_vote[k]['type'] == 'appkit.selection':
						v_a = title_value
						for a_k,a_v in title_value.items():
							if not a_isSelect.has_key(a_k):
								a_isSelect[a_k] = 0
							if a_v['isSelect'] == True:
								a_isSelect[a_k] += 1
								total_count += 1
					if q_vote[k]['type'] == 'appkit.qa':
						type_name = u'问答'
					if q_vote[k]['type'] == 'appkit.uploadimg':
						type_name = u'上传图片'

				for a_k in sorted(v_a.keys()):
					value ={}
					value['name'] = a_k.split('_')[1]
					title_type =  v_a[a_k]['type']
					value['count'] = a_isSelect[a_k]
					value['per'] =  '%d%s' % (a_isSelect[a_k]*100/float(total_count),'%')
					value_list.append(value)
				title_name = k.split('_')[1]
				result['title'] = title_name
				if title_type == 'radio':
					type_name = u'单选'
				elif title_type == 'checkbox':
					type_name = u'多选'

				result['title_type'] = type_name
				result['title_'] = k
				result['count'] = count
				question_list = []
				result['values'] = value_list if q_vote[k]['type'] == 'appkit.selection' else question_list
				result['type'] = q_vote[k]['type']
				result_list.append(result)

			project_id = 'new_app:survey:%s' % request.GET.get('related_page_id', 0)
		else:
			total_participance = 0
			result_list = None
			project_id = 'new_app:survey:0'
			survey_id = 0

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_customerized_apps(request),
			'second_nav_name': 'surveies',
			'titles': result_list,
			'total_participance': total_participance,
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
					if value['type'] == 'appkit.uploadimg':
						img_urls = []
						if len(value['value'])>1:
							index = 0
							for v in value['value']:
								img_urls.append('<img class="xui-uploadimg xa-uploadimg" id="uploadimg-%d" src="'%(index)+v+'">')
								index +=1
							result_list.append({
								'content': img_urls,
								'type': 'uploadimg',
								'created_at':participance['created_at'].strftime('%Y-%m-%d')
							})
						else:
							for v in value['value']:
								img_urls.append('<img class="xui-uploadimg xa-uploadimg" id=\"uploadimg-0\" src="'+v+'">')
							result_list.append({
								'content': img_urls,
								'type': 'uploadimg',
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

		# app_name = surveyStatistics_Export.app
		# excel_file_name = ('%s_id%s_%s.xls') % (app_name.split("/")[1],export_id,datetime.now().strftime('%Y%m%d%H%m%M%S'))
		excel_file_name = 'survey_statistic.xls'
		download_excel_file_name = u'用户调研统计.xls'
		export_file_path = os.path.join(settings.UPLOAD_DIR,excel_file_name)

		#Excel Process Part
		try:
			import xlwt
			data = app_models.surveyParticipance.objects(belong_to=export_id)
			total = data.count()
			member_id2termite_data={}
			for item in data:
				if item['member_id'] not in member_id2termite_data:
					member_id2termite_data[item['member_id']] = {'created_at':item['created_at'],'termite_data':item['termite_data']}

			#select sheet
			select_data = {}
			select_static ={}
			qa_static = {}
			uploadimg_static = {}
			for item in member_id2termite_data:
				record = member_id2termite_data[item]
				time = record['created_at']
				for termite in record['termite_data']:
					termite_dic = record['termite_data'][termite]
					if termite_dic['type']=='appkit.selection':
						if termite not in select_data:
							select_data[termite] = [termite_dic['value']]
						else:
							select_data[termite].append(termite_dic['value'])
					if termite_dic['type']=='appkit.qa':
						if termite not in qa_static:
							qa_static[termite]=[{'created_at':time,'answer':termite_dic['value']}]
						else:
							qa_static[termite].append({'created_at':time,'answer':termite_dic['value']})
					if termite_dic['type']=='appkit.uploadimg':
						if termite not in uploadimg_static:
							uploadimg_static[termite]=[{'created_at':time,'url':termite_dic['value']}]
						else:
							uploadimg_static[termite].append({'created_at':time,'url':termite_dic['value']})

			#select-data-processing
			total_count = 0
			for select in select_data:
				for s_list in select_data[select]:
					for s in s_list:
						if select not in select_static:
							select_static[select]={}
						if s not in select_static[select]:
							select_static[select][s]  = 0
						if s_list[s]['isSelect'] == True:
							select_static[select][s] += 1
							total_count += 1
			#workbook/sheet
			wb = xlwt.Workbook(encoding='utf-8')

			#select_sheet
			if select_static:
				ws = wb.add_sheet(u'选择题')
				header_style = xlwt.XFStyle()
				select_num = 0
				row = col =0
				for s in select_static:
					select_num += 1
					ws.write(row,col,'%d.'%select_num+s.split('_')[1]+u'(有效参与人数%d人)'%total)
					ws.write(row,col+1,u'参与人数/百分百')
					row += 1
					s_i_num = 0
					for s_i in select_static[s]:
						ws.write(row,col,s_i.split('_')[1])
						s_num = select_static[s][s_i]
						per = s_num*1.0/total_count*100
						ws.write(row,col+1,u'%d人/%.1f%%'%(s_num,per))
						row += 1
						s_i_num += 1
					ws.write(row,col,u'')
					ws.write(row,col+1,u'')
					row += 1
					ws.write(row,col,u'')
					ws.write(row,col+1,u'')
					row += 1

			#qa_sheet
			if qa_static:
				qa_num = 0
				for q in qa_static:
					qa_num += 1
					row = col = 0
					ws = wb.add_sheet(u'问题%d'%qa_num)
					header_style = xlwt.XFStyle()

					ws.write(row,col,u'提交时间')
					ws.write(row,col+1,q.split('_')[1]+u'(有效参与人数%d)'%total)

					for item in qa_static[q]:
						row +=1
						ws.write(row,col,item['created_at'].strftime("%Y/%m/%d %H:%M"))
						ws.write(row,col+1,item['answer'])

			#uploadimg_sheet
			if uploadimg_static:
				uploadimg_num = 0
				for u in uploadimg_static:
					uploadimg_num += 1
					row = col = 0
					ws = wb.add_sheet(u'图片%d'%uploadimg_num)
					header_style = xlwt.XFStyle()

					ws.write(row,col,u'上传时间')
					ws.write(row,col+1,u.split('_')[1]+u'(有效参与人数%d)'%total)

					for item in uploadimg_static[u]:
						row +=1
						ws.write(row,col,item['created_at'].strftime("%Y/%m/%d %H:%M"))
						for i in item['url']:
							if len(item['url'])>1:
								ws.write(row,col+1,i)
								row +=1
							else:
								ws.write(row,col+1,i)

			try:
				wb.save(export_file_path)
			except:
				print 'EXPORT EXCEL FILE SAVE ERROR'
				print '/static/upload/%s'%excel_file_name

			response = create_response(200)
			response.data = {'download_path':'/static/upload/%s'%excel_file_name,'filename':download_excel_file_name,'code':200}
		except:
			response = create_response(500)

		return response.get_response()