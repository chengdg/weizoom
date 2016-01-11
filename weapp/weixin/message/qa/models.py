# -*- coding: utf-8 -*-

__author__ = 'chuter'

from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

#########################################################################
# Rule：规则
#########################################################################
TEXT_TYPE = 1
NEWS_TYPE = 2
FOLLOW_TYPE = 3
UNMATCH_TYPE = 4
MENU_TYPE = 5
RULE_TYPES = (
	(TEXT_TYPE, '文本消息'),
	(NEWS_TYPE, '图文消息'),
	(FOLLOW_TYPE, '关注回复消息'),
	(UNMATCH_TYPE, '自动回复'),
	(MENU_TYPE, '自定义菜单回复')
)
RULE_ACTIVE_TYPE_INACTIVE = 0
RULE_ACTIVE_TYPE_ACTIVE = 1
RULE_ACTIVE_TYPE_TIMED_ACTIVE = 2
class Rule(models.Model):
	owner = models.ForeignKey(User)
	type = models.IntegerField(default=TEXT_TYPE, choices=RULE_TYPES)
	active_type = models.IntegerField(default=RULE_ACTIVE_TYPE_ACTIVE) #启用类型
	start_hour = models.IntegerField(default=0) #启用时间，在active_type = RULE_ACTIVE_TYPE_TIMED_ACTIVE有用
	end_hour = models.IntegerField(default=0) #禁用时间，在active_type = RULE_ACTIVE_TYPE_TIMED_ACTIVE有用
	created_at = models.DateTimeField(auto_now_add=True) #添加时间
	patterns = models.CharField(max_length=1024) #匹配词，以英文竖线'|'分隔
	answer = models.CharField(max_length=2048) #回答
	material_id = models.IntegerField(default=0) #素材id，type为NEWS_TYPE时有效
	#weapp 10.0 bert add
	is_url = models.BooleanField(default=False) #是否是url

	class Meta(object):
		managed = False
		db_table = 'qa_rule'
		verbose_name = '规则'
		verbose_name_plural = '规则'

	@property
	def is_news_type(self):
		return self.type == NEWS_TYPE or self.material_id > 0

	@property
	def is_active(self):
		if hasattr(self, '_is_active'):
			return self._is_active

		if self.active_type == RULE_ACTIVE_TYPE_ACTIVE:
			self._is_active = True
		elif self.active_type == RULE_ACTIVE_TYPE_INACTIVE:
			self._is_active = False
		else: #RULE_ACTIVE_TYPE_TIMED_ACTIVE
			cur_hour = datetime.now().hour
			self._is_active = cur_hour >= self.start_hour and cur_hour < self.end_hour

		return self._is_active

	@staticmethod
	def get_keyword_reply_rule(user, is_include_menu_reply_rule=False, order_query='-id'):
		query_types = [TEXT_TYPE, NEWS_TYPE]
		if is_include_menu_reply_rule:
			query_types.append(MENU_TYPE)
			
		return Rule.objects.filter(owner=user, type__in=query_types).order_by(order_query)


#########################################################################
# has_duplicate_pattern：检查是否有重复的pattern
#########################################################################
def has_duplicate_pattern(user, new_patterns, ignore_rule=None):
	#处理ignore_rule
	if ignore_rule:
		ignore_rule = int(ignore_rule)
	else:
		ignore_rule = -1

	#获得关键词回复规则
	rules = Rule.get_keyword_reply_rule(user, True)

	pattern2rule = {}
	for rule in rules:
		if ignore_rule and rule.id == ignore_rule:
			continue
		patterns = rule.patterns.split('|')
		for pattern in patterns:
			pattern2rule[pattern.strip().lower()] = rule

	existed_patterns = []
	for new_pattern in new_patterns.split('|'):
		if new_pattern in pattern2rule:
			existed_patterns.append(new_pattern)

	return len(existed_patterns) > 0, existed_patterns
