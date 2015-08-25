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
							print a_v,"a_v"
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