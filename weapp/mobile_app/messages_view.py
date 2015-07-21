# -*- coding: utf-8 -*-
import json
import urllib
import os

from django.template import Context, RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render_to_response, render
from django.contrib.auth.models import User
from django.contrib import auth
from core.paginator import paginate

from account.models import *
from account.social_account.models import SocialAccount

import types
from datetime import datetime, timedelta

from core.exceptionutil import unicode_full_stack
from core.jsonresponse import JsonResponse, create_response
from core import paginator
from weixin.message.message.models import *
import emotion
from market_tools import export
from modules.member.models import Member,MemberHasSocialAccount
from weixin.user.models import is_subscribed, get_system_user_binded_mpuser, MpuserPreviewInfo, DEFAULT_ICON, WeixinUser

from account.views import save_and_zip_base64_img_file_for_mobileApp,save_audio_file_for_mobileApp,save_and_zip_img_file_for_muiApp
from account.util import get_binding_weixin_mpuser, get_mpuser_accesstoken
from emotion import TITLE2EMOTION, mui_change_emotion_style

def __package_pageinfo(pageinfo):
	response = {
		'has_next': pageinfo.has_next,
		'has_tail': pageinfo.has_tail,
		'max_page': pageinfo.max_page,
		'next': pageinfo.next,
		'query_string': pageinfo.query_string
	}
	return response

def __format_datetime(datetime):
	if type(datetime) == unicode:
		datetime = __parse_datetime_raw_string(datetime)

	year = datetime.strftime('%Y')
	month = datetime.strftime('%m').lstrip('0')
	day = datetime.strftime('%d').lstrip('0')
	month_day = '%s-%s' % (month, day)
	if int(datetime.strftime('%H')) == 0:
		hour_minute = datetime.strftime('0:%M:%S')
	else:
		hour_minute = datetime.strftime('%H:%M:%S')
	return '%s %s' % (month_day, hour_minute)

EXPIRED_TIME = 48 #消息回复期限

#所有用户的消息列表
# @login_required(login_url="/mobile_app/")
def list_messages(request):
	page = request.GET.get('page', 1)
	count = int(request.GET.get('count', 10))
	mpuser = get_system_user_binded_mpuser(request.user)
	isManager = request.GET.get('isManager', 'false')
	isSystemMenager = request.GET.get('isSystemMenager', 'false')
	if mpuser is None:
		response = create_response(500)
		response.errMsg = u'没有该用户的消息'
		return response.get_jsonp_response(request)

	sessions = Session.objects.select_related().filter(mpuser=mpuser, is_show=True)

	#分页信息
	pageinfo, sessions = paginate(sessions, page, count, query_string=request.META['QUERY_STRING'])
	webapp_id=request.user_profile.webapp_id

	if isManager == "false" and isSystemMenager == "false":
		#清空未读消息数量
		RealTimeInfo.objects.filter(mpuser=mpuser).update(unread_count = 0)

	weixin_user_usernames = [s.weixin_user_id for s in sessions]
	weixin_users = WeixinUser.objects.filter(username__in=weixin_user_usernames)
	username2weixin_user = dict([(u.username, u) for u in weixin_users])
	sessions_list_json = []
	for session in sessions:
		weixin_user = username2weixin_user[session.weixin_user_id]
		content = session.latest_contact_content
		one_session = JsonResponse()
		one_session.id = session.id
		one_session.sender_fake_id = weixin_user.fake_id
		one_session.sender_username = weixin_user.username
		one_session.sender_name = weixin_user.nickname_for_html
		one_session.weixin_user_icon = weixin_user.weixin_user_icon if len(weixin_user.weixin_user_icon.strip()) > 0 else DEFAULT_ICON
		messages = Message.objects.filter(session=session.id).order_by('-created_at')
		message_st_type = messages[0].message_type
		if message_st_type == 'text':
			if len(content) > 10:
				content = content[0:10] + '...'
			elif len(content.strip())<=0:#如果类型为text但是内容为空，则视为voice，有问题？
				content = '[语音]'
		elif message_st_type == 'image':
			content = '[图片]'
		elif message_st_type == 'voice':
			content = '[语音]'
		elif message_st_type == 'video':
			content = '[视频]'
		one_session.content = content
		one_session.created_at = __format_datetime(session.latest_contact_created_at)
		one_session.unread_count = session.unread_count
		one_session.is_subscribed = is_subscribed(weixin_user)
		one_session.is_active = True if datetime.now() < session.latest_contact_created_at + timedelta(hours=EXPIRED_TIME) and datetime.now() > session.latest_contact_created_at else False

		try:
			account = SocialAccount.objects.get(webapp_id=webapp_id,openid=weixin_user.username)
			member = MemberHasSocialAccount.objects.filter(account=account)[0].member
			# member = Member.get_member_by_weixin_user_id(weixin_user.id)
			if member:
				one_session.member_id = member.id
				one_session.member_remarks_name = member.remarks_name
				if len(member.user_icon.strip()) > 0:
					one_session.weixin_user_icon = member.user_icon
				if member.username_for_html:
					one_session.sender_name = member.username_for_html
		except:
			# notify_message = u"设置会话信息失败, weixin_user_openid:{}, cause:\n{}".format(
			# 	session.weixin_user_id, unicode_full_stack())
			# watchdog_notice(notify_message)
			continue
			#raise
		sessions_list_json.append(one_session)
	response = create_response(200)
	response.data.iterms = sessions_list_json
	response.data.pressed_link = 'message'
	response.data.page_info = __package_pageinfo(pageinfo)
	return response.get_jsonp_response(request)

