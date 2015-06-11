# -*- coding: utf-8 -*-

__author__ = 'chuter'

import json
import urlparse

from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from core.jsonresponse import JsonResponse, create_response
from core.exceptionutil import unicode_full_stack
from core import paginator

from modules.member.models import *
from modules.member.integral import increase_member_integral
from apps.customerized_apps.shengjing.models import *

from utils.string_util import byte_to_hex

from datetime import datetime, timedelta

from util import * 

from watchdog.utils import watchdog_fatal, watchdog_error

COUNT_PER_PAGE = 15

########################################################################
# update_member: 更新会员信息
########################################################################
@login_required
def update_member(request):
	try:
		member_id = int(request.POST['member_id'])
		member = Member.objects.get(id=member_id)

		#先修改会员积分
		new_integral = int(request.POST['integral'].strip())

		old_grade_id = member.grade.id
			
		increase_member_integral(member, new_integral-member.integral, MANAGER_MODIFY)

		if old_grade_id == int(request.POST.get('grade_id')):
			grade_id = member.grade.id
		else:
			grade_id = int(request.POST.get('grade_id'))
		#然后更新会员等级和备注名称信息
		Member.objects.filter(id=member_id).update(
			grade = MemberGrade.objects.get(id=grade_id),
			remarks_name = request.POST.get('remarks_name', '').strip(),
			remarks_extra = request.POST.get('remarks_extra', '').strip(),
			is_for_buy_test = int(request.POST.get('is_for_buy_test', 0)),
			update_time  = datetime.now()
			)

		#最后更新会员详细信息
		MemberInfo.objects.filter(member_id=member_id).update(
			name = request.POST['name'].strip(),
			sex = int(request.POST.get('sex', SEX_TYPE_UNKOWN).strip()),
			phone_number = request.POST.get('phone_number', '').strip(),
			qq_number = request.POST.get('qq_number', '').strip(),
			weibo_nickname = request.POST.get('weibo_nickname', '').strip(),
			member_remarks = request.POST.get('member_remarks', '').strip(),
			)

		MemberHasTag.delete_tag_member_relation_by_member(member)
		tag_ids = request.POST.get('tag_ids', '')
		if tag_ids != '':
			if len(tag_ids) > 1:
				tag_ids = tag_ids[:-1].split(',')
			MemberHasTag.add_tag_member_relation(member,tag_ids)

		response = create_response(200)
	except:
		response = create_response(500)
		response.errMsg = u'保存失败' 
		response.innerErrMsg = unicode_full_stack()

	return response.get_response()

def __get_request_members_list(request):
	#获取当前页数
	cur_page = int(request.GET.get('page', '1'))
	#获取每页个数
	count = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
	#处理排序
	sort_attr = request.GET.get('sort_attr', '-created_at')


	filter_attr = request.GET.get('filter_attr', None)
	
	#处理搜索
	query = request.GET.get('query', None)
	#total_count = Member.objects.filter(webapp_id=request.user_profile.webapp_id, is_for_test=False, is_subscribed=True).count()
	if query:
		query_hex = byte_to_hex(query)
		members = Member.objects.filter(webapp_id=request.user_profile.webapp_id, is_for_test=False, username_hexstr__contains=query_hex)#.order_by(sort_attr)
	else:
		members = Member.objects.filter(webapp_id=request.user_profile.webapp_id, is_for_test=False)#.order_by(sort_attr)
	
	tag = request.GET.get('tag', None)
	if tag and int(tag) != -1:
		members = members.filter(id__in=[member_has_tag.member_id  for member_has_tag in MemberHasTag.objects.filter( member_tag_id=tag)])
	
	source = request.GET.get('source', None)
	if source and source != '-2':
		if int(source) == 0 or int(source) == -1:
			members = members.filter(source__in=[0, -1])
		else:
			members = members.filter(source=int(source))

	grade = request.GET.get('grade', None)
	if grade and int(grade) > 0:
		members = members.filter(grade_id=int(grade))

	subscribe_days = request.GET.get('subscribe', None)
	if subscribe_days:
		date_day = datetime.today()-timedelta(days=int(subscribe_days))
		members = members.filter(created_at__gte=date_day)

	pay_times = request.GET.get('pay_times', None)
	pay_days = request.GET.get('pay_days', None)
	from mall.models import Order
	if pay_days:
		webapp_user_ids = Order.get_webapp_user_ids_pay_days_in(request.user_profile.webapp_id, pay_days)
		member_ids = [webapp_user.member_id  for webapp_user in WebAppUser.objects.filter(id__in=list(set(webapp_user_ids)))]
		members = members.filter(id__in=member_ids)
	
	if pay_times:
		members = members.filter(pay_times__gte=int(pay_times))
	
	
	total_count = len(members)

	members = members.order_by(sort_attr)

	pageinfo, members = paginator.paginate(members, cur_page, count, query_string=request.GET.get('query', None))
	for member in members:
		if request.user.username == 'shengjing360':
			try:
				sj_binding_id = ShengjingBindingMember.objects.get(member_id=member.id).id
				sj_binding_member_info= ShengjingBindingMemberInfo.objects.get(binding_id=sj_binding_id)
				sj_name = sj_binding_member_info.name
				member.sj_name = sj_name
				member.sj_status = sj_binding_member_info.status_name
			except:
				# TODO 检查非学员是否正常
				member.sj_name = None
				member.sj_status = None
		else:
			member.sj_name = None
			member.sj_status = None
	 
	return pageinfo, list(members), total_count


