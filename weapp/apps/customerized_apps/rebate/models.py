# -*- coding: utf-8 -*-

from datetime import datetime

import mongoengine as models

STATUS_NOT_START = 0
STATUS_RUNNING = 1
STATUS_STOPED = 2
class Rebate(models.Document):
	owner_id = models.LongField() #创建人id
	name = models.StringField(default="", max_length=100) #名称
	start_time = models.DateTimeField() #开始时间
	end_time = models.DateTimeField() #结束时间
	status = models.IntField(default=0) #状态
	permission = models.BooleanField() #已关注会员可参与
	is_limit_first_buy = models.BooleanField() #订单返利条件是否限制首单
	is_limit_cash = models.BooleanField() #订单金额是否为现金
	rebate_order_price = models.FloatField() #订单返利需满多少元
	rebate_money = models.FloatField() #返利返多少元
	weizoom_card_ids = models.ListField() #发放微众卡卡号
	# weizoom_card_id_from = models.StringField() #发放微众卡号段
	# weizoom_card_id_to = models.StringField() #发放微众卡号段
	reply_type = models.IntField() #扫码后回复：1/文字，2/图文消息
	reply_detail = models.DynamicField() #扫码后回复文字
	reply_material_id = models.StringField() #扫码后回复图文id
	ticket_id = models.IntField() #唯一的字段，用于创建ticket时使用
	ticket = models.StringField(default="", max_length=256)
	is_deleted = models.BooleanField(default=False) #是否被删除
	created_at = models.DateTimeField() #创建时间
	
	meta = {
		'collection': 'rebate_rebate'
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

class RebateParticipance(models.Document):
	member_id= models.LongField(default=0) #参与者id
	belong_to = models.StringField(default="", max_length=100) #对应的活动id
	created_at = models.DateTimeField() #扫码时间
	is_new = models.BooleanField(default=True) #扫码之前没有关注过则为True

	meta = {
		'collection': 'rebate_rebate_participance'
	}

class RebateWaitingAction(models.Document):
	"""
	存储暂未满足发放微众卡条件的记录
	"""
	webapp_id = models.StringField(default="", max_length=100)
	record_id = models.StringField(default="", max_length=100) #对应的活动id
	member_id = models.LongField(default=0)

	meta = {
		'collection': 'rebate_waiting_action'
	}

class RebateWeizoomCardDetails(models.Document):
	"""
	发放返利微众卡的详情记录
	"""
	record_id = models.StringField(default="", max_length=100) #对应的活动id
	order_id = models.StringField(default="", max_length=100) #对应返利订单的order_id,注意，不是order.id ！！
	member_id = models.LongField(default=0)	#返利的会员
	weizoom_card_id = models.LongField(default=0) #返利的微众卡id
	created_at = models.DateTimeField() #发放时间

	meta = {
		'collection': 'rebate_weizoom_card_details'
	}