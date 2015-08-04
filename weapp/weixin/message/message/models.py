# -*- coding: utf-8 -*-

__author__ = 'bert'

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from weixin.user.models import WeixinUser, WeixinMpUser
from core import dateutil
from utils.string_util import byte_to_hex, hex_to_byte

import time
from datetime import datetime, timedelta

#########################################################################
# RealTimeInfo：实时信息, 和所绑定的微信公众号关联
#########################################################################
class RealTimeInfo(models.Model):
	mpuser = models.ForeignKey(WeixinMpUser)
	unread_count = models.IntegerField(default=0, db_index=True) #未读消息数

	class Meta(object):
		managed = False
		db_table = 'weixin_message_realtime_info'
		verbose_name = '微信消息实时状态信息'
		verbose_name_plural = '微信消息实时状态信息'		

#===============================================================================
# TempSendMessage : 公众账号发出的临时消息，用于测试和开发
#===============================================================================
class TempSendMessage(models.Model):
	mp_user_name = models.CharField(max_length=50) #发送消息的公众账号
	weixin_user_name = models.CharField(max_length=50) #接收消息的微信账号
	content = models.CharField(max_length=100) #消息内容
	is_processed = models.BooleanField(default=False)

	class Meta(object):
		db_table = 'mpuser_temp_send_message'

#########################################################################
# Session：会话抽象
#########################################################################
class Session(models.Model):
	mpuser = models.ForeignKey(WeixinMpUser)
	weixin_user = models.ForeignKey(WeixinUser, to_field='username', db_column='weixin_user_username')
	latest_contact_content = models.CharField(max_length=1024) #最后一次交互消息内容
	latest_contact_created_at = models.DateTimeField(auto_now_add=True) #最后一次交互时间
	is_latest_contact_by_viper = models.BooleanField(default=False) #最后一次交互是否是客户发出的
	unread_count = models.IntegerField(default=0) #未读消息数
	is_show = models.BooleanField(default=False) #是否显示(是否填充对应的WeixinUser)
	created_at = models.DateTimeField(auto_now_add=True)
	weixin_created_at = models.CharField(max_length=50) #微信平台提供的创建时间
	retry_count = models.IntegerField(default=0) #重試次數
	#add by bert at 20.0
	message_id = models.IntegerField(default=0)
	#add by slzhu
	member_user_username = models.CharField(default='', max_length=100)
	member_latest_content = models.CharField(default='', max_length=1024) #粉丝最近一条消息
	member_latest_created_at = models.CharField(default='', max_length=50) #粉丝最近一条消息时间
	is_replied = models.BooleanField(default=False) #是否回复过

	class Meta(object):
		managed = False
		ordering = ['-latest_contact_created_at']
		db_table = 'weixin_message_session'

def get_weixinuser_sessions(weixin_user_name):
	if weixin_user_name is None:
		return []

	return Session.objects.filter(weixin_user=weixin_user_name)


########################################################################
# Message：消息抽象
########################################################################
TEXT = 'text'
IMAGE = 'image'
VOICE = 'voice'
class Message(models.Model):
	mpuser = models.ForeignKey(WeixinMpUser)
	session = models.ForeignKey(Session)
	weixin_message_id = models.CharField(max_length=50, default='') #消息中的id
	mp_message_id = models.CharField(max_length=50, default='') #公众平台的id
	from_weixin_user_username = models.CharField(max_length=50) #消息发出者的username
	to_weixin_user_username = models.CharField(max_length=50) #消息接收者的username
	content = models.TextField()
	content_url = models.CharField(max_length=500, default='') #微信公众平台字段contentUrl,暂未使用
	has_reply = models.BooleanField(default=False) #微信公众平台字段hasReply,暂未使用
	created_at = models.DateTimeField(auto_now_add=True) #系统创建时间
	weixin_created_at = models.DateTimeField(auto_now_add=True) #在微信平台上创建的时间
	is_checked = models.BooleanField(default=False) #是否检查过
	is_reply = models.BooleanField(default=True) #是否是系统帐号回复
	#add by bert at 20.0
	message_type = models.CharField(default=TEXT, max_length=50)
	media_id = models.CharField(max_length=255,default='')
	msg_id = models.CharField(max_length=255,default='')
	pic_url = models.TextField()
	audio_url = models.TextField()
	is_updated = models.BooleanField(default=True)
 
	class Meta(object):
		managed = False
		db_table = 'weixin_message_message'
		ordering = ['-weixin_created_at']

def belong_to(webapp_id, mpuser, query):
	query_hex = byte_to_hex(query)
	data_before_tow_days =  time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()-2*24*60*60))
	weixin_user_usernames = [weixin_user.username for weixin_user in WeixinUser.objects.filter(webapp_id=webapp_id, is_subscribed=True, nick_name__contains=query_hex)]
	session_ids = [session.id for session in Session.objects.filter(weixin_user__in=weixin_user_usernames,mpuser=mpuser)]
	
	return Message.objects.filter(mpuser=mpuser).filter(~Q(from_weixin_user_username=webapp_id),created_at__gt=data_before_tow_days).filter(Q(session_id__in=session_ids)|Q(content__icontains=query)).order_by('-created_at')
Message.objects.belong_to  = belong_to

########################################################################
# CollectMessage:收藏消息
########################################################################
class CollectMessage(models.Model):
	owner = models.ForeignKey(User)
	message_id = models.IntegerField(default=0)
	status = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True) #系统创建时间

	class Meta(object):
		managed = False
		db_table = 'weixin_collect_message'

	@staticmethod
	def is_collected(message_id):
		if CollectMessage.objects.filter(message_id=message_id).count() > 0:
			return CollectMessage.objects.filter(message_id=message_id)[0].status
		else:
			return False

	@staticmethod
	def get_message_ids(owner):
		return [collect_message.message_id for collect_message in CollectMessage.objects.filter(owner=owner, status=True).order_by('-created_at')]

