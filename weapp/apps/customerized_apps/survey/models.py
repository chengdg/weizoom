# -*- coding: utf-8 -*-

from datetime import datetime

import mongoengine as models

class surveyParticipance(models.Document):
	webapp_user_id= models.LongField(default=0) #参与者id
	member_id= models.LongField(default=0) #参与者id
	belong_to = models.StringField(default="", max_length=100) #对应的活动id
	tel = models.StringField(default="", max_length=100)
	termite_data = models.DynamicField(default="") #termite数据
	prize = models.DynamicField(default="") #活动奖励
	created_at = models.DateTimeField() #创建时间

	meta = {
		'collection': 'survey_survey_participance',
		'db_alias': 'apps'
	}

class surveyParticipanceLog(models.Document):
	"""
	非会员参与调研，记录参与记录，待关注之后加入分组后删除该条记录
	"""
	member_id = models.LongField(default=0) #参与者id
	belong_to = models.StringField(default="", max_length=100) #对应的活动id
	created_at = models.DateTimeField() #创建时间

	meta = {
		'collection': 'survey_survey_participance_log',
		'db_alias': 'apps'
	}

STATUS_NOT_START = 0
STATUS_RUNNING = 1
STATUS_STOPED = 2
class survey(models.Document):
	owner_id = models.LongField() #创建人id
	name = models.StringField(default="", max_length=100) #名称
	start_time = models.DateTimeField() #开始时间
	end_time = models.DateTimeField() #结束时间
	status = models.IntField(default=0) #状态
	participant_count = models.IntField(default=0) #参与者数量
	tag_id = models.IntField(default=0) #添加到分组，默认为不添加
	related_page_id = models.StringField(default="", max_length=100) #termite page的id
	created_at = models.DateTimeField() #创建时间
	
	meta = {
		'collection': 'survey_survey',
		'db_alias': 'apps'
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


	
