# -*- coding: utf-8 -*-

#import json
#from datetime import datetime
#from django.http import HttpResponseRedirect
#from django.template import RequestContext
from django.contrib.auth.decorators import login_required
#from django.shortcuts import render_to_response
#from django.db.models import F

from core import resource
#from core import paginator
from core.jsonresponse import create_response
#from weixin.mp_decorators import mp_required
from core.exceptionutil import unicode_full_stack

DEFAULT_COUNT_PER_PAGE = 20

import chart_api


def __build_member_basic_json(member):
	return {
		'id': member.id,
		'username': member.username_for_html,
		'user_icon': member.user_icon,
		'integral': member.integral,
		'grade_name': member.grade.name
	}


class ActivityNetwork(resource.Resource):
	"""
	营销活动的人员参与网络（展示每个人是通过谁参加活动的）
	"""
	app = 'stats'
	resource = 'activity_network'

	@login_required
	def api_get(request):
		"""
		获取营销活动传播关系JSON数据的接口
		"""

		# 获取营销活动的类型
		activity_type = request.GET.get('type', 'qrcode')

		try:
			activity_id = int(request.GET['id'])
			if activity_type == 'lottery':
				data = chart_api.get_lottery_member_network_chart(activity_id)
			else:
				# 渠道扫码
				data = chart_api.get_channel_member_network_chart(activity_id)		

			response = create_response(200)
			response.data = data
		except:
			response = create_response(500)
			response.errMsg = u'不存在此活动信息'
			response.innerErrMsg = unicode_full_stack()
		return response.get_response()
