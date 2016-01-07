# -*- coding: utf-8 -*-

__author__ = 'chuter, bert'

import hashlib
from BeautifulSoup import BeautifulSoup

from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, Http404
from django.contrib.auth.models import User
from django.db.models import Q
from account.models import UserProfile

from core.exceptionutil import unicode_full_stack
from core.upyun_util import upload_qrcode_url_to_upyun

from watchdog.utils import watchdog_fatal, watchdog_error, watchdog_info
from util import get_query_auth, get_authorizer_info
from weixin.user.models import *
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
	is_from_simulator = False
	is_aeskey = False
	wxiz_msg_crypt = None

	msg_signature = request.GET.get('msg_signature', None)
	timestamp = request.GET.get('timestamp', None)
	nonce = request.GET.get('nonce', None)
	encrypt_type = request.GET.get('encrypt_type', None)
	signature = request.GET.get('signature', None)

	if request.method == "POST":
		"""
		接受微信服务器每隔10分钟推送过来的component_verify_ticket
		"""
		xml_message = _get_raw_message(request).decode('utf-8')
		xml_message_for_appid = BeautifulSoup(xml_message)
		appid = xml_message_for_appid.appid.text if xml_message_for_appid.appid else None
		if appid:
			try:
				component_info = ComponentInfo.objects.get(app_id=appid)
			except:
				notify_msg = u"没有app_id=%s的第三方平台账号帐号信息" % appid
				watchdog_error(notify_msg)
				return HttpResponse('success')

			wxiz_msg_crypt = WXBizMsgCrypt(component_info.token, component_info.ase_key, component_info.app_id)
			_,xml_message = wxiz_msg_crypt.DecryptMsg(xml_message, msg_signature, timestamp, nonce)
			xml_message = BeautifulSoup(xml_message)
			#ticket = xml_message.componentverifyticket.text

			if xml_message.componentverifyticket:
				#接受component_verify_ticket
				ticket = xml_message.componentverifyticket.text
				if ticket:
					component_info.component_verify_ticket = ticket
					component_info.last_update_time = datetime.datetime.now()
					component_info.save()
			elif xml_message.infotype and xml_message.infotype.text == 'unauthorized':
				#接受取消授权
				authorizerappid = xml_message.authorizerappid.text
				component_authed_appids = ComponentAuthedAppid.objects.filter(authorizer_appid=authorizerappid)
				if component_authed_appids.count() > 0:
					component_authed_appid = component_authed_appids[0]
					component_authed_appid.is_active = False
					component_authed_appid.save()
					user_id = component_authed_appid.user_id
					if WeixinMpUser.objects.filter(owner_id=user_id).count() > 0:
						mp_user = WeixinMpUser.objects.filter(owner_id=user_id)[0]
						mp_user.is_active = False
						mp_user.save()

						WeixinMpUserAccessToken.objects.filter(mpuser = mp_user).update(is_active=False)
					UserProfile.objects.filter(user_id=user_id).update(is_mp_registered=False)
		return HttpResponse('success')
	else:
		# 授权后的回调链接的响应函数，使用auth_code获取授权公众号的授权信息
		auth_code = request.GET.get('auth_code', None) # 授权码
		expires_in = request.GET.get('expires_in', None) # 过期时间

		if request.user.is_authenticated() and auth_code:
			request.user_profile = request.user.get_profile()
			webapp_id = request.user_profile.webapp_id
			user_id=request.user.id
			from weixin.user.util import get_component_info_from
			component_info = get_component_info_from(request) # 获取第三方开放平台的基本信息
			component_authed_appid = ComponentAuthedAppid.objects.get(component_info=component_info, user_id=user_id) # 获取用户委托的账户记录

			from core.wxapi.agent_weixin_api import WeixinApi, WeixinHttpClient
			weixin_http_client = WeixinHttpClient()
			weixin_api = WeixinApi(component_info.component_access_token, weixin_http_client)
			return_msg, mp_user = get_query_auth(component_info, weixin_api, auth_code, user_id)

			# 每个api请求如果失败就重试一次
			if return_msg == "success":
				is_success = get_authorizer_info(component_authed_appid, weixin_api, component_info, mp_user)
				if not is_success:
					get_authorizer_info(component_authed_appid, weixin_api, component_info, mp_user)
			else:
				return_msg, mp_user = get_query_auth(component_info, weixin_api, auth_code, user_id)
				if return_msg == "success":
					is_success = get_authorizer_info(component_authed_appid, weixin_api, component_info, mp_user)
					if not is_success:
						get_authorizer_info(component_authed_appid, weixin_api, component_info, mp_user)
			return HttpResponseRedirect('/new_weixin/mp_user/')

		else:
			raise Http404('请先登录系统，继续完成授权！')

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