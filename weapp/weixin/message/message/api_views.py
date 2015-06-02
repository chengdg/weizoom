# -*- coding: utf-8 -*-

__author__ = 'chuter'


import json
import weixin

from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.decorators import login_required

from core.paginator import paginate
from core import emotion
from core.exceptionutil import unicode_full_stack
from core.jsonresponse import JsonResponse, create_response
from core import dateutil
from models import *
from account.social_account.models import SocialAccount
from watchdog.utils import watchdog_notice,watchdog_error
from modules.member.models import Member,MemberHasSocialAccount
from weixin.user.models import is_subscribed, get_system_user_binded_mpuser, MpuserPreviewInfo, DEFAULT_ICON, WeixinUser


COUNT_PER_PAGE = 20
EXPIRED_TIME = 48

def __format_datetime(datetime):
	if type(datetime) == unicode:
		datetime = __parse_datetime_raw_string(datetime)
		
	year = datetime.strftime('%Y')
	month = datetime.strftime('%m').lstrip('0')
	day = datetime.strftime('%d').lstrip('0')
	month_day = '%s年%s月%s日' % (year, month, day)
	if int(datetime.strftime('%H')) == 0:
		hour_minute = datetime.strftime('0:%M:%S')
	else:
		hour_minute = datetime.strftime('%H:%M:%S')
	return '%s %s' % (month_day, hour_minute)


def __package_pageinfo(pageinfo):
	response = {
		'cur_page': pageinfo.cur_page,
		'display_pages': pageinfo.display_pages,
		'has_head': pageinfo.has_head,
		'has_next': pageinfo.has_next,
		'has_prev': pageinfo.has_prev,
		'has_tail': pageinfo.has_tail,
		'max_page': pageinfo.max_page,
		'next': pageinfo.next,
		'object_count': pageinfo.object_count,
		'prev': pageinfo.prev,
		'query_string': pageinfo.query_string
	}
	return response


########################################################################
# get_sessions: 获取会话列表
########################################################################
@login_required
def get_sessions(request):
	response = JsonResponse()
	response.code = 200
	response.data = JsonResponse()
	response.data.items = []

	mpuser = get_system_user_binded_mpuser(request.user)
	if mpuser is None:
		return response.get_response()

	#获取当前页数
	cur_page = int(request.GET.get('page', '1'))
	#获取每页个数
	count = int(request.GET.get('count', COUNT_PER_PAGE))
	
	is_debug = (request.GET.get('dbg', '0') == '1')
	#收藏记录
	is_collected = request.GET.get('is_collected', '0') 

	start_time = request.GET.get('start_time', '').strip()
	end_time = request.GET.get('end_time', '').strip()
	search_content = request.GET.get('search_content', '').strip()
	if is_debug:
		sessions = Session.objects.select_related().filter(mpuser=mpuser)
	else:
		sessions = Session.objects.select_related().filter(mpuser=mpuser, is_show=True)

	if start_time and end_time:
		start_time = '%s 0:0:0' % start_time
		end_time = '%s 23:59:59' % end_time
		sessions = sessions.filter(latest_contact_created_at__gte=start_time,latest_contact_created_at__lte=end_time)

	pageinfo, sessions = paginate(sessions, cur_page, count, query_string=request.META['QUERY_STRING'])

	#清空未读消息数量
	RealTimeInfo.objects.filter(mpuser=mpuser).update(unread_count = 0)
	
	webapp_id=request.user_profile.webapp_id
	weixin_user_usernames = [s.weixin_user_id for s in sessions]
	weixin_users = WeixinUser.objects.filter(username__in=weixin_user_usernames)
	username2weixin_user = dict([(u.username, u) for u in weixin_users])

	# session2member = dict([(member_has_social_account.account.openid, member_has_social_account.member) for member_has_social_account \
	# 	in MemberHasSocialAccount.objects.filter()])
	
	for session in sessions:
		weixin_user = username2weixin_user[session.weixin_user_id]
		one_session = JsonResponse()
		one_session.id = session.id
		one_session.session_id = session.id
		one_session.sender_fake_id = weixin_user.fake_id
		one_session.sender_username = weixin_user.username
		one_session.sender_name = weixin_user.nickname_for_html
		if weixin_user.weixin_user_icon:
			one_session.weixin_user_icon = weixin_user.weixin_user_icon if len(weixin_user.weixin_user_icon.strip()) > 0 else DEFAULT_ICON
		else:
			one_session.weixin_user_icon =  DEFAULT_ICON
		one_session.content = emotion.change_emotion_to_img(session.latest_contact_content)
		one_session.created_at = __format_datetime(session.latest_contact_created_at)
		one_session.unread_count = session.unread_count
		one_session.message_id = session.message_id
		one_session.is_collected = CollectMessage.is_collected(session.message_id) 
		one_session.for_collected = False
		one_session.hidden_a = False
		try:
			if session.message_id != 0:
				message = Message.objects.get(id=session.message_id)
				one_session.message_type = message.message_type
				one_session.pic_url = message.pic_url
				one_session.audio_url = message.audio_url
			else:
				one_session.message_type = 'text'
				one_session.pic_url = ''
				one_session.audio_url = ''
		except:
			one_session.message_type = 'text'
			one_session.pic_url = ''
			one_session.audio_url = ''

		one_session.is_subscribed = is_subscribed(weixin_user)
		one_session.is_active =  True if datetime.now() < session.latest_contact_created_at + timedelta(hours=EXPIRED_TIME) and datetime.now() > session.latest_contact_created_at else False
		try:
			account = SocialAccount.objects.get(webapp_id=webapp_id,openid=weixin_user.username)
			member = MemberHasSocialAccount.objects.filter(account=account)[0].member
			#member = session2member[session.weixin_user_id]
			if member:
				one_session.member_id = member.id
				one_session.member_remarks_name = member.remarks_name
				if member.user_icon and len(member.user_icon.strip()) > 0:
					one_session.weixin_user_icon = member.user_icon
				if member.username_for_html:
					one_session.sender_name = member.username_for_html
		except:
			notify_message = u"设置会话信息失败, weixin_user_openid:{}, webapp_id:{},cause:\n{}".format(
				session.weixin_user_id, webapp_id, unicode_full_stack())
			watchdog_notice(notify_message)
			continue

		response.data.items.append(one_session)
		response.data.page_info = __package_pageinfo(pageinfo)
	return response.get_response()

