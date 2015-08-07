# -*- coding: utf-8 -*-
# __author__ = 'chuter'
import re

from datetime import datetime


from django.conf import settings
from django.db import models
from django.db.models import signals, Sum
from django.utils.functional import cached_property

from account.models import UserProfile
from account.social_account.models import SocialAccount
from weixin.user.models import WeixinUser

from watchdog.utils import watchdog_fatal, watchdog_error
from market_tools.tools.coupon import models as coupon_model

from core.emojicons_util import encode_emojicons_for_html
from core.exceptionutil import unicode_full_stack

from utils.string_util import hex_to_byte, byte_to_hex

import member_settings

PRODUCT_DEFAULT_TYPE = 'object'
PRODUCT_DELIVERY_PLAN_TYPE = 'delivery'
PRODUCT_INTEGRAL_TYPE = 'integral'
#===============================================================================
# WebAppUser: WebApp的用户
#===============================================================================
class WebAppUser(models.Model):
	token = models.CharField(max_length=100, db_index=True)
	webapp_id = models.CharField(max_length=16, db_index=True)
	member_id = models.IntegerField(default=0, db_index=True) #会员记录的id
	has_purchased = models.BooleanField(default=False) #是否购买过
	father_id = models.IntegerField(default=0) #会员记录的id
	created_at = models.DateTimeField(auto_now_add=True) #创建时间

	class Meta(object):
		db_table = 'member_webapp_user'
		verbose_name = 'WebApp用户'
		verbose_name_plural = 'WebApp用户'

	@staticmethod
	def get_member_by_webapp_user_id(id):
		try:
			webapp_user = WebAppUser.objects.get(id=id)
			if webapp_user.member_id != 0 and webapp_user.member_id != -1:
				return Member.objects.get(id=webapp_user.member_id)
			elif father_id != 0:
				webapp_user = WebAppUser.objects.get(id=webapp_user.id)
				if webapp_user.member_id != 0 and webapp_user.member_id != -1:
					return Member.objects.get(id=webapp_user.member_id)
				else:
					return None
			else:
				return None
		except:
			return None

	#############################################################################
	# ship_info: 获取收货地址
	#############################################################################
	@property
	def ship_info(self):
		if hasattr(self, '_ship_info'):
			return self._ship_info
		else:
			try:
				_ship_infos = list(self.ship_infos.filter(is_selected=True))
				if len(_ship_infos) > 0:
					self._ship_info = _ship_infos[0]

				return self._ship_info
			except:
				return None

	#############################################################################
	# ship_info: 获取收货地址
	#############################################################################
	@property
	def ship_infos(self):
		if hasattr(self, '_ship_infos'):
			return self._ship_infos
		else:
			try:
				# 删除空的条目
				#ShipInfo.objects.filter(webapp_user_id=self.id, ship_name='').delete()
				self._ship_infos = ShipInfo.objects.filter(webapp_user_id=self.id, is_deleted=False)
				return self._ship_infos
			except:
				return None

	#############################################################################
	# update_ship_info: 更新收货地址
	#############################################################################
	def update_ship_info(self, ship_name=None, ship_address=None, ship_tel=None, area=None, ship_id=None):
		ship_infos = ShipInfo.objects.filter(webapp_user_id=self.id, is_selected=True)
		ShipInfo.objects.filter(webapp_user_id=self.id).update(is_selected=False)
		if ship_id > 0:
			ShipInfo.objects.filter(id=ship_id).update(
				ship_tel = ship_tel,
				ship_address = ship_address,
				ship_name = ship_name,
				area = area,
				is_selected = True
			)
		elif ship_infos.count() > 0 and ship_id is None:
			ship_infos.update(
				ship_tel = ship_tel,
				ship_address = ship_address,
				ship_name = ship_name,
				area = area,
				is_selected = True
			)
		else:
			ShipInfo.objects.create(
				webapp_user_id = self.id,
				ship_tel = ship_tel,
				ship_address = ship_address,
				ship_name = ship_name,
				area = area
			)

	@property
	def is_member(self):
		return self.member_id > 0

	#############################################################################
	# can_use_integral: 检查是否可用数量为integral的积分
	#############################################################################
	def can_use_integral(self, integral):
		if not self.is_member:
			return False

		remianed_integral = Member.objects.get(id=self.member_id).integral
		if remianed_integral >= integral:
			return True
		else:
			return False

	#############################################################################
	# integral_info: 获取积分信息
	#############################################################################
	@cached_property
	def integral_info(self):
		try:
			self.member = Member.objects.get(id=self.member_id)
			member = self.member
			count = member.integral
			target_grade_id = member.grade_id
			target_member_grade = self.webapp_owner_info.member2grade.get(target_grade_id, None)
			if target_member_grade:
				usable_integral_percentage_in_order = target_member_grade.usable_integral_percentage_in_order
			else:
				usable_integral_percentage_in_order = 100
		except:
			count = 0
			usable_integral_percentage_in_order = 100

		#计算积分金额
		if self.webapp_owner_info and hasattr(self.webapp_owner_info, 'integral_strategy_settings'):
			integral_strategy_settings = self.webapp_owner_info.integral_strategy_settings
		else:
			integral_strategy_settings = IntegralStrategySttings.objects.get(webapp_id=self.webapp_id)

		count_per_yuan = integral_strategy_settings.integral_each_yuan

		usable_integral_or_conpon = integral_strategy_settings.usable_integral_or_conpon
		return {
			'count': count,
			'count_per_yuan': count_per_yuan,
			'usable_integral_percentage_in_order' : usable_integral_percentage_in_order,
			'usable_integral_or_conpon' : usable_integral_or_conpon
		}

	#############################################################################
	# use_integral: 使用积分，返回积分对应的金额
	#############################################################################
	def use_integral(self, integral_count):
		from integral import use_integral_to_buy

		if integral_count == 0:
			return 0.0

		member = Member.objects.get(id=self.member_id)
		return use_integral_to_buy(member, integral_count)

	#############################################################################
	# coupons: 获取用户的优惠券信息
	#############################################################################
	@property
	def coupons(self):
		if self.member_id == 0:
			return []
		else:
			from market_tools.tools.coupon.util import get_my_coupons
			return get_my_coupons(self.member_id)

	#############################################################################
	# use_coupon: 使用优惠券
	#############################################################################
	def use_coupon(self, coupon_id, price=0):
		if coupon_id > 0:
			try:
				coupon = coupon_model.Coupon.objects.get(id=coupon_id, status=coupon_model.COUPON_STATUS_UNUSED)
			except:
				raise IOError
			coupon.money = float(coupon.money)
			coupon_role = coupon_model.CouponRule.objects.get(id=coupon.coupon_rule_id)
			coupon.valid_restrictions = coupon_role.valid_restrictions
			if coupon.valid_restrictions > price and coupon.valid_restrictions != -1:
				raise ValueError
			coupon_model.Coupon.objects.filter(id=coupon_id).update(status=coupon_model.COUPON_STATUS_USED)
		else:
			coupon = coupon_model.Coupon()
			coupon.money = 0.0
			coupon.id = coupon_id

		return coupon

	#############################################################################
	# use_coupon_by_coupon_id: 使用优惠券通过优惠券号
	#############################################################################
	def use_coupon_by_coupon_id(self, member_id, coupon_id, price=0, webapp_owner_id=-1):
		if coupon_id > 0:
			try:
				coupon = coupon_model.Coupon.objects.get(owner_id=webapp_owner_id, coupon_id=coupon_id, status=coupon_model.COUPON_STATUS_UNUSED)
			except:
				raise IOError
			coupon.money = float(coupon.money)
			coupon_role = coupon_model.CouponRule.objects.get(id=coupon.coupon_rule_id)
			coupon.valid_restrictions = coupon_role.valid_restrictions
			if coupon.valid_restrictions > price and coupon.valid_restrictions!=-1:
				raise ValueError
			coupon_model.Coupon.objects.filter(coupon_id=coupon_id).update(status=coupon_model.COUPON_STATUS_USED)
		else:
			coupon = coupon_model.Coupon()
			coupon.money = 0.0
			coupon.id = coupon_id

		return coupon

	#############################################################################
	# complete_payment: 完成支付，进行支付后的处理
	#############################################################################
	def complete_payment(self, request, order=None):
		if request is None:
			return

		from integral import increase_for_buy_via_shared_url
		#首先进行积分的处理
		#print '===========innnnnnnnnnnnnnnnnnnnnnnnnnnnnnn'
		increase_for_buy_via_shared_url(request, order)
		#进行分享链接的相关计算
		from modules.member.util import  process_payment_with_shared_info
		process_payment_with_shared_info(request)

	#############################################################################
	# get_discount: 获取折扣信息
	#############################################################################
	def get_discount(self):
		if not hasattr(self, '_grade'):
			if not self.is_member:
				self._grade = {'grade':'', 'discount':100}
			else:
				target_grade_id = self.member.grade_id
				target_member_grade = self.webapp_owner_info.member2grade.get(target_grade_id, None)

				if not target_member_grade:
					self._grade = {'grade':'', 'discount':100}
				else:
					self._grade = {'grade':target_member_grade.name, 'discount':target_member_grade.shop_discount}
		return self._grade

	#############################################################################
	# get_discounted_money: 获取折扣后的金额
	# product_type: 商品类型
	# 1、如果折扣为100% 或者 商品类型为积分商品，返回当前的价格
	# 2、折扣不为100% 并且不是积分商品，计算折扣
	#############################################################################
	def get_discounted_money(self, money, product_type=PRODUCT_DEFAULT_TYPE):
		return money, 0
		'''
		grade_discount = self.get_discount()
		if grade_discount['discount'] == 100 or product_type == PRODUCT_INTEGRAL_TYPE:
			return money, 0
		else:
			discount = grade_discount['discount'] / 100.0
			discounted_money = float('%.2f' % (money * discount))
			delta = money - discounted_money
			return discounted_money, delta
		'''

	#############################################################################
	# set_purchased: 设置已购买标识
	#############################################################################
	def set_purchased(self):
		if not self.has_purchased:
			WebAppUser.objects.update(has_purchased=True)

	@staticmethod
	def from_member(member):
		if member is None:
			return None

		try:
			return WebAppUser.objects.get(member_id=member.id, father_id=0, webapp_id=member.webapp_id)
		except WebAppUser.DoesNotExist:
			return None

	def consume_integral(self, count, type):
		member = Member.from_webapp_user(self)
		if member is None:
			return

		try:
			member.consume_integral(count, type)
		except:
			notify_msg = u"消费积分出错，会员id:{}, type:{}".format(member.id, type)
			watchdog_fatal(notify_msg)

