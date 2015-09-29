#coding: utf8

from core.jsonresponse import create_response
from django.contrib.auth.models import User
from account.models import UserProfile

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
