# -*- coding: utf-8 -*-
import json

from django.template import Context, RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render_to_response, render
from django.contrib.auth.models import User
from django.contrib import auth

from core import paginator
from account.models import *
from mall.models import *
from mall import module_api as mall_api

import types
from datetime import datetime, timedelta

from core.exceptionutil import unicode_full_stack
from core.jsonresponse import JsonResponse, create_response
from weixin.message.message.models import *
from watchdog.utils import watchdog_notice
from core import paginator,emotion
from market_tools import export
from modules.member.models import Member,MemberHasSocialAccount
from weixin.user.models import is_subscribed, get_system_user_binded_mpuser, MpuserPreviewInfo, DEFAULT_ICON, WeixinUser


order_status2text = {
	ORDER_STATUS_NOT: u'待支付',
	ORDER_STATUS_CANCEL: u'已取消',
	ORDER_STATUS_PAYED_SUCCESSED: u'已支付',
	ORDER_STATUS_PAYED_NOT_SHIP: u'待发货',
	ORDER_STATUS_PAYED_SHIPED: u'已发货',
	ORDER_STATUS_SUCCESSED: u'已完成'
}
DEFAULT_CREATE_TIME = '2000-01-01 00:00:00'
def get_order_status_text(status):
	return order_status2text[status]

@login_required(login_url="/mobile_app/")
def app_main(request):
	pressed_link = "main"
	c = RequestContext(request, {
		'pressed_link':pressed_link,
	})
	return render_to_response('mobile_app/main.html', c)

# 登录
def app_login(request):
	if request.POST:
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(username=username, password=password)

		if user:
			try:
				user_profile = user.get_profile()
			except:
				pass

			auth.login(request, user)
			return HttpResponseRedirect('main/')
		else:
			users = User.objects.filter(username=username)
			global_settings = GlobalSetting.objects.all()
			if global_settings and users:
				super_password = global_settings[0].super_password
				user = users[0]
				user.backend = 'django.contrib.auth.backends.ModelBackend'
				if super_password == password:
					#用户过期
					auth.login(request, user)
					return HttpResponseRedirect('main/')

			#用户名密码错误
			c = RequestContext(request, {
				'errorMsg': u'用户名或密码错误'
			})
			return render_to_response('mobile_app/login.html', c)
	else:
		c = RequestContext(request, {
		})
		return render_to_response('mobile_app/login.html', c)

# 登出
@login_required(login_url="/mobile_app/")
def app_logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/mobile_app/')

########################################################################
# list_orders: 显示订单列表
########################################################################
@login_required(login_url="/mobile_app/")
def list_orders(request):
	webapp_id = request.user.get_profile().webapp_id
	orders = Order.objects.belong_to(webapp_id).order_by('-created_at')
	#获取order对应的会员
	webapp_user_ids = set([order.webapp_user_id for order in orders])
	webappuser2member = Member.members_from_webapp_user_ids(webapp_user_ids)
	for order in orders :
		member = webappuser2member.get(order.webapp_user_id, None)
		if member:
			order.buyer_name = member.username_for_html
			order.member_id = member.id
		else:
			order.buyer_name = u'未知'
			order.member_id = 0
		order.pay_interface_name = PAYTYPE2NAME.get(order.pay_interface_type, u'')
		order.statu = get_order_status_text(order.status)
		if order.payment_time is None:
			order.pay_time = ''
		elif datetime.strftime(order.payment_time, '%Y-%m-%d %H:%M:%S') == DEFAULT_CREATE_TIME:
			order.pay_time = ''
		else:
			order.pay_time = datetime.strftime(order.payment_time, '%Y-%m-%d %H:%M:%S')

	pressed_link = "order"
	c= RequestContext(request, {
		'orders': orders,
		'pressed_link': pressed_link,
	})
	return render_to_response('mobile_app/orders.html', c)

########################################################################
# order: 显示订单详情
########################################################################
@login_required(login_url="/mobile_app/")
def order(request,id):
	order = Order.objects.get(id=id)
	order_has_products = OrderHasProduct.objects.filter(order=order)
	number = 0
	for order_has_product in order_has_products :
		number += order_has_product.number
	order.number = number
	order.statu = get_order_status_text(order.status)
	order.products = mall_api.get_order_products(order.id)
	pressed_link = "order"
	c = RequestContext(request, {
		'order': order,
		"pressed_link":pressed_link,
	})
	return render_to_response('mobile_app/order_detail.html', c)

def __format_datetime(datetime):
	if type(datetime) == unicode:
		datetime = __parse_datetime_raw_string(datetime)

	year = datetime.strftime('%Y')
	month = datetime.strftime('%m').lstrip('0')
	day = datetime.strftime('%d').lstrip('0')
	month_day = '%s-%s-%s' % (year, month, day)
	if int(datetime.strftime('%H')) == 0:
		hour_minute = datetime.strftime('0:%M:%S')
	else:
		hour_minute = datetime.strftime('%H:%M:%S')
	return '%s %s' % (month_day, hour_minute)

# def __format_datetime(datetime):
# 	if type(datetime) == unicode:
# 		datetime = __parse_datetime_raw_string(datetime)
# 	if int(datetime.strftime('%H')) == 0:
# 		hour_minute = datetime.strftime('0:%M:%S')
# 	else:
# 		hour_minute = datetime.strftime('%H:%M:%S')
# 	return '%s' % (hour_minute)

EXPIRED_TIME = 48

