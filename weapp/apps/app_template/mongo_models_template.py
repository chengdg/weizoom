# -*- coding: utf-8 -*-
__STRIPPER_TAG__
from datetime import datetime

__STRIPPER_TAG__
import mongoengine as models
__STRIPPER_TAG__
{% for resource in resources %}
{% if resource.need_user_participant %}
class {{resource.class_name}}Participance(models.Document):
	webapp_user_id= models.LongField(default=0) #参与者id
	member_id= models.LongField(default=0) #参与者id
	belong_to = models.StringField(default="", max_length=100) #对应的活动id
	tel = models.StringField(default="", max_length=100)
	termite_data = models.DynamicField(default="") #termite数据
	prize = models.DynamicField(default="") #活动奖励
	created_at = models.DateTimeField() #创建时间
__STRIPPER_TAG__
	meta = {
		'collection': '{{app_name}}_{{resource.lower_name}}_participance'
	}
__STRIPPER_TAG__
__STRIPPER_TAG__
{% endif %}

{% if resource.is_need_model %}
STATUS_NOT_START = 0
STATUS_RUNNING = 1
STATUS_STOPED = 2
class {{resource.class_name}}(models.Document):
	owner_id = models.LongField() #创建人id
	name = models.StringField(default="", max_length=100) #名称
	start_time = models.DateTimeField() #开始时间
	end_time = models.DateTimeField() #结束时间
	status = models.IntField(default=0) #状态
	participant_count = models.IntField(default=0) #参与者数量
	related_page_id = models.StringField(default="", max_length=100) #termite page的id
	created_at = models.DateTimeField() #创建时间
	
	__STRIPPER_TAG__
	meta = {
		'collection': '{{app_name}}_{{resource.lower_name}}'
	}
	
	__STRIPPER_TAG__
	@property
	def status_text(self):
		if self.status == STATUS_NOT_START:
			return u'未开启'
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

	__STRIPPER_TAG__
	@property
	def is_finished(self):
		status_text = self.status_text
		if status_text == u'已结束':
			return True
		else:
			return False


__STRIPPER_TAG__
__STRIPPER_TAG__
{% endif %}

{% endfor %}
	