#===============================================================================
# MemberGrade : 会员等级
#===============================================================================
class MemberGrade(models.Model):
	webapp_id = models.CharField(max_length=16, db_index=True, verbose_name='所关联的app id')
	name = models.TextField()
	is_auto_upgrade = models.BooleanField(default=False, verbose_name='是否凭经验值自动升级')
	upgrade_lower_bound = models.IntegerField(default=0, verbose_name='该等级的经验值下限')
	shop_discount = models.IntegerField(default=100, verbose_name='购物折扣')
	is_default_grade = models.BooleanField(default=False)
	# 14迭代 bert add
	usable_integral_percentage_in_order = models.IntegerField(verbose_name='一笔交易中能使用的多少积分', default=100) # -1 无限制

	pay_money = models.FloatField(default=0.00)
	pay_times = models.IntegerField(default=0)
	integral = models.IntegerField(default=0)

	class Meta(object):
		db_table = 'member_grade'
		verbose_name = '会员等级'
		verbose_name_plural = '会员等级'

	def __unicode__(self):
		return u"{}-{}".format(self.webapp_id, self.name)

	#############################################################################
	# integral_info: 获取积分信息
	#############################################################################
	@property
	def integral_info(self):
		count = Member.objects.get(id=self.member_id).integral
		count_per_yuan = IntegralStrategySttings.objects.get(webapp_id=self.webapp_id).integral_each_yuan
		return {
			'count': count,
			'count_per_yuan': count_per_yuan
		}

	@property
	def member_count(self):
		return Member.objects.filter(grade_id=self.id, is_for_test=False, is_subscribed=True).count()

	DEFAULT_GRADE_NAME = u'普通会员'
	@staticmethod
	def get_default_grade(webapp_id):
		try:
			return MemberGrade.objects.get(webapp_id=webapp_id, is_default_grade=True)
		except:
			return MemberGrade.objects.create(
				webapp_id = webapp_id,
				name = MemberGrade.DEFAULT_GRADE_NAME,
				upgrade_lower_bound = 0,
				is_default_grade = True
			)

	@staticmethod
	def get_all_grades_list(webapp_id):
		if webapp_id is None:
			return []
		member_grades = MemberGrade.objects.filter(webapp_id=webapp_id).order_by('id')

		for member_grade in member_grades:
			member_grade.pay_money = '%.2f' % member_grade.pay_money
		return member_grades

	@staticmethod
	def get_all_auto_grades_list(webapp_id):
		if webapp_id is None:
			return []
		member_grades = MemberGrade.objects.filter(webapp_id=webapp_id,is_auto_upgrade=True).order_by('id')

		for member_grade in member_grades:
			member_grade.pay_money = '%.2f' % member_grade.pay_money
		return member_grades