#单用户的消息历史
# @login_required(login_url="/mobile_app/")
def get_session_histories(request):
	session_id = request.GET['s_id']
	current_page = int(request.GET.get('cur_page', '1'))
	count = int(request.GET.get('count', 10))
	isManager = request.GET.get('isManager', 'false')
	isSystemMenager = request.GET.get('isSystemMenager', 'false')
	# user_id = request.GET['user_id']
	session = Session.objects.get(id=session_id)
	messages = Message.objects.filter(session=session_id).order_by('-id')
	#进行分页
	pageinfo, messages = paginator.paginate(messages, current_page, count)

	sender_usernames = [m.from_weixin_user_username for m in messages]
	recevier_usernames = [m.to_weixin_user_username for m in messages]
	weixin_user_usernames = set(sender_usernames + recevier_usernames)
	weixin_users = WeixinUser.objects.filter(username__in=weixin_user_usernames)
	username2weixin_user = dict([u.username, u] for u in weixin_users)

	mpuser = get_system_user_binded_mpuser(request.user)

	try:
		mpuser_preview_info = MpuserPreviewInfo.objects.get(mpuser=mpuser)
	except:
		response = create_response(500)
		response.errMsg = u'获取公众号预览信息失败'
		return response.get_jsonp_response(request)
	if isManager == "false" and isSystemMenager == "false":
		#清空未读消息
		Session.objects.filter(mpuser=mpuser,id=session_id).update(unread_count=0)
	sender_name_response = ""
	messages_list_json = []
	is_active =  True if datetime.now() < session.latest_contact_created_at + timedelta(hours=EXPIRED_TIME) and datetime.now() > session.latest_contact_created_at else False
	for message in reversed(messages):
		sender = username2weixin_user[message.from_weixin_user_username]
		one_message = JsonResponse()
		one_message.id = message.id
		one_message.weixin_message_id = message.weixin_message_id
		one_message.is_reply = message.is_reply
		one_message.message_type = message.message_type
		one_message.pic_url = message.pic_url
		one_message.audio_url = message.audio_url
		one_message.content = emotion.change_emotion_to_img(message.content)
		one_message.weixin_created_at = __format_datetime(message.weixin_created_at)

		if message.is_reply:
			one_message.sender_icon = mpuser_preview_info.image_path
			one_message.sender_name = mpuser_preview_info.name
		else:
			member = Member.get_member_by_weixin_user_id(sender.id)
			if member:
				one_message.sender_icon = member.user_icon if len(member.user_icon.strip()) > 0 else DEFAULT_ICON
				one_message.sender_name = member.username_for_html
				sender_name_response = one_message.sender_name
				if one_message.sender_icon != sender.weixin_user_icon:
					sender.weixin_user_icon = member.user_icon
			else:
				one_message.sender_icon = sender.weixin_user_icon if len(sender.weixin_user_icon.strip()) > 0 else DEFAULT_ICON
				one_message.sender_name = sender.weixin_user_nick_name
		messages_list_json.append(one_message)

	response = create_response(200)
	response.data = messages_list_json
	response.is_login = True
	response.is_active = is_active
	response.session_id = session_id
	response.weixin_user_id = session.weixin_user_id
	response.pressed_link = 'message'
	response.send_user_name = sender_name_response if sender_name_response != "" else session.weixin_user.weixin_user_nick_name
	response.page_info = __package_pageinfo(pageinfo)
	return response.get_jsonp_response(request)

