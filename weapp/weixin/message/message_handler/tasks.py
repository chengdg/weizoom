# -*- coding: utf-8 -*-

__author__ = 'bert'
# from __future__ import absolute_import
import random
import string
import urllib2

from django.conf import settings
from django.contrib.auth.models import User

from core.exceptionutil import full_stack

from core import emotion
from core import upyun_util

from watchdog.utils import watchdog_fatal, watchdog_error, watchdog_info

from modules.member.models import *

from weixin.message.handler.weixin_message import WeixinMessageTypes
from weixin.message.message import util as message_util
# from weixin.message.message.models import Message
# from weixin.message.qa.models import Rule
from weixin2.models import Rule, Message, WeixinUser
from weixin.user.models import WeixinMpUser, get_mpuser_access_token_by_userid

from weixin.statistics.models import increase_weixin_user_statistics, decrease_weixin_user_statistics

from account import models as account_models
from account.social_account import models as social_account_models
from account.util import get_binding_weixin_mpuser, get_mpuser_accesstoken

from celery import task

@task
def recorde_message(context):
	print 'call new recorde_message start'
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
		Member.objects.filter(id=member.id).update(session_id = session_info['session'].id, last_message_id = session_info['receive_message'].id)
	#最后记录自动回复的session history
	record_session_info(session_info, response_rule)

	#如果是声音消息 则语音转换
	upload_audio.delay(message.id, user_profile.user_idjj)

def _get_info_from_context(context):
	request = context["request"]
	if context["message"]:
		message = context["message"]
	else:
		message = None
	if context["user_profile_id"]:
		user_profile = account_models.UserProfile.objects.get(id = context["user_profile_id"])
	else:
		user_profile = None
	#添加随机回复功能后，不在这里获取response_rule,不然存到库里的会是原始的json串
	#duhao 2015.04.30
	response_rule = context["response_rule"]
	if not response_rule:
		if context["response_rule_id"] and context["response_rule_id"] != -1:
			response_rule = Rule.objects.get(id=context["response_rule_id"])
			response_rule = response_rule.format_to_dict()
		else:
			response_rule = None

	member = None
	if context["from_user_name"]:
		if WeixinUser.objects.filter(username=context["from_user_name"]).count() > 0:
			from_weixin_user = WeixinUser.objects.get(username=context["from_user_name"])
		else:
			if user_profile:
				from_weixin_user = WeixinUser.objects.create(username=context["from_user_name"], webapp_id=user_profile.webapp_id)
			else:
				from_weixin_user = None

		social_accounts  = social_account_models.SocialAccount.objects.filter(webapp_id=user_profile.webapp_id, openid=context["from_user_name"])
		if social_accounts.count() > 0:
			social_account = social_accounts[0]
			member_has_socials = MemberHasSocialAccount.objects.filter(account=social_account)
			if member_has_socials.count() > 0:
				member = member_has_socials[0].member
	else:
		from_weixin_user = None

	if context["is_from_simulator"]:
		is_from_simulator = context["is_from_simulator"]
	else:
		is_from_simulator = False

	return request, message, user_profile, member, response_rule, from_weixin_user, is_from_simulator

def _should_record_message(is_from_simulator, request):
	return True
	should_record_message = True
	'''
	if settings.RECORD_SIMULATOR_MESSAGE:
		return True
	'''
	if settings.MODE == 'deploy' and is_from_simulator:
		should_record_message = False
	# elif (settings.MODE == 'develop' or settings.MODE == 'test') and\
	# 		(is_from_simulator and int(request["POST"].get('is_user_logined', 0)) == 1):
		#用户登录情况下启动的模拟器，不能记录其信息流
	elif (settings.MODE == 'develop' or settings.MODE == 'test') and\
	 		(is_from_simulator):
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
		try:
			import time
			if picUrl.find('mmbiz.qpic.cn') > -1:
				nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 6))
				picUrlName = "%s%s" % (nonce_str,str(int(time.time() * 1000)))
				picUrl = upyun_util.upload_weixin_url_to_upyun(picUrl, picUrlName)
		except:
			print 'error at picUrl to upyun'

	#判断是否公众号信息: added by slzhu
	is_from_mp_user = False
	if response_rule:
		is_from_mp_user = True

	is_un_read_msg = True
	if response_rule and response_rule.has_key('type') and response_rule['type'] == 1:
		is_un_read_msg = False

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
		'media_id': mediaId,
		'is_from_mp_user': is_from_mp_user,
		'is_un_read_msg': is_un_read_msg
	}
	# if 'sender_fake_id' in request["POST"]:
	# 	params['sender_fake_id'] = request["POST"]['sender_fake_id']
	#return message_util.record_message(params)
	return message_util.record_message(params)


