#!/usr/bin/env python
# -*- coding: utf-8 -*-

from member import export

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.db.models import Q

from core.jsonresponse import JsonResponse, create_response
from core.exceptionutil import unicode_full_stack
from core import paginator
#import sys
from mall.models import Order, STATUS2TEXT

from modules.member.models import *
from watchdog.utils import watchdog_error
from weixin.user.models import DEFAULT_ICON, get_system_user_binded_mpuser
from excel_response import ExcelResponse
from market_tools.tools.coupon.util import get_coupon_rules, get_my_coupons
from market_tools.tools.member_qrcode.models import *
from apps.customerized_apps.shengjing.models import *
from core import resource

COUNT_PER_PAGE = 20

def get_request_members_list(request):
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
		#session_member_ids:通过最后对话时间而获取到会员id的list，先默认为false
		session_member_ids = False

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
		#最后对话时间和分组的处理：1、都存在，做交集运算2、最后对话时间存在，将它赋值给filter_data_args['id__in']，
		#3、最后对话时间存在，上面做了处理，不处理了。4、都不存在，pass
		if filter_data_args.has_key('id__in') and session_member_ids:
			member_ids = filter_data_args['id__in']
			member_ids = list(set(member_ids).intersection(set(session_member_ids)))
			filter_data_args['id__in'] = member_ids
		elif session_member_ids:
			filter_data_args['id__in'] = session_member_ids
		#最后对话时间和分组的处理

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


def build_return_member_json(member):
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
		'tags':build_member_has_tags_json(member),
		'is_subscribed':member.is_subscribed,
		'pay_money': '%.2f' % member.pay_money,
		'pay_times': member.pay_times,
		'unit_price': '%.2f' % member.unit_price,
		'is_selected': member.is_selected,
		'is_current_select': member.is_current_select,
		'experience': member.experience
	}

def build_member_has_tags_json(member):
	member_has_tags = []
	for member_has_tag in MemberHasTag.get_member_has_tags(member):
		member_has_tag_dict = {}
		member_has_tag_dict['id'] = member_has_tag.member_tag.id
		member_has_tag_dict['name'] = member_has_tag.member_tag.name
		member_has_tags.append(member_has_tag_dict)
	return member_has_tags

def get_tags_json(request):
	webapp_id=request.user_profile.webapp_id
	tags = MemberTag.get_member_tags(webapp_id)

	tags_json = []
	for tag in tags:
		tags_json.append({'id':tag.id,'name': tag.name})

	return tags_json

def build_follow_member_basic_json(follow_member, member_id):
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

def __count_member_follow_relations(member):
	return MemberFollowRelation.objects.filter(member_id=member.id).count()

class MemberList(resource.Resource):
	app = 'member'
	resource = 'member_list'

	@login_required
	def get(request):
		"""
		get_memers: 会员列表
		"""
		mpuser = get_system_user_binded_mpuser(request.user)
		webapp_id  = request.user_profile.webapp_id
		#处理来自“数据罗盘-会员分析-关注会员链接”过来的查看关注会员的请求
		#add by duhao 2015-07-13
		status = request.GET.get('status' , '1')
		member_tags = MemberTag.get_member_tags(webapp_id)
		#调整排序，将为分组放在最前面
		tags = []
		for tag in member_tags:
			if tag.name == '未分组':
				tags = [tag] + tags
			else:
				tags.append(tag)
		member_tags = tags
		c = RequestContext(request, {
			'first_nav_name': export.MEMBER_FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': export.MEMBERS,
			#'should_show_authorize_cover' : get_should_show_authorize_cover(request),
			'user_tags': member_tags,
			'grades': MemberGrade.get_all_grades_list(webapp_id),
			'counts': Member.objects.filter(webapp_id=webapp_id,is_for_test=0, status__in= [SUBSCRIBED, CANCEL_SUBSCRIBED]).count(),
			'status': status
		})

		return render_to_response('member/editor/members.html', c)

	@login_required
	def api_get(request):
		"""
		获取会员列表

		URL: http://weapp.weizoom.com/member/api/members/get/?design_mode=0&version=1&filter_value=pay_times:0-1|first_pay:2015-04-08%2000:00--2015-04-30%2000:00&page=1&count_per_page=50&enable_paginate=1&timestamp=1435216368297&_=1435215905446

		"""
		pageinfo, request_members, total_count = get_request_members_list(request)

		# 构造返回数据
		return_members_jsonarray = []
		for member in request_members:
			return_members_jsonarray.append(build_return_member_json(member))

		tags_json = get_tags_json(request)

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




class MemberFilterParams(resource.Resource):
	app = "member"
	resource = "members_filter_params"

	@login_required
	def api_get(request):
		webapp_id = request.user_profile.webapp_id
		tags = []
		for tag in MemberTag.get_member_tags(webapp_id):
			if tag.name == '未分组':
				tags = [{"id": tag.id,"name": tag.name}] + tags
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