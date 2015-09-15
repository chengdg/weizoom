# -*- coding: utf-8 -*-

__author__ = 'chuter'

import json
import urlparse
import time
import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from core.jsonresponse import JsonResponse, create_response
from core.exceptionutil import unicode_full_stack
from core import paginator

from modules.member.models import *
from modules.member.integral import increase_member_integral
from modules.member import module_api
from apps.customerized_apps.shengjing.models import *

from utils.string_util import byte_to_hex

from datetime import datetime, timedelta

from util import *

from watchdog.utils import watchdog_fatal, watchdog_error
from core.restful_url_route import *

from market_tools.tools.member_qrcode import api_views as member_qrcode_api_views
from core.restful_url_route import *
from weixin2.models import get_opid_from_session


COUNT_PER_PAGE = 20


def __get_request_members_list(request):
	"""
	获取会员列表
	"""
	#获取当前页数
	cur_page = int(request.GET.get('page', '1'))
	#获取每页个数
	count = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
	#处理排序
	sort_attr = request.GET.get('sort_attr', '-id')
	#会员过滤
	filter_value = request.GET.get('filter_value', None)

	filter_data_args = {}
	filter_data_args['webapp_id'] = request.user_profile.webapp_id
	filter_data_args['is_for_test'] = False
	filter_data_args['status__in'] = [SUBSCRIBED, CANCEL_SUBSCRIBED]

	#处理已经被选的会员
	selected_member_ids_str = request.GET.get('selectedMemberIds',"")
	selected_member_ids = []
	if selected_member_ids_str:
		selected_member_ids = selected_member_ids_str.split(",")

	#处理当前选择的会员
	current_member_id = int(request.GET.get('currentMemberId',"0"))
	#处理来自“数据罗盘-会员分析-关注会员链接”过来的查看关注会员的请求
	#add by duhao 2015-07-13
	status = request.GET.get('status', '-1')
	if not filter_value and status == '1':
		filter_data_args['is_subscribed'] = True

	if filter_value:
		filter_data_dict = {}

		for filter_data_item in filter_value.split('|'):
			try:
				key, value = filter_data_item.split(":")
			except:
				key = filter_data_item[:filter_data_item.find(':')]
				value = filter_data_item[filter_data_item.find(':')+1:]

			filter_data_dict[key] = value
			if key == 'name':
				query_hex = byte_to_hex(value)
				filter_data_args["username_hexstr__contains"] = query_hex
			if key == 'grade_id':
				filter_data_args["grade_id"] = value

			if key == 'tag_id':
				member_ids = [member.id for member in  MemberHasTag.get_member_list_by_tag_id(value)]
				filter_data_args["id__in"] = member_ids

			if key == 'status':
				#无论如何这地方都要带有status参数，不然从“数据罗盘-会员分析-关注会员链接”过来的查询结果会有问题
				if value == '1':
					filter_data_args["is_subscribed"] = True
				elif value == '0':
					filter_data_args["is_subscribed"] = False

			if key == 'source':
				if value in ['-1']:
					filter_data_args['source__in'] = [0,-1,1,2]
				elif value in ['0']:
					filter_data_args['source__in'] = [0,-1]
				else:
					filter_data_args["source"] = value

			if key in ['pay_times', 'pay_money', 'friend_count', 'unit_price', 'integral']:
				if value.find('-') > -1:
					val1,val2 = value.split('--')
					if float(val1) > float(val2):
						filter_data_args['%s__gte' % key] = float(val2)
						filter_data_args['%s__lte' % key] = float(val1)
					else:
						filter_data_args['%s__gte' % key] = float(val1)
						filter_data_args['%s__lte' % key] = float(val2)
				else:
					filter_data_args['%s__gte' % key] = value

			if key in ['first_pay', 'sub_date'] :
				if value.find('-') > -1:
					val1,val2 = value.split('--')
					if key == 'first_pay':
						filter_data_args['last_pay_time__gte'] = val1
						filter_data_args['last_pay_time__lte'] =  val2
					elif key == 'sub_date':

						filter_data_args['created_at__gte'] = val1
						filter_data_args['created_at__lte'] = val2
					else:
						filter_data_args['integral__gte'] = val1
						filter_data_args['integral__lte'] = val2

			if key  == 'last_message_time':
				val1,val2 = value.split('--')
				session_filter = {}
				session_filter['mpuser__owner_id'] = request.manager.id
				session_filter['member_latest_created_at__gte'] = time.mktime(time.strptime(val1,'%Y-%m-%d %H:%M'))
				session_filter['member_latest_created_at__lte'] = time.mktime(time.strptime(val2,'%Y-%m-%d %H:%M'))

				opids = get_opid_from_session(session_filter)
				session_member_ids = module_api.get_member_ids_by_opid(opids)
				if filter_data_args.has_key('id__in'):
					member_ids = filter_data_args['id__in']
					member_ids = list(set(member_ids).intersection(set(session_member_ids)))
					filter_data_args['id__in'] = member_ids
				else:
					filter_data_args['id__in'] = session_member_ids

	members = Member.objects.filter(**filter_data_args).order_by(sort_attr)
	total_count = members.count()
	pageinfo, members = paginator.paginate(members, cur_page, count, query_string=request.GET.get('query', None))
	for member in members:
		if str(member.id) in selected_member_ids:
			member.is_selected = True
		else:
			member.is_selected = False

		if member.id == current_member_id:
			member.is_current_select = True
		else:
			member.is_current_select = False

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
		'username': member.username_for_title,
		'username_truncated': member.username_truncated,
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
		'pay_times': member.pay_times,
		'unit_price': '%.2f' % member.unit_price,
		'is_selected': member.is_selected,
		'is_current_select': member.is_current_select,
		'experience': member.experience
	}

