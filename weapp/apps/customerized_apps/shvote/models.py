# -*- coding: utf-8 -*-

from datetime import datetime

import mongoengine as models

MEMBER_STATUS = {
	"ASKING": 0,
	"PASSED": 1
}
class ShvoteParticipance(models.Document):
	"""
	参与投票的选手信息记录表
	"""
	member_id= models.LongField(default=0, unique_with=['belong_to']) #参与者id
	belong_to = models.StringField(default="", max_length=100) #对应的活动id
	icon = models.StringField(default="", max_length=2048) #头像url
	name = models.StringField(default="", max_length=100) #名称
	group = models.StringField(default="", max_length=16) #所在分组
	serial_number = models.StringField(default="", max_length=16) #编号
	details = models.StringField(default="", max_length=10000) #详情
	pics = models.ListField() #详情中的图片链接
	count = models.LongField(default=0) #票数
	vote_log = models.DynamicField(default={}) #投票记录 结构为{"2016-04-10": [32,5432,234,123], "2016-04-11": [33,52432,2314,1223], ...}
	created_at = models.DateTimeField() #创建时间
	participate_time = models.DateTimeField() #审核通过时间
	status = models.IntField(default=MEMBER_STATUS['ASKING'])

	meta = {
		'collection': 'shvote_shvote_participance'
	}


STATUS_NOT_START = 0
STATUS_RUNNING = 1
STATUS_STOPED = 2
class Shvote(models.Document):
	owner_id = models.LongField() #创建人id
	name = models.StringField(default="", max_length=100) #名称
	rule = models.StringField(default="", max_length=200) #投票规则
	groups = models.ListField() #分组
	description = models.StringField(default="", max_length=10000) #活动描述
	start_time = models.DateTimeField() #开始时间
	end_time = models.DateTimeField() #结束时间
	status = models.IntField(default=0) #状态
	participant_count = models.IntField(default=0) #参与者数量
	related_page_id = models.StringField(default="", max_length=100) #termite page的id
	created_at = models.DateTimeField() #创建时间
	visits = models.LongField(default=0) #访问人数
	
	meta = {
		'collection': 'shvote_shvote'
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
