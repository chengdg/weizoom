# -*- coding: utf-8 -*-

from django.db import models
from modules.member.models import *
from django.contrib.auth.models import Group, User

class ChannelDistributionQrcodeSettings(models.Model):
	"""
	渠道分销二维码
	"""
	owner = models.ForeignKey(User)  # 所有者
	bing_member_title = models.CharField(max_length=512)  # 关联会员头衔
	award_prize_info = models.TextField(default='{"id":-1,"name":"no-prize"}')  # 关注奖励,奖品信息
	reply_type = models.IntegerField(max_length=1, default=0)  # 扫码后行为：0普通关注一致，1回复文字，2回复图文
	reply_detail = models.TextField(default='')  # 回复文字, 当reply_type为1时有效
	reply_material_id = models.IntegerField(default=0) # 图文id，reply_type为2时有效
	coupon_ids = models.TextField()  # 配置过的优惠券id集合
	bing_member_id = models.IntegerField(default=0) # 关联会员:创建二维码时选择关联的会员的ID
	return_standard = models.IntegerField(default=0)  # 多少天结算标准
	group_id = models.IntegerField(default=-1)  # 会员分组
	distribution_rewards = models.BooleanField(default=False)  # 分销奖励 False:没有 True:佣金
	commission_rate = models.IntegerField()  # 佣金返现率
	minimun_return_rate = models.IntegerField()  # 最低返现折扣
	commission_return_standard = models.DecimalField(max_digits=65, decimal_places=2)  # 佣金返现标准
	ticket = models.CharField(default='', max_length=256)  # ticket

	will_return_reward = models.DecimalField(max_digits=65, decimal_places=2, default=0)  # 实施奖励
	bing_member_count = models.IntegerField(default=0)  # 关注数量,该二维码下边的关注人数
	total_transaction_volume = models.DecimalField(max_digits=65, decimal_places=2, default=0)  # 总交易额:二维码自创建以来的所有交易额
	total_return = models.DecimalField(max_digits=65, decimal_places=2, default=0)  # 返现总额: 二维码所有的返现总额, 只包含已经提现的金额

	status = models.IntegerField(default=0)  # 取现进度 (0无状态,1等待审核,2正在返现,)
	extraction_money = models.DecimalField(max_digits=65, decimal_places=2, default=0)  # 提取的金额 (当用户提取佣金的时候,才会变动)
	current_transaction_amount = models.DecimalField(max_digits=65, decimal_places=2, default=0)  # 本期交易额 (点击取现后,清空)????
	commit_time = models.DateTimeField(default='0001-01-01')  # 提交时间

	created_at = models.DateTimeField(auto_now_add=True) # 添加时间

	class Meta:
		db_table = 'market_tool_channel_distribution_qrcode_setting'
		ordering = ['-id']


class ChannelDistributionQrcodeHasMember(models.Model):
	"""
	渠道分销扫码的会员,关注会有奖励,重复扫码没有奖励
	"""
	channel_qrcode_id = models.IntegerField()  # 渠道分销id
	member_id = models.IntegerField()  # 渠道分销商下的会员
	# is_new = models.BooleanField(default=True)  # 新关注 ?
	cost_money = models.DecimalField(max_digits=65, decimal_places=2, default=0)  # 消费金额
	commission = models.DecimalField(max_digits=65, decimal_places=2, default=0)  # 带来的佣金
	buy_times = models.IntegerField(default=0)  # 购买次数
	created_at = models.DateTimeField(auto_now_add=True)  # 添加时间

	class Meta:
		db_table = 'market_tool_channel_distribution_qrcode_has_member'


class ChannelDistributionDetail(models.Model):
	"""
	渠道分销明细表
	"""
	channel_qrcode_id = models.IntegerField()  # 渠道分销id
	money = models.DecimalField(max_digits=65, decimal_places=2, default=0)  # 操作金额 正为收入,负为提现
	member_id = models.IntegerField()  # 对应的会员id
	last_extract_time = models.DateTimeField(blank=True, null=True)  # 上次提现时间
	created_at = models.DateTimeField(auto_now_add=True)  # 添加时间
	# effect_status = models.BooleanField(default=False)  # 生效状态 ??????
	order_id = models.IntegerField(default=0)  # 订单id
	# effect_time = models.DateTimeField(blank=True, null=True)  # 生效时间 ????

	class Meta:
		db_table = 'market_tool_channel_distribution_detail'


# class ChannelDistributionProcess(models.Model):
# 	"""
# 	取现进度记录
# 	"""
# 	channel_qrcode_id = models.IntegerField()  # 渠道分销id
# 	member_id = models.IntegerField()  # 对应的会员id
# 	status = models.IntegerField()  # 取现进度
# 	money = models.DecimalField(max_digits=65, decimal_places=2, default=2)  # 提取的金额
# 	created_at = models.DateTimeField(auto_now_add=True)  # 创建时间
#
# 	class Meta(object):
# 		db_table = 'market_tool_channel_distribution_process'


class ChannelDistributionFinish(models.Model):
	"""
	完成过的订单记录
	"""
	order_id = models.IntegerField()  # 所有处理过的订单
	order_time = models.DateTimeField()  # 所有订单对应的日期

	class Meta(object):
		db_table = 'market_tool_channel_distribution_finish'