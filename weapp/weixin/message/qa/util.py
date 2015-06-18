# -*- coding: utf-8 -*-

__author__ = 'chuter'


from account.models import UserProfile
#from models import *
from weixin2.models import *
from weixin.message.material.models import News
import random
import json
from .tasks import record_keyword

########################################################################
# find_answer_for: 寻找user的配置中，与query匹配的答案
########################################################################
def find_answer_for(user_profile, query):
	#获得关键词消息
	rules = list(Rule.objects.filter(owner=user_profile.user))

	#允许部分匹配的列表
	pattern2rule_sub_match = {}
	#完全匹配的规则列表
	pattern2rule_not_sub_match = {}
	for rule in rules:
		try:
			for patterns in json.loads(rule.patterns):
				pattern = patterns['keyword']
				is_sub_match = int(patterns['type'])

				if not pattern or pattern == '':
					continue

				if is_sub_match == 1:
					pattern2rule_sub_match[pattern.strip().lower()] = rule
				else:
					pattern2rule_not_sub_match[pattern.strip().lower()] = rule
		except:
			patterns = rule.patterns.split('|')
			for pattern in patterns:
				if pattern == '':
					continue
				pattern2rule_not_sub_match[pattern.strip().lower()] = rule

	#先处理完全匹配
	for (pattern, rule) in pattern2rule_not_sub_match.items():
		if pattern == query:
			rule.patterns = pattern  #记录此次命中的关键词
			return rule

	#处理部分匹配
	for (pattern, rule) in pattern2rule_sub_match.items():
		if pattern in query:
			rule.patterns = pattern  #记录此次命中的关键词
			return rule

	return None

def _get_reply_rule_for(user_profile, reply_type):
	#user_profile = UserProfile.objects.get(webapp_id=webapp_id)

	#获得回复规则
	rules = Rule.objects.filter(owner_id=user_profile.user_id, type=reply_type)
	if rules.count() == 0:
		return None

	return (list(rules))[0]

def return_reply_rule(reply_rule):
	if reply_rule is None:
		return None

	if reply_rule.material_id > 0:
		newses = list(News.objects.filter(material_id=reply_rule.material_id, is_active=True))
		reply_rule.newses = newses
		return reply_rule

	if len(reply_rule.answer.strip()) == 0:
		return None

	return reply_rule

########################################################################
# find_follow_answer_for: 寻找关注自动回复
########################################################################
def find_follow_answer_for(user_profile):
	reply_rule = _get_reply_rule_for(user_profile, FOLLOW_TYPE)
	return return_reply_rule(reply_rule)
	
########################################################################
# find_unmatch_answer_for: 寻找关键词不匹配时的返回消息
########################################################################
def find_unmatch_answer_for(user_profile):
	reply_rule = _get_reply_rule_for(user_profile, UNMATCH_TYPE)
	return return_reply_rule(reply_rule)
