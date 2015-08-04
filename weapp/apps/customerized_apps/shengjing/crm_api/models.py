# -*- coding: utf-8 -*-
__author__ = 'lzx, taol'

import datetime

from django.db import models
from django.db.models import Q
import json

from core.exceptionutil import unicode_full_stack
from watchdog.utils import watchdog_alert, watchdog_fatal

from crm_settings import *

#===============================================================================
# CRMContact: 联系人
#===============================================================================
class CRMContact(models.Model):
	contact_id = models.IntegerField(primary_key=True)	
	contact_name = models.CharField(max_length=128)	# 学员名字
	mobile = models.CharField(max_length=40)	# 手机号码
	cnct_char03 = models.CharField(max_length=64)	# 手机号码2
	cnct_int01 = models.IntegerField(default=0)	# 1001 决策者；角色 if 联系人表 手机and手机2 isnull then 客户表 【手机】字段， if 一致，判定为决策人
	account_id = models.IntegerField(default=0)	# CRMAccount

	class Meta(object):
		managed = False
		db_table = 'tc_contact'


#===============================================================================
# CRMAccount: 客户
#===============================================================================
class CRMAccount(models.Model):
	account_id = models.IntegerField(primary_key=True)	
	acct_int02 = models.IntegerField(default=0)	# 客户池 客户池=已购池 判定为学员 否则非学员
	acct_char01 = models.CharField(max_length=64)	#决策人姓名
	account_name = models.CharField(max_length=128)	# 公司名
	account_mobile_phone = models.CharField(max_length=32)
	#account_phone = models.CharField(max_length=40)
	account_email = models.CharField(max_length=120)

	class Meta(object):
		managed = False
		db_table = 'tc_account'

	###########################################################
	# 根据电话号码和公司判断是否存在账号
	###########################################################
	@staticmethod
	def has_account(phone_number, company):
		if CRMAccount.objects.using(SHENGJINGD_DB).filter(account_mobile_phone=phone_number, account_name=company).count() > 0:
			return True
		return False

#===============================================================================
# CRMAccountAttr: 客户附属表
#===============================================================================
class CRMAccountAttr(models.Model):
	account_id = models.IntegerField(primary_key=True)	
	acct_char14 = models.CharField(max_length=64)	# 客户手机号

	class Meta(object):
		managed = False
		db_table = 'tc_account_attr'

OFFICIAL_CONTRACT = 2014	#正式订单

TIME_CARD = 1002	#时间卡
PERSON_CARD = 1001	#人次卡

#订单状态
USING = 0	#正在使用
USED = 1 	#已经使用
ALL_STATUS = 2 	#所有的

