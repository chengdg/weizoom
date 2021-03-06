#coding: utf8

from core.jsonresponse import create_response
from django.contrib.auth.models import User
from account.models import UserProfile
from wapi.logger.mongo_logger import MongoAPILogger
from django.conf import settings


_wapi_logger = None

def wapi_log(app, resource, method, params, time_in_s, status=0):
	"""
	记录WAPI信息，保存到mongo中
	"""
	if settings.WAPI_LOGGER_ENABLED:
		global _wapi_logger
		if _wapi_logger is None:
			_wapi_logger = MongoAPILogger()
		if settings.MODE == 'develop' or settings.MODE == 'test':
			print("called WAPI (in {} s): {} {}/{}, param: {}".format(time_in_s, method, app, resource, params))
		return _wapi_logger.log(app, resource, method, params, time_in_s, status)
	return


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
	#print("webapp_id: {}".format(profile.webapp_id))
	return profile.webapp_id


