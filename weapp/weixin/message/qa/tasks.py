# -*- coding: utf-8 -*-

__author__ = 'bert'
# from __future__ import absolute_import

from django.conf import settings
import time

from core.exceptionutil import full_stack

from core import emotion

from watchdog.utils import watchdog_fatal, watchdog_error, watchdog_info

from modules.member.models import *

from weixin.message.handler.weixin_message import WeixinMessageTypes
from weixin.message.message import util as message_util
from weixin.message.message.models import Message
#from weixin.message.qa.models import Rule
from weixin2.models import Rule, KeywordHistory
from weixin.user.models import WeixinMpUser, WeixinUser

from account import models as account_models

from celery import task

@task
def recorde_message(context):
	print 'call recorde_message start'
	_recorde_message(context)
	print 'OK'
	

def _recorde_message(context):  #response_rule, from_weixin_user, is_from_simulator):
	request, message, user_profile, member, response_rule, from_weixin_user, is_from_simulator = _get_info_from_context(context)
	#先对收到的消息进行记录处理
	session_info = None
	if _should_record_message(is_from_simulator, request):
		if message["msgType"] in [WeixinMessageTypes.VOICE, WeixinMessageTypes.IMAGE] or message["source"] == WeixinMessageTypes.TEXT:
			session_info = get_or_create_messge(context, from_weixin_user)

	#更新会员的最近会话信息
	if (member is not None) and (session_info is not None):
		# context.member.session_id = session_info['session'].id
		# context.member.last_message_id = session_info['receive_message'].id
		# context.member.save()
		Member.objects.filter(id=member.id).update(session_id = session_info['session'].id, last_message_id = session_info['receive_message'].id)

	#最后记录自动回复的session history
	record_session_info(session_info, response_rule)

def _get_info_from_context(context):
	request = context["request"]
	if context["message"]:
		message = context["message"]
	else:
		message = None
	if context["user_profile_id"]:
		print 
		user_profile = account_models.UserProfile.objects.get(id = context["user_profile_id"])
	else:
		user_profile = None

	if context["member_id"] and  context["member_id"] != -1:
		member = Member.objects.get(id=context["member_id"])
	else:
		member = None

	#添加随机回复功能后，不在这里获取response_rule,不然存到库里的会是原始的json串
	#duhao 2015.04.30
	response_rule = context["response_rule"]
	if not response_rule:
		if context["response_rule_id"] and context["response_rule_id"] != -1:
			response_rule = Rule.objects.get(id=context["response_rule_id"])
			response_rule = response_rule.format_to_dict()
		else:
			response_rule = None

	if context["from_weixin_user_id"] and context["from_weixin_user_id"] != -1:
		from_weixin_user = WeixinUser.objects.get(id=context["from_weixin_user_id"])
	else:
		from_weixin_user = None

	if context["is_from_simulator"]:
		is_from_simulator = context["is_from_simulator"]
	else:
		is_from_simulator = False

	return request, message, user_profile, member, response_rule, from_weixin_user, is_from_simulator

def _should_record_message(is_from_simulator, request):
	should_record_message = True
	
	'''
	if settings.RECORD_SIMULATOR_MESSAGE:
		return True
	'''

	if settings.MODE == 'deploy' and is_from_simulator:
		should_record_message = False
	elif (settings.MODE == 'develop' or settings.MODE == 'test') and\
			(is_from_simulator and int(request["POST"].get('is_user_logined', 0)) == 1):
		#用户登录情况下启动的模拟器，不能记录其信息流
		should_record_message = False

	return should_record_message

def get_or_create_messge(context, from_weixin_user):
	request, message, user_profile, member, response_rule, from_weixin_user, is_from_simulator = _get_info_from_context(context)

	try:
		mp_user = WeixinMpUser.objects.get(owner_id=user_profile.user_id)
	except:
		if settings.DUMP_DEBUG_MSG:
			from core.exceptionutil import full_stack
			print '========== start monitored exception =========='
			print full_stack()
			print 'no mp_user for webapp_id ', user_profile.webapp_id
			print '========== finish monitored exception =========='
		#没有注册mp user，人工客服不可用，直接返回
		return

	sender_icon = _get_weixin_user_head_icon(from_weixin_user.username)
	if message.has_key("content"):#:hasattr(message, 'content'):
		content = message["content"]
	else:
		content = ''
	mediaId,picUrl = '',''
	if message["msgType"] == WeixinMessageTypes.TEXT:
		content = message["content"]
	elif message["msgType"] == WeixinMessageTypes.VOICE:
		mediaId = message["mediaId"]
	elif message["msgType"] == WeixinMessageTypes.IMAGE:
		mediaId = message["mediaId"]
		picUrl = message["picUrl"]

	params = {
		'sender_username': from_weixin_user.username,
		'sender_nickname': from_weixin_user.username,
		'sender_fake_id': '',
		'sender_icon': sender_icon,
		'receiver_username': mp_user.username,
		'receiver_nickname': mp_user.username,
		'receiver_fake_id': '',
		'receiver_icon': '[not used]',
		'content': content,
		'mpuser': mp_user,
		'mode': settings.MODE,
		'weixin_created_at': message["createTime"],
		'message_type': message["msgType"],
		'msg_id': message["msgId"],
		'pic_url': picUrl,
		'media_id': mediaId
	}
	if 'sender_fake_id' in request["POST"]:
		params['sender_fake_id'] = request["POST"]['sender_fake_id']

	return message_util.record_message(params)


def record_session_info(session_info, response_rule):
	if session_info and response_rule:
		if response_rule['is_news_type']:
			content = u'[图文消息]'
		else:
			content = response_rule['answer'][0]['content']
		latest_message = Message.objects.create(
			mpuser=session_info['mpuser'], 
			session=session_info['session'], 
			from_weixin_user_username=session_info['receiver_username'], 
			to_weixin_user_username=session_info['sender_username'], 
			content=emotion.change_emotion_to_img(u'[自动回复]: %s' % content),
			is_reply=True
		)

def _get_weixin_user_head_icon(weixin_user_name):
	head_icon = '/static/img/user-1.jpg'

	if weixin_user_name == 'zhouxun':
		head_icon = '/static/img/zhouxun_50.jpg'
	elif weixin_user_name == 'yangmi':
		head_icon = '/static/img/yangmi_50.jpg'
	
	return head_icon

def record_keyword(owner_id, keyword):
	"""
	记录用户发来的有自动回复的关键词
	包装一层，避免外面每次调用都要获取date
	duhao
	"""
	date = time.strftime("%Y-%m-%d")
	_record_keyword.delay(owner_id, keyword, date)

@task
def _record_keyword(owner_id, keyword, date):
	"""
	记录用户发来的有自动回复的关键词，参数中要传date参数，避免celery执行时有跨日期问题
	duhao
	"""
	KeywordHistory.objects.create(
		owner_id=owner_id,
		keyword=keyword,
		date=date
	)