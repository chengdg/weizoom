# -*- coding: utf-8 -*-

import json
import random
from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.conf import settings

from core import resource
from core import paginator
from core import emotion
from core.jsonresponse import create_response
from utils.cache_util import delete_cache
from weixin2.models import News
import models as app_models
import export
from apps import request_util
from mall import export as mall_export
from modules.member import integral as integral_api
import termite.pagestore as pagestore_manager
from core.wxapi import get_weixin_api
from account.util import get_binding_weixin_mpuser, get_mpuser_accesstoken
from core.wxapi.api_create_qrcode_ticket import QrcodeTicket

FIRST_NAV = mall_export.MALL_PROMOTION_AND_APPS_FIRST_NAV
COUNT_PER_PAGE = 20

class RedPacket(resource.Resource):
	app = 'apps/rebate'
	resource = 'rebate'
	
	@login_required
	def get(request):
		"""
		响应GET
		"""
		rebate = None
		if 'id' in request.GET:
			try:
				rebate = app_models.Rebate.objects.get(id=request.GET['id'])
			except:
				c = RequestContext(request, {
					'first_nav_name': FIRST_NAV,
					'second_navs': mall_export.get_promotion_and_apps_second_navs(request),
					'second_nav_name': mall_export.MALL_APPS_SECOND_NAV,
					'third_nav_name': mall_export.MALL_APPS_REBATE_NAV,
					'is_deleted_data': True,
				})
				return render_to_response('rebate/templates/editor/create_rebate_rule.html', c)
			answer_content = {}
			if int(rebate.reply_material_id) > 0:
				answer_content['type'] = 'news'
				answer_content['newses'] = []
				answer_content['content'] = rebate.reply_material_id
				newses = News.get_news_by_material_id(rebate.reply_material_id)

				for news in newses:
					news_dict = {}
					news_dict['id'] = news.id
					news_dict['title'] = news.title
					answer_content['newses'].append(news_dict)
			else:
				answer_content['type'] = 'text'
				answer_content['content'] = emotion.change_emotion_to_img(rebate.reply_detail)
			jsons = [{
				"name": "qrcode_answer",
				"content": answer_content
			}]
			c = RequestContext(request, {
				'first_nav_name': FIRST_NAV,
				'second_navs': mall_export.get_promotion_and_apps_second_navs(request),
				'second_nav_name': mall_export.MALL_APPS_SECOND_NAV,
				'third_nav_name': mall_export.MALL_APPS_REBATE_NAV,
				'rebate_rule': rebate,
				'jsons': jsons
			})
			return render_to_response('rebate/templates/editor/create_rebate_rule.html', c)
		else:
			c = RequestContext(request, {
				'first_nav_name': FIRST_NAV,
				'second_navs': mall_export.get_promotion_and_apps_second_navs(request),
				'second_nav_name': mall_export.MALL_APPS_SECOND_NAV,
				'third_nav_name': mall_export.MALL_APPS_REBATE_NAV,
				'rebate_rule': rebate
			})
			return render_to_response('rebate/templates/editor/create_rebate_rule.html', c)
	
	@login_required
	def api_put(request):
		"""
		响应PUT
		"""
		data = request_util.get_fields_to_be_save(request)
		data['permission'] = True if data['permission']=='1' else False
		data['is_limit_first_buy'] = True if data['is_limit_first_buy']=='1' else False
		data['is_limit_cash'] = True if data['is_limit_cash']=='1' else False
		rebate = app_models.Rebate(**data)
		rebate.save()

		error_msg = None
		data = json.loads(rebate.to_json())
		data['id'] = data['_id']['$oid']

		if error_msg:
			data['error_msg'] = error_msg

		if settings.MODE != 'develop':
			mp_user = get_binding_weixin_mpuser(request.manager)
			mpuser_access_token = get_mpuser_accesstoken(mp_user)
			weixin_api = get_weixin_api(mpuser_access_token)
			try:
				qrcode_ticket = weixin_api.create_qrcode_ticket(data['id'], QrcodeTicket.PERMANENT)
				ticket = qrcode_ticket.ticket
			except Exception, e:
				print 'get qrcode_ticket fail:', e
				ticket = ''
		else:
			ticket = ''
		rebate.ticket = ticket
		rebate.save()
		response = create_response(200)
		response.data = data
		return response.get_response()
	
	@login_required
	def api_post(request):
		"""
		响应POST
		"""
		data = request_util.get_fields_to_be_save(request)
		data['permission'] = True if data['permission']=='1' else False
		data['is_limit_first_buy'] = True if data['is_limit_first_buy']=='1' else False
		data['is_limit_cash'] = True if data['is_limit_cash']=='1' else False

		update_data = {}
		update_fields = set(['name', 'start_time', 'end_time', 'permission', 'is_limit_first_buy', 'is_limit_cash', 'rebate_order_price', 'rebate_money', 'weizoom_card_id_from', 'weizoom_card_id_to', 'reply_type', 'reply_detail', 'reply_material_id'])
		for key, value in data.items():
			if key in update_fields:
				update_data['set__'+key] = value

		app_models.Rebate.objects(id=request.POST['id']).update(**update_data)

		#更新后清除缓存
		# cache_key = 'apps_rebate_%s_html' % request.POST['id']
		# delete_cache(cache_key)
		response = create_response(200)
		return response.get_response()
	
	@login_required
	def api_delete(request):
		"""
		响应DELETE
		"""
		app_models.Rebate.objects(id=request.POST['id']).delete()
		
		response = create_response(200)
		return response.get_response()
