# -*- coding: utf-8 -*-

from datetime import datetime

import mongoengine as models

STATUS_NOT_START = 0
STATUS_RUNNING = 1
STATUS_STOPED = 2
class Group(models.Document):
	owner_id = models.LongField() #创建人id
	related_page_id = models.StringField(default="", max_length=100) #termite page的id
	name = models.StringField(default="", max_length=100) #名称
	start_time = models.DateTimeField() #开始时间
	end_time = models.DateTimeField() #结束时间
	status = models.IntField(default=0) #状态
	created_at = models.DateTimeField() #创建时间
	product_dict = models.DynamicField() #活动商品
	product_id = models.IntField() #商品id
	group_dict = models.DynamicField() #团购活动字典{'0':{'group_type':'5','group_days':'10','group_price':'100.00'},...}
	rules = models.StringField()#团购说明
	material_image = models.StringField()#分享图片
	share_description = models.StringField()#分享描述
	visit_number = models.IntField(default=0) #浏览人数

	meta = {
		'collection': 'group_group'
	}

	@property
	def status_text(self):
		if self.status == STATUS_NOT_START:
			return u'未开始'
		elif self.status == STATUS_RUNNING:
			now = datetime.today()
			if now >= self.end_time:
				return u'已结束'
			else:
				return u'进行中'
		elif self.status == STATUS_STOPED:
			return u'已结束'
		else:
			return u'未知'

	@property
	def is_finished(self):
		status_text = self.status_text
		if status_text == u'已结束':
			return True
		else:
			return False

class GroupRelations(models.Document):
	"""
	用户自己发起的小团购记录表
	"""
	belong_to = models.StringField(default="", max_length=100) #对应的活动id
	member_id = models.StringField(default="", max_length=20, unique_with=['belong_to']) #团购发起者，团长的id
	product_id = models.IntField() #商品id
	group_type = models.StringField()  #小团购类型
	group_days = models.StringField() #团购时间
	group_price = models.FloatField() #团购价格
	is_valid = models.BooleanField(default=False) #是否开团成功
	group_status = models.BooleanField(default=False) #团购状态
	grouped_number = models.IntField(default=0) #团购人数
	grouped_member_ids = models.ListField() #团员的id List
	success_time = models.DateTimeField() #团购成功时间
	created_at = models.DateTimeField() #创建时间

	meta = {
		'collection': 'group_group_relations'
	}

class GroupDetail(models.Document):
	"""
	团购详情记录表
	"""
	relation_belong_to = models.StringField(default="", max_length=100) #对应的小团购id
	owner_id = models.LongField() #团购发起者id
	grouped_member_id = models.LongField(unique_with=['relation_belong_to']) #团购参与者id
	grouped_member_name = models.StringField(default='', max_length=1024) #团购参与者昵称
	is_already_paid = models.BooleanField(default=False) #是否已经支付成功
	order_id = models.StringField(default="", max_length=100) #对应的订单号
	created_at = models.DateTimeField() #创建时间

	meta = {
		'collection': 'group_group_detail'
	}