#回复消息
# @login_required(login_url="/mobile_app/")
def reply_session(request):
	session_id = request.GET['s_id']
	# user_id = request.GET['user_id']
	content = mui_change_emotion_style(urllib.unquote(request.GET['cont']))
	receiver_username = request.GET['r_u']
	receiver = WeixinUser.objects.get(username=receiver_username)
	mpuser = get_system_user_binded_mpuser(request.user)
	if mpuser is None:
		response = create_response(500)
		response.errMsg = u'请先进行公众号的绑定'
	#回复用户消息
	return_flag = send_custome_message(content,receiver_username,mpuser)
	if not return_flag :
		response = create_response(500)
		response.errMsg = u'发送消息失败'
	else :
		#存储数据库
		Session.objects.filter(id=session_id).update(latest_contact_content=content, latest_contact_created_at=datetime.today(), is_latest_contact_by_viper=True, unread_count=0)
		Message.objects.create(mpuser=mpuser, session_id=session_id,
			from_weixin_user_username=mpuser.username,
			to_weixin_user_username=receiver_username, content=content, is_reply=True)
		response = create_response(200)
	return response.get_jsonp_response(request)

def send_custome_message(content,openid_sendto,mpuser):
	try:
		if openid_sendto and get_weixinuser_sessions(openid_sendto).count() > 0:
			session = get_weixinuser_sessions(openid_sendto)[0]
			is_active =  True if datetime.now() < session.latest_contact_created_at + timedelta(hours=EXPIRED_TIME) and datetime.now() > session.latest_contact_created_at else False
			if is_active:
				_send_custom_message(mpuser, openid_sendto, content)
	except:
		return False
	return True

from core.wxapi import get_weixin_api
from core.wxapi.custom_message import TextCustomMessage,ImageCustomMessage,VoiceCustomMessage
from weixin.user.models import get_mpuser_access_token_for
def _send_custom_message(mpuser, send_to, content):
	mpuser_access_token = get_mpuser_access_token_for(mpuser)
	wxapi = get_weixin_api(mpuser_access_token)
	wxapi.send_custom_msg(send_to, TextCustomMessage(content))

from weixin.message.message.module_api import get_realtime_unread_count as get_realtime_unread_count_api
# @login_required
def get_realtime_unread_count(request):
	try:
		unread_realtime_count = get_realtime_unread_count_api(request.user)
		response = create_response(200)
		response.data = {
			'unread_count': unread_realtime_count
			}
	except:
		#TODO:异常处理
		response = create_response(200)
		response.data = {
			'unread_count': 0
			}

	return response.get_jsonp_response(request)

