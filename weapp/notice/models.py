# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


#########################################################################
# NoticeContent: 通知内容
#########################################################################
# ID_SHOW_NAME = []
# try:
# 	for user in User.objects.all():
# 		ID_SHOW_NAME.append((user.id,user.username))
# except Exception, e:
# 	pass

class Notice(models.Model):
	owner_id = models.IntegerField(db_index=True, unique=False, default=1, verbose_name='用户名')
	title = models.CharField(max_length=256, verbose_name='标题')
	content = models.TextField(default='', verbose_name='内容')
	create_time = models.DateTimeField(verbose_name='创建时间')
	has_read = models.BooleanField(default=False, verbose_name='已读')

	class Meta(object):
		db_table = 'notice'
		verbose_name = u'通知'
		verbose_name_plural = u'通知'


	def __unicode__(self):
		return u"{}-{}".format(self.owner_id, self.title)

	def to_json(self):
		return {
			"id" : self.id,
			"title" : self.title,
			"content" : self.content,
			"create_time" : str(self.create_time),
			"has_read" : self.has_read
		}

	def read(self):
		Notice.objects.filter(id=self.id).update(
			has_read = True
			)

	@staticmethod
	def read_notice(notice_id):
		if (notice_id is None) or (notice_id <= 0):
			return
		
		Notice.objects.filter(id=notice_id).update(
			has_read = True
			)		

	@staticmethod
	def notices_json_array(notices_list):
		if (notices_list is None) or (len(notices_list) == 0):
			return []

		json_array = []
		for notice in notices_list:
			json_array.append(notice.to_json())		
		for j in range(len(json_array)-1,-1,-1):
			for i in range(j):
				if json_array[i]['create_time'] > json_array[i+1]['create_time']:
					json_array[i],json_array[i+1] = json_array[i+1],json_array[i]
					
		return json_array[::-1]

	def show_username(self):
		return User.objects.get(id=self.owner_id).username
	show_username.short_description = '收信人'