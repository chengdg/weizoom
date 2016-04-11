# -*- coding: utf-8 -*-
# Create your models here.
from django.db import models
from django.contrib.auth.models import User

#########################################################################
# WeizoomCardRule ：微众卡规则
#########################################################################
#微众卡类型(实体卡、电子卡、条件卡、专属卡)
WEIZOOM_CARD_ENTITY = 0  #实体卡
WEIZOOM_CARD_ELECTRONIC = 1  #电子卡
WEIZOOM_CARD_CONDITION = 2  #条件卡
WEIZOOM_CARD_SPECIAL = 3  #专属卡
WEIZOOM_CARD_KIND2TEXT = {
	WEIZOOM_CARD_ENTITY: u'实体卡',
	WEIZOOM_CARD_ELECTRONIC: u'电子卡',
	WEIZOOM_CARD_CONDITION: u'条件卡',
	WEIZOOM_CARD_SPECIAL: u'专属卡'
}

#微众卡种类(通用卡、限制卡)
WEIZOOM_CARD_ORDINARY = 0  #通用卡
WEIZOOM_CARD_LIMIT = 1  #限制卡
WEIZOOM_CARD_CLASS2TEXT = {
	WEIZOOM_CARD_ORDINARY: u'通用卡',
	WEIZOOM_CARD_LIMIT: u'限制卡'
}

class WeizoomCardRule(models.Model):
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=20, null=True)  #名称
	weizoom_card_id_prefix = models.CharField(max_length=3)  #卡号前缀，不重复
	money = models.DecimalField(max_digits=65, decimal_places=2)  #微众卡面值
	count = models.IntegerField(default=0)  #发放总数量
	remark = models.CharField(max_length=20)  #备注
	valid_time_from = models.DateTimeField(null=True)  #有效范围开始时间
	valid_time_to = models.DateTimeField(null=True)  #有效范围结束时间(即过期时间)
	created_at = models.DateTimeField(auto_now_add=True)  #添加时间
	card_kind = models.IntegerField(default=0)  #微众卡类型
	card_class = models.IntegerField(default=0)  #微众卡的种类
	shop_limit_list = models.CharField(max_length=2048, default='-1')  #专属商家
	shop_black_list = models.CharField(max_length=2048, default='-1')  #不能使用微众卡的商家
	is_new_member_special = models.BooleanField(default=False)  #是否为新会员专属卡
	valid_restrictions = models.DecimalField(max_digits=65, decimal_places=2, default=-1) #订单满多少可以使用规则

	class Meta(object):
		db_table = 'weizoom_card_rule'
		verbose_name = '微众卡规则'
		verbose_name_plural = '微众卡规则'


#########################################################################
# WeizoomCard ：微众卡
#########################################################################
#微众卡使用状态
WEIZOOM_CARD_USE_STATUS_UNUSED = 0 #未使用
WEIZOOM_CARD_USE_STATUS_USED = 1 #使用中
WEIZOOM_CARD_USE_STATUS_EMPTY = 2 #已用完
WEIZOOM_CARD_USE_STATUS2TEXT = {
	WEIZOOM_CARD_USE_STATUS_UNUSED: u'未使用',
	WEIZOOM_CARD_USE_STATUS_USED: u'使用中',
	WEIZOOM_CARD_USE_STATUS_EMPTY: u'已用完'
}
#微众卡操作状态
WEIZOOM_CARD_OPERATE_STATUS_INACTIVE = 0 #未激活
WEIZOOM_CARD_OPERATE_STATUS_ACTIVED = 1 #已激活
WEIZOOM_CARD_OPERATE_STATUS_EDACTIVED = 2 #已停用
WEIZOOM_CARD_OPERATE_STATUS2TEXT = {
	WEIZOOM_CARD_OPERATE_STATUS_INACTIVE: u'未激活',
	WEIZOOM_CARD_OPERATE_STATUS_ACTIVED: u'已激活',
	WEIZOOM_CARD_OPERATE_STATUS_EDACTIVED: u'已停用'
}
#微众卡出库状态
WEIZOOM_CARD_STORAGE_STATUS_IN = 0 #待出库
WEIZOOM_CARD_STORAGE_STATUS_OUT = 1 #已出库
WEIZOOM_CARD_STORAGE_STATUS2TEXT = {
	WEIZOOM_CARD_STORAGE_STATUS_IN: u'待出库',
	WEIZOOM_CARD_STORAGE_STATUS_OUT: u'已出库',
}


