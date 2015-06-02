# -*- coding: utf-8 -*-
__author__ = 'bert'

from datetime import datetime

from django.conf import settings
from django.db import models
from django.db.models import signals, F, Sum
from django.contrib.auth.models import User

from modules.member.models import *
from modules.member.integral import *

from core.exceptionutil import full_stack, unicode_full_stack

from watchdog.utils import watchdog_fatal, watchdog_error, watchdog_debug, watchdog_info

#===============================================================================
# ShengjingBindingMember: ShengjingBindingMember 手机号绑定的weapp会员
#===============================================================================
class ShengjingBindingMember(models.Model):
	member_id = models.IntegerField(default=0, db_index=True) #会员记录的id
	webapp_id = models.CharField(max_length=20, verbose_name='webapp id')
	phone_number = models.CharField(max_length=32, blank=True)
	captcha = models.CharField(max_length=11, blank=True) #验证码
	created_at = models.DateTimeField(auto_now_add=True) #创建时间

	class Meta(object):
		db_table = 'shengjing_binding_member'
		verbose_name = '会员绑定手机号'
		verbose_name_plural = '会员绑定手机号'

	########################################################################
	# get_bingding_friends: 根据member获取绑定的好友信息
	########################################################################
	@staticmethod
	def get_binding_friends(member):
		binding_ids = list()
		for member_relation in  MemberFollowRelation.objects.filter(member_id=member.id, is_fans=True):
			if member_relation.follower_member_id > 0 and ShengjingBindingMember.objects.filter(member_id=member_relation.follower_member_id).count() > 0:
				binding_ids.append(ShengjingBindingMember.objects.filter(member_id=member_relation.follower_member_id)[0].id)
		binding_member_infos = ShengjingBindingMemberInfo.objects.filter(binding_id__in=binding_ids)
		for binding_member_info in binding_member_infos:
			binding_member_info.companys = ShengjingBindingMemberHasCompanys.objects.filter(binding=binding_member_info.binding)
			binding_member_info.member = Member.objects.get(id=binding_member_info.binding.member_id)

		return binding_member_infos

	########################################################################
	# has_member_with_phone_number(phone_number, member_id, webapp_id): 判断会员和手机号是否绑定过
	########################################################################
	@staticmethod
	def has_member_with_phone_number(phone_number, member_id, webapp_id):
		return True if ShengjingBindingMember.objects.filter(phone_number=phone_number, webapp_id=webapp_id, member_id=member_id).count() > 0 else False

	@staticmethod
	def is_can_binding(phone_number, member_id, webapp_id):
		if ShengjingBindingMember.objects.filter(webapp_id=webapp_id, member_id=member_id).count() > 0:
			return False

		if ShengjingBindingMember.objects.filter(phone_number=phone_number, webapp_id=webapp_id, member_id__gt=0).count() > 0:
			return False

		return True

	@staticmethod
	def has_record_with_phone_number(phone_number, webapp_id):
		return True if ShengjingBindingMember.objects.filter(phone_number=phone_number, webapp_id=webapp_id).count() > 0 else False

	@staticmethod
	def validated_phone_aptcha(phone_number, captcha, webapp_id):
		return True if ShengjingBindingMember.objects.filter(phone_number=phone_number, captcha=captcha, webapp_id=webapp_id).count() == 0 else False


#===============================================================================
# ShengjingBindingMemberInfo: 绑定会员信息
#===============================================================================
LEADER = 1
STAFF = 2
OUTSIDER = 0
IDENTITYS = (
	(OUTSIDER, '非盛景学员'),
	(STAFF, '盛景学员'),
	(LEADER, '盛景学员'),
)
class ShengjingBindingMemberInfo(models.Model):
	binding = models.ForeignKey(ShengjingBindingMember)
	name = models.TextField(default='')#姓名
	position = models.TextField(default='')
	status = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True) #创建时间

	class Meta(object):
		db_table = 'shengjing_binding_member_info'
		verbose_name = '会员绑定手机号'
		verbose_name_plural = '会员绑定手机号'

	@property
	def status_name(self):
		if hasattr(self, '_status_name'):
			return self._status_name
		else:
			try:				
				self._status_name = ''
				for item in IDENTITYS:
					if item[0] == self.status:
						self._status_name = item[1]
				return self._status_name
			except:
				return None

#===============================================================================
# ShengjingBindingMemberInfo: 绑定会员信息
#===============================================================================
LEADER = 1
STAFF = 2
OUTSIDER = 0
class ShengjingBindingMemberHasCompanys(models.Model):
	binding = models.ForeignKey(ShengjingBindingMember)
	name = models.CharField(max_length=256, blank=True) #姓名
	created_at = models.DateTimeField(auto_now_add=True) #创建时间
	
	class Meta(object):
		db_table = 'shengjing_binding_member_has_companys'
		verbose_name = '会员绑定手机号'
		verbose_name_plural = '会员绑定手机号'
		