#===============================================================================
# Member : 会员
#===============================================================================
SOURCE_SELF_SUB = 0  # 直接关注
SOURCE_MEMBER_QRCODE = 1  # 推广扫码
SOURCE_BY_URL = 2  # 会员分享

#status  会员状态
CANCEL_SUBSCRIBED = 0
SUBSCRIBED = 1
NOT_SUBSCRIBED = 2
class Member(models.Model):
	token = models.CharField(max_length=255, db_index=True, unique=True)
	webapp_id = models.CharField(max_length=16, db_index=True)
	username_hexstr = models.CharField(max_length=128, blank=True, null=True,verbose_name='会员名称的hex str')
	user_icon = models.CharField(max_length=1024, blank=True, verbose_name='会员头像')
	integral = models.IntegerField(default=0, verbose_name='积分')
	created_at = models.DateTimeField(auto_now_add=True)
	grade = models.ForeignKey(MemberGrade)
	experience = models.IntegerField(default=0, verbose_name='经验值')
	remarks_name = models.CharField(max_length=32, blank=True, verbose_name='备注名')
	remarks_extra = models.TextField(blank=True, null=True, verbose_name='备注信息')
	last_visit_time = models.DateTimeField(auto_now_add=True)
	last_message_id = models.IntegerField(default=-1, verbose_name="最近一条消息id")
	session_id = models.IntegerField(default=-1, verbose_name="会话id")
	is_for_test = models.BooleanField(default=False)
	is_subscribed = models.BooleanField(default=True)
	friend_count = models.IntegerField(default=0) #好友数量
	factor = models.FloatField(default=0.00) #社会因子
	source = models.IntegerField(default=-1) #会员来源
	is_for_buy_test = models.BooleanField(default=False)
	update_time = models.DateTimeField(default=datetime.now())#会员信息更新时间 2014-11-11
	pay_money = models.FloatField(default=0.0)
	pay_times =  models.IntegerField(default=0)
	last_pay_time = models.DateTimeField(blank=True, null=True, default=None)#会员信息更新时间 2014-11-11
	unit_price = models.FloatField(default=0.0) #ke dan jia
	city = models.CharField(default='', max_length=50)
	province = models.CharField(default='', max_length=50)
	country = models.CharField(default='', max_length=50)
	sex = models.IntegerField(default=0, verbose_name='性别')
	status = models.IntegerField(default=1, db_index=True)

	class Meta(object):
		db_table = 'member_member'
		verbose_name = '会员'
		verbose_name_plural = '会员'

	def __unicode__(self):
		return u'<member: %s %s>' % (self.webapp_id, self.username)

	@property
	def get_webapp_user_ids(self):
		return [webapp_user.id for webapp_user in WebAppUser.objects.filter(member_id=self.id)]


	@staticmethod
	def from_webapp_user(webapp_user):
		if (webapp_user is None) or (not webapp_user.is_member):
			return None

		try:
			return Member.objects.get(id=webapp_user.member_id)
		except:
			#TODO 进行异常处理？？
			return None

	@staticmethod
	def members_from_webapp_user_ids(webapp_user_ids):
		if not webapp_user_ids:
			return []

		webappuser2member = dict([(u.id, u.member_id) for u in WebAppUser.objects.filter(id__in=webapp_user_ids)])
		member_ids = set(webappuser2member.values())
		id2member = dict([(m.id, m) for m in Member.objects.filter(id__in=member_ids)])

		for webapp_user_id, member_id in webappuser2member.items():
			webappuser2member[webapp_user_id] = id2member.get(member_id, None)

		return webappuser2member

	@staticmethod
	def update_last_visit_time(member):
		if member is None:
			return

		member.last_visit_time = datetime.now()
		member.save()

	@property
	def username(self):
		if hasattr(self, '_username'):
			return self._username

		self._username = hex_to_byte(self.username_hexstr)
		return self._username

	@username.setter
	def username(self, username):
		self.username_hexstr = byte_to_hex(username)

	@cached_property
	def username_for_html(self):
		if hasattr(self, '_username_for_html'):
			return self._username_for_html

		if (self.username_hexstr is not None) and (len(self.username_hexstr) > 0):
			self._username_for_html = encode_emojicons_for_html(self.username_hexstr, is_hex_str=True)
		else:
			self._username_for_html = encode_emojicons_for_html(self.username)

		try:
			#解决用户名本身就是字节码串导致不能正常转换得问题，例如ae
			self._username_for_html.decode('utf8')
		except:
			self._username_for_html = self.username_hexstr

		return self._username_for_html

	'''
	@cached_property
	def username_for_html(self):
		if hasattr(self, '_username_for_html'):
			return self._username_for_html

		if (self.username_hexstr is not None) and (len(self.username_hexstr) > 0):
			self._username_for_html = encode_emojicons_for_html(self.username_hexstr, is_hex_str=True)
		else:
			self._username_for_html = encode_emojicons_for_html(self.username)

		try:
			#解决用户名本身就是字节码串导致不能正常转换得问题，例如ae
			self._username_for_html.decode('utf8')
		except:
			error_msg = u"用户名:{}; utf8解码失败, cause:\n{}".format(self._username_for_html, unicode_full_stack())
			watchdog_error(error_msg, 'mall')
			self._username_for_html = self.username_hexstr

		return self._username_for_html
	'''

	@cached_property
	def username_for_title(self):
		try:
			username = unicode(self.username_for_html, 'utf8')
			username = re.sub('<[^<]+?>', '', username)
			return username
		except:
			return self.username_for_html

	@cached_property
	def username_truncated(self):
		try:
			username = unicode(self.username_for_html, 'utf8')
			_username = re.sub('<[^<]+?>', '', username)
			if len(_username) <= 5:
				return username
			else:
				return u'%s...' % username[:5]
		except:
			return self.username_for_html[:5]

	@property
	def friends(self):
		if hasattr(self, '_friends'):
			return self._friends

		self._friends = MemberFollowRelation.get_follow_members_for(self.id)
		return self._friends

	@staticmethod
	def count(webapp_id):
		return Member.objects.filter(webapp_id=webapp_id).count()

	@staticmethod
	def update_factor(member):
		friends_count =len(MemberFollowRelation.get_follow_members_for(member.id, '1'))
		friends_from_qrcodes = len(MemberFollowRelation.get_follow_members_for(member.id, '1', True))
		#总点击数
		click_counts = MemberSharedUrlInfo.objects.filter(member=member).aggregate(Sum("pv"))

		if click_counts["pv__sum"]:
			click_counts = float(click_counts["pv__sum"])
		else:
			click_counts = 0

		if (click_counts + friends_from_qrcodes) != 0:
			factor =  float('%.2f' % (float(friends_count + friends_from_qrcodes) / float(friends_from_qrcodes + click_counts)))
			if member.factor != factor:
				Member.objects.filter(id=member.id).update(factor=factor)


	def consume_integral(self, count, type):
		if type is None:
			return

		from integral import increase_member_integral
		increase_member_integral(self, -count, type, to_task=False)

	def update_member_info(self, username, phone_number):
		if (username is None) or (phone_number is None):
			return

		MemberInfo.objects.filter(member=self).update(
			name = username,
			phone_number = phone_number
		)

	@property
	def member_info(self):
		try:
			return MemberInfo.objects.get(member=self)
		except:
			return MemberInfo.objects.create(
				member = Member.objects.get(id=self.id),
				name = ''
				)


	@staticmethod
	def increase_friend_count(member_ids):
		from django.db import connection, transaction
		cursor = connection.cursor()
		cursor.execute('update member_member set friend_count = friend_count + 1 where id in (%s);' % (member_ids))
		transaction.commit_unless_managed()

	@property
	def member_open_id(self):
		member_has_social_accounts = MemberHasSocialAccount.objects.filter(member=self)
		if member_has_social_accounts.count() > 0:
			return member_has_social_accounts[0].account.openid
		else:
			return None

	@staticmethod
	def get_members(webapp_id):
		return list(Member.objects.filter(webapp_id=webapp_id, is_subscribed=True, is_for_test=False))

	@staticmethod
	def get_member_list_by_grade_id(grade_id):
		return list(Member.objects.filter(grade_id=grade_id, is_subscribed=True, is_for_test=False))

	@staticmethod
	def get_member_by_weixin_user_id(id):
		try:
			weixin_user = WeixinUser.objects.get(id=id)
			social_account = SocialAccount.objects.get(openid=weixin_user.username, webapp_id=weixin_user.webapp_id)
			if MemberHasSocialAccount.objects.filter(account=social_account).count() > 0:
				return MemberHasSocialAccount.objects.filter(account=social_account)[0].member
			else:
				return None
		except:
			return None

	@staticmethod
	def update_member_grade(member_id, grade_id):
		from django.db import connection, transaction
		cursor = connection.cursor()
		cursor.execute('update member_member set grade_id = %d where id = %d;' % (grade_id, member_id))
		transaction.commit_unless_managed()

	@property
	def is_binded(self):
		if MemberInfo.objects.filter(member_id=self.id).count() > 0:
			member_info = MemberInfo.objects.filter(member_id=self.id)[0]
			return member_info.is_binded
		else:
			MemberInfo.objects.create(
				member=self,
				name='',
				weibo_nickname=''
				)
			return False