def __count_member_follow_relations(member):
	return MemberFollowRelation.objects.filter(member_id=member.id).count()


########################################################################
# get_members_filter_params: 获取商品过滤参数
########################################################################
@api(app='member', resource='members_filter_params', action='get')
@login_required
def get_members_filter_params(request):
	webapp_id = request.user_profile.webapp_id
	tags = []
	for tag in  MemberTag.get_member_tags(webapp_id):
		if tag.name == '未分组':
			tags = [tag] + tags
		else:
			tags.append({
				"id": tag.id,
				"name": tag.name
			})

	grades = []
	for grade in MemberGrade.get_all_grades_list(webapp_id):
		grades.append({
			"id": grade.id,
			"name": grade.name
		})

	response = create_response(200)
	response.data = {
		'tags': tags,
		'grades': grades
	}
	return response.get_response()


@api(app='member', resource='integral', action='update')
@login_required
def update_integral(request):
	member_id = request.POST.get('member_id', None)
	integral = request.POST.get('integral', 0)
	reason = request.POST.get('reason', '').strip()
	webapp_id=request.user_profile.webapp_id

	if Member.objects.filter(webapp_id=webapp_id, id=member_id).count() == 0:
		pass
	else:
		if int(integral) != 0:
			from modules.member.tasks import update_member_integral
			if int(integral) > 0:
				event_type = MANAGER_MODIFY_ADD
			else:
				event_type = MANAGER_MODIFY_REDUCT

			update_member_integral(member_id, None, int(integral), event_type, 0, reason, request.user.username)

	response = create_response(200)
	return response.get_response()


@api(app='member', resource='members', action='get')
@login_required
def get_members(request):
	"""
	获取会员列表

	URL: http://weapp.weizoom.com/member/api/members/get/?design_mode=0&version=1&filter_value=pay_times:0-1|first_pay:2015-04-08%2000:00--2015-04-30%2000:00&page=1&count_per_page=50&enable_paginate=1&timestamp=1435216368297&_=1435215905446

	"""
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

@api(app='member', resource='member_ids', action='get')
@login_required
def get_member_ids(request):
	"""
	获取会员id集(取消关注除外)

	"""
	pageinfo, request_members, total_count = __get_request_members_list(request)

	# 构造返回数据
	member_ids = []
	response = create_response(200)
	for member in request_members:
		if member.is_subscribed:
			member_ids.append(member.id)

	response.data = {
		'member_ids': member_ids,
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
	father_member = MemberFollowRelation.get_father_member(follow_member.id)
	if father_member:
		father_name = father_member.username_for_html
		father_id = father_member.id
	else:
		father_name = ''
		father_id = ''

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
		'pay_money': '%.2f' % follow_member.pay_money,
		'father_name': father_name,
		'father_id': father_id
	}

def __build_member_has_tags_json(member):
	member_has_tags = []
	for member_has_tag in MemberHasTag.get_member_has_tags(member):
		member_has_tag_dict = {}
		member_has_tag_dict['id'] = member_has_tag.member_tag.id
		member_has_tag_dict['name'] = member_has_tag.member_tag.name
		member_has_tags.append(member_has_tag_dict)
	return member_has_tags

