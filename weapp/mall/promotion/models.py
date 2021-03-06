# -*- coding: utf-8 -*-

from datetime import datetime


from django.db import models
from django.contrib.auth.models import User

from mall.models import Product, ProductPool
from modules.member.models import Member

DEFAULT_DATETIME = datetime.strptime('2000-01-01', '%Y-%m-%d')

#########################################################################
# ProductHasPromotion: <商品，促销>的关联
#########################################################################
PROMOTION_TYPE_ALL = 0
PROMOTION_TYPE_FLASH_SALE = 1
PROMOTION_TYPE_PREMIUM_SALE = 2
PROMOTION_TYPE_PRICE_CUT = 3
PROMOTION_TYPE_COUPON = 4
PROMOTION_TYPE_INTEGRAL_SALE = 5
PROMOTION2TYPE = {
	PROMOTION_TYPE_FLASH_SALE: {
		"name": 'flash_sale',
		"display_name": u'限时抢购'
	},
	PROMOTION_TYPE_PREMIUM_SALE: {
		"name": 'premium_sale',
		"display_name": u'买&nbsp;赠'
	},
	PROMOTION_TYPE_PRICE_CUT: {
		"name": 'price_cut',
		"display_name": u'满&nbsp;减'
	},
	PROMOTION_TYPE_COUPON:  {
		"name": 'coupon',
		"display_name": u'优惠券'
	},
	PROMOTION_TYPE_INTEGRAL_SALE:  {
		"name": 'integral_sale',
		"display_name": u'积分抵扣'
	}
}
PROMOTIONSTR2TYPE = {
	'all': PROMOTION_TYPE_ALL,
	'flash_sale': PROMOTION_TYPE_FLASH_SALE,
	'premium_sale': PROMOTION_TYPE_PREMIUM_SALE,
	'price_cut': PROMOTION_TYPE_PRICE_CUT,
	'coupon': PROMOTION_TYPE_COUPON,
	'integral_sale': PROMOTION_TYPE_INTEGRAL_SALE
}
PROMOTION_STATUS_NOT_START = 1
PROMOTION_STATUS_STARTED = 2
PROMOTION_STATUS_FINISHED = 3
PROMOTION_STATUS_DELETED = 4
PROMOTION_STATUS_DISABLE = 5
PROMOTIONSTATUS2NAME = {
	PROMOTION_STATUS_NOT_START: u'未开始',
	PROMOTION_STATUS_STARTED: u'进行中',
	PROMOTION_STATUS_FINISHED: u'已结束',
	PROMOTION_STATUS_DELETED: u'已删除',
	PROMOTION_STATUS_DISABLE: u'已失效'
}


