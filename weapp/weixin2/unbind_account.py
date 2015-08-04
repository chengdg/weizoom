# -*- coding: utf-8 -*-

#import json

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
#from django.db.models import F

#import models as weixin_models
from account import models as account_models
from core import resource
#from core import paginator
from core.jsonresponse import create_response
from weixin2 import export


class UnbindAccount(resource.Resource):
	app = 'new_weixin'
	resource = 'unbind_account'

	@login_required
	def get(request):
		"""
		获取一键绑定页面
		"""
		c = RequestContext(request, {
			'first_nav_name': export.UNBIND_ACCOUNT_FIRST_NAV,
			'second_navs': export.get_unbind_account_second_navs(request)
		})
		return render_to_response('weixin/unbind_account.html', c)

	@login_required
	def api_put(request):
		"""
		为公众号取消绑定
		"""
		account_models.UserProfile.objects.filter(user=request.manager).update(is_mp_registered=False)

		response = create_response(200)
		response.data = {
			'redirect_url': '/new_weixin/unbind_account/'
		}
		return response.get_response()