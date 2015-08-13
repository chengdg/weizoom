# -*- coding: utf-8 -*-
#
# __author__ = 'jiangzhe'
import random
from datetime import timedelta, datetime
from django.db import IntegrityError
from django.db.models import F

from mall.promotion import models as promotion_models
from mall.promotion.models import Coupon
from mall.promotion.utils import coupon_id_maker


def get_coupon_rules(owner):
	"""
	获取优惠券列表
	多个营销工具使用
	"""
	rules = list(promotion_models.CouponRule.objects.filter(owner=owner, is_active=True, end_date__gt=datetime.now()).order_by('-id'))

	return rules


def get_my_coupons(member_id):
	"""
	获取我所有的优惠券
	过滤掉 已经作废的优惠券
	"""
	#过滤已经作废的优惠券
	coupons = promotion_models.Coupon.objects.filter(member_id=member_id, status__lt=promotion_models.COUPON_STATUS_DISCARD).order_by('-id')
	coupon_rule_ids = [c.coupon_rule_id for c in coupons]
	coupon_rules = promotion_models.CouponRule.objects.filter(id__in=coupon_rule_ids)
	id2coupon_rule = dict([(c.id, c) for c in coupon_rules])
	# coupon_ids = []
	today = datetime.today()
	coupon_ids_need_expire = []
	for coupon in coupons:
		#添加优惠券使用限制
		coupon.valid_restrictions = id2coupon_rule[coupon.coupon_rule_id].valid_restrictions
		coupon.limit_product_id = id2coupon_rule[coupon.coupon_rule_id].limit_product_id
		coupon.name = id2coupon_rule[coupon.coupon_rule_id].name
		coupon.start_date = id2coupon_rule[coupon.coupon_rule_id].start_date
		# 优惠券倒计时
		if coupon.expired_time > today:
			valid_days = (coupon.expired_time - today).days
			if valid_days > 0:
				coupon.valid_time = '%d天' % valid_days
			else:
				#过期时间精确到分钟
				valid_seconds = (coupon.expired_time - today).seconds
				if valid_seconds > 3600:
					coupon.valid_time = '%d小时' % int(valid_seconds / 3600)
				else:
					coupon.valid_time = '%d分钟' % int(valid_seconds / 60)
			coupon.valid_days = valid_days
		else:
			# 记录过期并且是未使用的优惠券id
			if coupon.status == promotion_models.COUPON_STATUS_UNUSED:
				coupon_ids_need_expire.append(coupon.id)
				coupon.status = promotion_models.COUPON_STATUS_EXPIRED

	if len(coupon_ids_need_expire) > 0:
		promotion_models.Coupon.objects.filter(id__in=coupon_ids_need_expire).update(status=promotion_models.COUPON_STATUS_EXPIRED)

	return coupons


def get_can_use_coupon_count(member_id):
	"""
	可用优惠券数量
	个人中心调用
	"""
	return promotion_models.Coupon.objects.filter(member_id=member_id, status=promotion_models.COUPON_STATUS_UNUSED).count()


def consume_coupon(owner_id, rule_id, member_id, coupon_record_id=0):
	"""
	领用优惠券
	"""
	rules = promotion_models.CouponRule.objects.filter(id=rule_id, owner_id=owner_id)
	if len(rules) != 1:
		return None, u'该优惠券使用期已过，不能领取！'
	coupon_count = promotion_models.Coupon.objects.filter(coupon_rule_id=rule_id, member_id=member_id).count()
	if coupon_count >= rules[0].limit_counts and rules[0].limit_counts > 0:
		return None, u'该优惠券每人限领%s张，你已经领取过了！' % rules[0].limit_counts
	coupons = promotion_models.Coupon.objects.filter(coupon_rule_id=rule_id, member_id=0, status=promotion_models.COUPON_STATUS_UNGOT)[:1]
	if len(coupons) == 1:
		promotion_models.Coupon.objects.filter(id=coupons[0].id).update(
				status=promotion_models.COUPON_STATUS_UNUSED,
				member_id=member_id,
				provided_time=datetime.today(),
				coupon_record_id=coupon_record_id
			)
		if coupon_count:
			rules.update(remained_count=F('remained_count')-1, get_count=F('get_count')+1)
		else:
			rules.update(remained_count=F('remained_count')-1, get_person_count=F('get_person_count')+1, get_count=F('get_count')+1)
		return coupons[0], ''
	else:
		return None, u'该优惠券使用期已过，不能领取！'