#===============================================================================
# modify_member_grade : 进行会员的等级修改操作
#===============================================================================
def modify_member_grade(member):
	auto_upgrade_grades = MemberGrade.objects.filter(webapp_id=member.webapp_id, is_auto_upgrade=True,
		upgrade_lower_bound__lte=member.experience).order_by('-upgrade_lower_bound')

	if auto_upgrade_grades.count() > 0:
		new_grade = auto_upgrade_grades[0]

		member.grade = new_grade
		member.save()
		return True
	else:
		return False

SEX_TYPE_MEN = 1
SEX_TYPE_WOMEN = 2
SEX_TYPE_UNKOWN = 0
SEX_TYPES = (
	(SEX_TYPE_MEN, '男'),
	(SEX_TYPE_WOMEN, '女'),
	(SEX_TYPE_UNKOWN, '未知')
	)

class MemberInfo(models.Model):
	#member = models.ForeignKey(Member)
	member = models.OneToOneField(Member, primary_key=True)
	name = models.CharField(max_length=8, verbose_name='会员姓名')
	sex = models.IntegerField(choices=SEX_TYPES, verbose_name='性别')
	age = models.IntegerField(default=-1, verbose_name='年龄')
	address = models.CharField(max_length=32, blank=True, null=True, verbose_name='地址')
	phone_number = models.CharField(max_length=11, blank=True)
	qq_number = models.CharField(max_length=13, blank=True)
	weibo_nickname = models.CharField(max_length=16, verbose_name='微博昵称')
	member_remarks = models.TextField(max_length=1024, blank=True)
	#new add by bert
	is_binded = models.BooleanField(default=False)
	session_id = models.CharField(max_length=1024, blank=True)
	captcha = models.CharField(max_length=11, blank=True) #验证码
	binding_time = models.DateTimeField(blank=True, null=True) #绑定时间
	#is_passed = models.BooleanField(default=False)


	class Meta(object):
		#managed = False
		db_table = 'member_info'
		verbose_name = '会员详细资料'
		verbose_name_plural = '会员详细资料'

	@staticmethod
	def get_member_info(member_id):
		if member_id is None or member_id <= 0:
			return None
		try:
			return MemberInfo.objects.filter(member_id=member_id)[0]
		except:
			return MemberInfo.objects.create(
					member_id=member_id,
					name='',
					weibo_nickname='',
					sex=0
					)
	@staticmethod
	def is_can_binding(phone_number, member_id, webapp_id):
		return not MemberInfo.objects.filter(member__webapp_id=webapp_id, is_binded=True, phone_number=phone_number).count() > 0



