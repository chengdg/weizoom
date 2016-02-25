# -*- coding: utf-8 -*-

import json

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.db.models import F

from account import models as account_models
from weixin2 import export
import weixin2.models as weixin2_models
from core import resource
from core import paginator
from core.jsonresponse import create_response

import weixin.user.models as weixin_models
from watchdog.utils import watchdog_fatal, watchdog_error
from weixin.mp_decorators import mp_required
from django.conf import settings

COUNT_PER_PAGE = 20
FIRST_NAV = export.WEIXIN_HOME_FIRST_NAV

class MpUser(resource.Resource):
	app = 'new_weixin'
	resource = 'mp_user'
	@login_required
	def get(request):
		"""
		获得公众号详情
		"""
		user_profile = request.user_profile
		# request_user = request.user
		request_user = request.manager #duhao 20151020
		user_profile = account_models.UserProfile.objects.get(id=user_profile.id)

		if user_profile.is_mp_registered:
			try:
				mpuser = weixin_models.get_system_user_binded_mpuser(request_user)
				mpuser_preview_info = weixin_models.MpuserPreviewInfo.objects.get(mpuser=mpuser)
			except:
				mpuser = None
				mpuser_preview_info = None

		from weixin.user.util import get_component_info_from
		component_info = get_component_info_from(request)

		pre_auth_code = None
		request_host = settings.DOMAIN
		#request_host = request.META['HTTP_HOST']

		if component_info:
			from core.wxapi.agent_weixin_api import WeixinApi, WeixinHttpClient
			weixin_http_client = WeixinHttpClient()
			weixin_api = WeixinApi(component_info.component_access_token, weixin_http_client)
			result = weixin_api.api_create_preauthcode(component_info.app_id)
			print result
			if hasattr(result, 'pre_auth_code'):
				pre_auth_code = result['pre_auth_code']
			else:
				result = weixin_api.api_create_preauthcode(component_info.app_id)
				if result and result.has_key('pre_auth_code'):
					pre_auth_code = result['pre_auth_code']
				else:
					watchdog_error(result)

			if weixin_models.ComponentAuthedAppid.objects.filter(component_info=component_info, user_id=request.manager.id).count() == 0:
				weixin_models.ComponentAuthedAppid.objects.create(component_info=component_info, user_id=request.manager.id)
			auth_appid = weixin_models.ComponentAuthedAppid.objects.filter(component_info=component_info, user_id=request.manager.id)[0]

			if weixin_models.ComponentAuthedAppidInfo.objects.filter(auth_appid=auth_appid).count() > 0:
				auth_appid_info = weixin_models.ComponentAuthedAppidInfo.objects.filter(auth_appid=auth_appid)[0]
			else:
				auth_appid_info = None
		else:
			component_info = None
			auth_appid = None
			auth_appid_info = None

		#微众商城引流图文地址
		operation_settings_objs = account_models.OperationSettings.objects.filter(owner=request.manager)
		if operation_settings_objs.count() == 0:
			operation_settings = account_models.OperationSettings.objects.create(owner=request.manager)
		else:
			operation_settings = operation_settings_objs[0]

		if user_profile.is_mp_registered:
			mpuser_access_token = weixin_models.get_mpuser_access_token_for(mpuser)
			c = RequestContext(request, {
				'first_nav_name': FIRST_NAV,
				'second_navs': export.get_weixin_second_navs(request),
				'second_nav_name': export.WEIXIN_MPUSER_SECOND_NAV,
				'third_nav_name': export.MPUSER_BINDING_NAV,
				'component_info':component_info,
				'request_user': request_user,
				'user_profile': user_profile,
				'mpuser': mpuser,
				'mpuser_access_token': mpuser_access_token,
				'preview_user': mpuser_preview_info,
				'default_icon': weixin_models.DEFAULT_ICON,
				'is_mp_registered':user_profile.is_mp_registered,
				'pre_auth_code': pre_auth_code,
				'auth_appid_info':auth_appid_info,
				'request_host':request_host,
				'operation_settings': operation_settings
			})
			return render_to_response('weixin/mp_user/mp_user.html', c)
		else:
			c = RequestContext(request, {
				'first_nav_name': FIRST_NAV,
				'pre_auth_code': pre_auth_code,
				'request_user': request_user,
				'user_profile': user_profile,
				'default_icon': weixin_models.DEFAULT_ICON,
				'component_info': component_info,
				'is_mp_registered':user_profile.is_mp_registered,
				'auth_appid_info':auth_appid_info,
				'request_host':request_host,
				'operation_settings': operation_settings
			})
			return render_to_response('weixin/mp_user/mp_user_index.html', c)


	@login_required
	@mp_required
	def api_put(request):
		"""
		创建绑定后的公众号
		"""
		account_models.UserProfile.objects.filter(user=request.manager).update(is_mp_registered=True)

		response = create_response(200)
		response.data = {
			'redirect_url': '/new_weixin/mp_user/'
		}
		return response.get_response()

	@login_required
	@mp_required
	def api_post(request):
		"""
		修改预览头像
		"""
		mp_user_id = request.POST.get('mp_user_id')
		pic_url = request.POST.get('pic_url')
		# 微众商城代码
		# weshop_followurl = request.POST.get('weshop_followurl', '')
		try:
			# 微众商城代码
			# account_models.OperationSettings.objects.filter(owner=request.user).update(
			# 	weshop_followurl = weshop_followurl
			# )

			if weixin_models.MpuserPreviewInfo.objects.filter(mpuser_id=mp_user_id).count() > 0:
				weixin_models.MpuserPreviewInfo.objects.filter(mpuser_id=mp_user_id).update(image_path=pic_url)
			else:
				weixin_models.MpuserPreviewInfo.objects.create(
					mpuser_id=mp_user_id,
					name='',
					image_path=pic_url
					)
		except:
			response = create_response(500)
			return response.get_response()

		response = create_response(200)
		return response.get_response()