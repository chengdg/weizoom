# -*- coding: utf-8 -*-

from datetime import datetime
from hashlib import md5

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals
from django.conf import settings
from django.db.models import F
from datetime import datetime, timedelta

from core import dateutil
from modules.member.models import *
from account.models import *


#########################################################################
# WeizoomCardRule ：微众卡规则
#########################################################################
#微众卡类型
WEIZOOM_CARD_EXTERNAL_USER = 0 #外部卡
WEIZOOM_CARD_INTERNAL_USER = 1 #内部卡
WEIZOOM_CARD_GIFT_USER = 2 #赠品卡

class WeizoomCardRule(models.Model):
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=20, db_index=True) #名称
	money = models.DecimalField(max_digits=65, decimal_places=2) #微众卡金额
	count = models.IntegerField(default=0) #发放总数量
	remark = models.CharField(max_length=20, db_index=True) #备注
	expired_time = models.DateTimeField() #过期时间
	valid_time_from = models.DateTimeField() #有效范围开始时间
	valid_time_to = models.DateTimeField() #有效范围结束时间
	created_at = models.DateTimeField(auto_now_add=True) #添加时间
	card_type = models.IntegerField(default=WEIZOOM_CARD_EXTERNAL_USER) #微众卡类型

	@staticmethod
	def get_all_weizoom_card_rules_list(user):
		if user is None:
			return []

		return list(WeizoomCoinRule.objects.filter(owner=user))

	class Meta(object):
		db_table = 'market_tool_weizoom_card_rule'
		verbose_name = '微众卡规则'
		verbose_name_plural = '微众卡规则'


#########################################################################
# WeizoomCard ：微众卡
#########################################################################
#微众卡状态
WEIZOOM_CARD_STATUS_UNUSED = 0 #未使用
WEIZOOM_CARD_STATUS_USED = 1 #已被使用
WEIZOOM_CARD_STATUS_EMPTY = 2 #已用完
WEIZOOM_CARD_STATUS_INACTIVE = 3 #未激活

class WeizoomCard(models.Model):
	owner = models.ForeignKey(User)
	target_user_id = models.IntegerField(default=0, verbose_name="微众卡发放目标, WeizoomCardHasAccount.account.id即owner_id")
	weizoom_card_rule = models.ForeignKey(WeizoomCardRule) 
	status = models.IntegerField(default=WEIZOOM_CARD_STATUS_INACTIVE) #微众卡状态
	weizoom_card_id = models.CharField(max_length=50) #微众卡号
	money = models.DecimalField(max_digits=65, decimal_places=2) #剩余金额
	password = models.CharField(max_length=50) #微众卡密码
	expired_time = models.DateTimeField() #过期时间
	is_expired = models.BooleanField(default=False) #是否过期
	activated_at = models.DateTimeField(null=True) #激活时间
	created_at = models.DateTimeField(auto_now_add=True) #添加时间
	remark = models.CharField(max_length=20) #备注
	activated_to = models.CharField(max_length=20) #申请人
	active_card_user_id = models.IntegerField() #激活卡片人

	class Meta(object):
		db_table = 'market_tool_weizoom_card'
		verbose_name = '微众卡'
		verbose_name_plural = '微众卡'

	# @staticmethod
	# def check_card(weizoom_card_id, password):
	# 	return WeizoomCard.objects.filter(weizoom_card_id=weizoom_card_id, password=password).count() > 0


#########################################################################
# AccountHasWeizoomCardPermissions ：账号对应使用微众卡功能权限
#########################################################################
class AccountHasWeizoomCardPermissions(models.Model):
	owner_id = models.IntegerField(default=0, verbose_name='账号id')
	is_can_use_weizoom_card = models.BooleanField(default=False, verbose_name='是否可以使用微众卡')
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

	class Meta(object):
		db_table = 'market_tool_weizoom_card_account_has_permissions'
		verbose_name = '账号对应使用微众卡功能权限'
		verbose_name_plural = '账号对应使用微众卡功能权限'

	@staticmethod
	def is_can_use_weizoom_card_by_owner_id(owner_id):
		permissions = AccountHasWeizoomCardPermissions.objects.filter(owner_id=owner_id)
		if permissions.count() > 0:
			return permissions[0].is_can_use_weizoom_card
		else:
			return False


#########################################################################
# WeizoomCardUsedAuthKey : 微众卡支付AUTH_KEY
#########################################################################
class WeizoomCardUsedAuthKey(models.Model):
	auth_key = models.TextField(default='')
	weizoom_card_id = models.IntegerField()

	class Meta(object):
		db_table = 'market_tool_weizoom_card_used_auth_key'
		verbose_name = '微众卡支付AUTH_KEY'
		verbose_name_plural = '微众卡支付AUTH_KEY'

	@staticmethod
	def is_can_pay(auth_key, card_id):
		return WeizoomCardUsedAuthKey.objects.filter(auth_key=auth_key, weizoom_card_id=card_id).count() > 0


