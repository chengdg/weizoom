# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.shortcuts import render_to_response
from models import *
from modules.member import util as member_util
from core.jsonresponse import JsonResponse, create_response
from django.contrib.auth.decorators import login_required, permission_required
from core.exceptionutil import full_stack
from django.db.models import Q
import mobile_views
from account.views import save_base64_img_file_local_for_webapp

from core import apiview_util


########################################################################
# save_activity_apply:
########################################################################
def save_activity_apply(request, webapp_id, activity_id):
	member = mobile_views.__get_current_member(request)
	try:
		activity = Activity.objects.get(id=activity_id)
	except:
		response = create_response(500)
		response.errMsg = u'该活动不存在'
		response.innerErrMsg = full_stack()
		return response.get_response()

	if member is None:
		response = create_response(500)
		response.errMsg = u'您还不是会员'
		return response.get_response()

	if request.POST:
		try:
			items = ActivityItems.objects.filter(activity=activity)
			for item in items:
				input_name = '{}-{}'.format(item.id, item.type)
				if item.type == TYPE_IMAGE:
					file = request.POST[input_name]
					value = save_base64_img_file_local_for_webapp(request, file)
				else:
					value = request.POST.get(input_name, '')

				ItmesValue.objects.create(
					owner = request.user_profile.user,
					items = item,
					activity = activity,
					member = member,
					value = value
				)
			response = create_response(200)
		except:
			response = create_response(500)
			response.errMsg = u'提交错误'
			response.innerErrMsg = full_stack()
			return response.get_response()
	else:
		response = create_response(500)
		response.errMsg = u'is not POST method'
	return response.get_response()

###############################################################
#check_vote_settings_name_duplicate ：检查名字重复
###############################################################
@login_required
def check_activity_name_duplicate(request):
	name = request.POST['builtName'].strip()
	activity = Activity.objects.filter(owner=request.user, name=name)
	ignore_info_id = request.POST.get('id', None)
	if ignore_info_id:
		activity = activity.filter( ~Q(id=int(ignore_info_id)) )
	if activity.count() > 0:
		response = create_response(605)
		response.errMsg = u'名称已存在'
		return response.get_response()
	else:
		return create_response(200).get_response()

#===============================================================================
# upload_image : 上传微博图片
#===============================================================================
import time
import os
try:
    import Image
except:
    from PIL import Image
import base64
def upload_image(ajax_file, blogger_id=None):
	date = time.strftime("%Y_%m_%d")
	try:
		result = {}

		date = time.strftime('%Y%m%d')
		dir_path_suffix = '%d_%s' % (1, date)
		folder_path = os.path.join(settings.UPLOAD_DIR, dir_path_suffix)
		if not os.path.exists(folder_path):
			os.makedirs(folder_path)

		#获取文件的扩展名
		file_name = '%s.%s' % (time.strftime("%Y_%m_%d_%H_%M_%S"), 'png')
		ajax_path = '%s/%s' % (folder_path, file_name)
		ajax_file = ajax_file.split(',')
		print ajax_file
		image_content = base64.b64decode(ajax_file[1])
		image_file = open(ajax_path, 'wb')
		image_file.write(image_content)
		image_file.close()

		if hasattr(ajax_file, 'size'):
			file_size = ajax_file.size
		else:
			file_size = len(image_content)

		if file_size >= 5 * 1024 * 1024:
			result['result'] = 'fail'
		else:
			image = Image.open(ajax_path)
			width, height = image.size

			if max(width, height) > 200:
				smaller_scale = float(200) / float(max(width, height))
				width = int(width * smaller_scale)
				height = int(height * smaller_scale)

			result['width'] = str(width)
			result['height'] = str(height)
			result['image_name'] = file_name
			result['result'] = 'success'
		file_name = '/static/upload/%s/%s' % (dir_path_suffix, file_name)
		result['date'] = date
	except Exception, e:
		file_name = None
	#finally:
	#ajax_file.close()
	return file_name


def call_api(request):
	api_function = apiview_util.get_api_function(request, globals())
	return api_function(request)