# -*- coding: utf-8 -*-

from datetime import datetime

import mongoengine as models

class SignParticipance(models.Document):
	webapp_user_id= models.LongField(default=0) #参与者id
	member_id= models.LongField(default=0) #参与者id
	belong_to = models.StringField(default="", max_length=100) #对应的活动id
	tel = models.StringField(default="", max_length=100)
	termite_data = models.DynamicField(default="") #termite数据
	prize = models.DynamicField(default="") #活动奖励
	created_at = models.DateTimeField() #创建时间&第一次签到时间
	total_count = models.IntField(default=0) #总签到天数
	serial_count = models.IntField(default=0) #连续签到天数
	top_serial_count = models.IntField(default=0) #最高连续签到天数

	meta = {
		'collection': 'sign_sign_participance'
	}


STATUS_NOT_START = 0
STATUS_RUNNING = 1
STATUS_STOPED = 2
class Sign(models.Document):
	owner_id = models.LongField() #创建人id
	name = models.StringField(default="", max_length=100) #名称
	# start_time = models.DateTimeField() #开始时间
	# end_time = models.DateTimeField() #结束时间
	share = models.DynamicField(default="") #分享设置
	reply = models.DynamicField(default="") #自动回复设置
	signment = models.DynamicField(default="") #签到设置
	status = models.IntField(default=0) #状态
	participant_count = models.IntField(default=0) #参与者数量
	related_page_id = models.StringField(default="", max_length=100) #termite page的id
	created_at = models.DateTimeField() #创建时间
	
	meta = {
		'collection': 'sign_sign'
	}
	
	@property
	def status_text(self):
		return (u'未开始', u'进行中', u'已结束')[int(self.status)]

	@property
	def is_finished(self):
		status_text = self.status_text
		if status_text == u'已结束':
			return True
		else:
			return False


	
