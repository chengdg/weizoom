# -*- coding: utf-8 -*-

from datetime import datetime

import mongoengine as models

class ScratchParticipance(models.Document):
	webapp_user_id = models.LongField(default=0) #参与者id
	member_id= models.LongField(default=0) #参与者id
	belong_to = models.StringField(default="", max_length=100) #对应的活动id
	has_prize = models.BooleanField(default=False) #是否中奖
	total_count = models.IntField(default=0) #已参与次数
	can_play_count = models.IntField(default=0) #可参与次数
	scratch_date = models.DateTimeField() #最近一次刮刮卡时间

	meta = {
		'collection': 'scratch_scratch_participance',
		'db_alias': 'apps'
	}

class ScratchRecord(models.Document):
	"""
	刮刮卡记录表
	"""
	webapp_user_id = models.LongField(default=0) #参与者id
	member_id= models.LongField(default=0) #参与者id
	belong_to = models.StringField(default="", max_length=100) #对应的抽奖活动id
	scratch_name = models.StringField(default="", max_length=100) #对应的刮刮卡活动title
	prize_type = models.StringField(default="", max_length=16) #奖品类型
	prize_title = models.StringField(default="", max_length=16) #奖项标题
	prize_name = models.StringField(default="", max_length=100) #奖项名称
	prize_data = models.StringField(default="", max_length=100) #奖项数据
	tel = models.StringField(default="", max_length=20)
	status = models.BooleanField(default=False) #是否已领取
	created_at = models.DateTimeField() #创建时间

	meta = {
		'collection': 'scratch_scratch_record',
		'ordering': ['-id'],
		'db_alias': 'apps'
	}

STATUS_NOT_START = 0
STATUS_RUNNING = 1
STATUS_STOPED = 2
class Scratch(models.Document):
	owner_id = models.LongField() #创建人id
	name = models.StringField(default="", max_length=100) #名称
	scratch_type = models.StringField(default="roulette", max_length=100) #刮刮卡类型
	start_time = models.DateTimeField() #开始时间
	end_time = models.DateTimeField() #结束时间
	status = models.IntField(default=0) #状态
	participant_count = models.IntField(default=0) #参与者数量
	winner_count = models.IntField(default=0) #中奖人数
	related_page_id = models.StringField(default="", max_length=100) #termite page的id
	created_at = models.DateTimeField() #创建时间
	expend = models.IntField(default=0) #消耗积分
	delivery = models.IntField(default=0) #参与送积分
	delivery_setting = models.StringField(default="true", max_length=20) #送积分规则
	limitation = models.StringField(default="once_per_user", max_length=32) #抽奖限制
	chance = models.IntField(default=0) #中奖几率
	allow_repeat = models.StringField(default="true", max_length=10) #是否允许重复中奖
	prize = models.DynamicField() #每个奖项的奖品数量
	#证书文存放件路径
	cert_pem_path = models.StringField(default="", max_length=256) #证书
	key_pem_path = models.StringField(default="", max_length=256) #证书密钥

	
	meta = {
		'collection': 'scratch_scratch',
		'db_alias': 'apps'
	}

	@property
	def scratch_type_cn(self):
		return (u'大转盘', u'刮刮乐', u'红包')[('roulette', 'scratch', 'red').index(self.scratch_type)]

	@property
	def limitation_times(self):
		try:
			return (1, 1, 2, -1)[('once_per_user', 'once_per_day', 'twice_per_day', 'no_limit').index(self.limitation)]
		except:
			return 0

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

class ScratchControl(models.Document):
	belong_to = models.StringField(default="", max_length=100) #对应的刮刮卡活动id
	member_id= models.LongField(default=0) #参与者id
	date_control = models.StringField(default="", max_length=100)
	can_play_count_control_one = models.StringField(default="", max_length=100, unique_with=['belong_to', 'member_id', 'date_control']) #第一次参与
	can_play_count_control_two = models.StringField(default="", max_length=100, unique_with=['belong_to', 'member_id', 'date_control']) #第二次参与


	meta = {
		'collection': 'scratch_scratch_control',
		'db_alias': 'apps'
	}
