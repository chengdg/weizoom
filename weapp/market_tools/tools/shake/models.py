# -*- coding: utf-8 -*-
from datetime import timedelta, datetime, date

from django.db import models
from django.contrib.auth.models import User
from modules.member.models import Member
from market_tools.prize.models import Prize


#########################################################################
#摇一摇设置：shake
#########################################################################
class Shake(models.Model):
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=100, default='', verbose_name='名称')
	#total_award_value = models.TextField(verbose_name='总额值')
	not_winning_desc = models.TextField(verbose_name='未中奖描述')
	detail = models.TextField(verbose_name='活动描述')
	#daily_play_count = models.IntegerField(default=1, verbose_name='每人每天参与次数')
	#can_repeat = models.BooleanField(default=False) #是否可重复参与
	is_deleted = models.BooleanField(default=False) #是否删除
	#expected_participation_count = models.IntegerField() #预计参与人数
	#is_non_member = models.BooleanField(default=False) #是否非会员可参与
	#logo_url = models.CharField(max_length=1024) #商标图片
	wishing  = models.CharField(max_length=1024) #红包祝福语
	remark = models.CharField(max_length=1024) #猜越多得越多，快来抢！
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'market_tool_shake'
		verbose_name = '摇一摇现金'
		verbose_name_plural = '摇一摇现金'
		ordering = ['-id']

	
		
#########################################################################
# 摇一摇详情设置：shake_detail
#########################################################################	
class ShakeDetail(models.Model):
	shake = models.ForeignKey(Shake)
	start_at = models.DateTimeField()
	end_at = models.DateTimeField()
	play_count = models.IntegerField(default=1, verbose_name='每人每天参与次数')
	total_money = models.DecimalField(max_digits=16, decimal_places=2, default=0)#models.FloatField(default=0.0, verbose_name='奖池总金额')  #奖池总金额
	random_price_start = models.DecimalField(max_digits=16, decimal_places=2, default=0)#models.FloatField(default=1,verbose_name="随机初始金额") #'1-10'
	random_price_end = models.DecimalField(max_digits=16, decimal_places=2, default=0)#models.FloatField(default=1,verbose_name="随机最大金额") #'1-10'
	residue_price = models.DecimalField(max_digits=16, decimal_places=2, default=0)#models.FloatField(default=0,verbose_name="剩余金额") #'1-10'
	fixed_price = models.DecimalField(max_digits=16, decimal_places=2, default=0)#models.FloatField(default=0.0)  #固定金额红包
	fixed_price_number = models.IntegerField(default=0)  #固定金额红包数量
	fixed_price_residue_number = models.IntegerField(default=0)  #固定金额红包使用数量

	class Meta(object):
		db_table = 'market_tool_shake_detail'
		verbose_name = '红包奖品'
		verbose_name_plural = '红包奖品'


#########################################################################
# ShakeRecord：中奖记录
#########################################################################
class ShakeRecord(models.Model):
	owner = models.ForeignKey(User)
	shake_detail = models.ForeignKey(ShakeDetail)
	member = models.ForeignKey(Member)
	money = models.DecimalField(max_digits=16, decimal_places=2, default=0)
	is_sended = models.BooleanField(default=False)
	return_code = models.CharField(max_length=1024, default='') #发送后return 
	return_msg = models.CharField(max_length=1024, default='') #发送后return code
	xml_msg = models.CharField(max_length=1024, default='') #发送后xml
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'market_tool_shake_record'
		verbose_name = '摇一摇中奖记录'
		verbose_name_plural = '摇一摇中奖记录'