from core.wxapi import weixin_error_codes
from core.wxapi.weixin_api import WeixinApiError
@login_required
def send_custome_message(request):
	content = request.POST['text']
	openid_sendto = request.POST['openid']

	mpuser = get_system_user_binded_mpuser(request.user)
	if mpuser is None:
		response = create_response(500)
		response.errMsg = u'请先进行公众号的绑定'
	else:
		#进行实际消息的发送
		try:
			if openid_sendto and get_weixinuser_sessions(openid_sendto).count() > 0:
				session = get_weixinuser_sessions(openid_sendto)[0]
				is_active =  True if datetime.now() < session.latest_contact_created_at + timedelta(hours=EXPIRED_TIME) and datetime.now() > session.latest_contact_created_at else False
				if is_active:
					_send_custom_message(mpuser, openid_sendto, content)
					response = create_response(200)
				else:
					response = create_response(501)
					response.errMsg = u'互动已经超时'
			else:
				response = create_response(501)
				response.errMsg = u'互动已经超时'
		except WeixinApiError, error:
			response = create_response(500)

			error_code = error.error_response.errcode
			response.errMsg = weixin_error_codes.code2msg.get(error_code, error.error_response.errmsg)
			response.innerErrMsg = error.error_response.detail		
		except:
			response = create_response(500)
			response.errMsg = u'发送消息失败'
			response.innerErrMsg = unicode_full_stack()	

	return response.get_response()

########################################################################
# reply_session_write_back: 回复会话回写
########################################################################
@login_required
def reply_session_write_back(request):
	session_id = request.POST['session_id']
	content = request.POST['content']
	receiver_username = request.POST['receiver_username']
	
	receiver = WeixinUser.objects.get(username=receiver_username)
	mpuser = get_system_user_binded_mpuser(request.user)
	if mpuser is None:
		response = create_response(500)
		response.errMsg = u'请先进行公众号的绑定'

	Session.objects.filter(id=session_id).update(latest_contact_content=content, latest_contact_created_at=datetime.today(), is_latest_contact_by_viper=True, unread_count=0)
	Message.objects.create(mpuser=mpuser, session_id=session_id, 
		from_weixin_user_username=mpuser.username, 
		to_weixin_user_username=receiver_username, content=content, is_reply=True)
	
	return create_response(200).get_response()

