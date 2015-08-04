# -*- coding: utf-8 -*-
from datetime import timedelta, datetime, date

from django.db import models
from django.contrib.auth.models import User
from modules.member.models import Member
from market_tools.prize.models import Prize


#########################################################################
# RedEnvelope：红包
#########################################################################
class RedEnvelope(models.Model):
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=100, default='', verbose_name='名称')
	total_award_value = models.TextField(verbose_name='总额值')
	desc = models.TextField(verbose_name='描述')
	daily_play_count = models.IntegerField(default=1, verbose_name='每人每天参与次数')
	can_repeat = models.BooleanField(default=False) #是否可重复参与
	is_deleted = models.BooleanField(default=False) #是否删除
	expected_participation_count = models.IntegerField() #预计参与人数
	is_non_member = models.BooleanField(default=False) #是否非会员可参与
	logo_url = models.CharField(max_length=1024) #商标图片
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'market_tool_red_envelope'
		verbose_name = '红包'
		verbose_name_plural = '红包'
		ordering = ['-id']

	def get_involved_count(self):
		return RedEnvelopeRecord.objects.filter(red_envelope=self).values("id").count()
		
#########################################################################
# RedEnvelopeHasPrize：红包奖品
#########################################################################	
class RedEnvelopeHasPrize(models.Model):
	red_envelope = models.ForeignKey(RedEnvelope)
	prize = models.ForeignKey(Prize)
	prize_type = models.IntegerField(verbose_name='奖品类别') #0实物，1优惠券，2兑换码，3积分
	prize_source = models.CharField(max_length=100, default='', verbose_name='奖品来源')
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'market_tool_red_envelope_has_prize'
		verbose_name = '红包奖品'
		verbose_name_plural = '红包奖品'


#########################################################################
# RedEnvelopeRecord：中奖记录
#########################################################################
class RedEnvelopeRecord(models.Model):
	owner = models.ForeignKey(User)
	webapp_user_id = models.IntegerField(default=-1)
	red_envelope = models.ForeignKey(RedEnvelope)
	red_envelope_name = models.CharField(max_length=100) #活动名称
	prize_type = models.IntegerField() #0实物，1优惠券，2兑换码，3积分
	prize_name = models.CharField(max_length=30) #中奖名称
	prize_level = models.IntegerField(default=0) #中奖等级
	prize_number = models.CharField(max_length=30) #中奖编号
	prize_detail = models.CharField(max_length=30) #中奖详情  奖品名称、优惠券码
	prize_position = models.IntegerField(default=0) #中奖位置
	prize_money = models.DecimalField(max_digits=65, decimal_places=2) #优惠券金额
	created_at = models.DateTimeField(auto_now_add=True)
	awarded_at = models.DateTimeField(auto_now_add=True)
	is_awarded = models.BooleanField(default=False) #是否发奖

	class Meta(object):
		db_table = 'market_tool_red_envelope_record'
		verbose_name = '红包中奖记录'
		verbose_name_plural = '红包中奖记录'
		ordering = ['-id']
