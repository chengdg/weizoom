# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json

from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db.models import F

from core.jsonresponse import JsonResponse, create_response
from core.send_message import send_message
from account.models import UserProfile, increase_new_message_count

from weixin2.models import *
from weixin.user.models import WeixinMpUser

from utils.string_util import byte_to_hex
from weixin.message.handler.weixin_message import WeixinMessageTypes

from watchdog.utils import watchdog_warning, watchdog_error, watchdog_info
from core.exceptionutil import full_stack, unicode_full_stack

########################################################################
# record_message : 测试环境模拟收到消息
########################################################################
def record_message(args):
	sender_username = args['sender_username']
	sender_nickname = args['sender_nickname']
	sender_fake_id = args['sender_fake_id']
	sender_icon = args['sender_icon']
	receiver_username = args['receiver_username']
	receiver_nickname = args['receiver_nickname']
	receiver_fake_id = args['receiver_fake_id']
	receiver_icon = args['receiver_icon']
	content = args['content']
	mpuser = args['mpuser']
	mode = args['mode']
	weixin_created_at = args['weixin_created_at']
	#add by bert at 20.0
	msg_id = args['msg_id']
	pic_url = args['pic_url']
	message_type = args['message_type']
	media_id = args['media_id']
	is_un_read_msg = args['is_un_read_msg']

	session = None

	sender = WeixinUser.objects.get(username=sender_username)
	if sender_fake_id and sender.fake_id != sender_fake_id:
		sender.fake_id = sender_fake_id
		sender.save()
	# try:
	# 	print sender_username,']]]]]]]]]]', WeixinUser.objects.get(username=sender_username).id
	# 	sender = WeixinUser.objects.get(username=sender_username)
	# 	if sender_fake_id and sender.fake_id != sender_fake_id:
	# 		sender.fake_id = sender_fake_id
	# 		sender.save()
	# 		print '1-----2'
	# 	print '1-----3'
	# except:
	# 	print '2-----1'
	# 	sender = WeixinUser.objects.create(
	# 		username = sender_username, 
	# 		fake_id = sender_fake_id, 
	# 		nick_name = byte_to_hex(sender_nickname), 
	# 		weixin_user_icon = sender_icon
	# 		)
	
	try:
		receiver = WeixinUser.objects.get(username=receiver_username)
		if receiver_fake_id and receiver.fake_id != receiver_fake_id:
			receiver.fake_id = receiver_fake_id
			receiver.save()
	except:
		receiver = WeixinUser.objects.create(
			username=receiver_username, 
			fake_id=receiver_fake_id,
			nick_name = byte_to_hex(receiver_nickname), 
			weixin_user_icon=receiver_icon
			)
		
	should_increase_realtime_unread_count = False
	should_increase_new_message_count = False
	try:
		session = Session.objects.get(weixin_user=sender, mpuser=mpuser)
		
		should_increase_realtime_unread_count = True
		should_increase_new_message_count = True

		session.latest_contact_content = content
		session.latest_contact_created_at = datetime.today()
		session.is_latest_contact_by_viper = False
		if is_un_read_msg:
			session.unread_count +=  1
		session.retry_count = 0
		session.weixin_created_at = weixin_created_at
		#更新微信用户session信息, added by slzhu
		session.member_user = sender
		session.member_latest_content = content
		session.member_latest_created_at = weixin_created_at
		session.is_replied = False
		session.save()

		#通知客户端
		#TODO 使用其它通知方式？
		# try:
		# 	notifyclient.send_notify_to_all_user(
		# 		"WEIXIN_MESSAGE", 
		# 		u'[%s]: 用户%s发来新消息: %s' % (mpuser.owner.username, session.weixin_user_id, content), 
		# 		'http://%s/message/' % settings.DOMAIN
		# 	)
		# except:
		# 	pass
	except:
		import sys, traceback
		type, value, tb = sys.exc_info()

		traceback.print_tb(tb)
		if is_un_read_msg:
			unread_count = 1
		else:
			unread_count = 0
		if mode == 'test' or mode == 'develop':
			session = Session.objects.create(
				mpuser=mpuser,
				weixin_user=sender, 
				weixin_created_at = weixin_created_at,
				latest_contact_content=content, 
				unread_count=unread_count, 
				is_show=False,
				member_user_username = sender.username,
				member_latest_content = content,
				member_latest_created_at = weixin_created_at,
				is_replied = False
			)
			
			request = HttpRequest()
			request.GET['id'] = session.id
			enable_session(request)
		else:
			#正式环境中，新会话为显示状态, 同时直接进行通知
			session = Session.objects.create(
				mpuser=mpuser,
				weixin_user=sender, 
				weixin_created_at = weixin_created_at,
				latest_contact_content=content, 
				unread_count=unread_count, 
				is_show=True,
				member_user_username = sender.username,
				member_latest_content = content,
				member_latest_created_at = weixin_created_at,
				is_replied = False
			)

			#增加未读数
			# count = Message.objects.filter(session_id=session.id, is_reply=False).count()
			# RealTimeInfo.objects.filter(mpuser=mpuser).update(unread_count = F('unread_count') + count)

			# #增加首页显示的new message count
			# increase_new_message_count(user=mpuser.owner, count=session.unread_count)

			#通知客户端
			#TODO 改用其他通知方式？
			# try:
			# 	notifyclient.send_notify_to_all_user(
			# 		"WEIXIN_MESSAGE", 
			# 		u'[%s]: 用户%s发来新消息: %s' % (mpuser.owner.username, session.weixin_user_id, content), 
			# 		'http://%s/message/' % settings.DOMAIN
			# 	)
			# except:
			# 	pass

	# try:
	# 	realtime_info = RealTimeInfo.objects.get(mpuser=mpuser)
	# 	if should_increase_realtime_unread_count:
	# 		RealTimeInfo.objects.filter(mpuser=mpuser).update(unread_count=F('unread_count')+1)

	# 	if should_increase_new_message_count:
	# 		increase_new_message_count(user=mpuser.owner, count=1)
	# except:	
	# 	RealTimeInfo.objects.create(mpuser=mpuser, unread_count=0)

	if message_type == WeixinMessageTypes.VOICE:
		is_updated = False
	else:
		is_updated = True

	receive_message = Message.objects.create(
						mpuser=mpuser, 
						session=session, 
						from_weixin_user_username=sender_username, 
						to_weixin_user_username=receiver_username, 
						content=content, 
						is_reply=False, 
						#add by bert at 20
						msg_id=msg_id,
						pic_url=pic_url,
						media_id=media_id,
						is_updated = is_updated,
						message_type = message_type
						)
	if pic_url:
		content = pic_url
	#added by slzhu
	Session.objects.filter(id=session.id).update(message_id = receive_message.id, latest_contact_content = content, member_message_id = receive_message.id)

	if message_type == WeixinMessageTypes.VOICE:
		try:
			queue = '/queue/jms.com.wintim.service.weapp.weixin_upload_audio'
			response = JsonResponse()
			response.message_id = receive_message.id
			message = response.get_json()
			send_message(queue, message)
		except:
			notify_message = u"record_message Session cause:\n{}".format(unicode_full_stack())
			watchdog_warning(notify_message)
	return {
		'mpuser': mpuser, 
		'session': session,
		'receive_message': receive_message,
		'receiver_username': receiver_username,
		'sender_username': sender_username
	}