#发票信息
UNKNOW_BILL = -1 	#未知 
NO_BILL = 0	#没有发票信息
PENDING_BILL = 1 	#未开
SEND_BILL = 2	#已开已快递
SELF_BILL = 3 	#已开自带
#===============================================================================
# CRMContract: 订单
#===============================================================================
class CRMContract(models.Model):
	contract_id = models.IntegerField(primary_key=True)	# 订单ID
	contract_name = models.CharField(max_length=128)	# 主题
	contract_type = models.IntegerField(default=0)	# 订单类型，只有正式订单才显示
	account_id = models.IntegerField(default=0)	# 账号id
	cntrt_int02 = models.IntegerField(default=0)	# 是否为时间卡， 是=时间卡，否=人次卡
	contract_start_date = models.DateField(auto_now_add=True)	# 订单日期
	cntrt_date01 = models.DateField(auto_now_add=True)	# 订单终止日期
	cntrt_dec08 = models.IntegerField(default=0)	# 总人次(人次卡)
	cntrt_dec03 = models.IntegerField(default=0)	# 已上课人次
	cntrt_dec09 = models.IntegerField(default=0)	# 剩余人次
	cntrt_dec07 = models.CharField(max_length=50)	# 折后金额
	prod_invced_amount = models.IntegerField(default=0)	# 已开票金额
	close_flag = models.IntegerField(default=0)	# 改单终止的原订单
	is_deleted = models.IntegerField(default=0)	# 状态: 0可用
	# close_date = #	关闭时间


	class Meta(object):
		managed = False
		db_table = 'tc_contract'

	###########################################################
	# 判断是否存在正式订单
	###########################################################
	@staticmethod
	def exist_office_order(account_id):
		if CRMContract.objects.using(SHENGJINGD_DB).filter(account_id=account_id, contract_type=OFFICIAL_CONTRACT, close_flag=0, is_deleted=0).count() > 0:
			return True
		return False

	###########################################################
	# 获取订单状态:
	# 正在使用=【剩余人次】>0 and【订单终止日期】>当前日期
	# 否则: 已使用
	###########################################################
	def get_order_status(self):
		try:
			now_date = datetime.datetime.now().strftime('%Y-%m-%d')
			terminat_date = self.cntrt_date01.strftime('%Y-%m-%d')	# 终止日期
			if self.cntrt_int02 == TIME_CARD:
				if terminat_date > now_date:	# 时间卡，只要未到期，状态就是《已使用》
					return USING
				else:
					return USED
			elif self.cntrt_dec09 > 0 and terminat_date > now_date:	# 如果剩余人次大于0，并且终止日期大于现在
				return USING
			else:
				return USED
		except:
			if self.cntrt_dec09 > 0:
				return USING
			else:
				return USED

	###########################################################
	# 填充订单信息
	###########################################################
	def fill_order(self):
		is_time_card = False
		card = {}

		#基本信息
		if self.cntrt_int02 == TIME_CARD:
			is_time_card = True

		terminat_date = ''
		try:
			terminat_date = self.cntrt_date01.strftime('%Y-%m-%d')
		except:
			pass

		order_time = ''
		try:
			order_time = self.contract_start_date.strftime('%Y-%m-%d')
		except:
			pass

		card['order_id'] = self.contract_id
		card['order_time'] = order_time
		card['valid_time'] = terminat_date
		card['study_times'] = int(self.cntrt_dec03)
		card['person_times'] = int(self.cntrt_dec08)
		card['surplus_times'] = int(self.cntrt_dec09)
		card['is_time_card'] = is_time_card
		card['status'] = self.get_order_status()
		card['contract_name'] = self.get_product_name()

		#已签到课程信息
		course_info = {}		
		try:
			course_info = self.get_course_info()
			card['course_info'] = course_info
		except:
			alert_message = u'根据订单：{} 获取已签到课程信息时失败.\n couse: {}'.format(self.contract_id, unicode_full_stack())
			watchdog_alert(alert_message)

		#获取发票信息
		bill_status = UNKNOW_BILL
		bill_info = u'未知'
		try:
			bill_status, bill_info, bill_company = self.get_bill_info()
		except:
			alert_message = u'根据订单：{} 获取发票信息时失败.\n couse: {}'.format(self.contract_id, unicode_full_stack())
			watchdog_alert(alert_message)
		card['bill_status'] = bill_status
		card['bill_info'] = bill_info
		card['bill_company'] = bill_company

		return is_time_card, card

	###########################################################
	# 获取课程信息， 一个订单会关联多个教学计划
	###########################################################
	def get_course_info(self):
		course_infos = []
		if CRMSgnin.exist_sign_info(self.contract_id):
			signs = CRMSgnin.objects.using(SHENGJINGD_DB).filter(yckb_int03=SIGN, ref_3=self.contract_id)
			# 根据教学计划不同获取不同的签到人集合yckb_refid02
			jiaoxplan2contact = {}
			for sign in signs:
				contact = CRMContact.objects.using(SHENGJINGD_DB).get(contact_id=sign.yckb_refid01)
				if sign.yckb_refid02 in jiaoxplan2contact:
					jiaoxplan2contact[sign.yckb_refid02].append(contact.contact_name)
				else:
					jiaoxplan2contact[sign.yckb_refid02] = [contact.contact_name]
			
			for jiaoxplan_id in jiaoxplan2contact:
				course_info = {}
				teach_plan = CRMTeachplan.objects.using(SHENGJINGD_DB).get(jiaoxplan_id=jiaoxplan_id)
				course_info['name'] = teach_plan.jiaoxplan_name
				study_time = ''
				try:
					study_time = teach_plan.jiaoxplan_date01.strftime('%Y-%m-%d')
				except:
					pass
				course_info['study_time'] = study_time
				course_info['students'] = jiaoxplan2contact[jiaoxplan_id]
				course_infos.append(course_info)
		return course_infos

	###################################################
	# 获取发票信息
	# NO_BILL: 折后金额 = 0
	# PENDING_BILL: 已开票金额 = 0
	# SEND_BILL: 快递单号不为空
	# SELF_BILL: 财务审核状态 = 审核通过 and 快递单号=空
	###################################################
	def get_bill_info(self):
		bill_status = NO_BILL
		bill_info = ''
		zhje = 0
		try:
			zhje = int(self.cntrt_dec07)	#折后金额
		except:
			pass
		if zhje <= 0:
			bill_status = NO_BILL
			bill_info = u'赠品无发票'
			return bill_status, bill_info, ''

		if self.prod_invced_amount == 0:
			bill_status = PENDING_BILL
			bill_info = u'未开'
			return bill_status, bill_info, ''

		bill_status, bill_info, bill_company = CRMInvoiceDetail.get_invoice_info(self.contract_id)
		return bill_status, bill_info, bill_company

	###########################################################
	# 获取产品名称
	###########################################################
	def get_product_name(self):
		contract_detail = CRMContractDetail.objects.using(SHENGJINGD_DB).get(contract_id=self.contract_id)
		product = CRMProduct.objects.using(SHENGJINGD_DB).get(prod_id=contract_detail.prod_id)
		return product.get_pro_name()

