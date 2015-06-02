# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import F
from modules.member.models import Member

#===============================================================================
# MemberComplainSettings: 会员投诉设置
#===============================================================================
AWARD_INTEGRAL = 3 #积分
AWARD_COUPON = 1 #优惠劵
AWARD_NONE = 0
class MemberComplainSettings(models.Model):
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=100)
	detail = models.TextField(verbose_name=u'详情', null=True, blank=True, default='')
	is_allowed_image = models.BooleanField(default=False) #是否需要上传图片
	prize_type = models.IntegerField(max_length=1, verbose_name=u"奖励类型", default=AWARD_NONE) 
	prize_content = models.CharField(max_length=100)
	is_non_member = models.BooleanField(default=False) 
	created_at = models.DateTimeField(auto_now_add=True) #创建时间

	class Meta(object):
		db_table = 'market_tool_member_complain'
		verbose_name = '会员投诉'
		verbose_name_plural = '会员投诉'


#===============================================================================
# MemberComlainRecord: 会员反馈记录
#===============================================================================
class MemberComplainRecord(models.Model):
	complain_settings = models.ForeignKey(MemberComplainSettings)
	webapp_user_id = models.IntegerField(default=-1)
	pic_url = models.CharField(max_length=256) 
	content = models.CharField(max_length=256) 
	created_at = models.DateTimeField(auto_now_add=True) #创建时间	

	class Meta(object):
		db_table = 'market_tool_member_complain_record'
		verbose_name = '会员投诉记录'
		verbose_name_plural = '会员投诉记录'

	
# #===============================================================================
# # MemberFeedbackSettings: 会员反馈设置
# #===============================================================================

# class MemberFeedbackSettings(models.Model):
# 	owner = models.ForeignKey(User)
# 	name = models.CharField(max_length=100)
# 	detail = models.TextField(verbose_name=u'详情', null=True, blank=True, default='')
# 	is_allowed_image = models.BooleanField(default=False) #是否需要上传图片
# 	prize_type = models.IntegerField(max_length=1, verbose_name=u"奖励类型", default=AWARD_INTEGRAL) 
# 	prize_content = models.CharField(max_length=100)
# 	created_at = models.DateTimeField(auto_now_add=True) #创建时间

# 	class Meta(object):
# 		db_table = 'market_tool_member_feedback'
# 		verbose_name = '会员反馈'
# 		verbose_name_plural = '会员二维码'


# #===============================================================================
# # MemberComlainRecord: 会员反馈记录
# #===============================================================================
# class MemberFeedbackRecord(models.Model):
# 	feedback_settings = models.ForeignKey(MemberComplainSettings)
# 	member_id = models.IntegerField()
# 	pic_url = models.CharField(max_length=256) 
# 	content = models.CharField(max_length=256) 
# 	created_at = models.DateTimeField(auto_now_add=True) #创建时间	

# 	class Meta(object):
# 		db_table = 'market_tool_member_feedback_record'
# 		verbose_name = '会员反馈记录'
# 		verbose_name_plural = '会员反馈记录'