from core.wxapi import get_weixin_api
from core.wxapi.custom_message import TextCustomMessage
from weixin.user.models import get_mpuser_access_token_for
def _send_custom_message(mpuser, send_to, content):
	mpuser_access_token = get_mpuser_access_token_for(mpuser)
	wxapi = get_weixin_api(mpuser_access_token)
	wxapi.send_custom_msg(send_to, TextCustomMessage(content))

########################################################################
# delete_session: 删除会话
########################################################################
@login_required
def delete_session(request):
	session_id = request.GET['session_id']
	Session.objects.filter(id=session_id).delete()

	response = JsonResponse()
	response.code = 200
	return response.get_response()

import util
########################################################################
# enable_session: 显示会话
########################################################################
def enable_session(request):
	return util.enable_session(request)

########################################################################
# get_session_histories: 获取会话对话历史
########################################################################
@login_required
def get_session_histories(request):
	session_id = request.GET['session_id']
	messages = Message.objects.filter(session=session_id).order_by('-id')
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
		return response.get_response()

	response = create_response(200)
	response.data.items = []
	session = Session.objects.get(id=session_id)
	webapp_id=request.user_profile.webapp_id
	is_active =  True if datetime.now() < session.latest_contact_created_at + timedelta(hours=EXPIRED_TIME) and datetime.now() > session.latest_contact_created_at else False
	response.data.is_active = is_active
	for message in messages:
		sender = username2weixin_user[message.from_weixin_user_username]
		one_message = JsonResponse()
		one_message.id = message.id
		one_message.weixin_message_id = message.weixin_message_id
		one_message.is_reply = message.is_reply
		one_message.content = emotion.change_emotion_to_img(message.content)
		if one_message.content == None:
			one_message.content = ''
		one_message.weixin_created_at = __format_datetime(message.weixin_created_at)
		one_message.is_collected = CollectMessage.is_collected(message.id)
		one_message.message_type = message.message_type
		one_message.pic_url = message.pic_url
		one_message.audio_url = message.audio_url

		if message.message_type == IMAGE:
			one_message.content = message.pic_url

		if message.message_type == VOICE:
			one_message.content = message.audio_url
		if message.is_reply:
			one_message.sender_icon = mpuser_preview_info.image_path#sender.weixin_user_icon
			one_message.sender_name = mpuser_preview_info.name
		else:
			account = SocialAccount.objects.get(webapp_id=webapp_id,openid=sender.username)
			member = MemberHasSocialAccount.objects.filter(account=account)[0].member
			if member:
				if member.user_icon:
					one_message.sender_icon = member.user_icon if len(member.user_icon.strip()) > 0 else DEFAULT_ICON
				else:
					one_message.sender_icon = DEFAULT_ICON
				one_message.sender_name = member.username_for_html
				one_message.member_id = member.id
				if one_message.sender_icon != sender.weixin_user_icon:
					sender.weixin_user_icon = member.user_icon
			else:
				if sender.weixin_user_icon:
					one_message.sender_icon = sender.weixin_user_icon if len(sender.weixin_user_icon.strip()) > 0 else DEFAULT_ICON
				one_message.sender_name = sender.weixin_user_nick_name
		response.data.items.append(one_message)

	return response.get_response()

########################################################################
# reset_realtime_unread_count: 重置实时未读消息数量
########################################################################
@login_required
def reset_realtime_unread_count(request):
	mpuser = get_system_user_binded_mpuser(request.user)

	if mpuser is None:
		return create_response(200).get_response()
	else:
		RealTimeInfo.objects.filter(mpuser=mpuser).update(unread_count = 0)

		return create_response(200).get_response()

from weixin.message.message.module_api import get_realtime_unread_count as get_realtime_unread_count_api
@login_required
def get_realtime_unread_count(request):
	try:
		unread_realtime_count = get_realtime_unread_count_api(request.user)

		response = create_response(200)
		response.data = {
			'unread_count': unread_realtime_count
			}
	except:
		response = create_response(500)
		response.innerErrMsg = unicode_full_stack()
	
	return response.get_response()