class Promotion(models.Model):
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=256) #活动名
	promotion_title = models.CharField(max_length=256) #促销标题
	status = models.IntegerField(default=PROMOTION_STATUS_NOT_START) #促销状态
	start_date = models.DateTimeField() #开始日期
	end_date = models.DateTimeField() #结束日期
	type = models.IntegerField() #促销类型
	detail_id = models.IntegerField(default=0) #促销数据id
	member_grade_id = models.IntegerField(default=0) #会员等级
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = 'mallpromotion_promotion'

	def __update_status_if_necessary(self):
		now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

		if type(self.end_date) == datetime:
			end_date = self.end_date.strftime('%Y-%m-%d %H:%M:%S')
		else:
			end_date = self.end_date

		if type(self.start_date) == datetime:
			start_date = self.start_date.strftime('%Y-%m-%d %H:%M:%S')
		else:
			start_date = self.start_date

		if start_date <= now and end_date > now and self.status == PROMOTION_STATUS_NOT_START:
			# 未开始状态,但是时间已经再开始,由于定时任务尚未执行
			self.status = PROMOTION_STATUS_STARTED
			self.save()
		elif end_date <= now and (self.status == PROMOTION_STATUS_NOT_START or\
			self.status == PROMOTION_STATUS_STARTED or self.status == PROMOTION_STATUS_DISABLE):
			# 未开始,进行中状态,但是时间到期了,由于定时任务尚未执行
			# 已失效状态,优惠券需求要置为已过期
			self.status = PROMOTION_STATUS_FINISHED
			self.save()

	@property
	def status_name(self):
		self.__update_status_if_necessary()
		return PROMOTIONSTATUS2NAME.get(self.status, u'未知')

	@property
	def type_name(self):
		return PROMOTION2TYPE.get(self.type, u'未知')['display_name']

	@property
	def DetailClass(self):
		if self.type == PROMOTION_TYPE_FLASH_SALE:
			return FlashSale
		elif self.type == PROMOTION_TYPE_PRICE_CUT:
			return PriceCut
		elif self.type == PROMOTION_TYPE_INTEGRAL_SALE:
			return IntegralSale
		elif self.type == PROMOTION_TYPE_PREMIUM_SALE:
			return PremiumSale
		elif self.type == PROMOTION_TYPE_COUPON:
			return CouponRule
		else:
			return None

	@property
	def is_active(self):
		if self.status == PROMOTION_STATUS_FINISHED or self.status == PROMOTION_STATUS_DELETED:
			return False

		self.__update_status_if_necessary()

		now = datetime.today()#.strftime('%Y-%m-%d %H:%M:%S')
		if self.start_date > now:
			return False
		if self.end_date < now:
			return False

		return True

	@staticmethod
	def fill_product_detail(webapp_owner, promotions):
		promotions = [promotion for promotion in promotions if not hasattr(promotion, 'products')]

		#获取product列表
		for promotion in promotions:
			promotion.products = []

		id2promotion = dict([(promotion.id, promotion) for promotion in promotions])
		promotion_ids = [promotion.id for promotion in promotions]
		product_ids = [relation.product_id for relation in ProductHasPromotion.objects.filter(promotion_id__in=promotion_ids)]
		if webapp_owner:
			product_pool_id2product_pool = dict([(pool.product_id, pool) for pool in ProductPool.objects.filter(woid=webapp_owner.id,product_id__in=product_ids)])
		else:
			product_pool_id2product_pool = {}
		products = list(Product.objects.filter(id__in=product_ids))
	

		if product_pool_id2product_pool:
			mall_type = 1
		else:
			mall_type = 0

		Product.fill_details(webapp_owner, products, {
			'with_product_model': True,
			"with_model_property_info": True,
			'with_sales': True,
			'mall_type': mall_type,
			'product_pool_id2product_pool': product_pool_id2product_pool
		})
		id2product = dict([(product.id, product) for product in products])

		#获取<promotion, product_ids>关系集合
		for relation in ProductHasPromotion.objects.filter(promotion_id__in=promotion_ids):
			promotion = id2promotion[relation.promotion_id]
			product = id2product[relation.product_id]
			if hasattr(promotion, 'products'):
				promotion.products.append(product)
			else:
				promotion.products = [product]

	@staticmethod
	def fill_concrete_info_detail(webapp_owner, promotions):
		promotions = [promotion for promotion in promotions if not hasattr(promotion, 'detail')]

		#按type对promotion进行分类
		type2promotions = {}
		for promotion in promotions:
			promotion.end_date = promotion.end_date if isinstance(promotion.end_date, str) else promotion.end_date.strftime('%Y-%m-%d %H:%M:%S')
			promotion.created_at = promotion.created_at if isinstance(promotion.created_at, str) else promotion.created_at.strftime('%Y-%m-%d %H:%M:%S')
			promotion.start_date = promotion.start_date if isinstance(promotion.start_date, str) else promotion.start_date.strftime('%Y-%m-%d %H:%M:%S')
			type2promotions.setdefault(promotion.type, []).append(promotion)

		#对每种类型的promotion，获取detail
		for promotion_type, promotions in type2promotions.items():
			detail2promotion = dict([(promotion.detail_id, promotion) for promotion in promotions])
			detail_ids = [promotion.detail_id for promotion in promotions]
			DetailClass = promotions[0].DetailClass
			details = list(DetailClass.objects.filter(id__in=detail_ids))
			if hasattr(DetailClass, 'fill_related_details'):
				DetailClass.fill_related_details(webapp_owner, details)
			for detail in details:
				if promotion_type == PROMOTION_TYPE_COUPON:
					# CouponRule字段use_count(优惠券使用张数)为负数没法复现，暂时改为直接查库的方式 by Eugene
					detail.use_count = Coupon.objects.filter(coupon_rule__id=detail.id, status=COUPON_STATUS_USED).count()
				detail2promotion[detail.id].detail = detail.to_dict()

	@staticmethod
	def fill_details(webapp_owner, promotions, options):
		if len(promotions) == 0:
			return

		if options.get('with_concrete_promotion', False):
			Promotion.fill_concrete_info_detail(webapp_owner, promotions)

		if options.get('with_product', False):
			Promotion.fill_product_detail(webapp_owner, promotions)


#########################################################################
# ProductHasPromotion: <商品，促销>的关联
#########################################################################
class ProductHasPromotion(models.Model):
	product = models.ForeignKey(Product)
	promotion = models.ForeignKey(Promotion)

	class Meta(object):
		db_table = 'mallpromotion_product_has_promotion'