class WeizoomCard(models.Model):
	owner = models.ForeignKey(User)
	weizoom_card_rule = models.ForeignKey(WeizoomCardRule)
	use_status = models.IntegerField(default=0) #微众卡使用的状态
	operate_status = models.IntegerField(default=0) #微众卡操作的状态
	storage_status = models.IntegerField(default=0) #微众卡出库的状态
	weizoom_card_id = models.CharField(max_length=50) #微众卡号
	money = models.DecimalField(max_digits=65, decimal_places=2) #剩余金额
	password = models.CharField(max_length=50) #微众卡密码
	expired_time = models.DateTimeField(null=True) #过期时间
	is_expired = models.BooleanField(default=False) #是否过期
	activated_at = models.DateTimeField(null=True) #激活时间
	created_at = models.DateTimeField(auto_now_add=True) #添加时间
	remark = models.CharField(max_length=20,db_index=True) #备注
	activated_to = models.CharField(max_length=20, default="") #申请人
	department = models.CharField(max_length=20,default="") #申请部门
	active_card_user_id = models.IntegerField(default=0) #激活卡片人（最后操作人）
	weizoom_card_order_item_id = models.IntegerField(max_length=64, null=True) #所属订单的条目 id
	weizoom_card_order_id = models.CharField(max_length=64, null=True)  #对应发售订单号
	storage_time = models.DateTimeField(null=True)  #出库时间


	class Meta(object):
		db_table = 'weizoom_card'
		verbose_name = '微众卡'
		verbose_name_plural = '微众卡'


#########################################################################
# WeizommCardOrder: 卡订单
#########################################################################
#订单属性
WEIZOOM_CARD_ORDER_ATTRIBUTE_SALE = 0  #发售卡
WEIZOOM_CARD_ORDER_ATTRIBUTE_INTERNAL = 1  #内部领用卡
WEIZOOM_CARD_ORDER_ATTRIBUTE_REBATE = 2  #返点卡
WEIZOOM_CARD_ORDER_ATTRIBUTE2TEXT = {
	WEIZOOM_CARD_ORDER_ATTRIBUTE_SALE: u'发售卡',
	WEIZOOM_CARD_ORDER_ATTRIBUTE_INTERNAL: u'内部领用卡',
	WEIZOOM_CARD_ORDER_ATTRIBUTE_REBATE: u'返点卡'
}
#折扣方式
WEIZOOM_CARD_ORDER_DISCOUNT_RELIEF = 0  #减免支付
WEIZOOM_CARD_ORDER_DISCOUNT_REBATE = 1  #折扣返点卡
WEIZOOM_CARD_ORDER_DISCOUNT2TEXT = {
	WEIZOOM_CARD_ORDER_DISCOUNT_RELIEF: u'减免支付',
	WEIZOOM_CARD_ORDER_DISCOUNT_REBATE: u'返点卡'
}
class WeizoomCardOrder(models.Model):
	owner = models.ForeignKey(User)
	order_number = models.CharField(max_length=64)  #订单编号
	order_attribute = models.IntegerField(default=0) #订单属性
	company = models.CharField(max_length=64,null=True)  #客户企业信息
	responsible_person = models.CharField(max_length=64,null=True)  #客户经办人信息
	contact = models.CharField(max_length=64,null=True)  #客户联系方式
	sale_name = models.CharField(max_length=32,null=True)  #销售员姓名
	sale_departent = models.CharField(max_length=32,null=True)  #销售部门
	discount_way = models.IntegerField(default=0) #折扣方式
	discount_money = models.DecimalField(max_digits=65, decimal_places=2, default=0) #减免金额
	is_invoice = models.IntegerField(default=0) #是否需要发票
	invoice_title = models.CharField(max_length=64,null=True)  #发票抬头
	invoice_content = models.CharField(max_length=64,null=True)  #发票内容
	attachments = models.CharField(max_length=200,null=True)  #上传附件
	remark = models.CharField(max_length=300,null=True)  #备注
	use_departent = models.CharField(max_length=64,null=True)  #领用部门
	project_name = models.CharField(max_length=64,null=True)  #项目名称
	appliaction = models.CharField(max_length=64,null=True)  #用途
	use_persion = models.CharField(max_length=64,null=True)  #领用人
	weizoom_card_order_number = models.CharField(max_length=64, null=True) #返点卡对应发售订单号
	created_at = models.DateTimeField(auto_now_add=True) #添加时间
	status = models.IntegerField(default=0) #订单状态

	class Meta(object):
		db_table = 'weizoom_card_order'
		verbose_name = '卡订单'
		verbose_name_plural = '卡订单'


#########################################################################
# WeizoomCardOrderItem: 卡订单中的条目信息（卡订单对应卡规则）
#########################################################################
class WeizoomCardOrderItem(models.Model):
	weizoom_card_order = models.ForeignKey(WeizoomCardOrder)  #对应发售订单号
	weizoom_card_order_item_num = models.IntegerField(default=0) #每个条目包含卡的数量(出库数量)
	weizoom_card_rule_id = models.IntegerField(default=0) #对应的卡的规则的id
	valid_time_from = models.DateTimeField(blank=True) #有效范围开始时间
	valid_time_to = models.DateTimeField(blank=True) #有效范围结束时间
	created_at = models.DateTimeField(auto_now_add=True) #添加时间
	

	class Meta(object):
		db_table = 'weizoom_card_order_item'
		verbose_name = '卡订单中的条目信息'
		verbose_name_plural = '卡订单中的条目信息'