def record_session_info(session_info, response_rule):
	if session_info and response_rule:
		if response_rule['is_news_type']:
			# content = u'[图文消息]'
			content = ''
		else:
			content = response_rule['answer'][0]['content']
		latest_message = Message.objects.create(
			mpuser=session_info['mpuser'], 
			session=session_info['session'], 
			from_weixin_user_username=session_info['receiver_username'], 
			to_weixin_user_username=session_info['sender_username'], 
			content=emotion.change_emotion_to_img(u'【自动回复】 %s' % content),
			material_id=response_rule['material_id'],
			is_reply=True
		)

def _get_weixin_user_head_icon(weixin_user_name):
	head_icon = '/static/img/user-1.jpg'

	if weixin_user_name == 'zhouxun':
		head_icon = '/static/img/zhouxun_50.jpg'
	elif weixin_user_name == 'yangmi':
		head_icon = '/static/img/yangmi_50.jpg'
	
	return head_icon


@task
def weixin_user_statistics(user_id, is_increse):
	user = User.objects.get(id = user_id)
	if is_increse:
		increase_weixin_user_statistics(user)
	else:
		decrease_weixin_user_statistics(user)

@task
def update_weixin_user(openid, is_subscribed):
	WeixinUser.objects.filter(username=openid).update(is_subscribed=True)



User_Agent = "Mozilla/5.0 (Windows NT 5.1; rv:23.0) Gecko/20100101 Firefox/23.0"
Accept = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
Accept_Language = "en-US,en;q=0.5"
Accept_Encoding = "gzip, deflate"
Connection = "keep-alive"
DownloadfileUrlTmpl = "http://api.weixin.qq.com/cgi-bin/media/get?access_token={}&media_id={}"
TEMP_WORK_DIR = "/weapp/web/weapp/static/audio/"
MaxRetryTimes = 3


@task(bind=True)
def upload_audio(self, message_id, user_id):
	message = Message.objects.get(id=message_id)
	weixin_mp_user_access_token = get_mpuser_access_token_by_userid(user_id)
	__download_voice(message, weixin_mp_user_access_token)


def __build_weixin_request_operner():
	opener = urllib2.build_opener()
	
	opener.addheaders.append(('User-Agent', User_Agent))
	opener.addheaders.append(('Accept', Accept))
	opener.addheaders.append(('Accept-Language', Accept_Language))
	opener.addheaders.append(('Accept-Encoding', Accept_Encoding))
	opener.addheaders.append(('Connection', Connection))

	return opener

def __download_voice(message, weixin_mp_user_access_token):

	request_url = DownloadfileUrlTmpl.format(weixin_mp_user_access_token.access_token, message.media_id) 
	#try:
	message.audio_url = request_url
	opener = __build_weixin_request_operner()
	audio_content = None
	for retryTimes in xrange(MaxRetryTimes):
		try:
			response = opener.open(request_url)
			audio_content = response.read()
			break
		except:
			#下载失败预警后重试三次
			watchdog_notice(u"__download_voice, cause:\n{}".format(unicode_full_stack()))
	print audio_content,'=============================23'		
	if audio_content.find('errmsg') >= 0 or len(audio_content) == 0:
		watchdog_notice(u"__download_voice, cause:\n{}, {}".format(unicode_full_stack()), audio_content)
	else:
		#3. 转换音频格式（amr->mp3）
		mp3_url = _convert_amr_to_mp3(audio_content, message)
		if mp3_url:
			if mp3_url.find('/weapp/web/weapp') > -1:
				mp3_url = mp3_url.replace('/weapp/web/weapp/','/')
			message.audio_url = mp3_url
			message.is_updated = True
			message.save()

def _save_amr_audio(audio_content, message):

	if not os.path.exists(TEMP_WORK_DIR):
		os.makedirs(TEMP_WORK_DIR)

	path = os.path.join(TEMP_WORK_DIR, message.msg_id+'.amr')

	audio_file = None
	try:
		audio_file = open(path, 'wb')
		audio_file.write(audio_content)
		audio_file.flush()
		return path
	finally:
		if audio_file:
			try:
				audio_file.close()
			except:
				pass

def _convert_amr_to_mp3(audio_content, message):
	"""调用系统命令ffmpeg完成音频格式的转换"""

	amr_audio_file = _save_amr_audio(audio_content, message)
	mp3_audio_file_path = os.path.join(TEMP_WORK_DIR, message.msg_id+'.mp3')

	cmd = "ffmpeg -i {} {}".format(amr_audio_file, mp3_audio_file_path)
	cmd = "/usr/local/ffmpeg_2.4/bin/ffmpeg -i {} {}".format(amr_audio_file, mp3_audio_file_path)
	output = None
	try:
		converter = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		output = converter.communicate()[0]
		if not os.path.exists(mp3_audio_file_path):
			#raise Exception(u'没有找到转换后的mp3，确认ffmpeg操作正常')
			return None
	except:
		watchdog_notice(u"调用系统命令ffmpeg完成音频格式的转换, cause:\n{}".format(unicode_full_stack()))

	return mp3_audio_file_path