#########################################################################
# FlashSale：限时抢购
#########################################################################
class FlashSale(models.Model):
	owner = models.ForeignKey(User)
	limit_period = models.IntegerField(default=0) #限购周期
	promotion_price = models.FloatField(default=0.0) #限购价格
	count_per_purchase = models.IntegerField(default=1) #单人限购数量每次
	count_per_period = models.IntegerField(default=0)

	class Meta(object):
		db_table = 'mallpromotion_flash_sale'
		verbose_name = '限时抢购'
		verbose_name_plural = '限时抢购'

	def to_dict(self):
		return {
			'id': self.id,
			'limit_period': self.limit_period,
			'promotion_price': self.promotion_price,
			'count_per_purchase': self.count_per_purchase,
			'count_per_period': self.count_per_period
		}


#########################################################################
# ProductModelFlashSaleInfo：与商品规格相关的限时抢购详情
#########################################################################
# class ProductModelFlashSaleDetail(models.Model):
# 	owner = models.ForeignKey(User)
# 	flash_sale = models.ForeignKey(FlashSale)
# 	product_model = models.ForeignKey(ProductModel)
# 	promotion_price = models.FloatField(default=0.0) #促销价格

# 	class Meta(object):
# 		db_table = 'mallpromotion_product_model_flash_sale_detail'
# 		verbose_name = '商品的限时抢购详情'
# 		verbose_name_plural = '商品的限时抢购详情'


#########################################################################
# PriceCut：满减
#########################################################################
class PriceCut(models.Model):
	owner = models.ForeignKey(User)
	price_threshold = models.FloatField(default=0) #价格阈值
	cut_money = models.FloatField(default=0) #减价
	is_enable_cycle_mode = models.BooleanField(default=False) #是否启用循环满减

	class Meta(object):
		db_table = 'mallpromotion_price_cut'
		verbose_name = '满减'
		verbose_name_plural = '满减'

	def to_dict(self):
		return {
			'id': self.id,
			'price_threshold': self.price_threshold,
			'cut_money': self.cut_money,
			'is_enable_cycle_mode': self.is_enable_cycle_mode
		}


#########################################################################
# IntegralSale：积分应用
#########################################################################
INTEGRAL_SALE_TYPE_PARTIAL = 0 #部分抵扣
INTEGRAL_SALE_TYPE_TOTAL = 1 #全额抵扣
class IntegralSale(models.Model):
	owner = models.ForeignKey(User)
	type = models.IntegerField(default=INTEGRAL_SALE_TYPE_PARTIAL) #积分抵扣类型
	discount = models.IntegerField(default=0) #折扣上限
	discount_money = models.FloatField(default=0.0) #折扣金额
	integral_price = models.FloatField(default=0.0) #积分价
	is_permanant_active = models.BooleanField(default=False) #是否永久有效

	class Meta(object):
		db_table = 'mallpromotion_integral_sale'
		verbose_name = '积分应用'
		verbose_name_plural = '积分应用'

	@staticmethod
	def fill_related_details(webapp_owner, integral_sales):
		integral_sale_ids = []
		id2sale = {}
		for integral_sale in integral_sales:
			integral_sale.rules = []
			integral_sale_ids.append(integral_sale.id)
			id2sale[integral_sale.id] = integral_sale

		integral_sale_rules = list(IntegralSaleRule.objects.filter(integral_sale_id__in=integral_sale_ids))
		for integral_sale_rule in integral_sale_rules:
			integral_sale_id = integral_sale_rule.integral_sale_id
			data = integral_sale_rule.to_dict()
			id2sale[integral_sale_id].rules.append(data)

	def to_dict(self):
		if len(self.rules) == 0:
			discount = 0
			discount_money = 0
		elif len(self.rules) == 1:
			discount = str(self.rules[0]['discount']) + '%'
			discount_money = "%.2f" % self.rules[0]['discount_money']
		else:
			max_discount = str(max(list(rule['discount'] for rule in self.rules)))
			min_discount = str(min(list(rule['discount'] for rule in self.rules)))
			max_discount_money = str("%.2f" % max(list(rule['discount_money'] for rule in self.rules)))
			min_discount_money = str("%.2f" % min(list(rule['discount_money'] for rule in self.rules)))
			if max_discount == min_discount:
				discount = max_discount
			else:
				discount = min_discount + '% ~ ' + max_discount + '%'

			if max_discount_money == min_discount_money:
				discount_money = max_discount_money
			else:
				discount_money = min_discount_money + ' ~ ' + max_discount_money

		return {
			'id': self.id,
			'type': self.type,
			'type_name': u'部分抵扣' if self.type == INTEGRAL_SALE_TYPE_PARTIAL else u'全额抵扣',
			'is_permanant_active': self.is_permanant_active,
			'rules': self.rules,
			'discount': discount,
			'discount_money': discount_money
		}


