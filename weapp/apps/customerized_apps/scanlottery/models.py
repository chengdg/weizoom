# -*- coding: utf-8 -*-

from datetime import datetime

import mongoengine as models

NOT_USED = 0
HAS_USED = 1

class ScanlotteryRecord(models.Document):
	"""
	抽奖记录表
	"""
	member_id= models.LongField(default=0) #参与者id
	belong_to = models.StringField(default="", max_length=100) #对应的抽奖活动id
	scanlottery_name = models.StringField(default="", max_length=100) #对应的抽奖活动title
	prize_type = models.StringField(default="", max_length=16) #奖品类型
	prize_title = models.StringField(default="", max_length=16) #奖项标题
	prize_name = models.StringField(default="", max_length=100) #奖项名称
	prize_data = models.StringField(default="", max_length=100) #奖项数据
	tel = models.StringField(default="", max_length=20) #手机号
	name = models.StringField(default="", max_length=20) #姓名
	status = models.BooleanField(default=False) #是否已领取
	created_at = models.DateTimeField() #创建时间
	code = models.StringField(default="", max_length=20)  # 抽奖二维码

	meta = {
		'collection': 'scanlottery_scanlottery_record',
		'ordering': ['-id'],
		'db_alias': 'apps'
	}

STATUS_NOT_START = 0
STATUS_RUNNING = 1
STATUS_STOPED = 2
class Scanlottery(models.Document):
	owner_id = models.LongField() #创建人id
	name = models.StringField(default="", max_length=100) #名称
	lottery_type = models.StringField(default="roulette", max_length=100) #抽奖类型
	start_time = models.DateTimeField() #开始时间
	end_time = models.DateTimeField() #结束时间
	status = models.IntField(default=0) #状态
	participant_count = models.IntField(default=0) #参与者数量
	winner_count = models.IntField(default=0) #中奖人数
	related_page_id = models.StringField(default="", max_length=100) #termite page的id
	created_at = models.DateTimeField() #创建时间
	chance = models.IntField(default=0) #中奖几率
	prize = models.DynamicField() #每个奖项的奖品数量
	#证书文存放件路径
	cert_pem_path = models.StringField(default="", max_length=256) #证书
	key_pem_path = models.StringField(default="", max_length=256) #证书密钥

	
	meta = {
		'collection': 'scanlottery_scanlottery',
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

class ScanlotteryControl(models.Document):
	belong_to = models.StringField(default="", max_length=100) #对应的抽奖活动id
	member_id= models.LongField(default=0) #参与者id
	date_control = models.StringField(default="", max_length=100)
	can_play_count_control_one = models.StringField(default="", max_length=100, unique_with=['belong_to', 'member_id', 'date_control']) #第一次参与
	can_play_count_control_two = models.StringField(default="", max_length=100, unique_with=['belong_to', 'member_id', 'date_control']) #第二次参与


	meta = {
		'collection': 'scanlottery_scanlottery_control',
		'db_alias': 'apps'
	}