class MemberHasSocialAccount(models.Model):
	member = models.ForeignKey(Member)
	account = models.ForeignKey(SocialAccount, unique=True,db_index=True)
	webapp_id = models.CharField(max_length=50, db_index=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'member_has_social_account'
		verbose_name = '会员绑定的社会化账号'
		verbose_name_plural = '会员绑定的社会化账号'


class MemberFollowRelation(models.Model):
	member_id = models.IntegerField(db_index=True)
	follower_member_id = models.IntegerField(db_index=True)
	is_fans = models.BooleanField(default=False) #是否是member_id 粉丝
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'member_follow_relation'
		verbose_name = '会员间的关注关系'
		verbose_name_plural = '会员间的关注关系'

	@staticmethod
	def get_follow_members_for(member_id, is_fans='0', is_from_qrcode=False):
		if member_id is None or member_id <= 0:
			return []

		try:

			if is_fans != '0' and is_fans != None:
				follow_relations = MemberFollowRelation.objects.filter(member_id=member_id, is_fans=True).order_by('id')
			else:
				follow_relations = MemberFollowRelation.objects.filter(member_id=member_id).order_by('id')

			follow_member_ids = [relation.follower_member_id for relation in follow_relations]

			if is_from_qrcode:
				return Member.objects.filter(id__in=follow_member_ids,source=SOURCE_MEMBER_QRCODE,status__in=[SUBSCRIBED, CANCEL_SUBSCRIBED])
			else:
				return Member.objects.filter(id__in=follow_member_ids, status__in=[SUBSCRIBED, CANCEL_SUBSCRIBED])
		except:
			return []

	@staticmethod
	def get_follow_members_for_shred_url(member_id):
		if member_id is None or member_id <= 0:
			return []

		try:
			follow_relations = MemberFollowRelation.objects.filter(member_id=member_id, is_fans=True).order_by('id')
			follow_member_ids = [relation.follower_member_id for relation in follow_relations]
			return Member.objects.filter(id__in=follow_member_ids, source=SOURCE_BY_URL)
		except:
			return []


	@staticmethod
	def is_fan(member_id, follower_member_id):
		return 1 if MemberFollowRelation.objects.filter(member_id=member_id, follower_member_id=follower_member_id, is_fans=True).count() > 0 else 0

	@staticmethod
	def is_father(member_id, follow_mid):
		return 1 if MemberFollowRelation.objects.filter(member_id=follow_mid, follower_member_id=member_id, is_fans=True).count() > 0 else 0

	@staticmethod
	def get_father_member(member_id):
		member_relation = MemberFollowRelation.objects.filter(follower_member_id=member_id, is_fans=True)[0] if MemberFollowRelation.objects.filter(follower_member_id=member_id, is_fans=True).count() > 0 else None
		if member_relation:
			try:
				return Member.objects.get(id=member_relation.member_id)
			except:
				return None
		return None

class MemberSharedUrlInfo(models.Model):
	member = models.ForeignKey(Member)
	shared_url = models.CharField(max_length=1024)
	shared_url_digest = models.CharField(max_length=32, db_index=True)
	pv = models.IntegerField(default=1)
	leadto_buy_count = models.IntegerField(default=0)
	title = models.CharField(max_length=256, default='')
	cr = models.FloatField(default=0.0)
	followers = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'member_shared_url_info'
		verbose_name = '分享链接信息'
		verbose_name_plural = '分享链接信息'

	@staticmethod
	def get_member_share_url_info(member_id):
		if member_id is None or member_id <= 0:
			return []
		return list(MemberSharedUrlInfo.objects.filter(member_id=member_id))

class ShipInfo(models.Model):
	webapp_user_id = models.IntegerField(db_index=True, default=0)
	ship_name = models.CharField(max_length=100) # 收货人姓名
	ship_tel = models.CharField(max_length=100) # 收货人电话
	ship_address = models.CharField(max_length=200) # 收货人地址
	area = models.CharField(max_length=256) #地区
	is_selected = models.BooleanField(default=True) # 是否选中，默认是选中
	is_deleted = models.BooleanField(default=False) # 是否被删除
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'member_ship_info'
		verbose_name = '收货地址'
		verbose_name_plural = '收获地址'

	@property
	def get_str_area(self):
		from tools.regional import views as regional_util
		if self.area:
			return regional_util.get_str_value_by_string_ids(self.area)
		else:
			return ''


class AnonymousClickedUrl(models.Model):
	url = models.CharField(max_length=1024)
	url_digest = models.CharField(max_length=32, db_index=True) #md5
	uuid = models.CharField(max_length=100, db_index=True)
	followed_mid = models.IntegerField(db_index=True)
	webapp_user_id = models.IntegerField(db_index=True, default=0)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'anonymous_clicked_url'
		verbose_name = 'url匿名点击记录'
		verbose_name_plural = 'url匿名点击记录'


class MemberClickedUrl(models.Model):
	url = models.CharField(max_length=1024)
	url_digest = models.CharField(max_length=32, db_index=True) #md5
	mid = models.IntegerField(db_index=True)
	followed_mid = models.IntegerField(db_index=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'member_clicked_url'
		verbose_name = '会员url点击记录'
		verbose_name_plural = '会员url点击记录'

#########################################################################
# IntegralStrategySttings
#########################################################################
USABLE_BOTH = 0 #积分优惠券可以同时使用
USABLE_INTEGRAL = 1 #只可使用积分
USABLE_CONPON = 2 #只可使用优惠券
ONLY_ONE = 3 #仅可用一项
class IntegralStrategySttings(models.Model):
	webapp_id = models.CharField(max_length=20, verbose_name='webapp id', db_index=True, unique=True)

	click_shared_url_increase_count_after_buy = models.IntegerField(verbose_name='点击分享链接为购买后的分享者增加的额度', default=0)
	click_shared_url_increase_count_before_buy = models.IntegerField(verbose_name='点击分享链接为未购买的分享者增加的额度', default=0)
	buy_increase_count_for_father = models.IntegerField(verbose_name='成为会员增加额度', default=0)
	increase_integral_count_for_brring_customer_by_qrcode = models.IntegerField(verbose_name='使用二维码带来用户增加的额度', default=0)
	integral_each_yuan = models.IntegerField(verbose_name='一元是多少积分', default=0)
	usable_integral_or_conpon = models.IntegerField(verbose_name='积分与优惠券可同时使用', default=USABLE_BOTH)
	#v2
	be_member_increase_count = models.IntegerField(verbose_name='成为会员增加额度', default=0)
	order_money_percentage_for_each_buy = models.CharField(max_length=25, verbose_name="每次购物后，额外积分（以订单金额的百分比计算）", default="0.0")
	buy_via_offline_increase_count_for_author = models.IntegerField(verbose_name='线下会员购买为推荐者增加的额度', default=0)
	click_shared_url_increase_count = models.IntegerField(verbose_name='分享链接给好友点击', default=0)
	buy_award_count_for_buyer = models.IntegerField(verbose_name='购物返积分额度', default=0)
	buy_via_shared_url_increase_count_for_author = models.IntegerField(verbose_name='通过分享链接购买为分享者增加的额度', default=0)
	buy_via_offline_increase_count_percentage_for_author = models.CharField(max_length=25, verbose_name="线下会员购买为推荐者额外增加的额度(以订单金额的百分比计算）", default="0.0")
	use_ceiling = models.IntegerField(default=-1, verbose_name='订单积分抵扣上限')
	review_increase = models.IntegerField(default=0, verbose_name='商品好评送积分')
	is_all_conditions = models.BooleanField(default=False,verbose_name='自动升级条件')

	class Meta(object):
		db_table = 'member_integral_strategy_settings'
		verbose_name = '积分策略配置'
		verbose_name_plural = '积分策略配置'

	@staticmethod
	def get_integral_each_yuan(webapp_id):
		if IntegralStrategySttings.objects.filter(webapp_id=webapp_id).count() > 0:
			return IntegralStrategySttings.objects.filter(webapp_id=webapp_id)[0].integral_each_yuan
		else:
			return None

#===============================================================================
# create_webapp_member_integral_strategy_sttings : 自动创建webapp会员积分策略配置
#===============================================================================
def create_webapp_member_integral_strategy_sttings(instance, created, **kwargs):
	if created:
		webapp_id = instance.webapp_id.strip()
		if len(webapp_id) == 0:
			webapp_id = '%d' % (settings.MIXUP_FACTOR + instance.id)

		if IntegralStrategySttings.objects.filter(webapp_id=webapp_id).count() == 0:
			IntegralStrategySttings.objects.create(webapp_id=webapp_id)

signals.post_save.connect(create_webapp_member_integral_strategy_sttings, sender=UserProfile, dispatch_uid = "member.create_webapp_member_integral_strategy_sttings")

FIRST_SUBSCRIBE = u'首次关注'
#FOLLOWER_CLICK_SHARED_URL = u'好友奖励'
FOLLOWER_CLICK_SHARED_URL = u'好友点击分享链接奖励'
USE = '购物抵扣'
RETURN_BY_SYSTEM = '积分返还'
AWARD = '积分领奖'
BUY_AWARD = '购物返利'
#FOLLOWER_BUYED_VIA_SHARED_URL = u'好友奖励'
FOLLOWER_BUYED_VIA_SHARED_URL = u'好友通过分享链接购买奖励'
BRING_NEW_CUSTOMER_VIA_QRCODE = u'推荐扫码奖励'
MANAGER_MODIFY = '系统管理员修改'
MANAGER_MODIFY_ADD = '管理员赠送'
MANAGER_MODIFY_REDUCT = '管理员扣减'
CHANNEL_QRCODE = u'渠道扫码奖励'
BUY_INCREST_COUNT_FOR_FATHER = u'推荐关注的好友购买奖励'

class MemberIntegralLog(models.Model):
	member = models.ForeignKey(Member)
	webapp_user_id = models.IntegerField(default=0)
	event_type = models.CharField(max_length=64, verbose_name='引起积分变化事件类型')
	integral_count = models.IntegerField(default=0, verbose_name='积分量')
	follower_member_token = models.CharField(max_length=255, null=True, blank=True, verbose_name='所关注的会员的token')
	reason = models.CharField(max_length=255, default='')
	current_integral = models.CharField(default='0', max_length=255)
	manager = models.CharField(default='', max_length=255)
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='记录时间')

	class Meta(object):
		db_table = 'member_integral_log'
		verbose_name = '积分日志'
		verbose_name_plural = '积分日志'

	@staticmethod
	def update_follower_member_token(member):
		member_integral_logs = MemberIntegralLog.objects.filter(webapp_user_id__gt=0, follower_member_token='', member=member)
		for log in member_integral_logs:
			webapp_users = WebAppUser.objects.filter(id=log.webapp_user_id)
			if webapp_users.count() > 0:
				member_id = webapp_users[0].id
				if member_id != 0 and member_id != -1:
					try:
						member = Member.objects.get(id=member_id)
						log.follower_member_token = member.token
						log.save()
					except:
						pass


#########################################################################
# MemberBrowseRecordMiddleware
#########################################################################
class MemberBrowseRecord(models.Model):
	member = models.ForeignKey(Member)
	title = models.CharField(max_length=256, default='') #页面标题
	url = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'member_browse_record'
		verbose_name = '会员浏览记录'
		verbose_name_plural = '会员浏览记录'

	@staticmethod
	def get_title(member, url):
		if url.find('from') > -1:
			url = url[:url.find('from')]
		return MemberBrowseRecord.objects.filter(member=member,url__icontains=url)[0].title if MemberBrowseRecord.objects.filter(url__icontains=url,member=member).count() > 0 else ''

#########################################################################
# MemberBrowseRecordMiddleware
#########################################################################
class NonmemberFirstVisitRecord(models.Model):
	uuid = models.CharField(max_length=100, db_index=True)
	appid = models.CharField(max_length=100, db_index=True)
	url = models.TextField()
	title = models.CharField(max_length=256, default='')
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'nonmember_first_visit_record'
		verbose_name = '非会员浏览记录'
		verbose_name_plural = '非会员浏览记录'


class MemberTag(models.Model):
	"""
	表示会员的标签(分组)
	"""
	webapp_id = models.CharField(max_length=16, db_index=True)
	name = models.CharField(max_length=100, db_index=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'member_tag'
		verbose_name = '会员分组'
		verbose_name_plural = '会员分组'

	@staticmethod
	def get_member_tags(webapp_id):
		if webapp_id:
			return list(MemberTag.objects.filter(webapp_id=webapp_id))
		else:
			return []

	@staticmethod
	def get_member_tag(webapp_id, name):
		return MemberTag.objects.filter(webapp_id=webapp_id, name=name)[0] if MemberTag.objects.filter(webapp_id=webapp_id, name=name).count() > 0 else None

	@staticmethod
	def create(webapp_id, name):
		return MemberTag.objects.create(webapp_id=webapp_id, name=name)

#########################################################################
# MemberHasTag
#########################################################################
class MemberHasTag(models.Model):
	member = models.ForeignKey(Member)
	member_tag = models.ForeignKey(MemberTag)

	class Meta(object):
		db_table = 'member_has_tag'
		verbose_name = '会员所属分组'
		verbose_name_plural = '会员所属分组'

	@staticmethod
	def get_member_has_tags(member):
		if member:
			return list(MemberHasTag.objects.filter(member=member))
		return []

	@staticmethod
	def get_tag_has_member_count(tag):
		return MemberHasTag.objects.filter(member_tag=tag).count()

	@staticmethod
	def is_member_tag(member, member_tag):
		if member and member_tag:
			return MemberHasTag.objects.filter(member=member, member_tag_id=member_tag.id).count()
		else:
			return False

	@staticmethod
	def delete_tag_member_relation_by_member(member):
		if member:
			MemberHasTag.objects.filter(member=member).delete()

	@staticmethod
	def add_tag_member_relation(member, tag_ids_list):
		if member and len(tag_ids_list) > 0:
			for tag_id in tag_ids_list:
				if tag_id:
					if MemberHasTag.objects.filter(member=member, member_tag_id=tag_id).count() == 0:
						MemberHasTag.objects.create(member=member, member_tag_id=tag_id)
	@staticmethod
	def get_member_list_by_tag_id(tag_id):
		if tag_id:
			members = []
			for member_has_tag in MemberHasTag.objects.filter(member_tag_id=tag_id):
				members.append(member_has_tag.member)
			return members
		else:
			return []

	@staticmethod
	def add_members_tag(tag_id, member_ids):
		if tag_id:
			for member_id in member_ids:
				if MemberHasTag.objects.filter(member_tag_id=tag_id, member_id=member_id).count() == 0:
					MemberHasTag.objects.create(member_id=member_id, member_tag_id=tag_id)


MESSAGE_TYPE_TEXT = 0
MESSAGE_TYPE_NEWS = 1
class UserSentMassMsgLog(models.Model):
	webapp_id = models.CharField(max_length=16, db_index=True)
	msg_id = models.CharField(max_length=256)
	sent_count = models.IntegerField(default=0)
	total_count = models.IntegerField(default=0)
	filter_count = models.IntegerField(default=0)
	error_count = models.IntegerField(default=0)
	status = models.CharField(default='', max_length=256)
	message_type = models.IntegerField(default=MESSAGE_TYPE_TEXT)
	#message_content = models.CharField(default='', max_length=256)
	message_content = models.CharField(default='', max_length=1024)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'user_sent_mass_msg_log'
		verbose_name = '用户发送群发消息记录'
		verbose_name_plural = '用户发送群发消息记录'

	@staticmethod
	def update_log(webapp_id, msg_id, sent_count, total_count, filter_count, error_count, status):
		UserSentMassMsgLog.objects.filter(
										webapp_id=webapp_id,
										msg_id=msg_id
										).update(
										total_count=total_count,
										filter_count=filter_count,
										error_count=error_count,
										sent_count=sent_count,
										status=status
										)

	@staticmethod
	def create(webapp_id, msg_id, message_type, message_content):
		UserSentMassMsgLog.objects.create(
								webapp_id=webapp_id,
								msg_id=msg_id,
								message_type=message_type,
								message_content=message_content
								)

	@staticmethod
	def success_count(webapp_id):
		now = datetime.now()
		return UserSentMassMsgLog.objects.filter(webapp_id=webapp_id, status__contains='success', created_at__year=now.year, created_at__month=now.month).count()


#########################################################################
# IntegralStrategySttingsDetail
#########################################################################
class IntegralStrategySttingsDetail(models.Model):
	webapp_id = models.CharField(max_length=20, verbose_name='webapp id', db_index=True, unique=True)
	is_used = models.BooleanField(default=False)
	increase_count_after_buy = models.DecimalField(max_digits=65, decimal_places=1, default=0.0) #购买商品返积分
	buy_via_shared_url_increase_count_for_author = models.DecimalField(max_digits=65, decimal_places=1, default=0.0) # 通过分享链接购买后给分享者增加的积分
	buy_increase_count_for_father = models.DecimalField(max_digits=65, decimal_places=1, default=0.0)# 每次购买给邀请者增加的积分

	class Meta(object):
		db_table = 'member_integral_strategy_settings_detail'
		verbose_name = '积分详细设置'
		verbose_name_plural = '积分详细设置'


########################################################################
#MemberAbaktsus
########################################################################
#0代表其他 30代表扫二维码 17代表名片分享 35代表搜号码（即微信添加朋友页的搜索） 39代表查询微信公众帐号 43代表图文页右上角菜单
class MemberAnalysis(models.Model):
	owner_id = models.IntegerField(default=0)
	date_time = models.CharField(default='',max_length=50) #2014-12-07
	cumulate_user = models.IntegerField(default=0) #总用户量
	cancel_user = models.IntegerField(default=0) #cancel_user
	new_user = models.IntegerField(default=0) #新增的用户数量
	net_growth = models.IntegerField(default=0)#new_user -cancel_user

	class Meta(object):
		db_table = 'member_analysis'
		verbose_name = '用户统计'
		verbose_name_plural = '用户统计'

	@staticmethod
	def get_analysis_by_date(owner_id, date_time):
		try:
			return MemberAnalysis.objects.filter(owner_id=owner_id, date_time=date_time)[0]
		except:
			return None


class MemberAnalysisDetail(models.Model):
	member_analysis = models.ForeignKey(MemberAnalysis)
	user_source = models.CharField(default='0', max_length=50)
	new_user = models.IntegerField(default=0)
	cancel_user = models.IntegerField(default=0)

	class Meta(object):
		db_table = 'member_analysis_detail'
		verbose_name = '用户统计详情'
		verbose_name_plural = '用户统计详情'


class MemberMarketUrl(models.Model):
	member = models.ForeignKey(Member)
	market_tool_name = models.CharField(default='', max_length=50)
	url = models.TextField()
	page_title = models.CharField(default='', max_length=50)
	follower_member_token = models.CharField(default='', max_length=1024)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'member_market_url'
		verbose_name = '营销工具引流'
		verbose_name_plural = '营销工具引流'


class MemberRefueling(models.Model):
	member = models.ForeignKey(Member)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'member_refueling'
		verbose_name = '加油分享活动'
		verbose_name_plural = '加油分享活动'


class MemberRefuelingInfo(models.Model):
	member_refueling = models.ForeignKey(MemberRefueling)
	follow_member = models.ForeignKey(Member)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'member_refueling_info'
		verbose_name = '加油分享活动信息'
		verbose_name_plural = '加油分享活动信息'
		unique_together = ('member_refueling', 'follow_member')

class MemberRefuelingHasOrder(models.Model):
	member_refueling = models.ForeignKey(MemberRefueling)
	order_id = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'member_refueling_has_order'
		verbose_name = '加油分享活动下单记录'
		verbose_name_plural = '加油分享活动下单记录'
