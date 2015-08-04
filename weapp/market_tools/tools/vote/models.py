# -*- coding: utf-8 -*-

__author__ = 'chuter'

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

from modules.member.models import *

VOTE_TYPE_SINGLE = 0
VOTE_TYPE_MULTI = 1

SHOW_STYLE_MATRIX = 0
SHOW_STYLE_LINE = 1
#===============================================================================
# Vote: 投票
#===============================================================================
class Vote(models.Model):
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=18, verbose_name=u'投票名称')
	detail = models.TextField(verbose_name=u'投票详情', null=True, blank=True, default='')
	type = models.IntegerField(max_length=1, default=VOTE_TYPE_SINGLE)
	enable_other_options = models.BooleanField(verbose_name=u'是否启用输入其它选项', default=False)
	is_sort_by_votes = models.BooleanField(verbose_name=u'是否按票数进行排序', default=True)
	award_prize_info = models.TextField(default='{"id":-1,"name":"non-prize","type":"无奖励"}', verbose_name=u'奖品信息')
	created_at = models.DateTimeField(auto_now_add=True) #创建时间
	is_non_member = models.BooleanField(default=False)
	show_style = models.IntegerField(max_length=1, default=SHOW_STYLE_MATRIX)

	class Meta(object):
		db_table = 'market_tool_vote'
		verbose_name = '投票'
		verbose_name_plural = '投票'

	@property
	def is_reward_by_votes(self):
		return self.reward_points_for_vote > 0

	@staticmethod
	def get_webapp_user_voted_votes(webapp_user):
		webapp_user_voted_options_relations = VoteOptionHasWebappUser.voted_options_by_webapp_user(webapp_user)

		webapp_user_voted_options = []
		for webapp_user_voted_options_relation in webapp_user_voted_options_relations:
			webapp_user_voted_options.append(webapp_user_voted_options_relation.vote_option)

		vote_id_to_votes = {}
		for webapp_user_voted_option in webapp_user_voted_options:
			vote_id_to_votes[webapp_user_voted_option.vote.id] = webapp_user_voted_option.vote
		return vote_id_to_votes.values()

	@staticmethod
	def has_voted_by_webapp_user(vote_id, webapp_user):
		if (vote_id is None) or (vote_id <= 0)  or (webapp_user is None):
			return False

		options = VoteOption.objects.filter(vote_id=vote_id)
		option_ids = [option.id for option in options]
		option_has_webapp_users = VoteOptionHasWebappUser.objects.filter(webapp_user=webapp_user, vote_option_id__in=option_ids)
		return option_has_webapp_users.count() > 0
	
	@staticmethod
	def webapp_user_vote(vote_id, webapp_user):
		if (vote_id is None) or (vote_id <= 0)  or (webapp_user is None):
			return False

		options = VoteOption.objects.filter(vote_id=vote_id)
		option_ids = [option.id for option in options]
		option_has_webapp_users = VoteOptionHasWebappUser.objects.filter(webapp_user=webapp_user, vote_option_id__in=option_ids)
		
		if option_has_webapp_users.count():
			return option_has_webapp_users[0]
		else:
			return None

#########################################################################
# VoteOption：投票选项
#########################################################################
class VoteOption(models.Model):
	vote = models.ForeignKey(Vote)
	name = models.CharField(max_length=24, verbose_name=u'选项名称')
	pic_url = models.CharField(max_length=256)
	vote_count = models.IntegerField(default=0, verbose_name=u'票数')

	class Meta(object):
		db_table = 'market_tool_vote_option'
		verbose_name = '投票选项'
		verbose_name_plural = '投票选项'

	def to_json(self):
		option_json = dict()
		option_json['name'] = self.name
		option_json['pic_url'] =  self.pic_url
		option_json['vote_count'] = self.vote_count
		option_json['id'] = self.id
		return option_json

	@property
	def voted_webapp_users_count(self):
		if hasattr(self, '_voted_webapp_users_count'):
			return self._voted_webapp_users_count
		
		self._voted_webapp_users_count = VoteOptionHasWebappUser.objects.filter(vote_option_id=self.id).count()
		return self._voted_webapp_users_count
	
	@property
	def voted_members_count(self):
		if hasattr(self, '_voted_members_count'):
			return self._voted_members_count
		
		voted_webapp_users = [relation.webapp_user for relation in VoteOptionHasWebappUser.objects.filter(vote_option_id=self.id)]
		
		member_ids = [webapp_user.member_id for webapp_user in voted_webapp_users]
		
		self._voted_members_count = Member.objects.filter(id__in=member_ids).count()
		
		return self._voted_members_count

	@staticmethod
	def vote_by_webapp_user(vote_option_id, webapp_user):
		if (webapp_user is None) or (vote_option_id is None) or (vote_option_id <= 0):
			return

		from django.db import connection, transaction
		cursor = connection.cursor()
		cursor.execute('update market_tool_vote_option set vote_count=vote_count+1 where id = %d' % (vote_option_id))
		transaction.commit_unless_managed()
		
		VoteOptionHasWebappUser.create(vote_option_id, webapp_user)

#########################################################################
# VoteOptionHasWebappUser：投票记录
#########################################################################
class VoteOptionHasWebappUser(models.Model):
	vote_option = models.ForeignKey(VoteOption)
	webapp_user = models.ForeignKey(WebAppUser)
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = 'market_tool_vote_option_has_webapp_user'
		verbose_name = '投票记录'
		verbose_name_plural = '投票记录'

	@staticmethod
	def create(vote_option_id, webapp_user):
		return VoteOptionHasWebappUser.objects.create(
			vote_option_id = vote_option_id, 
			webapp_user = webapp_user
			)

	@staticmethod
	def voted_options_by_webapp_user(webapp_user):
		return VoteOptionHasWebappUser.objects.filter(webapp_user=webapp_user)

	@staticmethod
	def voted_options_by_webapp_user_for_vote(webapp_user, vote_id):
		if (webapp_user is None) or (vote_id <= 0):
			return []

		webapp_user_voted_options = [option_has_webapp_user.vote_option for option_has_webapp_user in VoteOptionHasWebappUser.objects.filter(webapp_user=webapp_user)]
		return [webapp_user_voted_option for webapp_user_voted_option in webapp_user_voted_options \
			if webapp_user_voted_option.vote.id == vote_id]