########################################################################
# enable_session: 显示会话
########################################################################
def enable_session(request):
	session_id = request.GET['id']
	session = Session.objects.get(id=session_id)

	#显示session
	Session.objects.filter(id=session_id).update(is_show=True)

	mpuser = session.mpuser #绑定到系统且该会话关联的微信公众号
	system_user = mpuser.owner #把该微信公众号绑定到系统的系统用户

	#通知客户端
	#TODO 使用其他通知方式？
	# try:
	# 	notifyclient.send_notify_to_all_user(
	# 		"WEIXIN_MESSAGE", 
	# 		u'[%s]: 有新用户%s发来消息' % (system_user.username, session.weixin_user_id), 
	# 		'http://%s/message/' % settings.DOMAIN
	# 	)
	# except:
	# 	message = u"发送消息失败:\n{}\n失败原因:\n{}".format(
	# 		u'[%s]: 有新用户%s发来消息' % (system_user.username, session.weixin_user_id),
	# 		unicode_full_stack()
	# 		)
	# 	watchdog_error(message)

	#增加未读数
	count = Message.objects.filter(session_id=session_id, is_reply=False).count()
	RealTimeInfo.objects.filter(mpuser=mpuser).update(unread_count = F('unread_count') + count)

	#增加首页显示的new message count
	increase_new_message_count(user=system_user, count=session.unread_count)

	#创建customer
	#customer_model.create_customer(session.owner, session.weixin_user)

	return create_response(200).get_response()