########################################################################
# collect_message: 收藏或取消消息
########################################################################
@login_required
def collect_message(request):
	response = create_response(201)
	if request.POST:
		message_id = request.POST.get('message_id', None)
		status = request.POST.get('status', None)
		if message_id and status and int(message_id) != 0:
			if CollectMessage.objects.filter(message_id=message_id).count() > 0:
				CollectMessage.objects.filter(message_id=message_id).update(status=int(status))
			else:
				CollectMessage.objects.create(message_id=message_id, status=int(status), owner=request.user)
			response = create_response(200)

	return response.get_response()

		
########################################################################
# get_messages: 获取消息
########################################################################
def get_messages(request):
	response = JsonResponse()
	response.code = 200
	response.data = JsonResponse()
	response.data.items = []

	mpuser = get_system_user_binded_mpuser(request.user)
	if mpuser is None:
		return response.get_response()

	#获取当前页数
	cur_page = int(request.GET.get('page', '1'))
	#获取每页个数
	count = int(request.GET.get('count', COUNT_PER_PAGE))
	
	is_debug = (request.GET.get('dbg', '0') == '1')
	
	is_collected = request.GET.get('is_collected', '')

	search_content = request.GET.get('search_content','')
	
	if is_collected:
		collected_message_ids = CollectMessage.get_message_ids(request.user)
		ordering = 'FIELD(`id`, %s)' % ','.join(str(id) for id in collected_message_ids)
		messages = Message.objects.filter(id__in=collected_message_ids).extra(
			select={'ordering': ordering}, order_by=('ordering',))
	elif search_content:
		data_before_tow_days = dateutil.get_previous_date('today', 2)
		messages = Message.objects.belong_to(request.user_profile.webapp_id, mpuser, search_content)
	else:
		messages = []
	pageinfo, messages = paginate(messages, cur_page, count, query_string=request.META['QUERY_STRING'])
	webapp_id = request.user_profile.webapp_id
	for message in messages:
		weixin_user = message.session.weixin_user
		one_session = JsonResponse()
		one_session.id = message.id
		one_session.session_id = message.session.id
		one_session.sender_fake_id = weixin_user.fake_id
		one_session.sender_username = weixin_user.username
		one_session.sender_name = weixin_user.nickname_for_html
		if weixin_user.weixin_user_icon:
			one_session.weixin_user_icon = weixin_user.weixin_user_icon if len(weixin_user.weixin_user_icon.strip()) > 0 else DEFAULT_ICON
		else:
			one_session.weixin_user_icon = DEFAULT_ICON

		one_session.content = emotion.change_emotion_to_img(message.content)
		one_session.is_active =  True if datetime.now() < message.created_at + timedelta(hours=EXPIRED_TIME) and datetime.now() > message.created_at else False
		if is_collected:
			one_session.is_active = False
			try:
				collect_message = CollectMessage.objects.get(message_id=message.id)
				one_session.created_at = __format_datetime(collect_message.created_at)
			except:
				one_session.created_at = __format_datetime(message.created_at)
		else:
			one_session.created_at = __format_datetime(message.created_at)
		one_session.message_id = message.id
		one_session.is_collected = CollectMessage.is_collected(message.id)
		one_session.message_type = message.message_type
		one_session.pic_url = message.pic_url
		one_session.audio_url = message.audio_url
		one_session.for_collected = is_collected
		one_session.hidden_a = True

		if message.message_type == IMAGE:
			one_session.content = message.pic_url

		if message.message_type == VOICE:
			one_session.content = message.audio_url

		one_session.is_subscribed = is_subscribed(weixin_user)
		
		try:
			account = SocialAccount.objects.get(webapp_id=webapp_id,openid=weixin_user.username)
			member = MemberHasSocialAccount.objects.filter(account=account)[0].member
			#member = session2member[session.weixin_user_id]
			if member:
				one_session.member_id = member.id
				one_session.member_remarks_name = member.remarks_name
				if member.user_icon and len(member.user_icon.strip()) > 0:
					one_session.weixin_user_icon = member.user_icon
				if member.username_for_html:
					one_session.sender_name = member.username_for_html
		except:
			notify_message = u"设置会话信息失败, weixin_user_openid:{}, cause:\n{}".format(
				session.weixin_user_id, unicode_full_stack())
			watchdog_notice(notify_message)

			continue

		response.data.items.append(one_session)
		response.data.page_info = __package_pageinfo(pageinfo)

	return response.get_response()
