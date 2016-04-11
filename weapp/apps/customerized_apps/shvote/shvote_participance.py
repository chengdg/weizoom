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
from modules.member import integral as integral_api
from mall.promotion import utils as mall_api
from mall import export as mall_export
import termite.pagestore as pagestore_manager
from core.exceptionutil import unicode_full_stack

FIRST_NAV = mall_export.MALL_PROMOTION_AND_APPS_FIRST_NAV
COUNT_PER_PAGE = 20

class ShvoteParticipance(resource.Resource):
	app = 'apps/shvote'
	resource = 'shvote_participance'



	def get(request):
		"""
		响应GET
		"""
		record = None

		def __itemName2item(itemName):
			itemName_dic={'small':u"初中组"}
			itemName_List = []
			for item in itemName:
				if item in itemName_dic:
					itemName_List.append(itemName_dic[item])
				else:
					itemName_List.append(item)
			return itemName_List

		if 'id' in request.GET:
			participance_data_count = 0
			id = request.GET['id']
			try:
				record = app_models.Shvote.objects.get(id=id)
				if request.member:
					participance_data_count = app_models.ShvoteParticipance.objects(belong_to=id, member_id=request.member.id).count()
			except:
				c = RequestContext(request,{
					'is_deleted_data': True
				})
				return render_to_response('shvote/templates/webapp/m_shvote.html', c)
			c = RequestContext(request, {
				'record_id': id,
				'page_title': record.name if record else u"投票",
				'groups': __itemName2item(record.groups),
				'is_already_participanted': (participance_data_count > 0),
				'is_hide_weixin_option_menu':True,
				'app_name': "shvote",
				'resource': "shvote",
				'hide_non_member_cover': True, #非会员也可使用该页面
				'share_to_timeline_use_desc': True  #分享到朋友圈的时候信息变成分享给朋友的描述
			})
			return render_to_response('shvote/templates/webapp/m_shvote_participance.html', c)
		else:
			c = RequestContext(request, {
				'record': record
			})
			return render_to_response('shvote/templates/webapp/m_shvote.html', c)
	
	def api_put(request):
		"""
		响应PUT
		"""
		try:
			result_list = []
			member_id = request.member.id
			id = request.POST['belong_to']
			termite_data = json.loads(request.POST['termite_data'])
			for k in sorted(termite_data.keys()):
				v = termite_data[k]
				pureName = k.split('_')[1]
				result_list_temp = {
					pureName : v['value']
				}
				result_list.append(result_list_temp)
			if result_list[4]['detail-pic']!='[]':
				detailPic = json.loads(result_list[4]['detail-pic'])
			else:
				detailPic = []
			try:
				sh_participance = app_models.ShvoteParticipance(
					belong_to = id,
					member_id = member_id,
					icon = '',
					name = result_list[0]['name'],
					group = 'small',
					serial_number = result_list[2]['number'],
					details = result_list[3]['details'],
					pics = detailPic,
					created_at = datetime.now()
				)
				sh_participance.save()
				response = create_response(200)
			except:
				response = create_response(500)
				response.errMsg = u'只能报名一次'
			return response.get_response()
		except Exception,e:
			print(e)
			response = create_response(500)
			response.errMsg = u'参与失败'
			response.inner_errMsg = unicode_full_stack()
			return response.get_response()

