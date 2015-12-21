# -*- coding: utf-8 -*-

import os
import subprocess
import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db.models import Q

from weixin.user.models import *
from core.wxapi.agent_weixin_api import WeixinApi, WeixinHttpClient
from core.upyun_util import upload_qrcode_url_to_upyun
weixin_http_client = WeixinHttpClient()
import datetime
from account.models import UserProfile
from watchdog.utils import watchdog_error, watchdog_info, watchdog_warning

class Command(BaseCommand):
	help = "init global navbar for all user"
	args = ''

	def handle(self, **options):
		for component in ComponentInfo.objects.filter(is_active=True):
			weixin_api = WeixinApi(None, weixin_http_client)
			from weixin.message.message_handler.tasks import record_call_weixin_api

			try:
				result = weixin_api.get_component_token(component.app_id, component.app_secret, component.component_verify_ticket)
				print result,'---'
				#watchdog_info('call weixin api: get_component_token , result:{}'.format(result))
				if result.has_key('errcode'):
					if result['errcode'] == -1 or result['errcode'] == 995995:
						result, success = self.__get_component_token_retry(weixin_api, component)
					else:
						success = False
						watchdog_error('call weixin api: get_component_token , result:{}'.format(result))
				else:
					success = True
			except:
				result, success = self.__get_component_token_retry(weixin_api, component)
			if result != None:
				record_call_weixin_api.delay('get_component_token', success)

			component_access_token = result['component_access_token']
			component.component_access_token = component_access_token
			component.save()
			mp_user = None
			#更新appid token


			weixin_api = WeixinApi(component_access_token, weixin_http_client)
			update_fail_auth_appid = []
			for auth_appid in ComponentAuthedAppid.objects.filter(is_active=True, component_info=component):
				self.__update_auth_appid(auth_appid, weixin_api, component, update_fail_auth_appid)

			print "更新失败重试数" + str(len(update_fail_auth_appid))
			if update_fail_auth_appid:
				for auth_appid in update_fail_auth_appid:
					self.__update_auth_appid(auth_appid, weixin_api, component)


	def __update_auth_appid(self, auth_appid = None, weixin_api = None, component = None, error_auth_appid = []):
		user_id = auth_appid.user_id
		print user_id,auth_appid.is_active
		if auth_appid.is_active is False:
			UserProfile.objects.filter(user_id=user_id).update(is_mp_registered=False)
			return

		result = weixin_api.api_authorizer_token(component.app_id, auth_appid.authorizer_appid, auth_appid.authorizer_refresh_token)

		if result.has_key('errcode') and (result['errcode'] == -1 or result['errcode'] == 995995):
			error_auth_appid.append(auth_appid)
		#print result['authorizer_access_token']
		if result.has_key('authorizer_access_token'):
			authorizer_access_token = result['authorizer_access_token']
			auth_appid.authorizer_access_token = result['authorizer_access_token']
			auth_appid.authorizer_refresh_token = result['authorizer_refresh_token']
			auth_appid.last_update_time = datetime.datetime.now()
			auth_appid.save()

			if WeixinMpUser.objects.filter(owner_id=user_id).count() > 0:
				mp_user = WeixinMpUser.objects.filter(owner_id=user_id)[0]
			else:
				mp_user = WeixinMpUser.objects.create(owner_id=user_id)

			if WeixinMpUserAccessToken.objects.filter(mpuser = mp_user).count() > 0:
				WeixinMpUserAccessToken.objects.filter(mpuser = mp_user).update(update_time=datetime.datetime.now(), access_token=authorizer_access_token, is_active=True, app_id = auth_appid.authorizer_appid)
			else:
				WeixinMpUserAccessToken.objects.filter(mpuser = mp_user).update(
					mpuser = mp_user,
					app_id = auth_appid.authorizer_appid,
					app_secret = '',
					access_token = authorizer_access_token
				)

		result = weixin_api.api_get_authorizer_info(component.app_id,auth_appid.authorizer_appid)
		print result
		try:
			watchdog_info('call weixin api: api_get_authorizer_info , result:{}'.format(result))
		except:
			pass
		if result.has_key('authorizer_info'):
			nick_name = result['authorizer_info'].get('nick_name', '')
			head_img = result['authorizer_info'].get('head_img', '')
			service_type_info = result['authorizer_info']['service_type_info'].get('id', '')
			verify_type_info = result['authorizer_info']['verify_type_info'].get('id', '')
			user_name = result['authorizer_info'].get('user_name', '')
			alias = result['authorizer_info'].get('alias', '')
			qrcode_url = result['authorizer_info'].get('qrcode_url','')

			#authorization_info
			appid = result['authorization_info'].get('authorizer_appid', '')

			func_info_ids = []
			func_info = result['authorization_info'].get('func_info')
			if  isinstance(func_info, list):
				for funcscope_category in func_info:
					funcscope_category_id = funcscope_category.get('funcscope_category', None)
					if funcscope_category_id:
						func_info_ids.append(str(funcscope_category_id.get('id')))


			if ComponentAuthedAppidInfo.objects.filter(auth_appid=auth_appid).count() > 0:
				auth_appid_info = ComponentAuthedAppidInfo.objects.filter(auth_appid=auth_appid)[0]
				if auth_appid_info.qrcode_url.find('mmbiz.qpic.cn') > -1 or auth_appid_info.nick_name != nick_name:
					try:
						qrcode_url = upload_qrcode_url_to_upyun(qrcode_url, auth_appid.authorizer_appid)
					except:
						print '>>>>>>>>>>>>>>>>>>>>upload_qrcode_url_to_upyun error'
				else:
					qrcode_url = auth_appid_info.qrcode_url

				ComponentAuthedAppidInfo.objects.filter(auth_appid=auth_appid).update(
					nick_name=nick_name,
					head_img=head_img,
					service_type_info=service_type_info,
					verify_type_info=verify_type_info,
					user_name=user_name,
					alias=alias,
					qrcode_url=qrcode_url,
					appid=appid,
					func_info=','.join(func_info_ids)
					)

			else:
				try:
					watchdog_info('call weixin api: api_get_authorizer_info , result:{}'.format(result))
					qrcode_url = upload_qrcode_url_to_upyun(qrcode_url, auth_appid.authorizer_appid)
				except:
					print '>>>>>>>>>>>>>>>>>>>>upload_qrcode_url_to_upyun error'
				ComponentAuthedAppidInfo.objects.create(
					auth_appid=auth_appid,
					nick_name=nick_name,
					head_img=head_img,
					service_type_info=service_type_info,
					verify_type_info=verify_type_info,
					user_name=user_name,
					alias=alias,
					qrcode_url=qrcode_url,
					appid=appid,
					func_info=','.join(func_info_ids)
					)

			is_service = False

			if int(service_type_info) > 1:
				is_service = True
			is_certified = False
			if int(verify_type_info) > -1:
				is_certified = True

			print '>>>>>>>>>>>>>>>>>service_type_info',service_type_info
			print '>>>>>>>>>>>>>>>>>is_certified',is_certified
			WeixinMpUser.objects.filter(owner_id=user_id).update(is_service=is_service, is_certified=is_certified, is_active=True)

			if mp_user:
				if MpuserPreviewInfo.objects.filter(mpuser=mp_user).count() > 0:
					MpuserPreviewInfo.objects.filter(mpuser=mp_user).update(image_path=head_img, name=nick_name)
				else:
					MpuserPreviewInfo.objects.create(mpuser=mp_user,image_path=head_img, name=nick_name)
			user_profile = UserProfile.objects.get(user_id=user_id)
			if is_service:
				if (user_profile.is_mp_registered is False) or (user_profile.is_oauth is False):
					UserProfile.objects.filter(user_id=user_id).update(is_mp_registered=True, is_oauth=True)
			else:
				if user_profile.is_oauth:
					UserProfile.objects.filter(user_id=user_id).update(is_mp_registered=True, is_oauth=False)

	def __get_component_token_retry(self, weixin_api=None, component = None):
		try:
			result = weixin_api.get_component_token(component.app_id, component.app_secret, component.component_verify_ticket)
			print 'justing,retry :\n{}'.format(result)
			#watchdog_info('call weixin api: get_component_token , result:{}'.format(result))
			if result.has_key('errcode'):
				success = False
				watchdog_error('call weixin api: get_component_token , result:{}'.format(result))
			else:
				success = True
			return result, success
		except:
			return None, False