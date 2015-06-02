# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.shortcuts import render_to_response
from models import *
from modules.member import util as member_util
from core.jsonresponse import JsonResponse, create_response
from django.contrib.auth.decorators import login_required, permission_required
from core.exceptionutil import full_stack
from core import paginator
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


#===============================================================================
# get_member_records : 获取活动信息
#===============================================================================
@login_required
def get_member_records(request):
	activity_id = int(request.GET['activity_id'])
	activity  = Activity.objects.get(id=activity_id)
	query = request.GET.get('query', None)
	filter_attr = request.GET.get('filter_attr', None)
	filter_value = request.GET.get('filter_value', None)
	
	is_enable_offline_sign = activity.is_enable_offline_sign
	
	weapp_users = activity.joined_weapp_users
	webapp_user_ids = [user.id for user in weapp_users]

	weapp_user_id_2_values = {}
	for item_value in ActivityItemValue.objects.filter(activity=activity, webapp_user_id__in=webapp_user_ids):
		weapp_user_id_2_values.setdefault(item_value.webapp_user_id, {})[item_value.item_id] = item_value

	items = list(ActivityItem.objects.filter(activity=activity))
	
	if activity.is_enable_offline_sign:
		activity_user_codes = ActivityUserCode.objects.filter(activity=activity, webapp_user_id__in=webapp_user_ids)
		if query:
			activity_user_codes = activity_user_codes.filter(sign_code=query)
		#处理过滤
		if filter_attr:
			if filter_value!='-1':
				activity_user_codes = activity_user_codes.filter(sign_status=int(filter_value))
		user_id2code = dict([(a.webapp_user_id, a.sign_code) for a in activity_user_codes])
		user_id2sign_status = dict([(a.webapp_user_id, a.sign_status) for a in activity_user_codes])
		weapp_users = [user for user in weapp_users if user.id in user_id2code]
	
	#进行分页
	count_per_page = int(request.GET.get('count_per_page', 15))
	cur_page = int(request.GET.get('page', '1'))
	pageinfo, weapp_users = paginator.paginate(weapp_users, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
	
	response = 	create_response(200)
	cur_weapp_users = []
	for weapp_user in weapp_users:
		cur_weapp_user = JsonResponse()
		cur_weapp_user.id = weapp_user.id
		member = weapp_user.get_member_by_webapp_user_id(weapp_user.id)
		if not activity.is_enable_offline_sign and query:
			if member:
				if member.username_for_html != query:
					continue
			else:
				continue
		
		cur_member = JsonResponse()
		if member:
			cur_member.id = member.id
			cur_member.user_icon = member.user_icon
			cur_member.username_for_html = member.username_for_html
		else:
			cur_member = ''
		cur_weapp_user.member = cur_member
		try:
			sign_code = user_id2code[weapp_user.id]
			sign_status = user_id2sign_status[weapp_user.id]	
		except:
			sign_code = ''
			sign_status = 0
		cur_weapp_user.sign_code = sign_code
		cur_weapp_user.sign_status = sign_status
		cur_weapp_user.item_values = []
		item_values = []
		for item in items:
			id2value = weapp_user_id_2_values[weapp_user.id]
			if not item.id in id2value:
				#存在非必填项
				continue

			value = id2value[item.id]
			user_input_value = value.value

			is_image = False
			if item.type == ACTIVITYITEM_TYPE_IMAGE:
				is_image = True
			cur_item = JsonResponse()
			cur_item.title = item.title
			cur_item.is_image = is_image
			cur_item.user_input_value = user_input_value
			item_values.append(cur_item)

		cur_weapp_user.item_values = item_values
		cur_weapp_users.append(cur_weapp_user)
	response.data.weapp_users = cur_weapp_users
	
	cur_activity = JsonResponse()
	cur_activity.id = activity.id
	cur_activity.name = activity.name
	cur_activity.start_date = activity.start_date
	cur_activity.end_date = activity.end_date
	cur_activity.is_enable_offline_sign = activity.is_enable_offline_sign
	response.data.activity = cur_activity
	response.data.pageinfo = paginator.to_dict(pageinfo)
	response.data.sortAttr = request.GET.get('sort_attr', '-created_at')
	return response.get_response()
	

def call_api(request):
	api_function = apiview_util.get_api_function(request, globals())
	return api_function(request)