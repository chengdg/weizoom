# -*- coding: utf-8 -*-

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
import weixin.user.models as weixin_models

class MSign(resource.Resource):
	app = 'apps/sign'
	resource = 'm_sign'
	
	def get(request):
		"""
		响应GET
		"""
		member = request.member
		isMember = member and member.is_subscribed
		webapp_owner_id = request.user.id
		record = app_models.Sign.objects(owner_id=webapp_owner_id)
		isPC = request.GET.get('isPC',0)
		if record.count() > 0:
			record = record[0]
			member_info = {
				'user_name': u'未知',
				'user_icon': '/static/img/user-1.jpg'
			}
			auth_appid_info = None
			participance_data_count = 0
			if not isPC:
				if not isMember:
					from weixin.user.util import get_component_info_from
					component_info = get_component_info_from(request)
					auth_appid = weixin_models.ComponentAuthedAppid.objects.filter(component_info=component_info, user_id=webapp_owner_id)[0]
					auth_appid_info = weixin_models.ComponentAuthedAppidInfo.objects.filter(auth_appid=auth_appid)[0]
				else:
					member_info = {
						'user_name': member.username_for_html,
						'user_icon': member.user_icon
					}
			activity_status = record.status_text

			project_id = 'new_app:sign:%s' % record.related_page_id
			id = record.id

			if member:
				participance_data_count = app_models.SignParticipance.objects(belong_to=id, member_id=member.id).count()
			if participance_data_count == 0 and request.webapp_user:
				participance_data_count = app_models.SignParticipance.objects(belong_to=id, webapp_user_id=request.webapp_user.id).count()

			request.GET._mutable = True
			request.GET.update({"project_id": project_id})
			request.GET._mutable = False
			html = pagecreater.create_page(request, return_html_snippet=True)

			c = RequestContext(request, {
				'record_id': id,
				'activity_status': activity_status,
				'is_already_participanted': (participance_data_count > 0),
				'page_title': "签到",
				'page_html_content': html,
				'app_name': "sign",
				'resource': "sign",
				'hide_non_member_cover': True, #非会员也可使用该页面
				'isPC': isPC,
				'isMember': isMember,
				'member_info':member_info,
				'auth_appid_info': auth_appid_info
			})
		else:
			c = RequestContext(request, {
				'is_deleted_data': True
			})

		return render_to_response('sign/templates/webapp/m_sign.html', c)

		# if 'id' in request.GET:
		# 	id = request.GET['id']
		# 	isPC = request.GET.get('isPC',0)
		# 	participance_data_count = 0
		# 	isMember = False
		# 	auth_appid_info = None
		# 	member_info = {
		# 		'user_name': u'未知',
		# 		'user_icon': '/static/img/user-1.jpg'
		# 	}
		# 	member = request.member
		# 	if not isPC:
		# 		isMember = member and member.is_subscribed
		# 		if not isMember:
		# 			from weixin.user.util import get_component_info_from
		# 			component_info = get_component_info_from(request)
		# 			auth_appid = weixin_models.ComponentAuthedAppid.objects.filter(component_info=component_info, user_id=request.user.id)[0]
		# 			auth_appid_info = weixin_models.ComponentAuthedAppidInfo.objects.filter(auth_appid=auth_appid)[0]
		# 		else:
		# 			member_info = {
		# 				'user_name': member.username_for_html,
		# 				'user_icon': member.user_icon
		# 			}
		# 	if 'new_app:' in id:
		# 		project_id = id
		# 		activity_status = u"未开启"
		# 	else:
		# 		#termite类型数据
		# 		record = app_models.Sign.objects.get(id=id)
		# 		activity_status = record.status_text
		#
		# 		project_id = 'new_app:sign:%s' % record.related_page_id
		#
		# 		if member:
		# 			participance_data_count = app_models.SignParticipance.objects(belong_to=id, member_id=member.id).count()
		# 		if participance_data_count == 0 and request.webapp_user:
		# 			participance_data_count = app_models.SignParticipance.objects(belong_to=id, webapp_user_id=request.webapp_user.id).count()
        #
		# 	request.GET._mutable = True
		# 	request.GET.update({"project_id": project_id})
		# 	request.GET._mutable = False
		# 	html = pagecreater.create_page(request, return_html_snippet=True)
		#
		# 	c = RequestContext(request, {
		# 		'record_id': id,
		# 		'activity_status': activity_status,
		# 		'is_already_participanted': (participance_data_count > 0),
		# 		'page_title': "签到",
		# 		'page_html_content': html,
		# 		'app_name': "sign",
		# 		'resource': "sign",
		# 		'hide_non_member_cover': True, #非会员也可使用该页面
		# 		'isPC': isPC,
		# 		'isMember': isMember,
		# 		'member_info':member_info,
		# 		'auth_appid_info': auth_appid_info
		# 	})
		#
		# 	return render_to_response('sign/templates/webapp/m_sign.html', c)
		# else:
		# 	record = None
		# 	c = RequestContext(request, {
		# 		'record': record
		# 	});
		#
		# 	return render_to_response('sign/templates/webapp/m_sign.html', c)

