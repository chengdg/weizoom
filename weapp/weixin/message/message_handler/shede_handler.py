# -*- coding: utf-8 -*-

__author__ = 'bert'

from weixin.message.handler.keyword_handler import *

from django.conf import settings
from django.db import connection, transaction

from core import emotion

from weixin.message.message import util as message_util
from weixin.message.qa import cache_util
from weixin2.models import *
from weixin.message.message.models import Message
from weixin.message import generator
from weixin.user.models import WeixinMpUser, SheDe, SheDeLog
from watchdog.utils import watchdog_warning, watchdog_error
from core.exceptionutil import unicode_full_stack
from modules.member.module_api import get_member_by_openid
from modules.member.integral import increase_member_integral
from weixin.message.handler.weixin_message import WeixinMessageTypes
"""
该处理对应系统中关键词回复功能

微信push过来的文本消息的处理，文本内容作为关键词，
在系统设定的关键词中查找与该查询关键词匹配的规则，
如有匹配，则返回对应规则中设定的回复内容，否则返
回None

且在处理过程中，进行收到的消息和会话记录处理，以
便系统用户能够及时获悉并进行人工消息回复等
"""

class SheDeHandler(KeywordHandler):

	def _handle_keyword(self, context, from_weixin_user, is_from_simulator):
		# request = context.request
		message = context.message
		user_profile = context.user_profile
		print '===========0', message.msgType, user_profile.user_id
		response = None
		response_rule = None
		response_content = None
		if message.msgType == WeixinMessageTypes.TEXT and user_profile.user_id not in [1]:
			content = message.content
			if content and content.strip().startswith('sxsdj'):
				member = get_member_by_openid( message.fromUserName, user_profile.webapp_id)
				print member,'==============23423'
				if member:
					print '===============1',content, '--',SheDe.objects.filter(number=content.strip()).count() 
					if SheDe.objects.filter(number=content.strip()).count() > 0:
						print '===============2'
						if SheDeLog.objects.filter(member_id=member.id).count() == 0:
							print '===============3'
							with transaction.atomic():
								print '===============4'
								she_de = SheDe.objects.select_for_update().get(number=content.strip())
								print '===============5'
								if she_de.is_send is False:
									print '===============6'
					 				increase_member_integral(member, she_de.integral, u'活动奖励')
									
									she_de.is_send = True
									she_de.save()
									SheDeLog.objects.create(member_id=member.id, shede=she_de)
									response_content = u'恭喜您获得的舍得酒业100积分已充值到<a href="http://%s/termite/workbench/jqm/preview/?module=user_center&model=user_info&action=get&workspace_id=mall&webapp_owner_id=%s&project_id=0">个人中心-我的积分</a>' % (user_profile.host, user_profile.user_id)
								else:
									response_content = u'抱歉，该验证码已使用！'
						else:
							response_content = u'抱歉，该验证码已使用！'
					else:
						response_content = u'抱歉，验证码错误！'


		if response_content:
			response = generator.get_text_response(message.fromUserName, message.toUserName, response_content, message.fromUserName, user_profile)

			try:
				self._process_recorde_message(context, response_rule, from_weixin_user, is_from_simulator)
			except:
				notify_message = u"_process_recorde_message, cause:\n{}".format(unicode_full_stack())
				message_tail = '\nanswer:%s,patterns:%s,owner_id:%d,id:%d' % (response_rule.answer, response_rule.patterns, response_rule.owner_id, response_rule.id)
				notify_message += message_tail
				print notify_message
				watchdog_error(notify_message)
		
		return response

	def _process_recorde_message(self, context, response_rule, from_weixin_user, is_from_simulator):
		new_context = {}
		new_context['member_id'] = context.member.id if context.member else -1
		new_context['message'] = context.message.__dict__ if context.message else None
		new_context['user_profile_id'] = context.user_profile.id if context.user_profile else None
		
		request = context.request
		post = {}
		post.update(request.POST)
		current_request_dict = {
			"POST":post
		}

		new_context['response_rule_id'] = response_rule.id if response_rule else -1
		#new_context['from_weixin_user_id'] = from_weixin_user.id if from_weixin_user else -1
		new_context['from_user_name'] = context.message.fromUserName
		
		new_context['is_from_simulator'] = is_from_simulator
		new_context['request'] = current_request_dict

		from weixin.message.message_handler.tasks import recorde_message, _recorde_message
		# if settings.TASKQUEUE_ENABLED:
		#增加response_rule参数，duhao 2015-04-30
		new_context['response_rule'] = response_rule.format_to_dict() if response_rule else None
		recorde_message.delay(new_context)

		# else:
		# 	_recorde_message(new_context)

		# #先对收到的消息进行记录处理
		# session_info = None
		# if self._should_record_message(is_from_simulator, request):
		# 	if message.msgType in [WeixinMessageTypes.VOICE, WeixinMessageTypes.IMAGE] or message.source == WeixinMessageTypes.TEXT:
		# 		session_info = self._record_message(request, message, user_profile, from_weixin_user)

		# #更新会员的最近会话信息
		# if (context.member is not None) and (session_info is not None):
		# 	member = context.member
		# 	context.member.session_id = session_info['session'].id
		# 	context.member.last_message_id = session_info['receive_message'].id
		# 	context.member.save()
		# #最后记录自动回复的session history
		# self._record_session_info(session_info, response_rule)

	def _build_response_with_auto_response_rule(self, user_profile, message, response_rule, is_from_simulator):
		return self._build_response_to_weixin_user(user_profile, message, response_rule, is_from_simulator)

	def _build_response_without_auto_response_rule(self, user_profile, message, is_from_simulator):
		#response_rule = qa_util.find_unmatch_answer_for(user_profile.webapp_id)
		#从缓存中获取数据  duhao  2015-03-09
		response_rule = cache_util.find_unmatch_answer_from_cache_for(user_profile)

		if response_rule and response_rule.is_active:
			#sdwex = self._get_token_for_weixin_user(user_profile, message.fromUserName, is_from_simulator)
			if response_rule.material_id > 0:
				response = generator.get_news_response(message.fromUserName, message.toUserName, response_rule.newses, message.fromUserName)
			else:
				if is_from_simulator:
					response = generator.get_text_response(message.fromUserName, message.toUserName, emotion.change_emotion_to_img(response_rule.answer), message.fromUserName, user_profile)
				else:
					response = generator.get_text_response(message.fromUserName, message.toUserName, response_rule.answer, message.fromUserName, user_profile)

			return 	response_rule, response
		else:
			return None, None

	def _should_record_message(self, is_from_simulator, request):
		should_record_message = True
		
		'''
		if settings.RECORD_SIMULATOR_MESSAGE:
			return True
		'''

		if settings.MODE == 'deploy' and is_from_simulator:
			should_record_message = False
		elif (settings.MODE == 'develop' or settings.MODE == 'test') and\
				(is_from_simulator and int(request.POST.get('is_user_logined', 0)) == 1):
			#用户登录情况下启动的模拟器，不能记录其信息流
			should_record_message = False

		return should_record_message

	def _get_weixin_user_head_icon(self, weixin_user_name):
		head_icon = '/static/img/user-1.jpg'

		if weixin_user_name == 'zhouxun':
			head_icon = '/static/img/zhouxun_50.jpg'
		elif weixin_user_name == 'yangmi':
			head_icon = '/static/img/yangmi_50.jpg'
		
		return head_icon

	########################################################################
	# _record_message: 记录收到的消息
	########################################################################
	def _record_message(self, request, message, user_profile, from_weixin_user):
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

		sender_icon = self._get_weixin_user_head_icon(from_weixin_user.username)
		if hasattr(message, 'content'):
			content = message.content
		else:
			content = ''
		mediaId,picUrl = '',''
		if message.msgType == WeixinMessageTypes.TEXT:
			content = message.content
		elif message.msgType == WeixinMessageTypes.VOICE:
			mediaId = message.mediaId
		elif message.msgType == WeixinMessageTypes.IMAGE:
			mediaId = message.mediaId
			picUrl = message.picUrl

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
			'weixin_created_at': message.createTime,
			'message_type': message.msgType,
			'msg_id': message.msgId,
			'pic_url': picUrl,
			'media_id': mediaId
		}
		if 'sender_fake_id' in request.POST:
			params['sender_fake_id'] = request.POST['sender_fake_id']

		return message_util.record_message(params)