########################################################################
# send_media: 发送图片、音频
########################################################################
def send_media(request):
	# 上传图片到云
	response = create_CORS_response(200,'','')
	file = request.POST.get('src')
	media_type = request.POST.get('type')
	receiver_username = request.POST.get('r_u')
	session_id = request.POST.get('s_id')
	domain = request.POST.get('domain')
	user = User.objects.get(id=int(request.POST.get('user')))
	user_profile = user.get_profile()
	request.user = user
	request.user_profile = user_profile
	mpuser = get_system_user_binded_mpuser(request.user)
	try:
		if user:
			try:
				mpuser_access_token = get_mpuser_access_token_for(mpuser)
				weixin_api = get_weixin_api(mpuser_access_token)
			except:
				response = create_CORS_response(500,u'微信公众号授权出错','')
				print response
				return response
		else:
			response = create_CORS_response(500,u'用户登陆信息出错','')
			return response
		upload_value = ''
		if file and media_type:
			if media_type == 'image':
				# 尝试上传图片到云，成功则返回云路径，否则返回服务器存储路径
				value = save_and_zip_base64_img_file_for_mobileApp(request, file)
				if not value:
					response = create_CORS_response(500,u'上传云失败','')
					return response
				if value.startswith('/') and value.find('http') == -1:
					upload_value = os.path.join(settings.PROJECT_HOME, '../', value[1:])
					value = '%s%s' % (domain,value)
				else:
					upload_value = value
				#上传到微信服务器
				result_info = weixin_api.upload_media_image(upload_value, True)
				if not result_info:
					response = create_CORS_response(500,u'发送图片失败,请重试..','')
					return response
				# 发送给用户
				res = weixin_api.send_custom_msg(receiver_username, ImageCustomMessage(result_info['media_id']))
				# 存储数据库
				Session.objects.filter(id=session_id).update(latest_contact_content='[图片]', latest_contact_created_at=datetime.today(), is_latest_contact_by_viper=True, unread_count=0)
				Message.objects.create(mpuser=mpuser, session_id=session_id,
					from_weixin_user_username=mpuser.username,
					to_weixin_user_username=receiver_username,
					pic_url=value,
					message_type='image',
					media_id=result_info['media_id'],
					content='',
					is_reply=True)
				response = create_CORS_response(200,'','')
			elif media_type == 'voice':
				# 尝试上传语音到云，成功则返回云路径，否则返回服务器存储路径
				file = request.FILES.get('file',None)
				if not file:
					response = create_CORS_response(500,u'不存在该文件','')
				value = save_audio_file_for_mobileApp(request, file)
				if not value:
					response = create_CORS_response(500,u'mp3文件没有找到','')
					return response

				if value.startswith('/') and value.find('http') == -1:
					upload_value = os.path.join(settings.PROJECT_HOME, '../', value[1:])
					value = '%s%s' % (domain,value)
				else:
					upload_value = value
				#上传到微信服务器
				result_info = weixin_api.upload_media_voice(upload_value, True)
				if not result_info:
					response = create_CORS_response(500,u'发送语音失败,请重试..','')
					return response
				# 发送给用户
				res = weixin_api.send_custom_msg(receiver_username, VoiceCustomMessage(result_info['media_id']))
				# 存储数据库
				Session.objects.filter(id=session_id).update(latest_contact_content='[语音]', latest_contact_created_at=datetime.today(), is_latest_contact_by_viper=True, unread_count=0)
				Message.objects.create(mpuser=mpuser, session_id=session_id,
					from_weixin_user_username=mpuser.username,
					to_weixin_user_username=receiver_username,
					audio_url=value,
					message_type='voice',
					media_id=result_info['media_id'],
					content='',
					is_reply=True)
				response = create_CORS_response(200,'','')
	except Exception:
		response = create_CORS_response(500,u'发送失败','')
	return response

def _get_mpuser_access_token(user):
	mp_user = get_binding_weixin_mpuser(user)
	if mp_user:
		mpuser_access_token = get_mpuser_accesstoken(mp_user)
	else:
		return False

	if mpuser_access_token is None:
		return False

	if mpuser_access_token.is_active:
		return mpuser_access_token
	else:
		return None

def create_CORS_response(code,errMsg,innerErrMsg):
	response = create_response(code)
	response.code = code
	response.errMsg = errMsg
	response.innerErrMsg =innerErrMsg
	if code == 200:
		response.success = True
	response.data = {}
	response = response.get_response()
	response['Access-Control-Allow-Origin'] = '*'
	response['Access-Control-Allow-Credentials'] = True
	return response

