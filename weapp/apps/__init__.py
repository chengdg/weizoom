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
	connect(settings.APP_MONGO['DB'], host=settings.APP_MONGO['HOST'], alias=settings.APP_MONGO['ALIAS'], username=settings.APP_MONGO['USERNAME'], password=settings.APP_MONGO['PASSWORD'])
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

#配置apps用的celery客户端
from celery import Celery
import logging
logging.info('init apps celery...')
celery = Celery()
celery.config_from_object('apps.celeryconfig')

from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack
def send_task(queue_name, args):
	try:
		celery.send_task(queue_name, args=[args], queue=queue_name)
	except:
		notify_message = u"queue_name:{}, args:{}, cause:\n{}".format(queue_name, args, unicode_full_stack())
		watchdog.error(notify_message)
