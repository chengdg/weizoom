# -*- coding: utf-8 -*-

#import json
#from datetime import datetime
#from django.http import HttpResponseRedirect
#from django.template import RequestContext
from django.contrib.auth.decorators import login_required
#from django.shortcuts import render_to_response
#from django.db.models import F

from stats import export
from core import resource
#from core import paginator
from core.jsonresponse import create_response
#from weixin.mp_decorators import mp_required
from core.exceptionutil import unicode_full_stack

FIRST_NAV = export.MARKETING_NAV
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

	# deprecated
	'''
	@login_required
	def get(request):
		"""
		显示营销活动参与人员的网络图
		"""
		# 营销活动ID
		activity_id = request.GET.get('id', '0')
		# 获取营销活动的类型
		activity_type = request.GET.get('type', 'qrcode')

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_market_second_navs(request),
			'second_nav_name': export.MARKETING_ACTIVITY_NAV,
			'activity_id': activity_id,
			'activity_type': activity_type,
		})
		return render_to_response('marketing/activity_network.html', c)
	'''		


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