class IntegralSaleRule(models.Model):
	"""
	积分应用规则
	"""
	owner = models.ForeignKey(User)
	integral_sale = models.ForeignKey(IntegralSale)
	member_grade_id = models.IntegerField(default=0) #会员等级
	discount = models.FloatField(default=0) #折扣上限
	discount_money = models.FloatField(default=0.0) #折扣金额

	class Meta(object):
		db_table = 'mallpromotion_integral_sale_rule'
		verbose_name = '积分应用规则'
		verbose_name_plural = '积分应用规则'

	def to_dict(self):
		return {
			'id': self.id,
			'member_grade_id': self.member_grade_id,
			'discount': self.discount,
			'discount_money': self.discount_money
		}


#########################################################################
# PremiumSale：买赠
#########################################################################
class PremiumSale(models.Model):
	owner = models.ForeignKey(User)
	count = models.IntegerField(default=0) #购买基数
	is_enable_cycle_mode = models.BooleanField(default=False) #循环买赠

	class Meta(object):
		db_table = 'mallpromotion_premium_sale'
		verbose_name = '买赠'
		verbose_name_plural = '买赠'

	@staticmethod
	def fill_related_details(webapp_owner, premium_sales):
		premium_sale_ids = []
		id2sale = {}
		for premium_sale in premium_sales:
			premium_sale.premium_products = []
			premium_sale_ids.append(premium_sale.id)
			id2sale[premium_sale.id] = premium_sale

		premium_sale_products = list(PremiumSaleProduct.objects.filter(premium_sale_id__in=premium_sale_ids))
		product_ids = [premium_sale_product.product_id for premium_sale_product in premium_sale_products]
		products = Product.objects.filter(id__in=product_ids)
		Product.fill_details(webapp_owner, products, {
			'with_product_model': True,
			"with_model_property_info": True,
			'with_sales': True
		})
		id2product = dict([(product.id, product) for product in products])

		for premium_sale_product in premium_sale_products:
			premium_sale_id = premium_sale_product.premium_sale_id
			product_id = premium_sale_product.product_id
			product = id2product[product_id]
			data = product.format_to_dict()
			data['premium_count'] = premium_sale_product.count
			data['premium_unit'] = premium_sale_product.unit
			id2sale[premium_sale_id].premium_products.append(data)

	def to_dict(self):
		return {
			'id': self.id,
			'count': self.count,
			'is_enable_cycle_mode': self.is_enable_cycle_mode,
			'premium_products': self.premium_products
		}


#########################################################################
# PremiumSaleProduct：买赠的赠品
#########################################################################
class PremiumSaleProduct(models.Model):
	owner = models.ForeignKey(User)
	premium_sale = models.ForeignKey(PremiumSale)
	product = models.ForeignKey(Product)
	count = models.IntegerField(default=1, verbose_name='赠送数量')
	unit = models.CharField(max_length=50, verbose_name='赠品单位')

	class Meta(object):
		db_table = 'mallpromotion_premium_sale_product'
		verbose_name = '买赠赠品'
		verbose_name_plural = '买赠赠品'


