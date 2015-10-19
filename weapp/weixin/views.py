# -*- coding: utf-8 -*-

__author__ = 'chuter, bert'

import hashlib

from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, Http404
from django.contrib.auth.models import User
from django.db.models import Q
from account.models import UserProfile

from core.exceptionutil import unicode_full_stack
from core.upyun_util import upload_qrcode_url_to_upyun

from watchdog.utils import watchdog_fatal, watchdog_error

from weixin.user.models import *

from BeautifulSoup import BeautifulSoup
from weixin.message_util.WXBizMsgCrypt import WXBizMsgCrypt

import datetime


########################################################################
# is_valid_request: 判断请求是否来自微信
###############	#########################################################
def is_valid_request(request, webapp_id):
	try:
		profile = UserProfile.objects.get(webapp_id=webapp_id)
		signature = request.GET['signature']
		timestamp = request.GET['timestamp']
		nonce = request.GET['nonce']
		token = profile.mp_token

		items = [token, timestamp, nonce]
		items.sort()
		real_signature = hashlib.sha1(''.join(items)).hexdigest()
		result = signature == real_signature
		if result:
			profile.is_mp_registered = 1
			profile.save()

		return result
	except:
		return False

message_pipeline = None
########################################################################
# handle: 接入微信平台
########################################################################
def handle(request, webapp_id):
	global message_pipeline

	if not message_pipeline:
		from weixin.message.message_pipeline import MessagePipeline
		message_pipeline = MessagePipeline()

	if 'echostr' in request.GET:
		if is_valid_request(request, webapp_id):
			return HttpResponse(request.GET['echostr'])
		else:
			return HttpResponse('')
	else:
		#通过微信来的数据kkj
		try:
			content = message_pipeline.handle(request, webapp_id)
		except:
			notify_message = u"进行消息处理失败，webapp_id:{} cause:\n{}".format(webapp_id, unicode_full_stack())
			watchdog_fatal(notify_message)
			content =None
		
		if content is None or len(content) == 0:
			return HttpResponse('')
		else:
			return HttpResponse(content, mimetype="application/xml")


