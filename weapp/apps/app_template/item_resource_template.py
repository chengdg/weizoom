# -*- coding: utf-8 -*-
__STRIPPER_TAG__
import json
from datetime import datetime

__STRIPPER_TAG__
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required

__STRIPPER_TAG__
from core import resource
from core import paginator
from core.jsonresponse import create_response

__STRIPPER_TAG__
import models as app_models
import export
from apps import request_util
from modules.member import integral as integral_api
from mall.promotion import utils as mall_api

__STRIPPER_TAG__
FIRST_NAV = 'apps'
COUNT_PER_PAGE = 20
__STRIPPER_TAG__
class {{resource.class_name}}(resource.Resource):
	app = 'apps/{{app_name}}'
	resource = '{{resource.lower_name}}'

	{% if resource.actions.get %}
	__STRIPPER_TAG__
	@login_required
	def get(request):
		"""
		响应GET
		"""
		if 'id' in request.GET:
			{{resource.lower_name}} = app_models.{{resource.class_name}}.objects.get(id=request.GET['id'])
			{% if resource.enable_termite %}
			is_create_new_data = False
			project_id = 'new_app:{{app_name}}:%s' % request.GET.get('related_page_id', 0)
			{% endif %}
		else:
			{{resource.lower_name}} = None
			{% if resource.enable_termite %}
			is_create_new_data = True
			project_id = 'new_app:{{app_name}}:0'
			{% endif %}
		__STRIPPER_TAG__
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': '{{resource.plural_name}}',
			'{{resource.lower_name}}': {{resource.lower_name}},
			{% if resource.enable_termite %}
			'is_create_new_data': is_create_new_data,
			'project_id': project_id,
			{% endif %}
		});
		__STRIPPER_TAG__
		{% if resource.enable_termite %}
		return render_to_response('{{app_name}}/templates/editor/workbench.html', c)
		{% else %}
		return render_to_response('{{app_name}}/templates/editor/{{resource.lower_name}}.html', c)
		{% endif %}
	{% endif %}

	{% if resource.actions.api_get %}
	__STRIPPER_TAG__
	@login_required
	def api_get(request):
		"""
		响应GET api
		"""
		if 'id' in request.GET:
			{{resource.lower_name}} = app_models.{{resource.class_name}}.objects.get(id=request.GET['id'])
			data = {{resource.lower_name}}.to_json()
		else:
			data = {}

		response = create_response(200)
		response.data = data
		return response.get_response()
	{% endif %} 

	{% if resource.actions.api_put %}
	__STRIPPER_TAG__
	{% if not resource.is_participance %}
	@login_required
	{% endif %}
	def api_put(request):
		"""
		响应PUT
		"""
		data = request_util.get_fields_to_be_save(request)
		{{resource.lower_name}} = app_models.{{resource.class_name}}(**data)
		{{resource.lower_name}}.save()
		{% if resource.is_participance %}
		__STRIPPER_TAG__
		#调整参与数量
		app_models.{{resource.item_class_name}}.objects(id=data['belong_to']).update(**{"inc__participant_count":1})
		__STRIPPER_TAG__
		#活动奖励
		prize = data.get('prize', None)
		error_msg = None
		if prize:
			prize_type = prize['type']
			if prize_type == 'no_prize':
				pass #不进行奖励
			elif prize_type == 'integral':
				if not request.member:
					pass #非会员，不进行积分奖励
				else:
					value = int(prize['data'])
					integral_api.increase_member_integral(request.member, value, u'参与活动奖励积分')
			elif prize_type == 'coupon':
				if not request.member:
					pass #非会员，不进行优惠券发放
				else:
					coupon_rule_id = int(prize['data']['id'])
					coupon, msg = mall_api.consume_coupon(request.webapp_owner_id, coupon_rule_id, request.member.id)
					if not coupon:
						error_msg = msg
		{% endif %}
		__STRIPPER_TAG__
		data = json.loads({{resource.lower_name}}.to_json())
		data['id'] = data['_id']['$oid']
		if error_msg:
			data['error_msg'] = error_msg
		response = create_response(200)
		response.data = data
		return response.get_response()
	{% endif %}

	{% if resource.actions.api_post %}
	__STRIPPER_TAG__
	@login_required
	def api_post(request):
		"""
		响应POST
		"""
		data = request_util.get_fields_to_be_save(request)
		update_data = {}
		update_fields = set(['name', 'start_time', 'end_time'])
		for key, value in data.items():
			if key in update_fields:
				update_data['set__'+key] = value
		
		app_models.{{resource.class_name}}.objects(id=request.POST['id']).update(**update_data)
		__STRIPPER_TAG__
		response = create_response(200)
		return response.get_response()
	{% endif %}

	{% if resource.actions.api_delete %}
	__STRIPPER_TAG__
	@login_required
	def api_delete(request):
		"""
		响应DELETE
		"""
		app_models.{{resource.class_name}}.objects(id=request.POST['id']).delete()
		__STRIPPER_TAG__
		response = create_response(200)
		return response.get_response()
	{% endif %}
