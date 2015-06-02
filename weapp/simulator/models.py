# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


#########################################################################
# SimulatorUser：模拟器用户
#########################################################################
class SimulatorUser(models.Model):
	name = models.CharField(max_length=100, default='')
	display_name = models.CharField(max_length=100, default='')

	class Meta(object):
		db_table = 'simulator_user'
		verbose_name = '模拟器用户'
		verbose_name_plural = '模拟器用户'


#########################################################################
# SimulatorUserRelation：模拟器用户关系
#########################################################################
class SimulatorUserRelation(models.Model):
	follower = models.ForeignKey(SimulatorUser, related_name='followed_relation')
	followed = models.ForeignKey(SimulatorUser, related_name='follower_relation')

	class Meta(object):
		db_table = 'simulator_user_relation'
		verbose_name = '模拟器用户关系'
		verbose_name_plural = '模拟器用户关系'


#########################################################################
# SharedMessage：分享到朋友圈的消息
#########################################################################
class SharedMessage(models.Model):
	owner = models.ForeignKey(SimulatorUser)
	message = models.CharField(max_length=100, default='') #消息内容
	link_title = models.CharField(max_length=100, default='') #链接标题
	link_url = models.CharField(max_length=256, default='') #链接url
	link_img = models.CharField(max_length=256, default='') #链接图片
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'simulator_shared_message'
		verbose_name = '朋友圈消息'
		verbose_name_plural = '朋友圈消息'