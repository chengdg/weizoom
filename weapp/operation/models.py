# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


#########################################################################
# CommonProblem:常见问题标题
#########################################################################
class CommonProblemTitle(models.Model):
	problem_title = models.CharField(max_length=50)
	created_at = models.DateTimeField(auto_now_add=True) #添加时间
	display_index = models.IntegerField(default=1)#显示的排序
	class Meta(object):
		db_table = 'operation_problem_title'
		verbose_name = '常见问题标题'
		verbose_name_plural = '常见问题标题'	


#########################################################################
# CommonProblem:常见问题
#########################################################################
class CommonProblem(models.Model):
	problem_title = models.ForeignKey(CommonProblemTitle)#问题标题
	problem = models.CharField(max_length=500)#问题
	answer = models.TextField()#答案
	created_at = models.DateTimeField(auto_now_add=True) #添加时间
	display_index = models.IntegerField(default=1)#显示的排序
	class Meta(object):
		db_table = 'operation_problem'
		verbose_name = '常见问题'
		verbose_name_plural = '常见问题'





#########################################################################
# version_updated ：版本更新
#########################################################################		
class VersionUpdated(models.Model):
	update_time = models.CharField(max_length=100)#更新时间
	update_content = models.TextField()#更新内容
	created_at = models.DateTimeField(auto_now_add=True) #添加时间
	display_index = models.IntegerField(default=1)#显示的排序
	class Meta(object):
		db_table = 'operation_version_updated'
		verbose_name = '版本更新'
		verbose_name_plural = '版本更新'


#########################################################################
# Feedback：反馈意见  
#########################################################################
class Feedback(models.Model):
	user = models.ForeignKey(User)
	webapp_temp = models.CharField(max_length=100)#模版名称
	content = models.TextField()#意见内容
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = 'operation_feedback'
		verbose_name = '反馈意见'
		verbose_name_plural = '反馈意见'

