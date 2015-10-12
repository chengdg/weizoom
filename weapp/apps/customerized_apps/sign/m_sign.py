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
		p_id = request.GET['id']
		member = request.member
		isPC = request.GET.get('isPC',0)
		isMember = member and member.status == 1
		webapp_owner_id = request.GET.get('webapp_owner_id', None)
		participance_data_count = 0
		auth_appid_info = None
		if 'new_app' in p_id:
			project_id = p_id
			activity_status = u"未开始"
			record_id = 0
			member_info = {}
			prize_info = {}
			record = None
		else:
			record = app_models.Sign.objects(owner_id=webapp_owner_id)
			if record.count() > 0:
				record = record[0]
				member_info = {
					'user_name': member.username_for_html if member and member.username_for_html else u'未知',
					'user_icon': member.user_icon if member and member.user_icon else '/static/img/user-1.jpg',
					'user_integral': member.integral if member else 0
				}
				prize_settings = record.prize_settings

				if not isPC:
					if not isMember:
						from weixin.user.util import get_component_info_from
						component_info = get_component_info_from(request)
						auth_appid = weixin_models.ComponentAuthedAppid.objects.filter(component_info=component_info, user_id=webapp_owner_id)[0]
						auth_appid_info = weixin_models.ComponentAuthedAppidInfo.objects.filter(auth_appid=auth_appid)[0]

				activity_status = record.status_text

				project_id = 'new_app:sign:%s' % record.related_page_id
				record_id = record.id
				signers = app_models.SignParticipance.objects(belong_to=str(record_id), member_id=member.id)
				participance_data_count = signers.count()
				signer = signers[0] if participance_data_count>0 else None
				#检查当前用户签到情况
				daily_prize = prize_settings['0']
				serial_prize = {}
				next_serial_prize = {}
				serial_integral = {}
				if signer:
					#检查是否已签到
					latest_sign_date = signer.latest_date.strftime('%Y-%m-%d')
					nowDate = datetime.now().strftime('%Y-%m-%d')
					if latest_sign_date == nowDate:
						activity_status = u'已签到'
						for name in sorted(prize_settings.keys()):
							setting = prize_settings[name]
							if int(name) > signer.serial_count:
								next_serial_prize = {
									'count': name,
									'prize': setting
								}
								break
					elif signer.serial_count >1:
						flag = False
						for name in sorted(prize_settings.keys()):
							setting = prize_settings[name]
							if flag or int(name)>signer.serial_count + 1:
								next_serial_prize = {
									'count': name,
									'prize': setting
								}
								break
							if int(name) == signer.serial_count + 1:
								serial_prize = {
									'count': name,
									'prize':setting
								}
								flag = True
					for name in sorted(prize_settings.keys()):
						setting = prize_settings[name]
						serial_integral[name]=setting['integral']

				prize_info = {
					'serial_count': signer.serial_count if signer else 0,
					'daily_prize': daily_prize,
					'serial_prize': serial_prize,
					'next_serial_prize': next_serial_prize,
					'serial_integral':serial_integral
				}
			else:
				c = RequestContext(request, {
					'is_deleted_data': True
				})
				return render_to_response('sign/templates/webapp/m_sign.html', c)

		request.GET._mutable = True
		request.GET.update({"project_id": project_id})
		request.GET._mutable = False
		html = pagecreater.create_page(request, return_html_snippet=True)
		c = RequestContext(request, {
			'record_id': record_id,
			'activity_status': activity_status,
			'is_already_participanted': (participance_data_count > 0),
			'page_title': u"签到",
			'page_html_content': html,
			'app_name': "sign",
			'resource': "sign",
			'hide_non_member_cover': True, #非会员也可使用该页面
			'isPC': isPC,
			'isMember': isMember,
			'member_info':json.dumps(member_info),
			'prize_info': json.dumps(prize_info),
			'auth_appid_info': auth_appid_info,
			'share_img_url': record.share['img'] if record else '',
			'share_page_desc': record.share['desc'] if record else ''

		})
		return render_to_response('sign/templates/webapp/m_sign.html', c)