#===============================================================================
# ShengjingCourseRegistration: ShengjingCourseRegistration 会员课程报名
#===============================================================================
class ShengjingCourseRegistration(models.Model):
	owner_id = models.IntegerField(default=0, db_index=True) #管理者的id
	referrer = models.CharField(max_length=256, blank=True) #推荐人
	member_id = models.IntegerField(default=0, db_index=True) #会员记录的id
	course_id = models.IntegerField(default=0, db_index=True) #课程id
	apply_number = models.IntegerField(default=0, db_index=True) #报名人数
	created_at = models.DateTimeField(auto_now_add=True) #创建时间

	class Meta(object):
		db_table = 'shengjing_course_registration'
		verbose_name = '会员课程报名'


#===============================================================================
# ShengjingEmailSettings: ShengjingEmailSettings 邮箱配置
#===============================================================================
class ShengjingEmailSettings(models.Model):
	owner = models.ForeignKey(User, unique=True) #管理者的id
	course_registration_email = models.CharField(max_length=100) #课程报名成功发送邮箱
	created_at = models.DateTimeField(auto_now_add=True) #创建时间

	class Meta(object):
		db_table = 'shengjing_email_settings'
		verbose_name = '胜景邮箱设置'
		
#===============================================================================
# ShengjingCourseConfig: ShengjingCourse 课程详情配置
#===============================================================================
class ShengjingCourseConfig(models.Model):
	owner = models.ForeignKey(User) #管理者的id
	name = models.CharField(max_length=50) #名称
	description = models.TextField() #课程详情描述
	introduction = models.CharField(max_length=500) #课程简介
	course_cover_pic_url = models.CharField(max_length=200) #课程封面图片
	update_time = models.DateTimeField(auto_now_add=True) #修改时间
	non_participants = models.BooleanField(default=0) # 非学员是否可报名
	created_at = models.DateTimeField(auto_now_add=True) #创建时间

	class Meta(object):
		db_table = 'shengjing_course_config'
		verbose_name = '课程详情配置'
		

#===============================================================================
# ShengjingCourseRelation 课程关系 
#===============================================================================
class ShengjingCourseRelation(models.Model):
	owner = models.ForeignKey(User) #管理者的id
	config = models.ForeignKey(ShengjingCourseConfig) #课程详情配置id
	course_id = models.IntegerField(default=0) #课程id
	created_at = models.DateTimeField(auto_now_add=True) #创建时间

	class Meta(object):
		db_table = 'shengjing_course_relation'
		verbose_name = '课程关系'


#########################################################################
# ShengjingIntegralStrategySttings
#########################################################################
class ShengjingIntegralStrategySttings(models.Model):
	webapp_id = models.CharField(max_length=20, verbose_name='webapp id', db_index=True, unique=True)
	binding_for_father = models.IntegerField(verbose_name='绑定胜景信息为上一级别增加积分', default=10)
	become_member_of_shengjing_for_father = models.IntegerField(verbose_name='在胜景成为会员为上级节点增加积分', default=10)
	after_applied_course = models.IntegerField(verbose_name='报名课程后增加的积分', default=0)
	
	class Meta(object):
		db_table = 'shengjing_integral_strategy_settings'
		verbose_name = '胜景积分策略配置'
		verbose_name_plural = '胜景积分策略配置'

	@staticmethod
	def increase_integral_for_father_by_binding_id(binding_id, webapp_id):
		try:
			member, settings = get_increase_member_and_integral_settings(binding_id, webapp_id)
			if member and settings:
				increase_member_integral(member, settings.binding_for_father, u'好友奖励')
		except:
			notify_msg = u"绑定成功后给上级节点增加积分，cause:\n{}".format(unicode_full_stack())
			watchdog_error(notify_msg)


	@staticmethod
	def increase_integral_become_member_of_shengjing_for_father(binding_id, webapp_id):
		try:
			member, settings = get_increase_member_and_integral_settings(binding_id, webapp_id)
			if member and settings:
				increase_member_integral(member, settings.become_member_of_shengjing_for_father, u'好友奖励')
		except:
			notify_msg = u"推荐他人成为盛景学员增加的积分，cause:\n{}".format(unicode_full_stack())
			watchdog_error(notify_msg)		
			

def get_increase_member_and_integral_settings(binding_id, webapp_id):
	if ShengjingBindingMember.objects.filter(id=binding_id).count() > 0\
			and ShengjingIntegralStrategySttings.objects.filter(webapp_id=webapp_id).count() > 0 and webapp_id:
		member_id = ShengjingBindingMember.objects.filter(id=binding_id)[0].member_id
		if MemberFollowRelation.objects.filter(follower_member_id=member_id, is_fans=True).count() > 0:
			father_member_id = MemberFollowRelation.objects.filter(follower_member_id=member_id, is_fans=True)[0].member_id
			member = Member.objects.get(id=father_member_id)
			if ShengjingBindingMember.objects.filter(member_id=member.id).count() > 0:
				return member, ShengjingIntegralStrategySttings.objects.filter(webapp_id=webapp_id)[0]
	return None, None