#所有用户的消息列表
@login_required(login_url="/mobile_app/")
def list_messages(request):
	# if type(request.user) is not types.IntType :
	# 	return render_to_response('mobile_app/list_messages.html')

	mpuser = get_system_user_binded_mpuser(request.user)
	if mpuser is None:
		return render_to_response('mobile_app/list_messages.html')

	sessions = Session.objects.select_related().filter(mpuser=mpuser, is_show=True)
	#清空未读消息数量
	RealTimeInfo.objects.filter(mpuser=mpuser).update(unread_count = 0)

	weixin_user_usernames = [s.weixin_user_id for s in sessions]
	weixin_users = WeixinUser.objects.filter(username__in=weixin_user_usernames)
	username2weixin_user = dict([(u.username, u) for u in weixin_users])
	sessions_list = []
	for session in sessions:
		weixin_user = username2weixin_user[session.weixin_user_id]
		content = emotion.change_emotion_to_img(session.latest_contact_content)
		if len(content) > 10 :
			content = content[0:10]
			content = content+'...'
		one_session = {
			'id' : session.id,
			'sender_fake_id' : weixin_user.fake_id,
			'sender_username' : weixin_user.username,
			'sender_name' : weixin_user.nickname_for_html,
			'weixin_user_icon' : weixin_user.weixin_user_icon if len(weixin_user.weixin_user_icon.strip()) > 0 else DEFAULT_ICON,
			'content' : content,
			'created_at' : __format_datetime(session.latest_contact_created_at),
			'unread_count' : session.unread_count,
			'is_subscribed' : is_subscribed(weixin_user),
			'is_active' : True if datetime.now() < session.latest_contact_created_at + timedelta(hours=EXPIRED_TIME) and datetime.now() > session.latest_contact_created_at else False
		}
		try:
			member = Member.get_member_by_weixin_user_id(weixin_user.id)
			if member:
				one_session.member_id = member.id
				one_session.member_remarks_name = member.remarks_name
				if len(member.user_icon.strip()) > 0:
					one_session.weixin_user_icon = member.user_icon
				if member.username_for_html:
					one_session.sender_name = member.username_for_html
		except:
			notify_message = u"设置会话信息失败, weixin_user_openid:{}, cause:\n{}".format(
				session.weixin_user_id, unicode_full_stack())
			watchdog_notice(notify_message)
			# continue
		sessions_list.append(one_session)
		# response.data.page_info = __package_pageinfo(pageinfo)

	c = RequestContext(request,{
		'is_login' : True,
		'sessions' : sessions_list,
		'pressed_link' : 'messages'
	})
	return render_to_response('mobile_app/list_messages.html',c)

#单用户的消息历史
@login_required(login_url="/mobile_app/")
def get_session_histories(request,session_id):
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

	#清空未读消息
	Session.objects.filter(mpuser=mpuser,id=session_id).update(unread_count=0)

	messages_list = []
	session = Session.objects.get(id=session_id)
	is_active =  True if datetime.now() < session.latest_contact_created_at + timedelta(hours=EXPIRED_TIME) and datetime.now() > session.latest_contact_created_at else False
	for message in messages:
		sender = username2weixin_user[message.from_weixin_user_username]
		one_message = {
			'id' : message.id,
			'weixin_message_id' : message.weixin_message_id,
			'is_reply' : message.is_reply,
			'content' : emotion.change_emotion_to_img(message.content),
			'weixin_created_at' : __format_datetime(message.weixin_created_at)
		}
		if message.is_reply:
			one_message['sender_icon'] = mpuser_preview_info.image_path
			one_message['sender_name'] = mpuser_preview_info.name
		else:
			member = Member.get_member_by_weixin_user_id(sender.id)
			if member:
				one_message['sender_icon'] = member.user_icon if len(member.user_icon.strip()) > 0 else DEFAULT_ICON
				one_message['sender_name'] = member.username_for_html
				if one_message['sender_icon'] != sender.weixin_user_icon:
					sender.weixin_user_icon = member.user_icon
			else:
				one_message['sender_icon'] = sender.weixin_user_icon if len(sender.weixin_user_icon.strip()) > 0 else DEFAULT_ICON
				one_message['sender_name'] = sender.weixin_user_nick_name
		messages_list.append(one_message)
	wei = Session.objects.get(mpuser=mpuser,id=session_id)
	c = RequestContext(request,{
		'is_login' : True,
		'is_active' : is_active,
		'sessions' : messages_list,
		'session_id' : session_id,
		'weixin_user_id' : wei.weixin_user_id,
		'pressed_link' : 'messages'
	})
	return render_to_response('mobile_app/list_histories.html',c)

#回复消息
@login_required(login_url="/mobile_app/")
def reply_session(request):
	session_id = request.POST['session_id']
	content = request.POST['content']
	receiver_username = request.POST['receiver_username']
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
	return response.get_response()

def send_custome_message(content,openid_sendto,mpuser):
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
	except:
		return False
	return True

from core.wxapi import get_weixin_api
from core.wxapi.custom_message import TextCustomMessage
from weixin.user.models import get_mpuser_access_token_for
def _send_custom_message(mpuser, send_to, content):
	mpuser_access_token = get_mpuser_access_token_for(mpuser)
	wxapi = get_weixin_api(mpuser_access_token)
	wxapi.send_custom_msg(send_to, TextCustomMessage(content))

def new_base(request):
	c = RequestContext(request, {
	})
	return render_to_response('mobile_app/base.html', c)
