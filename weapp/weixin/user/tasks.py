# -*- coding: utf-8 -*-

__author__ = 'bert'
# from __future__ import absolute_import

from django.conf import settings
from django.db.models import F

from core.exceptionutil import unicode_full_stack

from core import emotion

from watchdog.utils import watchdog_fatal, watchdog_error, watchdog_info

from modules.member.models import *

from weixin.user.models import *

from account.social_account.models import SocialAccount
from account import models as account_models

from celery import task

# @task
# def update_component_mp_info():
# 	"""
# 		更新第三方帐号信息
# 		更新委托第三方授权帐号信息（token）

# 		TODO:
# 			为兼容当前模式，保留WeixinMpUser ，WeixinMpUserAccessToken

# 	"""
# 	for component in ComponentInfo.objects.filter(is_active=True):
# 		weixin_api = WeixinApi(None, weixin_http_client)
# 		result = weixin_api.get_component_token(component.app_id, component.app_secret, component.component_verify_ticket)
# 		#try:
# 		component_access_token = result['component_access_token']
# 		component.component_access_token = component_access_token
# 		component.save()
# 		mp_user = None
# 		#更新appid token
# 		weixin_api = WeixinApi(component_access_token, weixin_http_client)
# 		for auth_appid in ComponentAuthedAppid.objects.filter(component_info=component):
# 			print '-----',component.app_id,auth_appid.authorizer_appid,auth_appid.authorizer_refresh_token
# 			result = weixin_api.api_authorizer_token(component.app_id, auth_appid.authorizer_appid, auth_appid.authorizer_refresh_token)
# 			user_id = auth_appid.user_id
# 			if result.has_key('authorizer_access_token'):
# 				auth_appid.authorizer_access_token = result['authorizer_access_token']
# 				auth_appid.authorizer_refresh_token = result['authorizer_refresh_token']
# 				auth_appid.last_update_time = datetime.datetime.now()
# 				auth_appid.save()

# 				if WeixinMpUserAccessToken.objects.filter(appid=auth_appid.authorizer_appid).count() > 0:
# 					WeixinMpUserAccessToken.objects.filter(appid=auth_appid.authorizer_appid).update(update_time=datetime.now(), access_token=authorizer_access_token, is_active=True)
# 				else:
					
# 					if WeixinMpUser.objects.filter(owner_id=user_id).count() > 0:
# 						mp_user = WeixinMpUser.objects.filter(owner_id=user_id)[0]
# 						WeixinMpUserAccessToken.objects.create(
# 							mpuser = mp_user,
# 							app_id = auth_appid.authorizer_appid,
# 							app_secret = '',
# 							access_token = authorizer_access_token
# 							)
# 					else:
# 						mp_user = WeixinMpUser.objects.create(owner_id=user_id)
# 						WeixinMpUserAccessToken.objects.create(
# 							mpuser = mp_user,
# 							app_id = auth_appid.authorizer_appid,
# 							app_secret = '',
# 							access_token = authorizer_access_token
# 							)

# 			result = weixin_api.api_get_authorizer_info(component.app_id,auth_appid.authorizer_appid)
# 			if result.has_key('authorizer_info'):
# 				nick_name = result['authorizer_info'].get('nick_name', '')
# 				head_img = result['authorizer_info'].get('head_img', '')
# 				service_type_info = result['authorizer_info']['service_type_info'].get('id', '')
# 				verify_type_info = result['authorizer_info']['verify_type_info'].get('id', '')
# 				user_name = result['authorizer_info'].get('user_name', '')
# 				alias = result['authorizer_info'].get('alias', '')
# 				qrcode_url = result['authorizer_info'].get('qrcode_url','')

# 				#authorization_info
# 				appid = result['authorization_info'].get('appid', '')

# 				func_info_ids = []
# 				func_info = result['authorization_info'].get('func_info')
# 				if  isinstance(func_info, list):
# 					for funcscope_category in func_info:
# 						funcscope_category_id = funcscope_category.get('funcscope_category', None)
# 						if funcscope_category_id:
# 							func_info_ids.append(str(funcscope_category_id.get('id')))

# 				if ComponentAuthedAppidInfo.objects.filter(auth_appid=auth_appid).count() > 0:
# 					ComponentAuthedAppidInfo.objects.filter(auth_appid=auth_appid).update(
# 						nick_name=nick_name,
# 						head_img=head_img,
# 						service_type_info=service_type_info,
# 						verify_type_info=verify_type_info,
# 						user_name=user_name,
# 						alias=alias,
# 						qrcode_url=qrcode_url,
# 						appid=appid,
# 						func_info=','.join(func_info_ids)
# 						)

# 				else:
# 					ComponentAuthedAppidInfo.objects.create(
# 						auth_appid=auth_appid,
# 						nick_name=nick_name,
# 						head_img=head_img,
# 						service_type_info=service_type_info,
# 						verify_type_info=verify_type_info,
# 						user_name=user_name,
# 						alias=alias,
# 						qrcode_url=qrcode_url,
# 						appid=appid,
# 						func_info=','.join(func_info_ids)
# 						)
# 				is_service = False
# 				if int(service_type_info) > 0:
# 					is_service = True
# 				is_certified = False
# 				if int(verify_type_info) > -1:
# 					is_certified = True


# 				WeixinMpUser.objects.filter(owner_id=user_id).update(is_service=is_service, is_certified=is_certified, is_active=True)

# 				if mp_user:
# 					if MpuserPreviewInfo.objects.filter(mpuser=mp_user).count() > 0:
# 						MpuserPreviewInfo.objects.filter(mpuser=mp_user).update(image_path=head_img, name=nick_name)
# 					else:
# 						MpuserPreviewInfo.objects.create(mpuser=mp_user,image_path=head_img, name=nick_name)

# @task
# def record_call_weixin_api(class_name):
# 	url = "http://index.weizzz.com/table/api/cell_increase/" 
# 	now_time = datetime.today().strftime('%Y-%m-%d')
# 	if settings.MODE == ''
# 	table = "%s_weixin_api" % settings.MODE
# 	params = {
# 		"table": table,
# 		"rkey": now_time,
# 		"cname": class_name,
# 		"val": '1'
# 	}
# 	req = urllib2.Request(url) 
# 	data = urllib.urlencode(data) 
# 	#enable cookie 
# 	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor()) 
# 	response = opener.open(req, data) 
# 	print 'record_call_weixin_api>>>',response.read() 

