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
from mall import export as mall_export
from modules.member.models import Member
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
		def __itemName2item(itemName):
			itemName_dic = {u"初中组":'small'}
			if itemName:
				return itemName_dic[itemName]
			else:
				return itemName
		try:
			result_list = []
			member_id = request.member.id
			id = request.POST['belong_to']
			termite_data = json.loads(request.POST['termite_data'])
			print(termite_data)
			for k in sorted(termite_data.keys()):
				v = termite_data[k]
				pureName = k.split('_')[1]
				print(v['value'])
				print('---------------------')
				result_list_temp = {
					pureName : v['value']
				}
				result_list.append(result_list_temp)
			if result_list[5]['detail-pic']!='[]':
				detailPic = json.loads(result_list[5]['detail-pic'])
			else:
				detailPic = []
			try:
				sh_participance = app_models.ShvoteParticipance(
					belong_to = id,
					member_id = member_id,
					icon = json.loads(result_list[0]['headImg'])[0],
					name = result_list[1]['name'],
					group = 'small',
					serial_number = result_list[3]['number'],
					details = result_list[4]['details'],
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
			response.errMsg = u'报名失败'
			response.inner_errMsg = unicode_full_stack()
			return response.get_response()

	def api_post(request):
		"""
		投票
		"""
		vote_to = request.POST.get('vote_to', None)
		member = request.member
		response = create_response(500)
		if not vote_to or not member:
			response.errMsg = u'会员信息出错'
			return response.get_response()
		record_id = request.POST.get('recordId', None)
		member_id = member.id
		#非会员不能投票
		if not member.is_subscribed:
			response.errMsg = 'none_member'
			return response.get_response()
		#不能给取消关注的会员投票
		try:
			target_member = Member.objects.get(id=vote_to)
			if not target_member.is_subscribed:
				response.errMsg = u'该用户已退出投票活动'
				return response.get_response()
		except:
			response.errMsg = u'不存在该用户'
			return response.get_response()

		target = None
		now_date_str = datetime.now().strftime('%Y-%m-%d')
		try:
			target = app_models.ShvoteParticipance.objects.get(belong_to=record_id, member_id=long(vote_to), status=app_models.MEMBER_STATUS['PASSED'])
		except:
			response.errMsg = u'用户信息出错'
			return response.get_response()

		result = target.modify(query={'vote_log__'+now_date_str+'__not__exists': member_id},
							   **{
								   'inc__count': 1,
								   'push__vote_log__'+now_date_str: member_id
							   })
		if not result:
			response.errMsg = u'只能投票一次'
			return response.get_response()

		response = create_response(200)
		return response.get_response()