#===============================================================================
# CRMContractDetail: 订单明细
#===============================================================================
class CRMContractDetail(models.Model):
	contract_id = models.IntegerField(primary_key=True)	# 订单ID
	prod_id = models.IntegerField(primary_key=True)	# 产品ID

	class Meta(object):
		managed = False
		db_table = 'tc_contract_d'

#===============================================================================
# CRMBasicProduct: 基础产品
#===============================================================================
class CRMBasicProduct(models.Model):
	basicpdu_id = models.IntegerField(primary_key=True)	# ID
	basicpdu_name = models.CharField(max_length=128)	# 课程基础项

	class Meta(object):
		managed = False
		db_table = 'tcu_basicpdu'

#===============================================================================
# CRMProduct: 产品
#===============================================================================
class CRMProduct(models.Model):
	prod_id = models.IntegerField(primary_key=True)	# 产品ID
	prod_name = models.CharField(max_length=128)	# 产品名称-版本号
	prod_refid01 = models.IntegerField(default=0) # 产品基础项 ID

	class Meta(object):
		managed = False
		db_table = 'tc_product'

	def get_pro_name(self):
		try:
			basic_prod = CRMBasicProduct.objects.using(SHENGJINGD_DB).get(basicpdu_id=self.prod_refid01)
			return basic_prod.basicpdu_name
		except:
			return ''


NO_SIGN = 1001
SIGN = 1002
#===============================================================================
# CRMSgnin: 学员签到表
#===============================================================================
class CRMSgnin(models.Model):
	yckb_id = models.IntegerField(primary_key=True)
	ref_3 = models.IntegerField(default=0) 	# 订单ID
	yckb_int03 = models.IntegerField(default=0)	# 是否签到
	yckb_refid02 = models.IntegerField(default=0)	# 教学计划ID
	yckb_refid01 = models.IntegerField(default=0)	# 学员ID

	class Meta(object):
		managed = False
		db_table = 'tcu_yckb'

	###################################
	# exist_sgnin_info: 根据订单号判断是否存在学员签到信息
	###################################
	@staticmethod
	def exist_sign_info(order_id):
		if CRMSgnin.objects.using(SHENGJINGD_DB).filter(yckb_int03=SIGN, ref_3=order_id).count() > 0:
			return True
		else:
			return False

#===============================================================================
# CRMLearnplanSgnin: 学习计划学员签到表
#===============================================================================
class CRMLearnplanSgnin(models.Model):
	ref_1 = models.IntegerField(primary_key=True)	#	学习计划ID
	yckb_id = models.IntegerField(default=0)	#	学员签到表ID
	

	class Meta(object):
		managed = False
		db_table = 'tcu_yckb_1_1'

