# # -*- coding: utf-8 -*-
# import random
# from datetime import timedelta, datetime, date
# from hashlib import md5

# from django.db import models
# from django.contrib.auth.models import Group, User
# from django.db.models import signals
# from django.conf import settings
# from django.db.models import F

# from core import dateutil


# #########################################################################
# # CouponRule ：优惠券规则
# #########################################################################
# #优惠券发放目标
# class CouponRule(models.Model):
# 	owner = models.ForeignKey(User, related_name='owned_coupon_rules')
# 	name = models.CharField(max_length=20, db_index=True) #名称
# 	valid_days = models.IntegerField(default=0) #过期天数
# 	money = models.DecimalField(max_digits=65, decimal_places=2) #金额
# 	count = models.IntegerField(default=0) #发放总数量
# 	remained_count = models.IntegerField(default=0) #剩余数量
# 	is_active = models.BooleanField(default=True) #是否可用
# 	valid_restrictions = models.IntegerField(default=-1) #订单满多少可以使用规则
# 	# created_at = models.DateTimeField(auto_now_add=True) #添加时间
# 	limit_counts = models.IntegerField(default=0) #每人限领
# 	limit_product = models.BooleanField(default=False) #限制指定商品
# 	remark = models.TextField(default='') #备注

# 	# @staticmethod
# 	# def award_coupon_for_member(coupon_rule_info, member):
# 	# 	rule = CouponRule.objects.get(id=coupon_rule_info.id)
# 	# 	coupons = create_coupons(rule.owner, rule.id, 1, member)

# 	@staticmethod
# 	def get_all_coupon_rules_list(user):
# 		if user is None:
# 			return []

# 		return list(CouponRule.objects.filter(owner=user, is_active=True))

# 	class Meta(object):
# 		db_table = 'market_tool_coupon_rule_old'
# 		verbose_name = '优惠券规则'
# 		verbose_name_plural = '优惠券规则'


# #########################################################################
# # Coupon ：优惠券
# #########################################################################
# #优惠券状态
# COUPON_STATUS_UNUSED = 0 #未使用
# COUPON_STATUS_USED = 1 #已被使用
# COUPON_STATUS_EXPIRED = 2 #已过期
# COUPON_STATUS_DISCARD = 3 #作废 手机端用户不显示
# COUPON_STATUS_UNGOT = 4 #未领取

# class Coupon(models.Model):
# 	owner = models.ForeignKey(User, related_name='mall_coupon')
# 	coupon_rule = models.ForeignKey(CouponRule) #coupon rule
# 	member_id = models.IntegerField(default=0) #优惠券分配的member的id
# 	status = models.IntegerField(default=COUPON_STATUS_UNUSED) #优惠券状态
# 	coupon_id = models.CharField(max_length=50) #优惠券号
# 	provided_time = models.DateTimeField() #发放时间
# 	expired_time = models.DateTimeField() #过期时间
# 	money = models.DecimalField(max_digits=65, decimal_places=2) #金额
# 	is_manual_generated = models.BooleanField(default=False) #是否手工生成
# 	created_at = models.DateTimeField(auto_now_add=True) #添加时间

# 	class Meta(object):
# 		db_table = 'market_tool_coupon_old'
# 		verbose_name = '优惠券'
# 		verbose_name_plural = '优惠券'
# 		unique_together = ('coupon_id',)


# #########################################################################
# # CouponConfig ：优惠券配置
# #########################################################################
# #使用类型
# COUPON_USE_TYPE_NOLIMIT = 0 #无限
# COUPON_USE_TYPE_DEPEND_ON_PRICE = 1 #依赖于coupon_price_boundary指定的金额
# #超额类型
# COUPON_OVERFLOW_TYPE_DROP = 0 #超额部分作废
# COUPON_OVERFLOW_TYPE_CHANGE_TO_SCORE = 1 #超额部分折换成积分返回给用户

# class CouponConfig(models.Model):
# 	owner = models.ForeignKey(User, related_name='mall_coupon_settings')
# 	use_type = models.IntegerField(default=COUPON_USE_TYPE_NOLIMIT) #优惠券使用类型
# 	activate_price = models.FloatField(default=0.0) #优惠券激活金额
# 	overflow_type = models.IntegerField(default=COUPON_OVERFLOW_TYPE_DROP) #优惠券超额策略
# 	created_at = models.DateTimeField(auto_now_add=True) #添加时间

# 	class Meta(object):
# 		db_table = 'market_tool_coupon_config'
# 		verbose_name = '优惠券策略'
# 		verbose_name_plural = '优惠券策略'
		

# def create_coupons(owner, rule_id, count, member):
# 	coupon_rule = CouponRule.objects.get(id=rule_id)

# 	today = datetime.today()
# 	expired_time = today + timedelta(coupon_rule.valid_days)

# 	#创建coupon
# 	coupons = []
# 	i = 1
# 	if count > 0:
# 		random_args_value = ['1','2','3','4','5','6','7','8','9','0']
# 		while True:
# 			coupon_id = '%03d%04d%s' % (owner.id, coupon_rule.id, ''.join(random.sample(random_args_value, 6)))
# 			try:
# 				new_coupon = Coupon.objects.create(
# 					owner = owner,
# 					member_id = member.id,
# 					coupon_id = coupon_id,
# 					provided_time = today,
# 					expired_time = expired_time,
# 					money = coupon_rule.money,
# 					coupon_rule_id = coupon_rule.id,
# 					is_manual_generated = False
# 				)
# 				coupons.append(new_coupon)
# 				if i >= count:
# 					break
# 				i += 1
# 			except:
# 				continue
# 	return coupons

# #########################################################################
# # CouponSallerDate ：优惠券排行榜时间
# #########################################################################
# #优惠券发放目标
# class CouponSallerDate(models.Model):
# 	owner = models.ForeignKey(User)
# 	start_date = models.DateTimeField() #开始时间
# 	end_date = models.DateTimeField() #结束时间
# 	created_at = models.DateTimeField(auto_now_add=True) #添加时间

# 	class Meta(object):
# 		db_table = 'market_tool_coupon_saller_date'
# 		verbose_name = '优惠券排行榜时间'
# 		verbose_name_plural = '优惠券排行榜时间'

# ########################################################################
# # _create_random_coupon_ids: 生成count个随机的优惠券id
# ########################################################################
# def _create_random_coupon_ids(owner_id, coupon_pool_id, count):
# 	random_args_value = ['1','2','3','4','5','6','7','8','9','0']
# 	ids = set()

# 	while True:
# 		id = '%03d%04d%s' % (owner_id, coupon_pool_id, ''.join(random.sample(random_args_value, 6)))

# 		ids.add(id)
# 		if len(ids) >= count:
# 			return ids


# ########################################################################
# # restore_coupon: 改变优惠券使用状态为未使用
# ########################################################################
# def restore_coupon(coupon_id):
# 	Coupon.objects.filter(id=coupon_id).update(status=0)