def create_coupons(owner, rule_id, count, member_id=0, coupon_record_id=0):
	"""
	生成指定张数优惠券
	TODO: 淘汰调用此方法
	"""
	coupon_rule = promotion_models.CouponRule.objects.get(id=rule_id)

	today = datetime.today()
	expired_time = today + timedelta(coupon_rule.valid_days)

	coupon_count = 0
	if member_id > 0:
		coupon_count = promotion_models.Coupon.objects.filter(coupon_rule_id=rule_id, member_id=member_id).count()
		if coupon_count == 0:
			coupon_count = 1
		else:
			coupon_count = 0
	promotion = promotion_models.Promotion.objects.filter(type=promotion_models.PROMOTION_TYPE_COUPON, detail_id=coupon_rule.id)[0]

	#创建coupon
	a = owner.id
	b = coupon_rule.id

	coupons = []
	i = 1
	if count > 0:
		while True:
		 	# 生成优惠券ID
			coupon_id = coupon_id_maker(a, b)
			while Coupon.objects.filter(coupon_id=coupon_id):
				coupon_id = coupon_id_maker(a, b)
			new_coupon = promotion_models.Coupon.objects.create(
				owner = owner,
				member_id = member_id,
				coupon_id = coupon_id,
				provided_time = today,
				start_time = promotion.start_date or coupon_rule.start_date,
				expired_time = promotion.end_date,
				money = coupon_rule.money,
				coupon_rule_id = coupon_rule.id,
				is_manual_generated = False,
				status = promotion_models.COUPON_STATUS_UNUSED,
				coupon_record_id=coupon_record_id
			)
			coupons.append(new_coupon)
			if i >= count:
				break
			i += 1

	promotion_models.CouponRule.objects.filter(id=rule_id).update(
			count=(coupon_rule.count+count),
			get_count=(coupon_rule.get_count+count),
			get_person_count=(coupon_rule.get_person_count+coupon_count)
		)
	return coupons


def has_can_use_by_coupon_id(coupon_id, owner_id, product_prices, product_ids, member_id):
	"""
	优惠券是否可用
	"""
	if coupon_id is None or coupon_id < 0:
		return '请输入正确的优惠券号', None

	coupon = promotion_models.Coupon.objects.filter(coupon_id=coupon_id,owner_id=owner_id)
	if len(coupon) > 0:
		coupon = coupon[0]
		today = datetime.today()
		if coupon.expired_time < today:
			return '该优惠券已过期', None
		if coupon.status != promotion_models.COUPON_STATUS_UNUSED and coupon.status != promotion_models.COUPON_STATUS_UNGOT:
			return '该优惠券已使用', None
		if coupon.member_id > 0 and coupon.member_id != member_id:
			return '该优惠券已被他人领取不能使用', None
		coupon_rule = promotion_models.CouponRule.objects.get(id=coupon.coupon_rule_id)
		order_price = sum(product_prices)
		if coupon_rule.start_date > today:
			return'该优惠券活动尚未开始', None
		if coupon_rule.valid_restrictions > order_price and coupon_rule.valid_restrictions != -1:
			return '该优惠券不满足使用金额限制', None
		if coupon_rule.limit_product:
			promotion = promotion_models.Promotion.objects.get(detail_id=coupon_rule.id, type=promotion_models.PROMOTION_TYPE_COUPON)
			cant_use_coupon = True
			for relation in promotion_models.ProductHasPromotion.objects.filter(promotion_id=promotion.id):
				if str(relation.product_id) in product_ids:
					# 单品券商品在订单列表中
					price = 0
					for i in range(len(product_ids)):
						if product_ids[i] == str(relation.product_id):
							price += product_prices[i]
					if coupon_rule.valid_restrictions > 0:
						# 单品券限制购物金额
						if coupon_rule.valid_restrictions > price:
							return '该优惠券指定商品金额不满足使用条件', None
					# 单品券只抵扣单品金额
					if price < coupon.money:
						coupon.money = round(price, 2)
					cant_use_coupon = False
			if cant_use_coupon:
				return '该优惠券不能购买订单中的商品', None
		coupon.money = float(coupon.money)
		return '', coupon
	else:
		return '请输入正确的优惠券号', None


def restore_coupon(coupon_id):
	"""
	改变优惠券使用状态为未使用
	"""
	promotion_models.Coupon.objects.filter(id=coupon_id).update(status=promotion_models.COUPON_STATUS_UNUSED)


def award_coupon_for_member(coupon_rule_info, member):
	"""
	给会员发奖
	"""
	rule = promotion_models.CouponRule.objects.get(id=coupon_rule_info.id)
	coupons = consume_coupon(rule.owner, rule.id, member.id)
