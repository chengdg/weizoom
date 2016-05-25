# -*- coding: utf-8 -*-

from datetime import datetime

import mongoengine as models

class feedbackParticipance(models.Document):
	webapp_user_id= models.LongField(default=0) #参与者id
	member_id= models.LongField(default=0) #参与者id
	tel = models.StringField(default="", max_length=100)
	termite_data = models.DynamicField(default="") #termite数据
	prize = models.DynamicField(default="") #反馈奖励
	created_at = models.DateTimeField() #创建时间

	meta = {
		'collection': 'feedback_feedback_participance',
		'db_alias': 'apps'
	}
