# -*- coding: utf-8 -*-

__author__ = 'bert'

from utils import cache_util
from weixin.user.models import *
from weixin.message.qa import util as qa_util


from account.models import UserProfile
from core.exceptionutil import unicode_full_stack
from watchdog.utils import watchdog_info
import cache
from django.db.models.query import QuerySet
import json
import random
from weixin2.models import *
from core import emotion
from message.qa.util import record_keyword

def get_mpuser_preview_info_from_db(**kwargs):
	def inner_func():
		try:
			mp_user_preview_info = MpuserPreviewInfo.objects.get(**kwargs)
			return {
				'keys': [
					'account_mpuser_preview_info_mpuser_id_%s' % mp_user_preview_info.mpuser_id,
				],
				'value': mp_user_preview_info
			}
		except:
			return None
	return inner_func
	

def get_mpuser_preview_info_by_mpuser_id(mpuser_id):
	key = 'account_mpuser_preview_info_mpuser_id_%s' % mpuser_id
	return cache_util.get_from_cache(key, get_mpuser_preview_info_from_db(mpuser_id=mpuser_id))


def get_weixin_mp_user_from_db(**kwargs):
	def inner_func():
		try:
			weixin_mp_user = WeixinMpUser.objects.get(**kwargs)
			return {
				'keys': [
					'weixin_mp_user_owner_id_%s' % weixin_mp_user.owner_id,
				],
				'value': weixin_mp_user
			}
		except:
			return None
	return inner_func

def get_weixin_mp_user_by_owner_id(owner_id):
	key = 'weixin_mp_user_owner_id_%s' % owner_id
	return cache_util.get_from_cache(key, get_weixin_mp_user_from_db(owner_id=owner_id))


###############################################################################
# get_auto_qa_message_material: 从数据库中获取自动回复消息素材模板
###############################################################################
def get_auto_qa_message_material_for_cache(user_profile, query):

	def inner_func():
		response_rule = qa_util.find_answer_for(user_profile, query.lower())
		webapp_id = user_profile.webapp_id
	
	 	if not response_rule:
			#user_profile = UserProfile.objects.get(webapp_id=webapp_id)
			webapp_owner_id = user_profile.user_id
			msg = u"获得user('{}')对应的material_news构建cache失败，query:{}"\
					.format(webapp_owner_id, query)
			watchdog_info(msg, user_id=webapp_owner_id)
			#add by bert None 需要保存吗？
			return response_rule

		return {
				'keys': [
					'auto_qa_message_webapp_id_%s_query_%s' % (webapp_id, query.lower())
				],
				'value': response_rule
			}
	return inner_func


def get_auto_qa_message_material(user_profile, query):
	if not query or query == '':
		return None
	key = 'auto_qa_message_webapp_id_%s_query_%s' % (user_profile.webapp_id, query.lower())

	reply_rule = cache_util.get_from_cache(key, get_auto_qa_message_material_for_cache(user_profile, query))
	return _parse_rule(user_profile, reply_rule)

def _parse_rule(user_profile, reply_rule):
	if not reply_rule:
		return None

	#解析自动回复内容
	try:
		answers = json.loads(reply_rule.answer)

		if reply_rule.type == FOLLOW_TYPE:
			#关注自动回复只有一条，不需要随机回复
			answer_data = answers
		else:
			#随机取一条进行回复
			random_index = random.randint(1, len(answers)) - 1
			answer_data = answers[random_index]
		
		if answer_data['type'] == 'news':
			reply_rule.material_id = int(answer_data['content'])
		else:
			reply_rule.answer = emotion.change_img_to_emotion(answer_data['content'])
	except Exception, e:
		print reply_rule.answer, 'is just single answer,Exception:', e

	if reply_rule.is_news_type:
		reply_rule.newses = list(News.objects.filter(material_id=reply_rule.material_id))
	else:
		#如果是文本消息，则在末尾加入小尾巴内容
		tails = Tail.objects.filter(owner_id=user_profile.user_id)
		if tails.count() > 0:
			tail = tails[0]
			if tail.is_active:
				reply_rule.answer = reply_rule.answer + tail.tail

	if (reply_rule.type == TEXT_TYPE or reply_rule.type == NEWS_TYPE) and reply_rule.patterns != '':
		record_keyword(user_profile.user_id, reply_rule.patterns)  #记录用户发送的关键词
	return reply_rule


########################################################################
# get_auto_reply_message_by_type_for_cache: 根据消息类型获取自动回复
########################################################################
def get_auto_reply_message_by_type_for_cache(user_profile, reply_type):
	def inner_func():
		webapp_id = user_profile.webapp_id
		if reply_type == FOLLOW_TYPE:
			reply_rule = qa_util.find_follow_answer_for(user_profile)
		elif reply_type == UNMATCH_TYPE:
			reply_rule = qa_util.find_unmatch_answer_for(user_profile)
		else:
			return None
		if not reply_rule:
			# user_profile = UserProfile.objects.get(webapp_id=webapp_id)
			webapp_owner_id = user_profile.user_id
			msg = u"获得user('{}')对应的 qa type {}构建cache失败，可能该app没有设置对应的自动回复内容"\
					.format(webapp_owner_id, reply_type)
			watchdog_info(msg, user_id=webapp_owner_id)

		return {
				'keys': [
					'auto_qa_message_webapp_id_%s_type_%s' % (webapp_id, reply_type)
				],
				'value': reply_rule
			}
	return inner_func

def get_auto_reply_message_by_type(user_profile, reply_type):
	if not reply_type or reply_type == '':
		return None
	key = 'auto_qa_message_webapp_id_%s_type_%s' % (user_profile.webapp_id, reply_type)
	reply_rule = cache_util.get_from_cache(key, get_auto_reply_message_by_type_for_cache(user_profile, reply_type))
	
	return _parse_rule(user_profile, reply_rule)


############################################################################################
# update_auto_qa_message_material_cache: 更新自动回复消息缓存，包括素材、关键词和素材id
############################################################################################
from django.dispatch.dispatcher import receiver
from django.db.models import signals
from weapp.hack_django import post_update_signal

def update_auto_qa_message_cache(**kwargs):
	if hasattr(cache, 'request'):
		if hasattr(cache.request.user_profile, 'webapp_id'):
			webapp_id = cache.request.user_profile.webapp_id

			key = 'auto_qa_message_webapp_id_%s_*' % (webapp_id)
			cache_util.delete_pattern(key)

post_update_signal.connect(update_auto_qa_message_cache, sender=News, dispatch_uid = "material_news.update")
signals.post_save.connect(update_auto_qa_message_cache, sender=News, dispatch_uid = "material_news.save")

post_update_signal.connect(update_auto_qa_message_cache, sender=Rule, dispatch_uid = "qa_rule.update")
signals.post_save.connect(update_auto_qa_message_cache, sender=Rule, dispatch_uid = "qa_rule.save")

signals.post_delete.connect(update_auto_qa_message_cache, sender=News, dispatch_uid = "material_news.delete")
signals.post_delete.connect(update_auto_qa_message_cache, sender=Rule, dispatch_uid = "qa_rule.delete")