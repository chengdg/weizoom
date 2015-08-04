# -*- coding: utf-8 -*

__author__ = 'herry'

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


from core.exceptionutil import unicode_full_stack
from core.jsonresponse import create_response

from models import Notice
import datetime
import time
from module_api import create_notice_for_user

@login_required
def get_notice(request):
	try:
		user_notices = list(Notice.objects.filter(owner_id=request.user.id))
		response = create_response(200)
		response.data.notices = Notice.notices_json_array(user_notices)
	except:
		response = create_response(500)
		response.errMsg = u'系统繁忙，请稍候重试'
		response.innerErrMsg = unicode_full_stack()

	return response.get_response()

@login_required
def delete_notice(request):
	try:
		notice_id = request.GET['notice_id']
		Notice.objects.filter(id=notice_id).delete()
		response = create_response(200)
	except:
		response = create_response(500)
		response.innerErrMsg = unicode_full_stack()

	return response.get_response()

@login_required
def create_read_notice(request):
	try:
		notice_id = int(request.GET['notice_id'])
		Notice.read_notice(notice_id)
		response = create_response(200)
	except:
		response = create_response(500)
		response.innerErrMsg = unicode_full_stack()	
	return response.get_response()

def get_land_notice(request):
	try:
		landing_notices = list(Notice.objects.filter(owner_id=1))
		response = create_response(200)
		response.data.notices = Notice.notices_json_array(landing_notices)
	except:
		response = create_response(500)
		response.errMsg = u'系统繁忙，请稍候重试'
		response.innerErrMsg = unicode_full_stack()

	return response.get_jsonp_response(request)

#user_chars为'test1,test2,test3',为user_chars里的用户创建通知
def create_notice(request):
	response = create_response(200)
	user_chars = request.POST['user_chars'].split(',')
	notice_title = request.POST['notice_title']
	notice_content = request.POST['notice_content']
	for username in user_chars:
		try:
			receive_user = User.objects.get(username=username) 
		except:
			response.errMsg += username +u'不存在'
			response.innerErrMsg = unicode_full_stack()
		else:
			create_notice_for_user(receive_user, notice_title, notice_content)
	return response.get_response()

from core import apiview_util
def call_api(request):
	api_function = apiview_util.get_api_function(request, globals())
	return api_function(request)