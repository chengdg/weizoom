# -*- coding: utf-8 -*-

__author__ = 'chuter'


from account.models import UserProfile
from models import *
from weixin.message.material.models import News
from weixin import cache_util

###############################################################################
# find_answer_from_cache_for: 从缓存中寻找user的配置中，与query匹配的答案
###############################################################################
def find_answer_from_cache_for(user_profile, query):
	return cache_util.get_auto_qa_message_material(user_profile, query)

def find_follow_answer_from_cache_for(user_profile):
	return cache_util.get_auto_reply_message_by_type(user_profile, FOLLOW_TYPE)

def find_unmatch_answer_from_cache_for(user_profile):
	return cache_util.get_auto_reply_message_by_type(user_profile, UNMATCH_TYPE)