FORMAL_LEARNING_PLAN=2151
HAVING_JOINED=1001
#===============================================================================
# CRMLearnplan: 学习计划
#===============================================================================
class CRMLearnplan(models.Model):
	learnplan_id = models.IntegerField(primary_key=True)
	# learnplan_name 测试库里没有
	# learnplan_name = models.CharField(max_length=128)	# 主题
	learnplan_refid02 = models.IntegerField(default=0)	# 教学计划 ID
	account_id = models.IntegerField(default=0)	# account_id 学员 ID
	learnplan_dec01 = models.IntegerField(default=0)	# plan_count 计划人数
	learnplan_dec04 = models.IntegerField(default=0)	# 签到人数
	learnplan_dec08 = models.IntegerField(default=0) # 学习计划ID
	learnplan_type = models.IntegerField(default=0)	# 学习计划类型
	learnplan_int07 = models.IntegerField(default=0)	# 参课判定

	class Meta(object):
		managed = False
		db_table = 'tcu_learnplan'

#===============================================================================
# CRMTeachplan: 教学计划
#===============================================================================
class CRMTeachplan(models.Model):
	jiaoxplan_id = models.IntegerField(primary_key=True)	# 教学计划 ID
	jiaoxplan_name = models.CharField(max_length=128)	# 名称
	jiaoxplan_date01 = models.DateField(auto_now_add=True)	# start_date 开始日期
	jiaoxplan_date02 = models.DateField(auto_now_add=True)	# end_date 结束日期
	# 课程状态 未开课=学习计划：结束日期>today &【参课判定】=参加；已开课=学习计划：结束日期<today &【已签到人数】>0

	class Meta(object):
		managed = False
		db_table = 'tcu_jiaoxplan'

	@staticmethod
	def exist_teach_plan(jiaoxplan_id):
		if CRMTeachplan.objects.using(SHENGJINGD_DB).filter(jiaoxplan_id=jiaoxplan_id).count() > 0:
			return True
		return False

PSEUDO_C2BILL_C = {
	'sf':'shunfeng',
	'ems': 'ems',
	'yt': 'yuantong',
	'st': 'shentong',
	'tt': 'tiantian',
	'zgyz': 'zhongguoyouzheng',
	'yd': 'yunda',
	'ht': 'huitong',
	'qf': 'quanfeng',
	'db': 'debang',
	'zjs': 'zhaijisong'
}
FINANCE_APPROVED = 1001	#财务审核通过 
#===============================================================================
# CRMInvoiceDetail: 发票明细
#===============================================================================
class CRMInvoiceDetail(models.Model):
	invc_d_id = models.IntegerField(primary_key=True)
	contract_id = models.IntegerField(default=0)	# 订单ID
	invc_id = models.IntegerField(default=0)	# 发票ID

	class Meta(object):
		managed = False
		db_table = 'tc_invoice_d'

	##############################################
	# 根据订单 获取发票信息
	##############################################
	@staticmethod
	def get_invoice_info(contract_id):
		invoice_details = CRMInvoiceDetail.objects.using(SHENGJINGD_DB).filter(contract_id=contract_id)
		if invoice_details.count > 0:
			invoice_detail = invoice_details[0]
			invoice = CRMInvoice.objects.using(SHENGJINGD_DB).get(invc_id=invoice_detail.invc_id)
			if invoice.invc_int04 == FINANCE_APPROVED:
				if invoice.invc_char01 == '':
					
					return SELF_BILL, u'已开自带', ''
				try:
					bill_info = invoice.invc_char01.lower()
					bill_company = ''
					pseudo_code = ''
					for key in PSEUDO_C2BILL_C.keys():
						if bill_info.startswith(key):
							pseudo_code = key
							bill_company = PSEUDO_C2BILL_C[key]
							break;
					infos = bill_info.split(pseudo_code)
					return SEND_BILL, infos[1], bill_company
				except:
					return SEND_BILL, '', ''
		return PENDING_BILL, u'未开', ''

#===============================================================================
# CRMInvoice: 发票
#===============================================================================
class CRMInvoice(models.Model):
	invc_id = models.IntegerField(primary_key=True)	# 发票ID
	invc_int04 = models.IntegerField(default=0)	# 财务审核状态
	invc_char01 = models.CharField(max_length=64)	# 快递单号

	class Meta(object):
		managed = False
		db_table = 'tc_invoice'

