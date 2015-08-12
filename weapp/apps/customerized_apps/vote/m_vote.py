# -*- coding: utf-8 -*-
from collections import OrderedDict

import json
from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required

from core import resource
from core import paginator
from core.jsonresponse import create_response

import models as app_models
import export
from apps import request_util
from termite2 import pagecreater
from termite import pagestore as pagestore_manager

class Mvote(resource.Resource):
	app = 'apps/vote'
	resource = 'm_vote'
	
	def get(request):
		"""
		响应GET
		"""
		if 'id' in request.GET:
			id = request.GET['id']
			participance_data_count = 0
			if 'new_app:' in id:
				project_id = id
				activity_status = u"未开启"
			else:
				#termite类型数据
				record = app_models.vote.objects.get(id=id)
				activity_status = record.status_text
				project_id = 'new_app:vote:%s' % record.related_page_id

				if request.member:
					participance_data_count = app_models.voteParticipance.objects(belong_to=id, member_id=request.member.id).count()
				if participance_data_count == 0 and request.webapp_user:
					participance_data_count = app_models.voteParticipance.objects(belong_to=id, webapp_user_id=request.webapp_user.id).count()
			
			request.GET._mutable = True
			request.GET.update({"project_id": project_id})
			request.GET._mutable = False
			html = pagecreater.create_page(request, return_html_snippet=True)

			
			c = RequestContext(request, {
				'record_id': id,
				'activity_status': activity_status,
				'is_already_participanted': (participance_data_count > 0),
				'page_title': '用户调研',
				'page_html_content': html,
				'app_name': "vote",
				'resource': "vote",
				'hide_non_member_cover': True #非会员也可使用该页面
			})
			# vote/templates/webapp/result_vote.html
			# workbench/wepage_webapp_page.html
			return render_to_response('workbench/wepage_webapp_page.html', c)
		else:
			record = None
			c = RequestContext(request, {
				'record': record
			});
			
			return render_to_response('vote/templates/webapp/m_vote.html', c)


class resultVote(resource.Resource):
	app = 'apps/vote'
	resource = 'result_vote'

	def get(request):
		print request.GET
		if 'id' in request.GET:
			id = request.GET['id']
			vote_detail ={}

			vote_vote = app_models.vote.objects.get(id=id)
			vote_detail['name'] = vote_vote['name']
			vote_detail['start_time'] = vote_vote['start_time'].strftime('%Y-%m-%d %H:%M')
			vote_detail['end_time'] = vote_vote['end_time'].strftime('%Y-%m-%d %H:%M')

			votes = app_models.voteParticipance.objects(belong_to=id)
			q_vote ={}
			result_list = []

			for vote in votes:
				for k,v in vote.termite_data.items():
					if v['type'] != 'appkit.shortcuts':
						if not q_vote.has_key(k):
							q_vote[k] = [v['value']]
						else:
							q_vote[k].append(v['value'])

			for k,v in q_vote.items():
				a_isSelect = {}
				result = {}
				total_count = len(v)
				value_list = []

				v_a = {}
				for a in v:
					v_a = a.items()
					for a_k,a_v in a.items():
						if not a_isSelect.has_key(a_k):
							a_isSelect[a_k] = 0/total_count
						if a_v['isSelect'] == True:
							a_isSelect[a_k] += 1*100/float(total_count)
				for a_k,a_v in reversed(v_a):
					value ={}
					value['name'] = a_k
					value['per'] =  a_isSelect[a_k]
					value_list.append(value)
				result['title'] = k
				result['values'] = value_list
				result_list.append(result)

			record = app_models.vote.objects.get(id=id)
			related_page_id = record.related_page_id
			activity_status = record.status_text

			pagestore = pagestore_manager.get_pagestore('mongo')
			page = pagestore.get_page(related_page_id, 1)
			page_info = page['component']['components'][0]['model']
			vote_detail['subtitle'] = page_info['subtitle']
			vote_detail['description'] = page_info['description']
			vote_detail['prize_type'] = page_info['prize']['type']
			vote_detail['prize_data'] = page_info['prize']['data']
			c = RequestContext(request, {
				'vote_detail': vote_detail,
				'record_id': id,
				'activity_status': activity_status,
				'page_title': '用户调研',
				'app_name': "vote",
				'resource': "vote",
				'q_vote': result_list,
				'hide_non_member_cover': True #非会员也可使用该页面
			})
			return render_to_response('vote/templates/webapp/result_vote.html', c)