FORBIDDEN_STATUS_NOT_START = 1
FORBIDDEN_STATUS_STARTED = 2
FORBIDDEN_STATUS_FINISHED = 3
FORBIDDENSTATUS2NAME = {
	FORBIDDEN_STATUS_NOT_START: u'未开始',
	FORBIDDEN_STATUS_STARTED: u'进行中',
	FORBIDDEN_STATUS_FINISHED: u'已结束'
}
class ForbiddenCouponProduct(models.Model):
	owner = models.ForeignKey(User)
	product = models.ForeignKey(Product)
	status = models.IntegerField(default=FORBIDDEN_STATUS_NOT_START) #促销状态
	start_date = models.DateTimeField() #开始日期
	end_date = models.DateTimeField() #结束日期
	is_permanant_active = models.BooleanField(default=False) #永久有效
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = 'mall_forbidden_coupon_product'
		verbose_name = '禁用通用优惠券的商品'
		verbose_name_plural = '禁用通用优惠券的商品'

	def __update_status_if_necessary(self):
		if self.is_permanant_active:
			if self.status != FORBIDDEN_STATUS_STARTED:
				self.status = FORBIDDEN_STATUS_STARTED
				self.save()
			return
		now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

		if type(self.end_date) == datetime:
			end_date = self.end_date.strftime('%Y-%m-%d %H:%M:%S')
		else:
			end_date = self.end_date

		if type(self.start_date) == datetime:
			start_date = self.start_date.strftime('%Y-%m-%d %H:%M:%S')
		else:
			start_date = self.start_date

		if start_date <= now and end_date > now and self.status == FORBIDDEN_STATUS_NOT_START:
			# 未开始状态,但是时间已经再开始,由于定时任务尚未执行
			self.status = FORBIDDEN_STATUS_STARTED
			self.save()
		elif end_date <= now and (self.status == FORBIDDEN_STATUS_NOT_START or self.status == FORBIDDEN_STATUS_STARTED):
			# 未开始,进行中状态,但是时间到期了,由于定时任务尚未执行
			self.status = FORBIDDEN_STATUS_FINISHED
			self.save()

	@property
	def status_name(self):
		self.__update_status_if_necessary()
		return FORBIDDENSTATUS2NAME.get(self.status, u'未知')

	@property
	def is_active(self):
		if self.is_permanant_active and self.status != FORBIDDEN_STATUS_FINISHED:
			return True

		if self.status == FORBIDDEN_STATUS_FINISHED:
			return False

		self.__update_status_if_necessary()

		if self.status == FORBIDDEN_STATUS_NOT_START or self.status == FORBIDDEN_STATUS_FINISHED:
			return False

		return True

	@property
	def is_overdue(self):
		if self.status == FORBIDDEN_STATUS_FINISHED:
			return True

		if self.is_permanant_active:
			return False

		self.__update_status_if_necessary()

		if self.status == FORBIDDEN_STATUS_FINISHED:
			return True

		return False

	def to_dict(self):
		Product.fill_details(self.owner, [self.product], {
			'with_product_model': True,
			"with_model_property_info": True,
			'with_sales': True
		})
		return {
			'id': self.id,
			'product': self.product.format_to_dict(),
			'status': self.status,
			'status_name': self.status_name,
			'start_date': self.start_date.strftime('%Y-%m-%d %H:%M:%S'),
			'end_date': self.end_date.strftime('%Y-%m-%d %H:%M:%S'),
			'is_permanant_active': self.is_permanant_active,
			'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
		}

	# 用于存入缓存的dict zhutianqi
	def to_cache_dict(self):
		Product.fill_details(self.owner, [self.product], {
			'with_product_model': True,
			"with_model_property_info": True,
			'with_sales': True
		})
		return {
			'id': self.id,
			'owner_id': self.owner_id,
			'product_id': self.product_id,
			'status': self.status,
			'status_name': self.status_name,
			'start_date': self.start_date.strftime('%Y-%m-%d %H:%M:%S'),
			'end_date': self.end_date.strftime('%Y-%m-%d %H:%M:%S'),
			'is_permanant_active': self.is_permanant_active,
			'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
		}


class CouponRule(models.Model):
	"""
	优惠券规则
	"""
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=20, db_index=True) #名称
	valid_days = models.IntegerField(default=0) #过期天数
	is_active = models.BooleanField(default=True) #是否可用
	created_at = models.DateTimeField(auto_now_add=True) #添加时间
	start_date = models.DateTimeField() #有效期开始时间
	end_date = models.DateTimeField() #有效期结束时间
	# v2
	valid_restrictions = models.IntegerField(default=-1) #订单满多少可以使用规则
	money = models.DecimalField(max_digits=65, decimal_places=2) #金额
	count = models.IntegerField(default=0) #发放总数量
	remained_count = models.IntegerField(default=0) #剩余数量
	limit_counts = models.IntegerField(default=0) #每人限领
	limit_product = models.BooleanField(default=False) #限制指定商品
	limit_product_id = models.CharField(max_length=2048,default=0) #限制指定商品ID
	remark = models.TextField(default='') #使用说明
	note = models.TextField(default='') #优惠券备注
	get_person_count = models.IntegerField(default=0) #领取人数
	get_count = models.IntegerField(default=0) #领取次数
	use_count = models.IntegerField(default=0) #使用次数
	receive_rule = models.BooleanField(default=False) #领取规则，仅未下单用户可领取

	class Meta(object):
		db_table = 'market_tool_coupon_rule'
		verbose_name = '优惠券规则'
		verbose_name_plural = '优惠券规则'

	# @staticmethod
	# def award_coupon_for_member(coupon_rule_info, member):
	# 	from market_tools.tools.coupon.util import create_coupons
	# 	rule = CouponRule.objects.get(id=coupon_rule_info.id)
	# 	coupons = create_coupons(rule.owner, rule.id, 1, member.id)

	@staticmethod
	def get_all_coupon_rules_list(user):
		if user is None:
			return []

		return list(CouponRule.objects.filter(owner=user, is_active=True, end_date__gt=datetime.now()).order_by('-id'))

	def to_dict(self):
		return {
			'id': self.id,
			'name': self.name,
			'note': self.note,
			'owner_id': self.owner_id,
			'count': self.count,
			'remained_count': self.remained_count,
			'limit_counts': self.limit_counts,
			'limit_product': self.limit_product,
			'money': '%.2f' % self.money,
			'get_person_count': self.get_person_count,
			'get_count': self.get_count,
			'use_count': self.use_count,
		}