def __build_return_member_json(member):
	from mall.models import Order
	return {
		'id': member.id,
		'username': member.username_for_html,
		'user_icon': member.user_icon,
		'grade_name': member.grade.name,
		'integral': member.integral,
		'factor': member.factor,
		'remarks_name': member.remarks_name,
		'sj_name': member.sj_name,
		'sj_status': member.sj_status,
		'created_at': datetime.strftime(member.created_at, '%Y-%m-%d'),
		'last_visit_time': datetime.strftime(member.last_visit_time, '%Y-%m-%d') if member.last_visit_time else '-',
		'session_id': member.session_id,
		'friend_count':  member.friend_count,
		'source':  member.source,
		'fans_count': len(MemberFollowRelation.get_follow_members_for(member.id, '1')),
		'tags':__build_member_has_tags_json(member),
		'is_subscribed':member.is_subscribed,
		'pay_money': '%.2f' % member.pay_money,
		'pay_times': member.pay_times
	}

def __count_member_follow_relations(member):
	return MemberFollowRelation.objects.filter(member_id=member.id).count()	

########################################################################
# get_members: 获取member列表
########################################################################
@login_required
def get_members(request):
	sort_attr = request.GET.get('sort_attr', '-created_at')
	pageinfo, request_members, total_count = __get_request_members_list(request)

	# 构造返回数据
	return_members_jsonarray = []
	for member in request_members:
		return_members_jsonarray.append(__build_return_member_json(member))

	tags_json = _get_tags_json(request)

	response = create_response(200)
	if request.user.username == 'shengjing360':
		is_shengjing = True
	else:
		is_shengjing = False
	response.data = {
		'is_shengjing': is_shengjing,
		'items': return_members_jsonarray,
		'sortAttr': request.GET.get('sort_attr', '-created_at'),
		'pageinfo': paginator.to_dict(pageinfo),
		'tags': tags_json,
		'selected_count': len(request_members),
		'total_count': total_count
	}
	return response.get_response()

def _get_tags_json(request):
	webapp_id=request.user_profile.webapp_id
	tags = MemberTag.get_member_tags(webapp_id)

	tags_json = []
	for tag in tags:
		tags_json.append({'id':tag.id,'name': tag.name})

	return tags_json

def __build_follow_member_basic_json(follow_member, member_id):
	
	return {
		'id': follow_member.id,
		'username': follow_member.username_for_html,
		'user_icon': follow_member.user_icon,
		'integral': follow_member.integral,
		'grade_name': follow_member.grade.name,
		'created_at': datetime.strftime(follow_member.created_at, '%Y-%m-%d'),
		'source':  follow_member.source,
		'is_fans': MemberFollowRelation.is_fan(member_id, follow_member.id),
		'is_father': MemberFollowRelation.is_father(member_id, follow_member.id),
		
	}
def __build_member_has_tags_json(member):
	member_has_tags = []
	for member_has_tag in MemberHasTag.get_member_has_tags(member):
		member_has_tag_dict = {}
		member_has_tag_dict['name'] = member_has_tag.member_tag.name
		member_has_tags.append(member_has_tag_dict)
	return member_has_tags

########################################################################
# get_member_follow_relations: 获取该会员对应的关系链
########################################################################
@login_required
def get_member_follow_relations(request, member_id, only_fans):
	follow_members = MemberFollowRelation.get_follow_members_for(member_id, only_fans)

	return_follow_members_json_array = []
	for follow_member in follow_members:
		return_follow_members_json_array.append(__build_follow_member_basic_json(follow_member, member_id))

	response = create_response(200)
	response.data.items = return_follow_members_json_array
	return response.get_response()

def __build_member_basic_json(follow_member):
	return {
		'id': follow_member.id,
		'username': follow_member.username_for_html,
		'user_icon': follow_member.user_icon,
		'integral': follow_member.integral
	}

########################################################################
# get_grade_has_members: 获取会员等级对应的会员信息
########################################################################
@login_required
def get_grade_has_members(request, grade_id):
	if int(grade_id) == 0:
		grade_id = MemberGrade.get_default_grade(request.user_profile.webapp_id).id

	members = Member.objects.filter(grade_id = grade_id, is_subscribed=True, is_for_test=False).order_by('-integral')
	
	return_members_json_array = []
	for member in members:
		return_members_json_array.append(__build_member_basic_json(member))

	response = create_response(200)
	response.data.items = return_members_json_array
	return response.get_response()

########################################################################
# send_mass_message: 群发消息
########################################################################
@login_required
def send_mass_message(request):

	group_id = request.POST.get('group_id', None)
	if group_id == None or group_id == '':
		response = create_response(400)
		return response.get_response()

	content = request.POST.get('content', None)
	if content == None or content == '':
		response = create_response(400)
		return response.get_response()

	send_type  = request.POST.get('send_type', None)

	if send_type == None or send_type == '':
		response = create_response(400)
		return response.get_response()

	if int(send_type) == 0:
		result = send_mass_text_message(request.user_profile, group_id, content)
	else:
		result = send_mass_new_message(request.user_profile, group_id, content)
	if result:
		response = create_response(200)
	else:
		response = create_response(400)
	return response.get_response()