########################################################################
# get_member_follow_relations: 获取该会员对应的关系链
########################################################################
@api(app='member', resource='follow_relations', action='get')
@login_required
def get_member_follow_relations(request):
	member_id = request.GET.get('member_id', 0)
	only_fans = request.GET.get('only_fans', 'false')
	data_value = request.GET.get('data_value', None)
	sort_attr = request.GET.get('sort_attr', '-id')
	if only_fans == 'true':
		only_fans = '1'
	else:
		only_fans = '0'

	if data_value:
		if data_value == 'shared':
			follow_members = MemberFollowRelation.get_follow_members_for_shred_url(member_id)
		elif  data_value == 'qrcode':
			follow_members=  MemberFollowRelation.get_follow_members_for(member_id, '1', True)
		else:
			follow_members = []
	else:
		follow_members = MemberFollowRelation.get_follow_members_for(member_id, only_fans)

	#增加计算follow_members的人数、下单人数、成交金额
	population = len(follow_members)
	population_order = 0
	for follow_member in follow_members:
		user_orders = Order.get_orders_from_webapp_user_ids(follow_member.get_webapp_user_ids)
		if user_orders:
			population_order += 1
	#成交金额
	amount = 0
	for follow_member in follow_members:
		amount += follow_member.pay_money

	#增加计算follow_members的人数、下单人数、成交金额

	#进行排序
	follow_members = follow_members.order_by(sort_attr)
	if data_value:
		filter_date_follow_members = follow_members
	else:
		filter_date_follow_members = []
	#进行分页
	count_per_page = int(request.GET.get('count_per_page', 8))
	cur_page = int(request.GET.get('page', '1'))
	pageinfo, follow_members = paginator.paginate(follow_members, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

	return_follow_members_json_array = []

	if data_value:
		follow_members = filter_date_follow_members

	for follow_member in follow_members:
		return_follow_members_json_array.append(__build_follow_member_basic_json(follow_member, member_id))

	response = create_response(200)
	response.data = {
		'items': return_follow_members_json_array,
		'pageinfo': paginator.to_dict(pageinfo),
		'only_fans':only_fans,
		'sortAttr': request.GET.get('sort_attr', '-created_at'),
		'population': population,
		'population_order': population_order,
		'amount': '%.2f' % amount
	}
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


########################################################################
# edit_member_qrcode: 编辑会员扫码
########################################################################
@api(app='member', resource='member_qrcode', action='edit')
@login_required
def edit_member_qrcode(request):
	response = member_qrcode_api_views.edit_member_qrcode_settings(request)
	return response


########################################################################
# get_members_filter_params: 获取商品过滤参数
########################################################################
@api(app='member', resource='tags', action='get')
@login_required
def get_member_tags(request):
	webapp_id = request.user_profile.webapp_id
	tags = []
	for tag in  MemberTag.get_member_tags(webapp_id):
		tags.append({
			"id": tag.id,
			"name": tag.name
		})

	grades = []
	for grade in MemberGrade.get_all_grades_list(webapp_id):
		grades.append({
			"id": grade.id,
			"name": grade.name
		})

	response = create_response(200)
	response.data = {
		'tags': tags,
		'grades': grades
	}

	return response.get_response()


########################################################################
# update_tag 修改tag（等级或者分组）
########################################################################
@api(app='member', resource='tag', action='update')
@login_required
def update_tag(request):
	webapp_id = request.user_profile.webapp_id
	type = request.POST.get('type', None)
	checked_ids = request.POST.get('checked_ids', None)
	member_id = request.POST.get('member_id', None)

	if type and member_id:
		member = Member.objects.get(id=member_id)
		if member.webapp_id == webapp_id:
			if type == 'tag':
				tag_ids = checked_ids.split('_')
				MemberHasTag.delete_tag_member_relation_by_member(member)
				tag_ids = [id for id in tag_ids if id]
				if tag_ids:
					MemberHasTag.add_tag_member_relation(member, tag_ids)
				else:
					tag_ids.append(MemberTag.get_default_tag(webapp_id).id)
					MemberHasTag.add_tag_member_relation(member, tag_ids)
			elif type == 'grade':
				member.grade = MemberGrade.objects.get(id=checked_ids)
				member.save()

	response = create_response(200)
	return response.get_response()


########################################################################
# update_tag 修改等级
########################################################################
@api(app='member', resource='grade', action='batch_update')
@login_required
def batch_update_grade(request):
	webapp_id = request.user_profile.webapp_id
	grade_id = request.POST.get('grade_id', None)
	post_ids = request.POST.get('ids', None)
	grade = MemberGrade.objects.get(id=grade_id)

	status = request.POST.get('update_status', 'selected')
	if status == 'all':
		filter_value = request.POST.get('filter_value', '')
		request.GET = request.GET.copy()
		request.GET['filter_value'] = filter_value
		request.GET['count_per_page'] = 999999999
		_, request_members, _ = __get_request_members_list(request)
		post_ids = [m.id for m in request_members]
	else:
		post_ids = post_ids.split('-')

	if grade.webapp_id == webapp_id and post_ids:
		Member.objects.filter(id__in=post_ids).update(grade=grade)

	response = create_response(200)
	response.data.post_ids = post_ids
	return response.get_response()


########################################################################
# update_tag 修改tag（等级或者分组）
########################################################################
@api(app='member', resource='tag', action='batch_update')
@login_required
def batch_update_tag(request):
	webapp_id = request.user_profile.webapp_id
	tag_id = request.POST.get('tag_id', None)
	post_ids = request.POST.get('ids', None)

	status = request.POST.get('update_status', 'selected')
	if status == 'all':
		filter_value = request.POST.get('filter_value', '')
		request.GET = request.GET.copy()
		request.GET['filter_value'] = filter_value
		request.GET['count_per_page'] = 999999999
		_, request_members, _ = __get_request_members_list(request)
		post_ids = [m.id for m in request_members]
	else:
		post_ids = post_ids.split('-')
	tag = MemberTag.objects.get(id=tag_id)
	if tag.webapp_id == webapp_id and post_ids:
		default_tag_id = MemberTag.get_default_tag(webapp_id).id
		MemberHasTag.add_members_tag(default_tag_id, tag_id, post_ids)

	response = create_response(200)
	return response.get_response()


########################################################################
# update_tag 修改tag（等级或者分组）
########################################################################
@api(app='member', resource='member', action='update')
@login_required
def update_member(request):
	webapp_id = request.user_profile.webapp_id
	member_id = request.POST.get('member_id', None)
	grade_id = request.POST.get('grade_id', None)
	member_remarks = request.POST.get('member_remarks', None)
	name = request.POST.get('name', None)
	sex = request.POST.get('sex', None)
	phone_number = request.POST.get('phone_number', None)
	is_for_buy_test = request.POST.get('is_for_buy_test', 0)
	member = Member.objects.get(id=member_id)
	tag_ids = request.POST.get('tag_ids', None)

	if member.webapp_id == webapp_id:
		if grade_id:
			member.grade = MemberGrade.objects.get(id=grade_id)
			member.save()
		member_info_update = {}
		if member_remarks:
			member_info_update['member_remarks'] = member_remarks
		if name:
			member_info_update['name'] = name
		if phone_number:
			member_info_update['phone_number'] = phone_number.strip()

		if sex != None:
			member_info_update['sex'] = sex
		member.is_for_buy_test = is_for_buy_test
		member.save()
		if member_info_update:
			if MemberInfo.objects.filter(member=member).count() > 0:
				MemberInfo.objects.filter(member=member).update(**member_info_update)
			else:
				member_info_update['member'] = member
				MemberInfo.objects.create(**member_info_update)

		if tag_ids:
			tag_id_list = tag_ids.split('_')
			MemberHasTag.delete_tag_member_relation_by_member(member)
			MemberHasTag.add_tag_member_relation(member, tag_id_list)

	response = create_response(200)
	return response.get_response()

########################################################################
# get_member_logs 修改tag（等级或者分组）
########################################################################
@api(app='member', resource='member_logs', action='get')
@login_required
def get_member_logs(request):
	member_id = request.GET.get('member_id', '')
	if member_id:
		member_logs = MemberIntegralLog.objects.filter(member_id=member_id).order_by('-id')
	else:
		member_logs = ''

	#进行分页
	count_per_page = int(request.GET.get('count_per_page', 10))
	cur_page = int(request.GET.get('page', '1'))
	pageinfo, member_logs = paginator.paginate(member_logs, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
	data = []
	for log in member_logs:
		data.append(
			{'event_type': log.event_type,
			'integral_count': log.integral_count,
			'created_at': log.created_at.strftime('%Y/%m/%d %H:%M:%S'),
			'manager': log.manager,
			'reason': log.reason,
			'current_integral': log.current_integral
			})

	response = create_response(200)
	response.data = {
		'items': data,
		'pageinfo': paginator.to_dict(pageinfo),
	}

	return response.get_response()
