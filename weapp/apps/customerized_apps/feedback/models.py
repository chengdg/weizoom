# -*- coding: utf-8 -*-

from datetime import datetime

import mongoengine as models

class feedbackParticipance(models.Document):
	webapp_user_id= models.LongField(default=0) #参与者id
	member_id= models.LongField(default=0) #参与者id
	username = models.StringField(default="", max_length=100) #参与者用户名
	feedback_type = models.IntField(default=0) #反馈类型
	termite_data = models.DynamicField(default="") #termite数据
	created_at = models.DateTimeField() #创建时间

	meta = {
		'collection': 'feedback_feedback_participance'
	}
