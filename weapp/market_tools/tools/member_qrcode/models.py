# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import F
from modules.member.models import Member

# from shop.models import Site
#from core import dateutil

# class QcrodLogin(models.Model):
# 	ticket = models.TextField()
# 	token = models.CharField(max_length=100, null=True)
# 	is_login = models.IntegerField(default=0) #如果重复使用ticke时 is_login 0时未登录 1：登录
# 	created_at = models.DateTimeField(auto_now_add=True)

# 	class Meta(object):
# 		db_table = 'qcrod_login'
# 		verbose_name = '二维码登录'
# 		verbose_name_plural = '二维码登录'

# #######################################################################################
# # 当二维码登录页面刷新时 如果没有用户扫描登录则重复使用ticket
# #######################################################################################

# class QcrodLoginTicket(models.Model):
# 	uuid =  models.CharField(max_length=100)
# 	shop_name = models.CharField(max_length=10)
# 	ticket = models.TextField()
# 	expired_second = models.IntegerField()
# 	created_time = models.IntegerField()
	
# 	class Meta(object):
# 		db_table = 'qcrod_login_ticket'
# 		verbose_name = '二维码登录ticket'
# 		verbose_name_plural = '二维码登录ticket'	

# class SpreadQrcode(models.Model):
# 	ticket = models.TextField()
# 	open_id = models.CharField(max_length=50) #微博id 。。
# 	token = models.CharField(max_length=50,default='') # token 公众账号下该会员的token信息
# 	task_id = models.CharField(max_length=10)
# 	is_used = models.IntegerField(default=0) #是否使用
# 	is_buyed = models.IntegerField(default=0) #是否购买商品
# 	is_active = models.IntegerField(default=1) #是有效
# 	created_at = models.DateTimeField(auto_now_add=True)

# 	class Meta(object):
# 		db_table = 'spread_qcrod'
# 		verbose_name = '推广二维码'
# 		verbose_name_plural = '推广二维码'

AWARD_INTEGRAL = 3 #积分
AWARD_COUPON = 1 #优惠劵
AWARD_MEMBER_TYPE_ALL = 1 #统一奖励
AWARD_MEMBER_TYPE_LEVEL = 0 #按会员等级奖励
#===============================================================================
# MemberQrcode: 会员二维码设置
#===============================================================================
class MemberQrcodeSettings(models.Model):
	owner = models.ForeignKey(User)
	detail = models.TextField(verbose_name=u'详情', null=True, blank=True, default='')
	award_member_type = models.IntegerField(max_length=1, verbose_name=u'扫码后奖励会员', default=AWARD_MEMBER_TYPE_ALL) #扫码后奖励类型
	created_at = models.DateTimeField(auto_now_add=True) #创建时间

	class Meta(object):
		db_table = 'market_tool_member_qrcode_settings'
		verbose_name = '会员二维码配置'
		verbose_name_plural = '会员二维码配置'


class MemberQrcodeAwardContent(models.Model):
	member_qrcode_settings = models.ForeignKey(MemberQrcodeSettings)
	member_level =  models.IntegerField(max_length=1, verbose_name=u"会员等级", default=-1) 
	award_type = models.IntegerField(max_length=1, verbose_name=u"奖励类型", default=AWARD_INTEGRAL) 
	award_content = models.CharField(max_length=256, verbose_name=u'奖励内容') #目前奖励内容为：1，奖励积分分值 2，优惠券id
	created_at = models.DateTimeField(auto_now_add=True) #创建时间

	class Meta(object):
		db_table = 'market_tool_member_qrcode_award_content'
		verbose_name = '会员二维码奖励内容'
		verbose_name_plural = '会员二维码奖励内容'

	# @property
	# def is_reward_by_votes(self):
	# 	return self.reward_points_for_vote > 0

	# @staticmethod
	# def get_member_voted_votes(member):
	# 	member_voted_options_relations = VoteOptionHasMember.voted_options_by_member(member)

	# 	member_voted_options = []
	# 	for member_voted_options_relation in member_voted_options_relations:
	# 		member_voted_options.append(member_voted_options_relation.vote_option)

	# 	vote_id_to_votes = {}
	# 	for member_voted_option in member_voted_options:
	# 		vote_id_to_votes[member_voted_option.vote.id] = member_voted_option.vote

	# 	return vote_id_to_votes.values()

	# @staticmethod
	# def has_voted_by_member(vote_id, member):
	# 	if (vote_id is None) or (vote_id <= 0)  or (member is None):
	# 		return False

	# 	options = VoteOption.objects.filter(vote_id=vote_id)
	# 	option_ids = [option.id for option in options]
	# 	option_has_members = VoteOptionHasMember.objects.filter(member=member, vote_option_id__in=option_ids)
	# 	return option_has_members.count() > 0

class MemberQrcode(models.Model):
	owner = models.ForeignKey(User)
	ticket = models.CharField(default='', max_length=256)
	#ticket = models.TextField() #获取的ticket值
	member = models.ForeignKey(Member) #会员id
	expired_second = models.IntegerField(default=1800) #临时二维码失效时间
	created_time = models.IntegerField()
	is_active = models.IntegerField(default=1)
	created_at = models.DateTimeField(auto_now_add=True) #创建时间

	class Meta(object):
		db_table = 'market_tool_member_qrcode'
		verbose_name = '会员二维码'
		verbose_name_plural = '会员二维码'

class MemberQrcodeLog(models.Model):
	member_qrcode = models.ForeignKey(MemberQrcode)
	member_id = models.CharField(max_length=100, db_index=True)

	class Meta(object):
		db_table = 'market_tool_member_qrcode_log'
		verbose_name = '会员二维码使用记录'
		verbose_name_plural = '会员二维码使用记录'
