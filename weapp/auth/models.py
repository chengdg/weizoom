# # -*- coding: utf-8 -*-
# #duhao 20151019全部注释

# import os
# import json
# from hashlib import md5

# from django.db import models
# from django.contrib.auth.models import User


# #########################################################################
# # Permission: 系统权限 
# #########################################################################
# class SystemPermission(models.Model):
# 	parent_id = models.IntegerField(default=0)
# 	name = models.CharField(max_length=50)
# 	code_name = models.CharField(max_length=100)

# 	class Meta(object):
# 		db_table = 'account_permission'
# 		verbose_name = '系统权限'
# 		verbose_name_plural = '系统权限'
# Permission = SystemPermission


# #########################################################################
# # UserHasPermission: <用户, 权限>关系 
# #########################################################################
# class UserHasPermission(models.Model):
# 	owner = models.ForeignKey(User, related_name='owned_user_permission_relations')
# 	permission = models.ForeignKey(SystemPermission)
# 	user = models.ForeignKey(User)
# 	created_at = models.DateTimeField(auto_now_add=True) #添加时间

# 	class Meta(object):
# 		db_table = 'account_user_has_permission'


# #########################################################################
# # Group: 组 
# #########################################################################
# class SystemGroup(models.Model):
# 	owner = models.ForeignKey(User)
# 	name = models.CharField(max_length=50) 
# 	code_name = models.CharField(max_length=100)

# 	class Meta(object):
# 		db_table = 'account_group'
# Group = SystemGroup


# #########################################################################
# # UserHasGroup: <用户, 组>关系 
# #########################################################################
# class UserHasGroup(models.Model):
# 	user = models.ForeignKey(User)
# 	group = models.ForeignKey(SystemGroup)
# 	created_at = models.DateTimeField(auto_now_add=True) #添加时间

# 	class Meta(object):
# 		db_table = 'account_user_has_group'


# #########################################################################
# # GroupHasPermission: <组, 权限>关系 
# #########################################################################
# class GroupHasPermission(models.Model):
# 	owner = models.ForeignKey(User)
# 	group = models.ForeignKey(SystemGroup)
# 	permission = models.ForeignKey(SystemPermission)
# 	created_at = models.DateTimeField(auto_now_add=True) #添加时间

# 	class Meta(object):
# 		db_table = 'account_group_has_permission'


# #########################################################################
# # Department: 部门
# #########################################################################
# class Department(models.Model):
# 	owner = models.ForeignKey(User)
# 	name = models.CharField(max_length=50) 
	
# 	class Meta(object):
# 		db_table = 'account_department'


# #########################################################################
# # DepartmentHasUser: <部门，员工>关系
# #########################################################################
# class DepartmentHasUser(models.Model):
# 	owner = models.ForeignKey(User, related_name='owned_departments')
# 	department = models.ForeignKey(Department) 
# 	user = models.ForeignKey(User)
	
# 	class Meta(object):
# 		db_table = 'account_department_has_user'

