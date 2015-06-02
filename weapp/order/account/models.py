# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.hashers import *
from django.contrib.auth.models import User
from account.models import UserProfile

#===============================================================================
# OperationUser ： 用户
#===============================================================================
USER_STATUS_NORMAL = 0
USER_STATUS_BUSY = 1
USER_STATUS_DISABLED = 2
USER_STATUSES = (
(USER_STATUS_NORMAL, '正常'),
(USER_STATUS_BUSY, '忙碌'),
(USER_STATUS_DISABLED, '停用')
	)
class FreightUser(models.Model):
	owner = models.ForeignKey(User) #微站拥有者id
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=128)
	status = models.IntegerField(default=USER_STATUS_NORMAL, choices=USER_STATUSES)

	class Meta(object):
		db_table = 'freight_user'
		verbose_name = '订单管理用户'
		verbose_name_plural = '订单管理用户'

	def init_user_info(self):
		users = FreightUser.objects.filter(username='test')
		if users.count() == 0:
			use = User.objects.get(username='test')
			user = FreightUser.objects.create(
				username="test",
				password=make_password("test"),
				owner=use
			)
		else:
			user = users[0]
		return user


	def is_login_success(self):
		try:
			user = FreightUser.objects.get(username=self.username)
		except:
			return {'code': 'error', 'msg': u'用户名不存在！'}

		if check_password(self.password, user.password):
			return {'code': 'success', 'msg': u'登陆成功！', 'user_id': user.id}

		return {'code': 'error', 'msg': u'密码不正确！'}


	def get_profile(self):
		profiles = UserProfile.objects.filter(user=self.owner)
		if profiles.count() > 0:
			return profiles[0]

		return None

def get_make_password(password):
	return make_password(password)