#优惠券状态
COUPON_STATUS_UNUSED = 0 #已领取
COUPON_STATUS_USED = 1 #已被使用
COUPON_STATUS_EXPIRED = 2 #已过期
COUPON_STATUS_DISCARD = 3 #作废 手机端用户不显示
COUPON_STATUS_UNGOT = 4 #未领取
COUPON_STATUS_Expired = 5 #已失效
COUPONSTATUS = {
	COUPON_STATUS_UNUSED: {
		"name": u'未使用'
	},
	COUPON_STATUS_USED: {
		"name": u'已使用'
	},
	COUPON_STATUS_EXPIRED: {
		"name": u'已过期'
	},
	COUPON_STATUS_DISCARD: {
		"name": u'作废'
	},
	COUPON_STATUS_UNGOT: {
		"name": u'未领取'
	},
	COUPON_STATUS_Expired: {
		"name": u'已失效'
	}
}
class Coupon(models.Model):
	"""
	优惠券
	"""
	owner = models.ForeignKey(User)
	coupon_rule = models.ForeignKey(CouponRule) #coupon rule
	member_id = models.IntegerField(default=0) #优惠券分配的member的id
	coupon_record_id = models.IntegerField(default=0) #优惠券记录的id
	status = models.IntegerField(default=COUPON_STATUS_UNUSED) #优惠券状态
	coupon_id = models.CharField(max_length=50) #优惠券号
	provided_time = models.DateTimeField(default=DEFAULT_DATETIME) #领取时间
	start_time = models.DateTimeField() #优惠券有效期开始时间
	expired_time = models.DateTimeField() #过期时间
	money = models.DecimalField(max_digits=65, decimal_places=2) #金额
	is_manual_generated = models.BooleanField(default=False) #是否手工生成
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = 'market_tool_coupon'
		verbose_name = '优惠券'
		verbose_name_plural = '优惠券'
		unique_together = ('coupon_id',)


class CouponRecord(models.Model):
	"""
	发优惠券记录
	"""
	owner = models.ForeignKey(User)
	coupon_rule_id = models.IntegerField(default=0) # 所发优惠券规则的ID
	pre_person_count = models.IntegerField(default=1) #每人几张
	person_count = models.IntegerField(default=0) #发放的人数
	coupon_count = models.IntegerField(default=0) #发放的张数
	send_time = models.DateTimeField(auto_now_add=True) #发放时间
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = 'mall_issuing_coupon_record'
		verbose_name = '发优惠券记录'
		verbose_name_plural = '发优惠券记录'


