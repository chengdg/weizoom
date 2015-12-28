# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.conf import settings
from datetime import datetime, date
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
			all_vote_participances = app_models.voteParticipance.objects(belong_to=request.GET['id'])
			total_count = all_vote_participances.count()
			titles_list = get_vote_title_select_datas(request)
			for data in titles_list:
				data['title_name'] = data['title_name'].split('_')[1]
				data_values = data['title_value']
				for data_value in data_values:
					data_value['item_name'] = data_value['item_name'].split('_')[1]


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
		export_id = request.GET.get('id')
		trans2zh = {u'phone':u'手机',u'email':u'邮箱',u'name':u'姓名',u'tel':u'电话'}

		# app_name = voteStatistic_Export.app
		# excel_file_name = ('%s_id%s_%s.xls') % (app_name.split("/")[1],export_id,datetime.now().strftime('%Y%m%d%H%m%M%S'))

		excel_file_name = 'vote_statistic_'+datetime.now().strftime('%H_%M_%S')+'.xls'
		dir_path_suffix = '%d_%s' % (request.user.id, date.today())
		dir_path = os.path.join(settings.UPLOAD_DIR, dir_path_suffix)

		if not os.path.exists(dir_path):
			os.makedirs(dir_path)
		export_file_path = os.path.join(dir_path,excel_file_name)
		download_excel_file_name = u'微信投票统计.xls'

		#Excel Process Part
		try:
			import xlwt
			titles_list = get_vote_title_select_datas(request)
			for data in titles_list:
				data['title_name'] = data['title_name'].split('_')[1]
				data_values = data['title_value']
				for data_value in data_values:
					data_value['item_name'] = data_value['item_name'].split('_')[1]

			wb = xlwt.Workbook(encoding='utf-8')
			select_num = 0
			row = col =0
			ws = wb.add_sheet(u'选择题')
			for data in titles_list:
				select_num += 1
				ws.write(row,col,'%d.'%select_num+data['title_name']+u'(有效参与人数%d人)'% data['title_valid_count'])
				is_top_tilte = False
				for data_value in data['title_value']:
					if not is_top_tilte:
						if data_value.has_key('image'):
							ws.write(row,col+1,u'选项图片')
							ws.write(row,col+2,u'参与人数/百分百')
						else:
							ws.write(row,col+1,u'参与人数/百分百')
						is_top_tilte = True
					row += 1
					ws.write(row,col,data_value['item_name'])
					if data_value.has_key('image'):
						ws.write(row,col+1,data_value['image'])
						ws.write(row,col+2,'%d人/%s' % (data_value['counter'],data_value['percent']))
					else:
						ws.write(row,col+1,'%d人/%s' % (data_value['counter'],data_value['percent']))
				row += 1
				ws.write(row,col,u'')
				ws.write(row,col+1,u'')
				row += 1
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


def get_vote_title_select_datas(request):
	'''
	投票数据例如：
	{
	"_id" : ObjectId("567b5134ed8d712214296cb2"),
	"webapp_user_id" : NumberLong(2),
	"member_id" : NumberLong(2),
	"belong_to" : "567a75d2ed8d711854c0be10",
	"tel" : "",
	"termite_data" : {
		"04_name" : {"type" : "appkit.textlist","value" : "asdaasdad"},
		"01_单选的i哦" : {"type" : "appkit.imageselection","display_type" : "list","value" : {
				"00_1" : {"isSelect" : false,"mt" : "15px","image" : "/static/upload/13_20151218/1450426957004_630.jpg","type" : "radio"},
				"01_1" : {"isSelect" : false,"mt" : "15px","image" : "/static/upload/13_20151218/1450426935062_309.jpg","type" : "radio"},
				"02_1" : {"isSelect" : true,"mt" : "15px","image" : "/static/upload/13_20151218/145042695002_639.jpg","type" : "radio"}}},
		"05_phone" : {"type" : "appkit.textlist","value" : "15896321478"},
		"00_asd" : {"type" : "appkit.selection","display_type" : "","value" : {
				"00_1" : {"isSelect" : false,"type" : "radio"},
				"01_2" : {"isSelect" : false,"type" : "radio"},
				"06_3" : {"isSelect" : true,"type" : "radio"}}},
		"02_多选的哦" : {"type" : "appkit.imageselection","display_type" : "table","value" : {
				"01_2" : {"isSelect" : false,"mt" : "0px","image" : "/static/upload/13_20151218/145042695002_639.jpg","type" : "checkbox"},
				"00_2" : {"isSelect" : false,"mt" : "0px","image" : "/static/upload/13_20151218/1450426935062_309.jpg","type" : "checkbox"},
				"02_2" : {"isSelect" : true,"mt" : "0px","image" : "/static/upload/13_20151218/1450426982081_980.jpg","type" : "checkbox"}}}},
	"prize" : {"type" : "no_prize","data" : null},
	"created_at" : ISODate("2015-12-24T09:58:12.907Z")}
	@param request: request参数
	变量名：
		all_vote_participances: 所有投票数据
		all_title_select_list: 所有标题-选项及对应百分比信息
		title: 标题
		select_data_value: 某个标题下的所有选项信息
		select_title: 每个选项的标题
		value: 每个选项是否被选中及其他信息
	@return: all_title_select_list
	'''
	all_vote_participances = app_models.voteParticipance.objects(belong_to=request.GET['id'])
	all_title_select_list = []
	select_title2itemCount = {}
	title_valid_dict = {}
	total_title_valid_dict ={}
	title_type_dict = {}
	title_image_dict = {}
	title_disp_type = {}
	member_dict = {}
	for p in all_vote_participances:
		for title, select_datas in p.termite_data.items():
			title_type = u''
			if select_datas['type'] in ['appkit.selection', 'appkit.imageselection', 'appkit.textselection']:
				is_Select = False
				select_data_value = select_datas['value']
				select_title_index = 0
				for select_title in sorted(select_data_value.keys()):
					value = select_data_value[select_title]
					select_title = select_title.split('_')[1]
					if len(str(select_title_index))< 2:
						select_title = '0%s_%s' % (str(select_title_index), select_title)
					else:
						select_title = '%s_%s' % (str(select_title_index),select_title)
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
					if value.has_key('image'):
						title_image_dict[title+select_title] = value['image']
					title_type = value['type']
					member_dict[title+select_title] = p.member_id
					select_title_index += 1
				if select_datas.has_key('display_type'):
					title_disp_type[title] = select_datas['display_type']
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
				title_type_dict[title] = title_type

	for title in sorted(select_title2itemCount.keys()):
		single_title_dict = {}
		single_title_dict['title_name'] = title
		single_title_dict['title_valid_count'] = title_valid_dict[title]
		single_title_dict['type'] = u'单选' if title_type_dict[title] == 'radio' else u'多选'
		single_title_dict['display_type'] = single_title_dict['display_type'] = title_disp_type.get(title,None)
		single_title_dict['title_value'] = []
		for select_title in sorted(select_title2itemCount[title].keys()):
			item_value = select_title2itemCount[title][select_title]
			single_item_value = {}
			single_item_value['member_id'] = member_dict[title+select_title]
			single_item_value['item_name'] = select_title
			single_item_value['counter'] = item_value
			if title_image_dict.has_key(title+select_title):
				single_item_value['image'] = title_image_dict[title+select_title]
			single_item_value['percent'] = '%d%s' % (item_value / float(total_title_valid_dict[title]) * 100 if total_title_valid_dict[title] else 0, '%')
			single_title_dict['title_value'].append(single_item_value)

		all_title_select_list.append(single_title_dict)
	return  all_title_select_list