######################################################
# mui版本接口
######################################################
#所有用户的消息列表
# @login_required(login_url="/mobile_app/")
def mui_list_messages(request):
	page = request.GET.get('page', 1)
	count = int(request.GET.get('count', 10))
	mpuser = get_system_user_binded_mpuser(request.user)
	isManager = request.GET.get('isManager', 'false')
	isSystemMenager = request.GET.get('isSystemMenager', 'false')
	if mpuser is None:
		response = create_response(500)
		response.errMsg = u'没有该用户的消息'
		return response.get_jsonp_response(request)

	sessions = Session.objects.select_related().filter(mpuser=mpuser, is_show=True)

	#分页信息
	pageinfo, sessions = paginate(sessions, page, count, query_string=request.META['QUERY_STRING'])
	webapp_id=request.user_profile.webapp_id

	if isManager == "false" and isSystemMenager == "false":
		#清空未读消息数量
		RealTimeInfo.objects.filter(mpuser=mpuser).update(unread_count = 0)

	weixin_user_usernames = [s.weixin_user_id for s in sessions]
	weixin_users = WeixinUser.objects.filter(username__in=weixin_user_usernames)
	username2weixin_user = dict([(u.username, u) for u in weixin_users])
	sessions_list_json = []
	for session in sessions:
		weixin_user = username2weixin_user[session.weixin_user_id]
		content = session.latest_contact_content
		one_session = JsonResponse()
		one_session.id = session.id
		one_session.sender_fake_id = weixin_user.fake_id
		one_session.sender_username = weixin_user.username
		one_session.sender_name = weixin_user.nickname_for_html
		one_session.weixin_user_icon = weixin_user.weixin_user_icon if len(weixin_user.weixin_user_icon.strip()) > 0 else DEFAULT_ICON
		messages = Message.objects.filter(session=session.id).order_by('-created_at')
		message_st_type = messages[0].message_type
		if message_st_type == 'text':
			# if len(content) > 10:
			# 	count = 0 #计数
			# 	index = 0 #
			#
			# 	showcontent = "" #显示的消息
			# 	while count < 10 and index < len(content):
			# 		if content[index] == '/':
			# 			for i in range(1, 10):
			# 				emotion_title = content[index+1:index+1+i]
			# 				if emotion_title in TITLE2EMOTION:
			# 					emotion_png = '<img src="../img/weixin/%s" width="20px" />' % TITLE2EMOTION[emotion_title]
			# 					showcontent += emotion_png
			# 					count += 4
			# 					index += len(emotion_title) + 1
			# 					break
			# 		else:
			# 			showcontent += content[index]
			# 			index += 1
			# 			count += 1
			# 	if index >= len(content):
			# 		content = showcontent
			# 	else:
			# 		content = showcontent + '...'
			# elif len(content.strip())<=0:#如果类型为text但是内容为空，则视为voice，有问题？
			# 	content = '[语音]'
			# else:
			# 	content = emotion.mui_change_emotion_to_img(content)
			if len(content.strip())<=0:#如果类型为text但是内容为空，则视为voice，有问题？
				content = '[语音]'
			else:
				content = emotion.mui_change_emotion_to_img(content)
		elif message_st_type == 'image':
			content = '[图片]'
		elif message_st_type == 'voice':
			content = '[语音]'
		elif message_st_type == 'video':
			content = '[视频]'
		one_session.content = content
		one_session.created_at = __format_datetime(session.latest_contact_created_at)
		one_session.unread_count = session.unread_count
		one_session.is_subscribed = is_subscribed(weixin_user)
		one_session.is_active = True if datetime.now() < session.latest_contact_created_at + timedelta(hours=EXPIRED_TIME) and datetime.now() > session.latest_contact_created_at else False

		try:
			account = SocialAccount.objects.get(webapp_id=webapp_id,openid=weixin_user.username)
			member = MemberHasSocialAccount.objects.filter(account=account)[0].member
			# member = Member.get_member_by_weixin_user_id(weixin_user.id)
			if member:
				one_session.member_id = member.id
				one_session.member_remarks_name = member.remarks_name
				if len(member.user_icon.strip()) > 0:
					one_session.weixin_user_icon = member.user_icon
				if member.username_for_html:
					one_session.sender_name = member.username_for_html
		except:
			# notify_message = u"设置会话信息失败, weixin_user_openid:{}, cause:\n{}".format(
			# 	session.weixin_user_id, unicode_full_stack())
			# watchdog_notice(notify_message)
			# continue
			raise
		sessions_list_json.append(one_session)
	response = create_response(200)
	response.data.iterms = sessions_list_json
	response.data.pressed_link = 'message'
	response.data.page_info = __package_pageinfo(pageinfo)
	return response.get_jsonp_response(request)