class RedEnvelopeRule(models.Model):
	"""
	红包规则
	"""
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=128)
	coupon_rule_id = models.IntegerField(default=0)
	limit_time = models.BooleanField(default=False)
	start_time = models.DateTimeField(default=DEFAULT_DATETIME)
	end_time = models.DateTimeField(default=DEFAULT_DATETIME)
	limit_order_money = models.DecimalField(max_digits=65, decimal_places=2, default=0.0)
	use_info = models.TextField()
	share_title = models.CharField(max_length=256)
	share_pic = models.CharField(max_length=256)
	is_delete = models.BooleanField(default=False)
	status = models.BooleanField(default=False) #状态默认关闭
	receive_method = models.BooleanField(default=False) #领取方式默认为下单领取
	order_index = models.IntegerField(default=0) #记录排序，置后为-1
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'mall_red_envelope_rule'
		verbose_name = '红包规则记录'
		verbose_name_plural = '红包规则记录'

	@staticmethod
	def can_show_red_envelope(order, red_envelope):
		"""判断订单是否能显示分享红包
		@params order: 需要判断的订单，需要使用订单商品价格，订单运费等价格信息
		@params red_envelope: 红包规则，注意是从request.webapp_owner_info缓存中获取
			由缓存抓取时判断红包状态、优惠券库存问题

		@return
			True: 订单可以显示分享红包按钮
			False: 订单不可以显示分享红包按钮
		### 注: 此方法不需要查询数据库
		"""
		from mall import models as mall_models
		if order.status <= mall_models.ORDER_STATUS_CANCEL or order.status >= mall_models.ORDER_STATUS_REFUNDING:
			return False

		now = datetime.now()
		if red_envelope and (red_envelope['limit_time'] or red_envelope['end_time'] > now):
			# 缓存里有分享红包规则，并且红包规则未到期，注：红包规则状态在缓存抓取时判断
			if red_envelope['limit_time'] and red_envelope['created_at'] > order.created_at or \
				not red_envelope['limit_time'] and red_envelope['start_time'] > order.created_at:
				return False
			coupon_rule = red_envelope['coupon_rule']
			if coupon_rule and coupon_rule.get('end_date', now) > now:
				# 红包规则对应的优惠券未到期，注：优惠券库存在缓存抓取时判断
				if order.product_price + order.postage >= red_envelope['limit_order_money']:
					# 商品价格+运费应大于等于红包规则订单金额设置
					return True
		return False

class RedEnvelopeToOrder(models.Model):
	"""
	红包关联订单记录表
	"""
	owner = models.ForeignKey(User)
	member_id = models.IntegerField(default=0)
	order_id = models.IntegerField(default=0) #订单领取记录订单id
	material_id = models.IntegerField(default=0) #图文领取记录图文id
	red_envelope_rule_id = models.IntegerField(default=0)
	count = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'mall_red_envelope_to_order'
		verbose_name = '红包关联订单记录'
		verbose_name_plural = '红包关联订单记录'

	def __getitem__(self, name):
		return getattr(self, name, None)

class GetRedEnvelopeRecord(models.Model):
	"""
	红包领用记录
	"""
	owner = models.ForeignKey(User)
	coupon_id = models.CharField(max_length=50)
	red_envelope_rule_id = models.IntegerField(default=0)
	red_envelope_relation_id = models.IntegerField(default=0)
	member = models.ForeignKey(Member)
	#member_name = models.CharField(max_length=128, null=True)
	#member_header_img = models.CharField(max_length=256, null=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'mall_red_envelope_record'
		verbose_name = '红包领用记录'
		verbose_name_plural = '红包领用记录'

class RedEnvelopeParticipences(models.Model):
	"""
	红包领用记录
	"""
	owner = models.ForeignKey(User)
	coupon = models.ForeignKey(Coupon)
	red_envelope_rule_id = models.IntegerField(default=0)
	red_envelope_relation_id = models.IntegerField(default=0)
	member = models.ForeignKey(Member)
	is_new = models.BooleanField(default=False)
	introduced_by = models.IntegerField(default=0)  #由谁引入
	introduce_new_member = models.IntegerField(default=0) #引入新关注
	introduce_used_number = models.IntegerField(default=0) #引入使用人数
	introduce_received_number = models.IntegerField(default=0) #引入领取人数
	introduce_sales_number = models.FloatField(default=0.0) #引入消费额
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'mall_red_envelope_participences'
		verbose_name = '红包领用分析'
		verbose_name_plural = '红包领用分析'

#########################################################################
# CardExchange: 商家设置的卡兑换
#########################################################################

NO_REQUIRE = 0          #无条件
TELEPHONE_REQUIRE = 1    #绑定手机号
EXCHANGE_REQUIRE = {
	NO_REQUIRE: u'无条件',
	TELEPHONE_REQUIRE: u'绑定手机号'
}

WEIZOOM_CARD = 0     #微众卡
EXCHANGE_REWARD = {
	WEIZOOM_CARD: u'微众卡'
}

class CardExchange(models.Model):
	webapp_id = models.CharField(max_length=20)  # webapp,商家id
	require = models.IntegerField(default=NO_REQUIRE)   #兑换需求
	reward_type = models.IntegerField(default=WEIZOOM_CARD)   #兑换奖励类型

	class Meta(object):
		db_table = 'mallpromotion_card_exchange'

