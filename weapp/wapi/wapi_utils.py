#coding: utf8

from core.jsonresponse import create_response
from django.contrib.auth.models import User
from account.models import UserProfile
from wapi.logger.mongo_logger import MongoAPILogger

_wapi_logger = None

def wapi_log(level, app, resource, params, status=0):
	"""
	记录WAPI信息，保存到mongo中
	"""
	global _wapi_logger
	if _wapi_logger is None:
		_wapi_logger = MongoAPILogger()
	return _wapi_logger.log(app, resource, params, status)


def create_json_response(code, data):
	response = create_response(code)
	response.data = data
	return response.get_response()

def get_webapp_id_via_oid(owner_id):
	"""
	获取user对应的webapp id

	@TODO 优化缓存
	"""
	#print("owner_id: {}".format(owner_id))
	user = User.objects.get(id=owner_id)
	profile = UserProfile.objects.get(user=user)
	print("webapp_id: {}".format(profile.webapp_id))
	return profile.webapp_id


