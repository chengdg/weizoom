# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.conf import settings
from datetime import datetime, date
import os

from core import resource
from core import paginator
from core.jsonresponse import create_response
import models as app_models
from mall import export

FIRST_NAV = export.MALL_PROMOTION_AND_APPS_FIRST_NAV
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
			survey_id = request.GET['id']
			total_participance = app_models.surveyParticipance.objects(belong_to=request.GET['id']).count()
			all_participances = surveyStatistics.get_survey_title_select_datas(request)

			for participance in all_participances:
				if participance['type'] == 'appkit.textlist':
					all_participances.remove(participance)

			project_id = 'new_app:survey:%s' % request.GET.get('related_page_id', 0)
		else:
			total_participance = 0
			all_participances = None
			project_id = 'new_app:survey:0'
			survey_id = 0

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_promotion_and_apps_second_navs(request),
			'second_nav_name': export.MALL_APPS_SECOND_NAV,
            'third_nav_name': export.MALL_APPS_SURVEY_NAV,
			'titles': all_participances,
			'total_participance': total_participance,
			'project_id': project_id,
			'survey_id':survey_id

		})

		return render_to_response('survey/templates/editor/survey_statistics.html', c)


	@staticmethod
	def get_survey_title_select_datas(request):
		all_survey_participances = app_models.surveyParticipance.objects(belong_to=request.GET['id'])
		all_title_select_list = []
		select_title2itemCount = {}
		title_valid_dict = {}
		total_title_valid_dict ={}
		title_type_dict = {}
		title_image_dict = {}
		title_select_type_dict = {}
		member_dict = {}
		for p in all_survey_participances:
			for title, select_datas in p.termite_data.items():
				title_type = u''
				if select_datas['type'] =='appkit.selection':
					is_Select = False
					select_data_value = select_datas['value']
					for select_title in sorted(select_data_value.keys()):
						value = select_data_value[select_title]
						if value['isSelect']:
							is_Select = True
						if select_title2itemCount.has_key(title):
							if select_title2itemCount[title].has_key(select_title):
								select_title2itemCount[title][select_title] += 1 if value['isSelect'] else 0
							else:
								select_title2itemCount[title][select_title] = 1 if value['isSelect'] else 0
						else:
							select_title2itemCount[title] = {}
							select_title2itemCount[title][select_title] = 1 if value['isSelect'] else 0
						title_type = value['type']
					if is_Select:
						if total_title_valid_dict.has_key(title):
							total_title_valid_dict[title] += 1
						else:
							total_title_valid_dict[title] = 1
						if title_valid_dict.has_key(title):
							title_valid_dict[title] += 1
						else:
							title_valid_dict[title] = 1
					else:
						if not total_title_valid_dict.has_key(title):
							total_title_valid_dict[title] = 0
						if not title_valid_dict.has_key(title):
							title_valid_dict[title] = 0
					title_select_type_dict[title] = title_type
				if select_datas['type']  in ['appkit.textlist','appkit.uploadimg','appkit.qa']:
					if not select_title2itemCount.has_key(title):
						select_title2itemCount[title] = [{
							'created_at': p.created_at.strftime("%Y-%m-%d %H:%M:%S"),
							'value': select_datas['value']
						}]
					else:
						select_title2itemCount[title].append({
							'created_at': p.created_at.strftime("%Y-%m-%d %H:%M:%S"),
							'value': select_datas['value']
						})
				title_type_dict[title] = select_datas['type']
		for title in sorted(select_title2itemCount.keys()):
			single_title_dict = {}
			single_title_dict['title'] = title.split('_')[1]
			single_title_dict['type'] = title_type_dict[title]
			single_title_dict['values'] = []
			if title_type_dict[title] == 'appkit.selection':
				single_title_dict['title_valid_count'] = title_valid_dict[title]
				single_title_dict['title_type'] = u'单选' if title_select_type_dict[title] == 'radio' else u'多选'
				for select_title in sorted(select_title2itemCount[title].keys()):
					item_value = select_title2itemCount[title][select_title]
					single_item_value = {}
					single_item_value['name'] = select_title.split('_')[1]
					single_item_value['count'] = item_value
					if title_image_dict.has_key(select_title):
						single_item_value['image'] = title_image_dict[select_title]
					single_item_value['per'] = '%d%s' % (item_value / float(total_title_valid_dict[title]) * 100 if total_title_valid_dict[title] else 0, '%')
					single_title_dict['values'].append(single_item_value)
			else:
				type_name = u''
				if title_type_dict[title] == 'appkit.qa':
					type_name= u'问答'
				elif title_type_dict[title] == 'appkit.uploadimg':
					type_name= u'上传图片'
				single_title_dict['title_type'] = type_name
				single_title_dict['title_valid_count'] = len(select_title2itemCount[title])
				single_title_dict['complete_title'] = title
				single_title_dict['values'] = select_title2itemCount[title]
			all_title_select_list.append(single_title_dict)
		return  all_title_select_list

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
						if value['value']:
							result_list.append({
								'content': value['value'],
								'created_at':participance['created_at'].strftime('%Y-%m-%d')
							})
					if value['type'] == 'appkit.uploadimg':
						img_urls = []
						index = 0
						if value['value']:
							for v in value['value']:
								if v:
									img_urls.append('<img class="xui-uploadimg xa-uploadimg" id="uploadimg-%d" src="'%(index)+v+'">')
									index +=1
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

		excel_file_name = 'survey_statistic_'+datetime.now().strftime('%H_%M_%S')+'.xls'
		dir_path_suffix = '%d_%s' % (request.user.id, date.today())
		dir_path = os.path.join(settings.UPLOAD_DIR, dir_path_suffix)

		if not os.path.exists(dir_path):
			os.makedirs(dir_path)
		export_file_path = os.path.join(dir_path,excel_file_name)
		download_excel_file_name = u'用户调研统计.xls'

		#Excel Process Part
		try:
			import xlwt
			all_participances = surveyStatistics.get_survey_title_select_datas(request)
			#workbook/sheet
			wb = xlwt.Workbook(encoding='utf-8')

			#add_sheet
			if all_participances:
				ws_select = None
				ws_image = None
				ws_qa = None
				sheet_types = set()
				for participance in all_participances:
					if participance['type'] in ['appkit.selection','appkit.uploadimg','appkit.qa']:
						sheet_types.add(participance['type'])
					else:
						all_participances.remove(participance)
				if sheet_types:
					for sheet in sheet_types:
						if sheet == 'appkit.selection':
							ws_select = wb.add_sheet(u'选择题')
						elif sheet == 'appkit.uploadimg':
							ws_image = wb.add_sheet(u'上传图片')
						else:
							ws_qa = wb.add_sheet(u'问答题')
				select_num = image_num = qa_num = 0
				select_row = select_col = image_row = imge_col = qa_row = qa_col =0
				for participance in all_participances:
					if participance['type'] == 'appkit.selection':
						select_num += 1
						ws_select.write(select_row,select_col,'%d.'%select_num+participance['title']+u'(有效参与人数%d人)'% participance['title_valid_count'])
						is_top_tilte = False
						for data_value in participance['values']:
							if not is_top_tilte:
								ws_select.write(select_row,select_col+1,u'参与人数/百分百')
								is_top_tilte = True
							select_row += 1
							ws_select.write(select_row,select_col,data_value['name'])
							ws_select.write(select_row,select_col+1,'%d人/%s' % (data_value['count'],data_value['per']))
						select_row += 1
						ws_select.write(select_row,select_col,u'')
						ws_select.write(select_row,select_col+1,u'')
						select_row += 1
					elif participance['type'] == 'appkit.uploadimg':
						image_num += 1
						ws_image.write(image_row,imge_col,u'上传时间')
						is_top_tilte = False
						for data_value in participance['values']:
							if not is_top_tilte:
								ws_image.write(image_row,imge_col+1,participance['title']+u'(有效参与人数%d人)'% participance['title_valid_count'])
								is_top_tilte = True
							image_row += 1
							ws_image.write(image_row,imge_col,data_value['created_at'])
							for value in data_value['value']:
								ws_image.write(image_row,imge_col+1,value)
								image_row += 1
							image_row -= 1

						image_row += 1
						ws_image.write(image_row,imge_col,u'')
						ws_image.write(image_row,imge_col+1,u'')
						image_row += 1
					else:
						qa_num += 1
						ws_qa.write(qa_row,qa_col,u'提交时间')
						is_top_tilte = False
						for data_value in participance['values']:
							if not is_top_tilte:
								ws_qa.write(qa_row,qa_col+1,participance['title']+u'(有效参与人数%d人)'% participance['title_valid_count'])
								is_top_tilte = True
							qa_row += 1
							ws_qa.write(qa_row,qa_col,data_value['created_at'])
							ws_qa.write(qa_row,qa_col+1,data_value['value'])
						qa_row += 1
						ws_qa.write(qa_row,qa_col,u'')
						ws_qa.write(qa_row,qa_col+1,u'')
						qa_row += 1

			try:
				wb.save(export_file_path)
			except:
				print 'EXPORT EXCEL FILE SAVE ERROR'
				print '/static/upload/%s/%s'%(dir_path_suffix,excel_file_name)

			response = create_response(200)
			response.data = {'download_path':'/static/upload/%s/%s'%(dir_path_suffix,excel_file_name),'filename':download_excel_file_name,'code':200}
		except:
			response = create_response(500)

		return response.get_response()