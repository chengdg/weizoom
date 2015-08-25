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
import export
from datetime import datetime

FIRST_NAV = 'apps'
COUNT_PER_PAGE = 20
ITEM_FOR_DISPLAY = {
	'phone': u'手机',
	'name': u'姓名',
	'QQ': u'QQ'
}
TYPE_FOR_DISPLAY = {
	'0': u'服务',
	'1': u'功能',
	'2': u'操作',
	'3': u'新的需求',
	'4': u'其他'
}
class feedbacks(resource.Resource):
	app = 'apps/feedback'
	resource = 'feedbacks'
	
	@login_required
	def get(request):
		"""
		响应GET
		"""
		has_data = app_models.feedbackParticipance.objects.count()
		
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': "feedbacks",
			'has_data': has_data
		});
		
		return render_to_response('feedback/templates/editor/feedbacks.html', c)
	
	@staticmethod
	def get_datas(request):
		participant_name = request.GET.get('participant_name', '')
		feedback_type = int(request.GET.get('feedback_type', -1))
		start_time = request.GET.get('start_time', '')
		end_time = request.GET.get('end_time', '')
		phone = request.GET.get('phone', '')
		name = request.GET.get('name', '')
		qq = request.GET.get('qq', '')

		if participant_name:
			members = member_models.Member.get_by_username(participant_name)
		else:
			members = member_models.Member.get_members(request.user_profile.webapp_id)
		member_ids = [member.id for member in members]
		webapp_user_ids = [webapp_user.id for webapp_user in member_models.WebAppUser.objects.filter(member_id__in=member_ids)]
		if not webapp_user_ids:
			webapp_user_ids = [-1]
		else:
			webapp_user_ids = []

		params = {}
		params_id_length = 0 #在按照一个以上查找条件筛选时，会因为都是对id进行查找而造成BUG,
		# 所以对按照id查找的次数进行计数,如查找两个以上条件，只展示符合所有查找条件id的交集
		records = app_models.feedbackParticipance.objects.all()
		if webapp_user_ids:
			params['webapp_user_id__in'] = webapp_user_ids
		if feedback_type != -1:
			params_id_length += 1
			choosen_ids = []
			for record in records:
				for k, v in record.termite_data.items():
					if v['type'] == 'type':
						data_feedback_type = int(v['value'])
						if data_feedback_type == feedback_type:
							if params_id_length > 1:
								if record.id in params['id__in']:
									choosen_ids.append(record.id)
							else:
								choosen_ids.append(record.id)
			params['id__in'] = choosen_ids
		if start_time:
			params['created_at__gte'] = start_time
		if end_time:
			params['created_at__lte'] = end_time
		if phone:
			params_id_length += 1
			choosen_ids = []
			for record in records:
				for k, v in record.termite_data.items():
					pureName = k.split('_')[1]
					if pureName == 'phone':
						data_tel = v['value']
						if phone in data_tel:
							if params_id_length > 1:
								if record.id in params['id__in']:
									choosen_ids.append(record.id)
							else:
								choosen_ids.append(record.id)
			params['id__in'] = choosen_ids
		if name:
			params_id_length += 1
			choosen_ids = []
			for record in records:
				for k, v in record.termite_data.items():
					pureName = k.split('_')[1]
					if pureName == 'name':
						data_name = v['value']
						if name in data_name:
							if params_id_length > 1:
								if record.id in params['id__in']:
									choosen_ids.append(record.id)
							else:
								choosen_ids.append(record.id)
			params['id__in'] = choosen_ids
		if qq:
			params_id_length += 1
			choosen_ids = []
			for record in records:
				for k, v in record.termite_data.items():
					pureName = k.split('_')[1]
					if pureName == 'QQ':
						data_qq = v['value']
						if qq in data_qq:
							if params_id_length > 1:
								if record.id in params['id__in']:
									choosen_ids.append(record.id)
							else:
								choosen_ids.append(record.id)
			params['id__in'] = choosen_ids
		datas = app_models.feedbackParticipance.objects(**params).order_by('-id')

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
		pageinfo, datas = feedbacks.get_datas(request)

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
			item_informations_list = []
			feedback_type = ''
			feedback_content = ''
			feedback_participance = app_models.feedbackParticipance.objects.get(id=data.id)
			termite_data = feedback_participance.termite_data
			for k, v in termite_data.items():
				if v['type'] == 'appkit.qa':
					feedback_content = v['value']
				elif v['type'] == 'appkit.shortcuts':
					item_data = {}
					pureName = k.split('_')[1]
					item_data['item_name'] = ITEM_FOR_DISPLAY[pureName]
					item_data['item_value'] = v['value']
					item_informations_list.append(item_data)
				else:
					feedback_type = TYPE_FOR_DISPLAY[v['value']]
			items.append({
				'id': str(data.id),
				'participant_name': data.participant_name,
				'participant_icon': data.participant_icon,
				'informations': item_informations_list,
				'feedback_type': feedback_type,
				'feedback_content': feedback_content,
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