#########################################################################
# WeizoomCardExchangeRule: 商家设置的卡兑换规则
#########################################################################
class CardExchangeRule(models.Model):
	exchange = models.ForeignKey(CardExchange)
	integral = models.IntegerField(default=0)  # 积分
	money = models.FloatField(default=0.0)  # 积分对应兑换金额
	card_number = models.CharField(max_length=256)  #微众卡号段

	class Meta(object):
		db_table = 'mallpromotion_card_exchange_rule'

#########################################################################
# CardHasExchanged: 卡兑换记录
#########################################################################
CARD_SOURCE_INTEGRAL = 0	#积分兑换
CARD_SOURCE_REBATE = 1	#返利活动
class CardHasExchanged(models.Model):
	webapp_id = models.CharField(max_length = 20)  # webapp,商家id
	card_id = models.CharField(max_length=100)    #微众卡id
	owner_id = models.IntegerField()    #卡拥有者
	owner_name = models.CharField(max_length = 256) #拥有者姓名
	created_at = models.DateTimeField(auto_now_add=True)  #兑换时间
	source = models.IntegerField(default=CARD_SOURCE_INTEGRAL) #微众卡来源（积分兑换 & 返利活动）
	rebate_id = models.CharField(max_length=50,default='') #返利活动ID,默认为空

	class Meta(object):
		db_table = 'mallpromotion_card_has_exchanged'


WEIZOOM_CARD_SOURCE_WEAPP = 0	#目前没用到
WEIZOOM_CARD_SOURCE_REBATE = 1	#返利活动
WEIZOOM_CARD_SOURCE_VIRTUAL = 2  #福利卡券
WEIZOOM_CARD_SOURCE_BIND = 3 # 绑定卡
class MemberHasWeizoomCard(models.Model):
	"""
	给会员发放的微众卡
	"""
	member_id = models.IntegerField() #会员id
	member_name = models.CharField(max_length=1024) #会员名称
	card_number = models.CharField(max_length=50) #微众卡卡号
	card_password = models.CharField(max_length=512) #微众卡密码
	relation_id = models.CharField(max_length=128) #关联的活动id
	source = models.IntegerField() #微众卡来源

	created_at = models.DateTimeField(auto_now_add=True) #发放时间

	class Meta(object):
		db_table = 'member_has_weizoom_card'


class VirtualProduct(models.Model):
	"""
	福利卡券活动
	"""
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=128) #活动名称
	product = models.ForeignKey(Product)  #活动关联的商品
	is_finished = models.BooleanField(default=False)  #活动是否结束
	created_at = models.DateTimeField(auto_now_add=True)  #创建时间

	class Meta(object):
		db_table = 'mallpromotion_virtual_product'


CODE_STATUS_NOT_GET = 0 #未领取
CODE_STATUS_GET = 1 #已领取
CODE_STATUS_OVERDUE = 2 #已过期
CODE_STATUS_EXPIRED = 3 #已失效
CODE2TEXT = {
	CODE_STATUS_NOT_GET: u'未领取',
	CODE_STATUS_GET: u'已领取',  #已领取的就不判断是否过期，即使过期了数据库里依然是已领取状态，但是用户卡包里显示已过期
	CODE_STATUS_OVERDUE: u'已过期',  #已过期的一定是没有被领取过的
	CODE_STATUS_EXPIRED: u'已失效'
}
class VirtualProductHasCode(models.Model):
	"""
	福利卡券活动关联的卡券码
	"""
	owner = models.ForeignKey(User)
	virtual_product = models.ForeignKey(VirtualProduct)
	code = models.CharField(max_length=128) #卡号
	password = models.CharField(max_length=512) #密码
	start_time = models.DateTimeField() #有效期起始时间
	end_time = models.DateTimeField()#有效期结束时间
	status = models.IntegerField(default=CODE_STATUS_NOT_GET) #状态
	get_time = models.DateTimeField(null=True) #领取/发放时间
	member_id = models.CharField(max_length=20, default='') #会员id
	oid = models.CharField(max_length=20, default='') #订单id
	order_id = models.CharField(max_length=35, default='') #订单order_id
	created_at = models.DateTimeField(auto_now_add=True)  #创建时间

	class Meta(object):
		db_table = 'mallpromotion_virtual_product_has_code'

	def __update_status_if_necessary(self):
		now = datetime.now()
		if self.status == CODE_STATUS_NOT_GET and self.end_time <= now:
			# 未领取的卡券如果过期了则更新状态
			self.status = CODE_STATUS_OVERDUE
			self.save()

	@property
	def can_not_use(self):
		self.__update_status_if_necessary()
		if self.status in [CODE_STATUS_OVERDUE, CODE_STATUS_EXPIRED]:
			return True
		else:
			return False