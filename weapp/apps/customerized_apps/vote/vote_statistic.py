# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.conf import settings
from datetime import datetime
import os

from core import resource
from core.jsonresponse import create_response
import models as app_models
from mall import export

FIRST_NAV = export.MALL_PROMOTION_AND_APPS_FIRST_NAV
COUNT_PER_PAGE = 20

class voteStatistic(resource.Resource):
	app = 'apps/vote'
	resource = 'vote_statistic'
	
	@login_required
	def get(request):
		"""
		响应GET
		"""
		if 'id' in request.GET:
			all_participances = app_models.voteParticipance.objects(belong_to=request.GET['id'])
			total_count = all_participances.count()
			titles_list = []
			title2itemCount = {}
			title_valid_dict = {}
			total_title_valid_dict ={}
			title_type_dict = {}
			for p in all_participances:
				for title, data in p.termite_data.items():
					title_type = u''
					if data['type'] == 'appkit.selection':
						is_valid = False
						for item, value in data['value'].items():
							if value['isSelect']:
								is_valid = True
								if total_title_valid_dict.has_key(title):
									total_title_valid_dict[title] += 1
								else:
									total_title_valid_dict[title] = 1
							if title2itemCount.has_key(title):
								if title2itemCount[title].has_key(item):
									title2itemCount[title][item] += 1 if value['isSelect'] else 0
								else:
									title2itemCount[title][item] = 1 if value['isSelect'] else 0
							else:
								title2itemCount[title] = {}
								title2itemCount[title][item] = 1 if value['isSelect'] else 0
							title_type = value['type']
						if is_valid:
							if title_valid_dict.has_key(title):
								title_valid_dict[title] += 1
							else:
								title_valid_dict[title] = 1
						title_type_dict[title] = title_type

			for title in sorted(title2itemCount.keys()):
				print title,"title"
				single_title_dict = {}
				single_title_dict['title_name'] = title.split('_')[1]
				single_title_dict['title_valid_count'] = title_valid_dict[title]
				single_title_dict['type'] = u'单选' if title_type_dict[title] == 'radio' else u'多选'
				single_title_dict['title_value'] = []
				for item in sorted(title2itemCount[title].keys()):
					item_value = title2itemCount[title][item]
					single_item_value = {}
					single_item_value['item_name'] = item.split('_')[1]
					single_item_value['counter'] = item_value
					single_item_value['percent'] = '%d%s' % (item_value / float(total_title_valid_dict[title]) * 100, '%')
					single_title_dict['title_value'].append(single_item_value)

				titles_list.append(single_title_dict)

			project_id = 'new_app:vote:%s' % request.GET.get('related_page_id', 0)
		else:
			total_count = 0
			titles_list = None
			project_id = 'new_app:vote:0'
		
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_promotion_and_apps_second_navs(request),
			'second_nav_name': export.MALL_APPS_SECOND_NAV,
			'third_nav_name': export.MALL_APPS_VOTE_NAV,
			'titles': titles_list,
			'total_count': total_count,
			'project_id': project_id,
		})
		
		return render_to_response('vote/templates/editor/vote_statistic.html', c)

class voteStatistic_Export(resource.Resource):
	'''
	批量导出
	'''
	app = 'apps/vote'
	resource = 'vote_statistic-export'

	@login_required
	def api_get(request):
		"""
		不同类型分页统计
		"""
		export_id = request.GET.get('export_id')
		trans2zh = {u'phone':u'手机',u'email':u'邮箱',u'name':u'姓名',u'tel':u'电话'}

		# app_name = voteStatistic_Export.app
		# excel_file_name = ('%s_id%s_%s.xls') % (app_name.split("/")[1],export_id,datetime.now().strftime('%Y%m%d%H%m%M%S'))
		excel_file_name = 'vote_statistic.xls'
		download_excel_file_name = u'微信投票统计.xls'
		export_file_path = os.path.join(settings.UPLOAD_DIR,excel_file_name)

		#Excel Process Part
		try:
			import xlwt
			data = app_models.voteParticipance.objects(belong_to=export_id)
			total = data.count()
			member_id2termite_data={}
			for item in data:
				if item['member_id'] not in member_id2termite_data:
					member_id2termite_data[item['member_id']] = {'created_at':item['created_at'],'termite_data':item['termite_data']}

			#select sheet
			select_data = {}
			select_static ={}
			qa_static = {}
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
			#select-data-processing
			for select in select_data:
				for s_list in select_data[select]:
					for s in s_list:
						if select not in select_static:
							select_static[select]={}
						if s not in select_static[select]:
							select_static[select][s]  = 0
						if s_list[s]['isSelect'] == True:
							select_static[select][s] += 1
					print s_list
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
					all_select_num = 0
					s_i_num = 0
					for s_i in select_static[s]:
						s_num = select_static[s][s_i]
						if s_num :
							all_select_num += s_num
					for s_i in select_static[s]:
						s_num = select_static[s][s_i]
						ws.write(row,col,s_i.split('_')[1])
						per = s_num*1.0/all_select_num*100
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