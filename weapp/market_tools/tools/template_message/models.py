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

########################################################################
# MarketToolsIndustry: 行业信息
########################################################################
INDUSTR_IT = 0 #IT科技
INDUSTR_CONSUMER_GOODS = 1  #消费品
INDUSTR_AMOUNT = 2   #金融
INDUSTR_RESTAURANT = 3 #餐饮
INDUSTR_TRANSPORT = 4 #运输
INDUSTR_EDUCATION = 5 #教育education
INDUSTR_GOVERNMENT = 6 #government
INDUSTR_MEDICAL = 7 #medical 
INDUSTR_TRAFFIC = 8 #traffic 交通
INDUSTR_ESTATE = 9 #state 房地产
INDUSTR_BUSINESS_SERVICE = 10 #business service 商业服务
INDUSTR_ENTERTAINMENT = 11 #entertainment 文体娱乐
INDUSTR_TRAVEL = 12 #旅游
INDUSTR_PRINTING = 13 #印刷 printing
INDUSTR_OTHER = 14 #其它
TYPE2INDUSTRY = {
	INDUSTR_IT: u'IT科技',
	INDUSTR_CONSUMER_GOODS: u'消费品',
	INDUSTR_AMOUNT: u'金融',
	INDUSTR_RESTAURANT: u'餐饮',
	INDUSTR_TRANSPORT: u'运输',
	INDUSTR_EDUCATION: u'教育',
	INDUSTR_GOVERNMENT: u'政府',
	INDUSTR_MEDICAL: u'医药',
	INDUSTR_TRAFFIC: u'交通',
	INDUSTR_ESTATE: u'房地产',
	INDUSTR_BUSINESS_SERVICE: u'商业服务',
	INDUSTR_ENTERTAINMENT: u'文体娱乐',
	INDUSTR_TRAVEL: u'旅游',
	INDUSTR_PRINTING: u'印刷',
	INDUSTR_OTHER: u'其他'
}
INDUSTRY2TYPE = {
	u'IT科技': INDUSTR_IT,
	u'消费品': INDUSTR_CONSUMER_GOODS,
	u'金融': INDUSTR_AMOUNT,
	u'餐饮': INDUSTR_RESTAURANT,
	u'运输': INDUSTR_TRANSPORT,
	u'教育': INDUSTR_EDUCATION,
	u'政府': INDUSTR_GOVERNMENT,
	u'医药': INDUSTR_MEDICAL,
	u'交通': INDUSTR_TRAFFIC,
	u'房地产': INDUSTR_ESTATE,
	u'商业服务': INDUSTR_BUSINESS_SERVICE,
	u'文体娱乐': INDUSTR_ENTERTAINMENT,
	u'旅游': INDUSTR_TRAVEL,
	u'印刷': INDUSTR_PRINTING,
	u'其他': INDUSTR_OTHER
}
class MarketToolsIndustry(models.Model):
	industry_type = models.IntegerField(default=INDUSTR_IT)
	industry_name = models.TextField() #模版id

	class Meta(object):
		db_table = 'market_tools_industry'
		verbose_name = '行业信息'
		verbose_name_plural = '行业信息'

		
########################################################################
# TemplateMessage: 模版消息  模版消息不同类型的行业模版格式不同 
########################################################################
PAY_ORDER_SUCCESS = 0 		#订单支付成功
PAY_DELIVER_NOTIFY = 1 		#发货通知
COUPON_ARRIVAL_NOTIFY = 2 	#优惠劵到账通知
COUPON_EXPIRED_REMIND = 3 	#优惠劵过期提醒
class MarketToolsTemplateMessage(models.Model):
	industry = models.IntegerField(default=INDUSTR_IT)
	title = models.CharField(max_length=256) #标题
	send_point = models.IntegerField(default=PAY_ORDER_SUCCESS) #发送点
	attribute =models.TextField() #属性1  orderProductPrice:final_price,
	
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = 'market_tools_template_message'
		verbose_name = '模板消息'
		verbose_name_plural = 'template_message'


########################################################################
# MarketToolsTemplateMessageDetail: 模版消息详情
########################################################################
MAJOR_INDUSTRY_TYPE = 0 #主营行业
DEPUTY_INDUSTRY_TYPE = 1 #副营行业
class MarketToolsTemplateMessageDetail(models.Model):
	owner = models.ForeignKey(User)
	template_message = models.ForeignKey(MarketToolsTemplateMessage)
	industry = models.IntegerField(default=INDUSTR_IT)
	template_id = models.TextField() #模版id
	first_text = models.CharField(max_length=1024)
	remark_text = models.CharField(max_length=1024)
	type = models.SmallIntegerField(default=MAJOR_INDUSTRY_TYPE)
	status = models.SmallIntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = 'market_tools_template_message_detail'
		verbose_name = '模板消息详情'
		verbose_name_plural = 'market_tools_template_message_detail'
		ordering = ['-status', 'type']


########################################################################
# MarketToolsTemplateMessageSendDetail: 模版消息发送信息
########################################################################
class MarketToolsTemplateMessageSendRecord(models.Model):
	owner = models.ForeignKey(User)
	template_id = models.TextField() #模版id
	member_id = models.IntegerField(default=0)
	status = models.IntegerField(default=0)
	order_id = models.CharField(max_length=200, default='')
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = 'market_tools_template_message_send_record'
		verbose_name = '模板消息发送记录'
		verbose_name_plural = 'market_tools_template_message_send_record'
	