# -*- coding: utf-8 -*-

import json
from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.template.loader import render_to_string

from core import resource

import models as app_models
from core.jsonresponse import create_response
from termite2 import pagecreater
from utils import url_helper
from utils.cache_util import GET_CACHE, SET_CACHE
from modules.member.models import Member

class MGroup(resource.Resource):
	app = 'apps/group'
	resource = 'm_group'

	def api_get(request):
		response = create_response(200)
		return response.get_response()

	def get(request):
		"""
		响应GET
		"""
		all_groups_can_open = []
		# all_groups_can_join = []
		#获取webapp_owner_id
		owner_id = request.webapp_owner_id
		#我要开团
		groups = app_models.Group.objects(owner_id=owner_id,status=app_models.STATUS_RUNNING).order_by('-created_at')
		for group in groups:
			try:
				group_id = group.id
				all_groups_can_open.append({
					'id': str(group_id),
					'name': group.name,
					'product_img': group.product,
					'group_list': group.group_list,
					'end_time': group.end_time.strftime('%y-%m-%d'),
					'rules': group.rules,
					'url': '/m/apps/group/m_group/?webapp_owner_id=%d&id=%s' % (owner_id, str(group_id))
				})
			except:
				pass

		#直接参团
		# lotteries = app_models.lottoryRecord.objects.filter(member_id=member.id).order_by('-created_at')
		# for lottery in lotteries:
		# 	try:
		# 		lottery_id = lottery.belong_to
		# 		lottery_details = app_models.lottery.objects.get(id=lottery_id )
		# 		all_groups_can_join.append({
		# 			'id': str(lottery_id),
		# 			'name': lottery_details.name,
		# 			'url': '/m/apps/lottery/m_lottery/?webapp_owner_id=%d&id=%s' % (lottery_details.owner_id, str(lottery_id)),
		# 			'participant_time': lottery.created_at.strftime('%m月%d日')
		# 		})
		# 	except:
		# 		pass

		c = RequestContext(request, {
			'page_title': u'团购列表',
			'all_groups_can_open': all_groups_can_open,
			# 'all_groups_can_join': all_groups_can_join,
			'is_hide_weixin_option_menu':True
		})
		return render_to_response('group/templates/webapp/m_group_list.html', c)