#单用户的消息历史
# @login_required(login_url="/mobile_app/")
def mui_get_session_histories(request):
	session_id = request.GET['s_id']
	current_page = int(request.GET.get('cur_page', '1'))
	count = int(request.GET.get('count', 10))
	isManager = request.GET.get('isManager', 'false')
	isSystemMenager = request.GET.get('isSystemMenager', 'false')
	# user_id = request.GET['user_id']
	session = Session.objects.get(id=session_id)
	messages = Message.objects.filter(session=session_id).order_by('-id')
	#进行分页
	pageinfo, messages = paginator.paginate(messages, current_page, count)

	sender_usernames = [m.from_weixin_user_username for m in messages]
	recevier_usernames = [m.to_weixin_user_username for m in messages]
	weixin_user_usernames = set(sender_usernames + recevier_usernames)
	weixin_users = WeixinUser.objects.filter(username__in=weixin_user_usernames)
	username2weixin_user = dict([u.username, u] for u in weixin_users)

	mpuser = get_system_user_binded_mpuser(request.user)

	try:
		mpuser_preview_info = MpuserPreviewInfo.objects.get(mpuser=mpuser)
	except Exception,e:
		print e.message
		response = create_response(500)
		response.errMsg = u'获取公众号预览信息失败'
		return response.get_jsonp_response(request)
	if isManager == "false" and isSystemMenager == "false":
		#清空未读消息
		Session.objects.filter(mpuser=mpuser,id=session_id).update(unread_count=0)
	sender_name_response = ""
	messages_list_json = []
	is_active =  True if datetime.now() < session.latest_contact_created_at + timedelta(hours=EXPIRED_TIME) and datetime.now() > session.latest_contact_created_at else False
	for message in reversed(messages):
		sender = username2weixin_user[message.from_weixin_user_username]
		one_message = JsonResponse()
		one_message.id = message.id
		one_message.weixin_message_id = message.weixin_message_id
		one_message.is_reply = message.is_reply
		one_message.message_type = message.message_type
		one_message.pic_url = message.pic_url
		one_message.audio_url = message.audio_url
		one_message.content = emotion.mui_change_emotion_to_img(message.content)
		one_message.weixin_created_at = __format_datetime(message.weixin_created_at)

		if message.is_reply:
			one_message.sender_icon = mpuser_preview_info.image_path
			one_message.sender_name = mpuser_preview_info.name
		else:
			member = Member.get_member_by_weixin_user_id(sender.id)
			if member:
				one_message.sender_icon = member.user_icon if len(member.user_icon.strip()) > 0 else DEFAULT_ICON
				one_message.sender_name = member.username_for_html
				sender_name_response = one_message.sender_name
				if one_message.sender_icon != sender.weixin_user_icon:
					sender.weixin_user_icon = member.user_icon
			else:
				one_message.sender_icon = sender.weixin_user_icon if len(sender.weixin_user_icon.strip()) > 0 else DEFAULT_ICON
				one_message.sender_name = sender.weixin_user_nick_name
		messages_list_json.append(one_message)

	response = create_response(200)
	response.data = messages_list_json
	response.is_login = True
	response.is_active = is_active
	response.session_id = session_id
	response.weixin_user_id = session.weixin_user_id
	response.pressed_link = 'message'
	response.send_user_name = sender_name_response if sender_name_response != "" else session.weixin_user.weixin_user_nick_name
	response.page_info = __package_pageinfo(pageinfo)
	return response.get_jsonp_response(request)


