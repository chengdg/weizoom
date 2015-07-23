# -*- coding: utf-8 -*-

__author__ = 'liupeiyu'


from django.db import models
from django.contrib.auth.models import User
from account.models import UserProfile

#===============================================================================
# CloudUser ： 云管家用户
#===============================================================================
USER_STATUS_NORMAL = 0
USER_STATUS_BUSY = 1
USER_STATUS_DISABLED = 2
USER_STATUSES = (
(USER_STATUS_NORMAL, '正常'),
(USER_STATUS_BUSY, '忙碌'),
(USER_STATUS_DISABLED, '停用')
	)
class CloudUser(models.Model):
	owner = models.ForeignKey(User, related_name='owned_cloud')
	phone_number = models.CharField(max_length=50)
	captcha = models.CharField(max_length=128, default="-1")
	status = models.IntegerField(default=USER_STATUS_NORMAL, choices=USER_STATUSES)
	is_deleted = models.BooleanField(default=False) #是否删除

	class Meta(object):
		db_table = 'cloud_user'
		verbose_name = '云管家用户'
		verbose_name_plural = '云管家用户'

	def is_login_success(self):
		try:
			user = CloudUser.objects.get(phone_number=self.phone_number)
		except:
			return {'code': 501, 'msg': u'手机号码不存在'}

		if self.captcha == user.captcha:
			return {'code': 200, 'msg': u'登陆成功！', 'user_id': user.id}

		return {'code': 502, 'msg': u'验证码不正确！'}


	def get_profile(self):
		profiles = UserProfile.objects.filter(user=self.owner)
		if profiles.count() > 0:
			return profiles[0]

		return None


	def get_webapp_id(self):
		if hasattr(self, '_webapp_id'):
			return self._webapp_id
		else:
			try:
				self._webapp_id = UserProfile.objects.get(user_id=self.owner.id).webapp_id
				return self._webapp_id
			except:
				return None


#===============================================================================
# CloudReport ： 报告
#===============================================================================
CLOUD_WEEKLY = 1
Cloud_Monthly = 2
class CloudReport(models.Model):
	webapp_id = models.CharField(max_length=16, verbose_name='对应的webapp id')
	start_date = models.DateTimeField(verbose_name='开始时间')
	end_date = models.DateTimeField(verbose_name='结束时间')
	status = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'cloud_report'
		verbose_name = '云管家报告'
		verbose_name_plural = '云管家报告'

	@staticmethod
	def get_weeklys_by_webapp_id(webapp_id):
		return CloudReport.objects.filter(webapp_id=webapp_id, status=CLOUD_WEEKLY).order_by('-start_date')

	@staticmethod
	def get_monthlys_by_webapp_id(webapp_id):
		return CloudReport.objects.filter(webapp_id=webapp_id, status=Cloud_Monthly).order_by('-start_date')
