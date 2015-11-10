# -*- coding: utf-8 -*-

__author__ = 'bert'

from django.conf import settings
from weixin.user.models import *


def get_component_info_from(request):
	#request_host = request.get_host()
	request_host = settings.DOMAIN
	if request_host == 'member.weapp.weizzz.com':
		component_info = ComponentInfo.objects.filter(app_id='wx984abb2d00cc47b8')[0]
	elif request_host == 'weixin.weapp.weizzz.com':
		component_info = ComponentInfo.objects.filter(app_id='wxba6fccbdcccbea49')[0]
	elif request_host == 'docker.test.weizzz.com':
		component_info = ComponentInfo.objects.filter(app_id='wx9b89fe19768a02d2')[0]
	elif request_host == 'red.weapp.weizzz.com':
		component_info = ComponentInfo.objects.filter(app_id='wxa823309fb403f661')[0]
	elif request_host == 'nj.weapp.weizzz.com':
		component_info = ComponentInfo.objects.filter(app_id='wxb04d4cdf32b59823')[0]
	elif request_host == 'yanshi.weizoom.com':
		component_info = ComponentInfo.objects.filter(app_id='wxe8bdf8eb296716f2')[0]
	else:
		component_info = ComponentInfo.objects.filter(app_id='wx8209f1f63f0b1d26')[0]

	return component_info