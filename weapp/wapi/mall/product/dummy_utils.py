#coding: utf8
from account.models import UserProfile

class DummyUserProfile:
	"""
	模拟webapp_owner_user_profile，用于cache调用
	"""
	def __init__(self, webapp_id=0, user_id=0):
		self.webapp_id = webapp_id
		self.user_id = user_id
		up = UserProfile.objects.filter(user_id=user_id).first()
		# todo 优化,外部传值
		if up:
			self.webapp_type = up.webapp_type
		else:
			self.webapp_type = 0


class DummyRequest(object):
	"""
	模拟Django Request
	"""
	def __init__(self):
		pass

class DummyModel(object):
	"""
	模拟数据库Model
	"""

	def __init__(self):
		pass
