# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from core import resource
from watchdog.utils import *
from weixin.manage.customerized_menu.models import *
from weixin2 import export
from account.models import *
from weixin.mp_decorators import mp_required
from core.jsonresponse import create_response


FIRST_NAV = export.MPUSER_FIRST_NAV

class DirectFollow(resource.Resource):
	app = 'new_weixin'
	resource = 'direct_follow'
	
	@login_required
	@mp_required
	def get(request):
		"""
		快速关注页面
		"""
		operation_settings_objs = OperationSettings.objects.filter(owner=request.user)
		if operation_settings_objs.count() == 0:
			operation_settings = OperationSettings.objects.create(owner=request.user)
		else:
			operation_settings = operation_settings_objs[0]

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_mpuser_second_navs(request),
			'second_nav_name': export.MPUSER_DIRECT_FOLLOW_NAV,
			'operation_settings': operation_settings,
		})
		return render_to_response('weixin/mp_user/direct_follow.html', c)

	@login_required
	@mp_required
	def api_post(request):
		"""
		更新快速关注信息
		"""
		non_member_followurl = request.POST.get('non_member_followurl', '')
		weshop_followurl = request.POST.get('weshop_followurl', '')

		OperationSettings.objects.filter(owner=request.user).update(
			non_member_followurl = non_member_followurl,
			weshop_followurl = weshop_followurl
		)

		response = create_response(200)
		return response.get_response()