def receiveauthcode(request):
	#@if request.body:
	is_from_simulator = False
	is_aeskey = False
	wxiz_msg_crypt = None

	msg_signature = request.GET.get('msg_signature', None)
	timestamp = request.GET.get('timestamp', None)
	nonce = request.GET.get('nonce', None)
	encrypt_type = request.GET.get('encrypt_type', None)
	signature = request.GET.get('signature', None)
	#component_info = ComponentInfo.objects.filter(is_active=True)
	if request.method == "POST":
		"""
			增加微众测试接口
		"""
		# if 'weizoom_test_data' in request.GET:
		# 	xml_message = _get_raw_message(request)
		# else:
		xml_message = _get_raw_message(request).decode('utf-8')
		xml_message_for_appid = BeautifulSoup(xml_message)
		print xml_message
		if xml_message_for_appid.appid and xml_message_for_appid.appid.text:
			appid = xml_message_for_appid.appid.text
			component_info = ComponentInfo.objects.get(app_id=appid)
			wxiz_msg_crypt = WXBizMsgCrypt(component_info.token, component_info.ase_key, component_info.app_id)
			_,xml_message = wxiz_msg_crypt.DecryptMsg(xml_message, msg_signature, timestamp, nonce)
			print xml_message
			xml_message = BeautifulSoup(xml_message)
			ticket = xml_message.componentverifyticket.text

			if appid and ticket:
				if ComponentInfo.objects.filter(app_id=appid).count() > 0:
					ComponentInfo.objects.filter(app_id=appid).update(component_verify_ticket=ticket, last_update_time=datetime.datetime.now())
				else:
					ComponentInfo.objects.create(app_id=appid,component_verify_ticket=ticket)
				return HttpResponse('success') 
	else:
		auth_code = request.GET.get('auth_code', None)
		expires_in = request.GET.get('expires_in', None)

		# if auth_code and expires_in:
		# 	pass

		if request.user.is_authenticated() and auth_code:
			request.user_profile = request.user.get_profile()
			webapp_id = request.user_profile.webapp_id
			user_id=request.user.id
			# component_info = ComponentInfo.objects.filter(is_active=True)[0]
			# if ComponentAuthedAppid.objects.filter(component_info=component_info, user_id=request.user.id).count() > 0:
			# 	ComponentAuthedAppid.objects.filter(component_info=component_info, user_id=request.user.id).update(last_update_time=datetime.datetime.now(), auth_code=auth_code)
			# else:
			# 	ComponentAuthedAppid.objects.create(component_info=component_info, user_id=request.user.id, auth_code=auth_code)
			from weixin.user.util import get_component_info_from
			request_host = request.get_host()
			component_info = get_component_info_from(request)
			component_authed_appid = ComponentAuthedAppid.objects.get(component_info=component_info, user_id=request.user.id)
			component_info = component_authed_appid.component_info

			"""
			TODO: 使用授权码换取公众号的授权信息 放到 消息队列里 ，并且进行监控， 保证100%成功
			"""
			#try:
			from core.wxapi.agent_weixin_api import WeixinApi, WeixinHttpClient
			weixin_http_client = WeixinHttpClient()
			weixin_api = WeixinApi(component_info.component_access_token, weixin_http_client)
			result = weixin_api.api_query_auth(component_info.app_id, auth_code)
			print '===============query_auth',result
			mp_user = None
			if result.has_key('authorization_info'):
				authorization_info = result['authorization_info']
				func_info_ids = []
				func_info = authorization_info['func_info']
				if  isinstance(func_info, list):
					for funcscope_category in func_info:
						funcscope_category_id = funcscope_category.get('funcscope_category', None)
						if funcscope_category_id:
							func_info_ids.append(str(funcscope_category_id.get('id')))
				print func_info_ids,'=============================='
				authorizer_appid = authorization_info['authorizer_appid']
				authorizer_access_token=authorization_info['authorizer_access_token']
				authorizer_refresh_token=authorization_info['authorizer_refresh_token']
				
				if authorizer_appid:
					ComponentAuthedAppid.objects.filter(user_id=user_id).update(
						authorizer_appid=authorizer_appid,
						authorizer_access_token=authorizer_access_token,
						authorizer_refresh_token=authorizer_refresh_token,
						last_update_time=datetime.datetime.now(),
						func_info = ','.join(func_info_ids),
						is_active = True
						)

					if WeixinMpUser.objects.filter(owner_id=user_id).count() > 0:
						mp_user = WeixinMpUser.objects.filter(owner_id=user_id)[0]
					else:
						mp_user = WeixinMpUser.objects.create(owner_id=user_id)

					if WeixinMpUserAccessToken.objects.filter(mpuser = mp_user).count() > 0:
						WeixinMpUserAccessToken.objects.filter(mpuser = mp_user).update(update_time=datetime.datetime.now(), access_token=authorizer_access_token, is_active=True)
					else:
						WeixinMpUserAccessToken.objects.create(
							mpuser = mp_user,
							app_id = authorizer_appid,
							app_secret = '',
							access_token = authorizer_access_token,
							update_time=datetime.datetime.now()
						)
					#UserProfile.objects.filter(id=request.user_profile.id).update(is_mp_registered=True)
					"""
						处理公众号绑定过其它系统帐号情况
					"""
					update_user_ids = []
					for authed_appid in ComponentAuthedAppid.objects.filter(~Q(user_id=request.user.id), authorizer_appid=authorizer_appid):
						authed_appid.is_active = False
						authed_appid.save()
						update_user_ids.append(authed_appid.user_id)
					UserProfile.objects.filter(user_id__in=update_user_ids).update(is_mp_registered=False)


			# except:
			# 	print '授权失败，请重新授权'
			# 	raise Http404('授权失败，请重新授权')
			"""
				处理公众号mp相关信息
			"""
			try:
				result = weixin_api.api_get_authorizer_info(component_info.app_id,authorizer_appid)
				if result.has_key('authorizer_info'):
					nick_name = result['authorizer_info'].get('nick_name', '')
					head_img = result['authorizer_info'].get('head_img', '')
					service_type_info = result['authorizer_info']['service_type_info'].get('id', '')
					verify_type_info = result['authorizer_info']['verify_type_info'].get('id', '')
					user_name = result['authorizer_info'].get('user_name', '')
					alias = result['authorizer_info'].get('alias', '')
					qrcode_url = result['authorizer_info'].get('qrcode_url','')

					appid = result['authorization_info'].get('authorizer_appid', '')

					func_info_ids = []
					func_info = result['authorization_info'].get('func_info')
					if  isinstance(func_info, list):
						for funcscope_category in func_info:
							funcscope_category_id = funcscope_category.get('funcscope_category', None)
							if funcscope_category_id:
								func_info_ids.append(str(funcscope_category_id.get('id')))
					if ComponentAuthedAppidInfo.objects.filter(auth_appid=component_authed_appid).count() > 0:
						auth_appid_info = ComponentAuthedAppidInfo.objects.filter(auth_appid=component_authed_appid)[0]
						if auth_appid_info.qrcode_url.find('mmbiz.qpic.cn') > -1 or auth_appid_info.nick_name != nick_name:
							try:
								qrcode_url = upload_qrcode_url_to_upyun(qrcode_url, authorizer_appid)
							except:
								print '>>>>>>>>>>>>>>>>>>>>upload_qrcode_url_to_upyun error'
						ComponentAuthedAppidInfo.objects.filter(auth_appid=component_authed_appid).update(
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
							qrcode_url = upload_qrcode_url_to_upyun(qrcode_url, authorizer_appid)
						except:
							print '>>>>>>>>>>>>>>>>>>>>upload_qrcode_url_to_upyun error'
						ComponentAuthedAppidInfo.objects.create(
							auth_appid=component_authed_appid,
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
					WeixinMpUser.objects.filter(owner_id=user_id).update(is_service=is_service, is_certified=is_certified, is_active=True)
					
					if is_certified:
						UserProfile.objects.filter(id=request.user_profile.id).update(is_mp_registered=True, is_oauth=True)
					else:
						UserProfile.objects.filter(id=request.user_profile.id).update(is_mp_registered=True, is_oauth=False)
				
					try:
						if mp_user:
							if MpuserPreviewInfo.objects.filter(mpuser=mp_user).count() > 0:
								MpuserPreviewInfo.objects.filter(mpuser=mp_user).update(image_path=head_img, name=nick_name)
							else:
								MpuserPreviewInfo.objects.create(mpuser=mp_user,image_path=head_img, name=nick_name)
					except:
						notify_msg = u"处理公众号mp相关信息:MpuserPreviewInfo, cause:\n{}".format(unicode_full_stack())
						watchdog_error(notify_msg)		
					
			except:
				notify_msg = u"处理公众号mp相关信息, cause:\n{}".format(unicode_full_stack())
				watchdog_error(notify_msg)

			return HttpResponseRedirect('/new_weixin/mp_user/')

		else:
			raise Http404('请先登录系统，继续完成授权！')

		print auth_code, expires_in, '>>>>>>>'
	return HttpResponse('') 


def _get_raw_message(request):
	if 'weizoom_test_data' in request.GET:
		#通过模拟器来的数据
		return request.POST['weizoom_test_data']
	else:
		#通过微信来的数据
		if hasattr(request, 'raw_post_data'):
			return request.raw_post_data
		else:
			return request.body

def component_handle(request, appid):
	global message_pipeline

	if not message_pipeline:
		from weixin.message.message_pipeline import MessagePipeline
		message_pipeline = MessagePipeline()

	# if ComponentAuthedAppid.objects.filter(authorizer_appid=appid, is_active=True).count() > 0:
	# 	print '------------in1'
	# 	user_id = ComponentAuthedAppid.objects.filter(authorizer_appid=appid, is_active=True)[0].user_id
	# 	user = User.objects.get(id=user_id)
	# 	request.user_profile = user.get_profile()
	# 	request.webapp_owner_id = user_id
	# 	print '------------in2'


	# if 'echostr' in request.GET:
	# 	if is_valid_request(request, request.user_profile.webapp_id):
	# 		return HttpResponse(request.GET['echostr'])
	# 	else:
	# 		return HttpResponse('')
	# else:
	# 	if appid == "wx570bc396a51b8ff8":
	# 		webapp_id = None
	# 		user_profile = None
	# 	else:
	# 		webapp_id = request.user_profile.webapp_id
	# 		user_profile = request.user_profile


 	try:
		content = message_pipeline.handle_component(request, appid)
	except:
		notify_message = u"进行消息处理失败，cause:\n{}".format(unicode_full_stack())
		watchdog_fatal(notify_message)
		content =None
	
	if content is None or len(content) == 0:
		return HttpResponse('')
	else:
		return HttpResponse(content, mimetype="application/xml")

	#return HttpResponse('')


	