# -*- coding: utf-8 -*-

from datetime import datetime

import mongoengine as models

class PowerMeControl(models.Document):
	member_id= models.LongField(default=0) #参与者id
	powered_member_id = models.LongField(default=0) #被助力者id
	belong_to = models.StringField(default="", max_length=100) #对应的活动id
	powerme_control = models.StringField(default="", max_length=100, unique_with=['belong_to', 'member_id', 'powered_member_id'])

	meta = {
		'collection': 'powerme_powerme_control',
		'db_alias': 'apps'
	}

class PowerMeRelations(models.Document):
	belong_to = models.StringField(default="", max_length=100) #对应的活动id
	member_id= models.StringField(default="", max_length=20) #参与者id
	powered_member_id = models.StringField(default="", max_length=20, unique_with=['belong_to', 'member_id']) #被助力者id

	meta = {
		'collection': 'powerme_powerme_relations',
		'db_alias': 'apps'
	}

class PowerMeParticipance(models.Document):
	member_id= models.LongField(default=0) #参与者id
	belong_to = models.StringField(default="", max_length=100) #对应的活动id
	created_at = models.DateTimeField() #创建时间
	has_join = models.BooleanField(default=False) #是否已参与微助力
	power = models.IntField(default=0) #助力值
	powered_member_id = models.DynamicField() #已助力的会员id list

	meta = {
		'collection': 'powerme_powerme_participance',
		'db_alias': 'apps'
	}


STATUS_NOT_START = 0
STATUS_RUNNING = 1
STATUS_STOPED = 2
class PowerMe(models.Document):
	owner_id = models.LongField() #创建人id
	name = models.StringField(default="", max_length=100) #名称
	start_time = models.DateTimeField() #开始时间
	end_time = models.DateTimeField() #结束时间
	status = models.IntField(default=0) #状态
	related_page_id = models.StringField(default="", max_length=100) #termite page的id
	timing = models.BooleanField(default=True) #是否显示倒计时
	reply_content = models.StringField(default="", max_length=50) #参与活动回复语
	material_image = models.StringField(default="", max_length=1024) #分享的图片链接
	qrcode = models.DynamicField() #带参数二维码ticket，name
	created_at = models.DateTimeField() #创建时间
	
	meta = {
		'collection': 'powerme_powerme',
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


class PowerLog(models.Document):
	belong_to = models.StringField(default="", max_length=100) #对应的活动id
	power_member_id = models.LongField() #助力者id
	be_powered_member_id = models.LongField() #被助力者id
	created_at = models.DateTimeField(default=datetime.now()) #创建时间

	meta = {
		'collection': 'powerme_powered_log',
		'db_alias': 'apps'
	}

class PoweredDetail(models.Document):
	"""
	助力详情表
	"""
	belong_to = models.StringField(default="", max_length=100) #对应的活动id
	owner_id = models.LongField()
	power_member_id = models.LongField() #助力者id
	power_member_name = models.StringField(default='', max_length=1024) #助力者昵称
	has_powered = models.BooleanField(default=False) #是否已助力(针对未关注用户)
	created_at = models.DateTimeField() #创建时间

	meta = {
		'collection': 'powerme_powered_detail',
		'db_alias': 'apps'
	}

class PoweredLimitRelation(models.Document):
	"""
	限制的微助力的log
	"""
	belong_to = models.StringField(default="", max_length=100)  #对应的活动id
	member_id = models.LongField()  #助力者的id
	powered_member_id = models.LongField()  #被助力者id
	created_at = models.DateTimeField()  #创建时间

	meta = {
		'collection': 'powerme_powered_limit_relation',
		'db_alias': 'apps'
	}