########################################################################
# send_mui_media: 发送图片、音频
########################################################################
def send_mui_media(request):
	# 上传图片到云
	uploadAction = request.POST.get('action',None)
	response = create_CORS_response(200,'','')
	if uploadAction and uploadAction == 'query':
		return response
	filename = request.POST.get('filename')
	media_type = request.POST.get('type')
	receiver_username = request.POST.get('r_u')
	session_id = request.POST.get('s_id')
	domain = request.POST.get('domain')
	user = User.objects.get(id=request.POST.get('user'))
	user_profile = user.get_profile()
	request.user = user
	request.user_profile = user_profile
	mpuser = get_system_user_binded_mpuser(request.user)
	try:
		if user:
			try:
				mpuser_access_token = get_mpuser_access_token_for(mpuser)
				weixin_api = get_weixin_api(mpuser_access_token)
			except:
				response = create_CORS_response(500,u'微信公众号授权出错','')
				return response
		else:
			response = create_CORS_response(500,u'用户登陆信息出错','')
			return response
		upload_value = ''
		if filename and media_type:
			if media_type == 'image':
				# 尝试上传图片到云，成功则返回云路径，否则返回服务器存储路径
				value = save_and_zip_img_file_for_muiApp(request, filename)
				if not value:
					response = create_CORS_response(500,u'上传云失败','')
					return response
				if value.startswith('/') and value.find('http') == -1:
					upload_value = os.path.join(settings.PROJECT_HOME, '../', value[1:])
					value = '%s%s' % (domain,value)
				else:
					upload_value = value
				#上传到微信服务器
				result_info = weixin_api.upload_media_image(upload_value, True)
				if not result_info:
					response = create_CORS_response(500,u'发送图片失败,请重试..','')
					return response
				# 发送给用户
				res = weixin_api.send_custom_msg(receiver_username, ImageCustomMessage(result_info['media_id']))
				# 存储数据库
				Session.objects.filter(id=session_id).update(latest_contact_content='[图片]', latest_contact_created_at=datetime.today(), is_latest_contact_by_viper=True, unread_count=0)
				Message.objects.create(mpuser=mpuser, session_id=session_id,
					from_weixin_user_username=mpuser.username,
					to_weixin_user_username=receiver_username,
					pic_url=value,
					message_type='image',
					media_id=result_info['media_id'],
					content='',
					is_reply=True)
				response = create_CORS_response(200,'','')
			elif media_type == 'voice':
				# 尝试上传语音到云，成功则返回云路径，否则返回服务器存储路径
				file = request.FILES.get('upload_file',None)
				if not file:
					response = create_CORS_response(500,u'不存在该文件','')
				value = save_audio_file_for_mobileApp(request, file)
				if not value:
					response = create_CORS_response(500,u'mp3文件没有找到','')
					return response

				if value.startswith('/') and value.find('http') == -1:
					upload_value = os.path.join(settings.PROJECT_HOME, '../', value[1:])
					value = '%s%s' % (domain,value)
				else:
					upload_value = value
				#上传到微信服务器
				result_info = weixin_api.upload_media_voice(upload_value, True)
				if not result_info:
					response = create_CORS_response(500,u'发送语音失败,请重试..','')
					return response
				# 发送给用户
				res = weixin_api.send_custom_msg(receiver_username, VoiceCustomMessage(result_info['media_id']))
				# 存储数据库
				Session.objects.filter(id=session_id).update(latest_contact_content='[语音]', latest_contact_created_at=datetime.today(), is_latest_contact_by_viper=True, unread_count=0)
				Message.objects.create(mpuser=mpuser, session_id=session_id,
					from_weixin_user_username=mpuser.username,
					to_weixin_user_username=receiver_username,
					audio_url=value,
					message_type='voice',
					media_id=result_info['media_id'],
					content='',
					is_reply=True)
				response = create_CORS_response(200,'','')
	except Exception:
		response = create_CORS_response(500,u'发送失败','')
	return response