WEIZOOM_CARD_LOG_TYPE_ACTIVATION = u'激活'
WEIZOOM_CARD_LOG_TYPE_DISABLE = u'停用'
WEIZOOM_CARD_LOG_TYPE_BUY_USE = u'使用'
WEIZOOM_CARD_LOG_TYPE_BUY_RETURN = u'返还'
WEIZOOM_CARD_LOG_TYPE_RETURN_BY_SYSTEM = u'积分兑换'
WEIZOOM_CARD_LOG_TYPE_MANAGER_MODIFY = u'系统管理员修改'
TYPE_OWES = [
	WEIZOOM_CARD_LOG_TYPE_BUY_RETURN
]
TYPE_ZERO = [
	WEIZOOM_CARD_LOG_TYPE_ACTIVATION,
	WEIZOOM_CARD_LOG_TYPE_DISABLE
]
#########################################################################
# WeizoomCardHasOrder : 消费记录 order_id == -1 是积分兑换
#########################################################################
class WeizoomCardHasOrder(models.Model):
	owner_id = models.IntegerField() #商家
	card_id = models.IntegerField() #weizoom card id  
	order_id = models.CharField(max_length=50, default='-1') #订单号  order_id == -1 是积分兑换
	money = models.DecimalField(max_digits=65, decimal_places=2) #金额
	created_at = models.DateTimeField(auto_now_add=True) #添加时间
	event_type = models.CharField(max_length=64, verbose_name='事件类型')
	member_integral_log_id = models.IntegerField(default=0, verbose_name='积分日志id')

	class Meta(object):
		db_table = 'market_tool_weizoom_card_has_order'
		verbose_name = '微众卡支付交易记录'
		verbose_name_plural = '微众卡支付交易记录'

	@property
	def card(self):		
		if hasattr(self, '_card'):
			return self._card

		if self.card_id > 0:
			self._card = WeizoomCard.objects.get(id=self.card_id)
		else:
			self._card = None

		return self._card

	@property
	def owner(self):		
		if hasattr(self, '_owner'):
			return self._owner

		if self.owner_id > 0:
			self._owner = User.objects.get(id=self.owner_id)
		else:
			self._owner = None

		return self._owner

	@property
	def get_money(self):
		return self.money	


#########################################################################
# WeizoomCardHasOrder : 微众卡记录操作日志
#########################################################################
class WeizoomCardOperationLog(models.Model):
	card = models.ForeignKey(WeizoomCard, related_name='market_tool_weizoom_card')
	operater = models.ForeignKey(User, related_name='auth_user')
	operater_name = models.CharField(max_length=64)
	operate_log = models.CharField(max_length=64, verbose_name='事件类型')
	created_at = models.DateTimeField(auto_now_add=True)
	remark = models.CharField(max_length=20) #备注
	activated_to = models.CharField(max_length=20) #申请人
	class Meta(object):
		db_table = 'market_tool_weizoom_card_operation_log'

#########################################################################
# WeizoomCardHasAccount ：微众卡账号管理
#########################################################################
class WeizoomCardHasAccount(models.Model):
	owner = models.ForeignKey(User, related_name='weizoom_card_owner')
	account = models.ForeignKey(User, related_name='owner_has_account', verbose_name='添加账号')
	account_name = models.CharField(max_length=50, default='', db_index=True)
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

	class Meta(object):
		db_table = 'market_tool_weizoom_card_has_account'
		verbose_name = '微众卡商户对应系统账号'
		verbose_name_plural = '微众卡商户对应系统账号'
		unique_together = ['owner', 'account']
		
	@staticmethod
	def get_all_weizoom_card_accounts(user):
		if user is None:
			return []
		return list(WeizoomCardHasAccount.objects.filter(owner=user))

	@staticmethod
	def get_weizoom_card_account_name_by_user(request, user_id):
		try:
			return WeizoomCardHasAccount.objects.get(owner=request.user, account_id=user_id).account_name
		except:
			return None


class WeiZoomCardManager(models.Model):
	user = models.ForeignKey(User)
	username = models.CharField(max_length=100) #
	nickname = models.CharField(max_length=100) #实名

	class Meta(object):
		db_table = 'market_tool_weizoom_card_manager'
		verbose_name = '微众卡管理员'
		verbose_name_plural = '微众卡管理员'


class WeiZoomCardPermission(models.Model):
	user = models.ForeignKey(User)  
	can_create_card = models.BooleanField(default=False)#能否创建卡
	can_export_batch_card = models.BooleanField(default=False)#能否批量导出
	can_add_card = models.BooleanField(default=False)#能否追加卡库
	can_batch_stop_card = models.BooleanField(default=False)#能否批量停用
	can_batch_active_card = models.BooleanField(default=False)#能否批量激活
	can_view_card_details = models.BooleanField(default=False)#能否显示微众卡使用详情
	can_stop_card = models.BooleanField(default=False)#能否停用
	can_active_card = models.BooleanField(default=False)#能否激活
	can_change_shop_config = models.BooleanField(default=False)#能否开启关闭
	can_view_statistical_details = models.BooleanField(default=False)#能否查看数据统计使用详情
	can_export_statistical_details= models.BooleanField(default=False)#能否批量导出统计
	can_delay_card= models.BooleanField(default=False)#能否延期卡

	class Meta(object):
		db_table = 'market_tool_weizoom_card_permission'