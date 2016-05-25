# -*- coding: utf-8 -*-

__author__ = 'chuter'


FIRST_NAV_NAME = 'apps'

#install all the apps

#modified by duhao 20150321
#from apps_manager import manager
#manager.install_all_apps()

import module_api

get_mobile_response = module_api.get_mobile_response
get_mobile_api_response = module_api.get_mobile_api_response
get_apps = module_api.get_apps


#连接app mongo
from django.conf import settings
try:
	from mongoengine import connect
	connect(settings.WEAPP_MONGO['DB'], host=settings.WEAPP_MONGO['HOST'])
	connect(settings.APP_MONGO['DB'], host=settings.APP_MONGO['HOST'], alias=settings.APP_MONGO['ALIAS'])
except:
	print '[WARNING]: You have not installed mongoengine. App\'s data store will not be used. Please use "easy_install mongoengine" or "pip install mongoengine" to install it'

# #####################################################################################
# # get_mobile_response ：获取app的移动页面
# #####################################################################################
# def get_mobile_response(request):
# 	c = RequestContext(request, {
# 		'hide_non_member_cover': True
# 	})
# 	return render_to_response('app_demo_mobile_page.html', c)


# #####################################################################################
# # get_mobile_api_response ：获取app的api的调用结果
# #####################################################################################
# def get_mobile_api_response(request):
# 	response = create_response(200)
# 	response.data = 'you call api: %s' % request.POST['target_api']

# 	return response.get_response()