########################################################################
# mui_get_additional_histories: 获取新的消息
########################################################################
def mui_get_additional_histories(request):
	end_id = request.GET['end_id']
	session_id = request.GET['s_id']
	current_page = 1
	count = int(request.GET.get('count', 10))
	isManager = request.GET.get('isManager', 'false')
	isSystemMenager = request.GET.get('isSystemMenager', 'false')
	# user_id = request.GET['user_id']
	session = Session.objects.get(id=session_id)
	messages = Message.objects.filter(session=session_id).order_by('-id')
	#进行分页
	pageinfo, messages = paginator.paginate(messages, current_page, count)

	sender_usernames = [m.from_weixin_user_username for m in messages]
	recevier_usernames = [m.to_weixin_user_username for m in messages]
	weixin_user_usernames = set(sender_usernames + recevier_usernames)
	weixin_users = WeixinUser.objects.filter(username__in=weixin_user_usernames)
	username2weixin_user = dict([u.username, u] for u in weixin_users)

	mpuser = get_system_user_binded_mpuser(request.user)

	try:
		mpuser_preview_info = MpuserPreviewInfo.objects.get(mpuser=mpuser)
	except:
		response = create_response(500)
		response.errMsg = u'获取公众号预览信息失败'
		return response.get_jsonp_response(request)
	if isManager == "false" and isSystemMenager == "false":
		#清空未读消息
		Session.objects.filter(mpuser=mpuser,id=session_id).update(unread_count=0)
	sender_name_response = ""
	messages_list_json = []
	is_active =  True if datetime.now() < session.latest_contact_created_at + timedelta(hours=EXPIRED_TIME) and datetime.now() > session.latest_contact_created_at else False

	r_messages = []

	for message in messages:
		if message.id == end_id:
			break
		else:
			r_messages.append(message)

	if not r_messages:
		response = create_response(500)
		return response.get_jsonp_response(request)

	for message in reversed(r_messages):
		sender = username2weixin_user[message.from_weixin_user_username]
		one_message = JsonResponse()
		one_message.id = message.id
		one_message.weixin_message_id = message.weixin_message_id
		one_message.is_reply = message.is_reply
		one_message.message_type = message.message_type
		one_message.pic_url = message.pic_url
		one_message.audio_url = message.audio_url
		one_message.content = emotion.mui_change_emotion_to_img(message.content)
		one_message.weixin_created_at = __format_datetime(message.weixin_created_at)

		if message.is_reply:
			one_message.sender_icon = mpuser_preview_info.image_path
			one_message.sender_name = mpuser_preview_info.name
		else:
			member = Member.get_member_by_weixin_user_id(sender.id)
			if member:
				one_message.sender_icon = member.user_icon if len(member.user_icon.strip()) > 0 else DEFAULT_ICON
				one_message.sender_name = member.username_for_html
				sender_name_response = one_message.sender_name
				if one_message.sender_icon != sender.weixin_user_icon:
					sender.weixin_user_icon = member.user_icon
			else:
				one_message.sender_icon = sender.weixin_user_icon if len(sender.weixin_user_icon.strip()) > 0 else DEFAULT_ICON
				one_message.sender_name = sender.weixin_user_nick_name
		messages_list_json.append(one_message)

	response = create_response(200)
	response.data = messages_list_json
	response.is_login = True
	response.is_active = is_active
	response.session_id = session_id
	response.weixin_user_id = session.weixin_user_id
	response.pressed_link = 'message'
	response.send_user_name = sender_name_response if sender_name_response != "" else session.weixin_user.weixin_user_nick_name
	response.page_info = __package_pageinfo(pageinfo)
	response.r_messages_count = len(r_messages)
	return response.get_jsonp_response(request)
