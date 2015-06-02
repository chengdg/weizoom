# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response
from django.conf import settings
from django.contrib.auth.models import User

from core import paginator
from modules.member.models import *

from watchdog.utils import *
from core.jsonresponse import JsonResponse, create_response
import module_api
from util import *

MESSAGE_COUNT_PER_PAGE = 50
COUNT_PER_PAGE = 1
def __get_request_members_list(request, webapp_id):
	#获取当前页数
	cur_page = int(request.GET.get('page', '1'))
	#获取每页个数
	count = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
	#处理排序
	#sort_attr = request.GET.get('sort_attr', '-created_at')

	# filter_attr = request.GET.get('filter_attr', None)
	search_type = request.GET.get('search_type', '0')
	start_time = request.GET.get('start_time', None)
	end_time = request.GET.get('end_time', None)
	if int(search_type) == 0:
		if start_time and end_time:
			members = Member.objects.filter(webapp_id=webapp_id, is_for_test=False, update_time__gte=start_time, update_time__lt=end_time)
			total_count = members.count()
		
		elif start_time:
			members = Member.objects.filter(webapp_id=webapp_id, is_for_test=False, update_time__gte=start_time)
			total_count = members.count()

		elif end_time:
			members = Member.objects.filter(webapp_id=webapp_id, is_for_test=False, update_time__lt=end_time)
			total_count = members.count()
		else:
			members = Member.objects.filter(webapp_id=webapp_id, is_for_test=False)
			total_count = members.count()
	else:
		members = Member.objects.filter(webapp_id=webapp_id, is_for_test=False)
		total_count = members.count()

	pageinfo, members = paginator.paginate(members, cur_page, count, query_string=request.GET.get('query', None))

	return pageinfo, list(members), total_count

SOURCE_SELF_SUB = 0
SOURCE_MEMBER_QRCODE = 1
SOURCE_BY_URL = 2
def __build_return_member_json(member):
	if member.source == SOURCE_SELF_SUB:
		source = u'直接关注'

	if member.source == SOURCE_MEMBER_QRCODE:
		source = u'推广扫描'

	if member.source == SOURCE_BY_URL:
		source = u'会员分享'	

	 
	return {
		'id': member.id,
		'username': member.username_for_html,
		'user_icon': member.user_icon,
		'grade_name': member.grade.name,
		'integral': member.integral,
		'factor': member.factor,
		'remarks_name': member.remarks_name,
		'created_at': datetime.strftime(member.created_at, '%Y-%m-%d %H:%M:%S'),
		'update_time': datetime.strftime(member.update_time, '%Y-%m-%d %H:%M:%S'),
		'last_visit_time': datetime.strftime(member.last_visit_time, '%Y-%m-%d %H:%M:%S') if member.last_visit_time else '-',
		'friend_count':  member.friend_count,
		'source':  source,
	}


########################################################################
# get_members: 获取member列表
########################################################################
@arguments_required('token')
@session_required
def get_members(request):
	search_type = request.GET.get('search_type', '0')
	return_members_jsonarray = []
	webapp_id = request.user.get_profile().webapp_id
	pageinfo, request_members, total_count = __get_request_members_list(request, webapp_id)

	# 构造返回数据
	for member in request_members:
		return_members_jsonarray.append(__build_return_member_json(member))

	response = create_response(200)
	response.data = {
		'items': return_members_jsonarray,
		'pageinfo': paginator.to_dict(pageinfo),
		'total_count': total_count,
		'search_type': search_type
	}
	return response.get_response()


########################################################################
# get_members: 获取member列表
########################################################################
@arguments_required('token', 'member_id')
@session_required
def get_member(request):
	token = request.GET.get('token', '').strip()

	return_member_jsonarray = []

	member_id = request.GET.get('member_id', None)
	try:
		if member_id and Member.objects.filter(id=member_id).count() > 0:
			member = Member.objects.get(id=member_id)
			member_json = __build_return_member_json(member)
			response = create_response(200)
			response.data = {
				'items': [member_json],
			}
			return response.get_response()
		elif member_id:
			response = create_response(530)
			response.errMsg = u'会员不存'
			return response.get_response()	
		else:	
			response = create_response(531)
			response.errMsg = u'缺少参数member_id'
			return response.get_response()	
	except:
		response = create_response(590)
		response.errMsg = u'会员不存'
		return response.get_response()	
	
	