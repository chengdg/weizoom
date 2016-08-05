#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.db.models import Q
from django.conf import settings

from core.jsonresponse import JsonResponse, create_response
from core.exceptionutil import unicode_full_stack
from core import paginator
#import sys
from mall.models import Order, STATUS2TEXT, ORDER_STATUS_SUCCESSED

from modules.member.models import *
from watchdog.utils import watchdog_error
from weixin.user.models import DEFAULT_ICON, get_system_user_binded_mpuser
from excel_response import ExcelResponse
from market_tools.tools.coupon.util import get_coupon_rules, get_my_coupons
from market_tools.tools.member_qrcode.models import *
from apps.customerized_apps.shengjing.models import *
from weixin2.models import get_opid_from_session
from core import resource

from market_tools.tools.coupon.util import get_member_coupons

import export
from export_job.models import ExportJob
from datetime import datetime
import time
#from modules.member.models import *
from utils.dateutil import now,get_date_after_days


COUNT_PER_PAGE = 20

def get_request_members_list(request, export=False):
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
	if not filter_value:
		if status == '1':
			filter_data_args['is_subscribed'] = True
		elif status == '0':
			filter_data_args['is_subscribed'] = False
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
				# member_ids = [member.id for member in  MemberHasTag.get_member_list_by_tag_id(value)]
				# member_ids = [member_has_tag.member.id for member_has_tag in  MemberHasTag.objects.filter(member_tag_id=value)]
				member_ids = list(MemberHasTag.objects.filter(member_tag_id=value).values_list('member_id', flat=True))
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

			if key in ['first_pay', 'sub_date', 'cancel_subscribe'] :
				if value.find('-') > -1:
					val1,val2 = value.split('--')
					if key == 'first_pay':
						filter_data_args['last_pay_time__gte'] = val1
						filter_data_args['last_pay_time__lte'] =  val2
					elif key == 'sub_date':

						filter_data_args['created_at__gte'] = val1
						filter_data_args['created_at__lte'] = val2
					elif key == 'cancel_subscribe':
						filter_data_args['cancel_subscribe_time__gte'] = val1
						filter_data_args['cancel_subscribe_time__lte'] = val2
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
	# print '################################################'
	# print filter_data_args
	# print '################################################'

	members = Member.objects.filter(**filter_data_args).order_by(sort_attr)

	if export:
		# return members
		return filter_data_args,sort_attr

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

	return pageinfo, members, total_count


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
		'fans_count': member.fans_count,
		'tags':build_member_has_tags_json(member),
		'is_subscribed':member.is_subscribed,
		'pay_money': '%.2f' % member.pay_money,
		'pay_times': member.pay_times,
		'unit_price': '%.2f' % member.unit_price,
		'is_selected': member.is_selected,
		'is_current_select': member.is_current_select,
		'experience': member.experience,
		'purchase_frequency':member.purchase_frequency,
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
		'is_subscribed': follow_member.is_subscribed,
		'is_fans': MemberFollowRelation.is_fan(member_id, follow_member.id),
		'is_father': MemberFollowRelation.is_father(member_id, follow_member.id),
		'pay_money': '%.2f' % follow_member.pay_money,
		'pay_times': follow_member.pay_times,
		'father_name': father_name,
		'father_id': father_id
	}


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
		#获取未完成的任务
		woid = request.webapp_owner_id
		export_jobs = ExportJob.objects.filter(woid=woid,type=0,is_download=0).order_by("-id")
		if export_jobs:
			export2data = {
				"woid":int(export_jobs[0].woid) ,#
				"status":1 if export_jobs[0].status else 0,
				"is_download":1 if export_jobs[0].is_download else 0,
				"id":int(export_jobs[0].id),
				# "file_path": export_jobs[0].file_path,
				}
		else:
			export2data = {
				"woid":0,
				"status":1,
				"is_download":1,
				"id":0,
				"file_path":0,
				}
			
		c = RequestContext(request, {
			'first_nav_name': export.MEMBER_FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': export.MEMBERS,
			#'should_show_authorize_cover' : get_should_show_authorize_cover(request),
			'user_tags': member_tags,
			'grades': MemberGrade.get_all_grades_list(webapp_id),
			'counts': Member.objects.filter(webapp_id=webapp_id,is_for_test=0, status__in= [SUBSCRIBED, CANCEL_SUBSCRIBED]).count(),
			'status': status,
			'export2data': export2data,
		})

		return render_to_response('member/editor/members.html', c)

	@login_required
	def api_get(request):
		"""
		获取会员列表

		URL: http://weapp.weizoom.com/member/api/member_list/?design_mode=0&version=1&filter_value=pay_times:0-1|first_pay:2015-04-08%2000:00--2015-04-30%2000:00&page=1&count_per_page=50&enable_paginate=1&timestamp=1435216368297&_=1435215905446

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

def count_member_follow_relations(member):
	count = 0
	for member_follow_relation in MemberFollowRelation.objects.filter(member_id=member.id):
		try:
			follower_member = Member.objects.get(id=member_follow_relation.follower_member_id)
			if follower_member.status != NOT_SUBSCRIBED:
				count = count + 1
		except:
			continue

	return count

def get_member_orders(member):
	if member is None:
		return None
	webapp_user_ids = member.get_webapp_user_ids
	return Order.by_webapp_user_id(webapp_user_ids).order_by("-created_at")

def get_member_shared_urls(member):
	return MemberSharedUrlInfo.objects.filter(member_id=member.id)

def get_member_ship_info(member):
	if member is None:
		return None

	webapp_user = WebAppUser.from_member(member)
	if webapp_user is None:
		notify_message = u"获取会员对应webappuser失败，member id:{}".format(member.id)
		watchdog_error(notify_message)
		return None

	return webapp_user.ship_info

def get_member_info(member):
	try:
		return MemberInfo.objects.get(member_id=member.id)
	except:
		return None

def get_purchased_fans(follow_members):
	count = 0
	for follow_member in follow_members:
		user_orders = Order.get_orders_from_webapp_user_ids(follow_member.get_webapp_user_ids)
		if user_orders and user_orders.filter(status=5).count() > 0:
			count += 1
	return count

import logging
class MemberDetail(resource.Resource):
	app = "member"
	resource = "detail"

	@login_required
	def get(request):
		webapp_id = request.user_profile.webapp_id
		member_id = request.GET.get('id', None)
		ship_infos = None
		orders = []
		weizoom_card_total_money = 0
		#try:
		if member_id:
			member = Member.objects.get(id=member_id, webapp_id=webapp_id)
			orders = get_member_orders(member)
			pay_money = 0
			pay_times = 0
			if orders.filter(status__gte=2).count() > 0:
				payment_time = orders.order_by('-payment_time')[0].payment_time
				member.last_pay_time = payment_time
			for order in orders:
				order.final_price = order.final_price + order.weizoom_card_money
				if order.status == 5:
					pay_money += order.final_price
					pay_times += 1
					weizoom_card_total_money += order.weizoom_card_money

			member.pay_times = pay_times
			member.pay_money = pay_money
			try:
				member.unit_price = pay_money/pay_times
			except:
				member.unit_price = 0

			try:
				member.friend_count = count_member_follow_relations(member)
			except:
				notify_message = u"更新会员好友数量失败:cause:\n{}".format(unicode_full_stack())
				watchdog_error(notify_message)
			try:
				date_before_30 = get_date_after_days(now(),-30).strftime("%Y-%m-%d")
				webapp_user_ids = member.get_webapp_user_ids
				purchase_count_30days = Order.objects.filter(webapp_user_id__in=webapp_user_ids, payment_time__gte=date_before_30,status=ORDER_STATUS_SUCCESSED,origin_order_id__lte=0).count()
				member.purchase_frequency = purchase_count_30days
			except:
				notify_message = u"更新会员30天购买次数失败:cause:\n{}".format(unicode_full_stack())
				watchdog_error(notify_message)
			member.save()
		else:
			raise Http404(u"不存在该会员")
		#except:
		#	raise Http404(u"不存在该会员")
		from modules.member.member_info_util import update_member_basic_info
		if (not member.user_icon or not member.username_hexstr) and (settings.MODE != 'develop'):
			update_member_basic_info(request.user_profile, member)

		#完善会员的基本信息
		if member.user_icon:
			member.user_icon = member.user_icon if len(member.user_icon.strip()) > 0 else DEFAULT_ICON
		else:
			member.user_icon = DEFAULT_ICON

		if member.unit_price > 0:
			member.unit_price = '%.2f' % member.unit_price

		if member.pay_money > 0:
			member.pay_money = '%.2f' % member.pay_money

		member_browse_records = MemberBrowseRecord.objects.filter(~Q(title=''), member=member).order_by('-created_at')

		#会员标签
		webapp_id  = request.user_profile.webapp_id

		member_has_tags = MemberHasTag.get_member_has_tags(member)

		fans_count = MemberFollowRelation.get_follow_members_for(member.id, '1')

		#我的优惠券
		coupons = get_member_coupons(member)

		# 组织盛景定制信息
		shengjing_register_info = dict()
		if request.user.username == 'shengjing360':
			is_shengjing = True
			try:
				sj_binding_member = ShengjingBindingMember.objects.get(member_id=member_id)
				sj_binding_member_info= ShengjingBindingMemberInfo.objects.get(binding_id=sj_binding_member.id)
				sj_binding_member_companys= ShengjingBindingMemberHasCompanys.objects.filter(binding_id=sj_binding_member.id)
				shengjing_register_info['phone_number'] = sj_binding_member.phone_number
				shengjing_register_info['position'] = sj_binding_member_info.position
				shengjing_register_info['status'] = sj_binding_member_info.status_name
				if sj_binding_member_info.status == LEADER:
					shengjing_register_info['is_leader'] = u'是'
				else:
					shengjing_register_info['is_leader'] = u'否'
				shengjing_register_info['crm_name'] = sj_binding_member_info.name
				shengjing_register_info['crm_companys'] = []
				for company in sj_binding_member_companys:
					shengjing_register_info['crm_companys'].append(company.name)
				shengjing_register_info['name'] = shengjing_register_info['crm_name']
				shengjing_register_info['companys'] = shengjing_register_info['crm_companys']
				# 如果未绑定CRM，则crm_name与crm_companys置空
				if sj_binding_member_info.status == STAFF or sj_binding_member_info.status == LEADER:
					pass
				else:
					shengjing_register_info['crm_name'] = ''
					shengjing_register_info['crm_companys'] = []
				shengjing_register_info['phone_number'] = sj_binding_member.phone_number
			except:
				notify_message = u"shengjing360:cause:\n{}".format(unicode_full_stack())
				watchdog_error(notify_message)
		else:
			is_shengjing = False

			webapp_user_ids = member.get_webapp_user_ids

			ship_infos = ShipInfo.objects.filter(webapp_user_id__in=webapp_user_ids)
			for ship_info in ship_infos:
				province = ''
				city = ''
				village = ''
				if ship_info.get_str_area:
					area_list  = ship_info.get_str_area.split(' ')
					if len(area_list) == 3:
						province = area_list[0]
						city = area_list[1]
						village = area_list[2]
					elif len(area_list) == 2:
						province = area_list[0]
						city = area_list[1]
					else:
						province = area_list[0]

				ship_info.province = province
				ship_info.city = city
				ship_info.village = village

		shared_url_infos = get_member_shared_urls(member)

		numbers = shared_url_infos.aggregate(Sum("followers"))
		# shared_url_lead_number = 0
		# if numbers["followers__sum"] is not None:
		# 	shared_url_lead_number = numbers["followers__sum"]

		numbers = shared_url_infos.aggregate(Sum("pv"))
		shared_url_pv = 0
		if numbers["pv__sum"] is not None:
			shared_url_pv = numbers["pv__sum"]

		qrcode_friends = 0
		purchased_fans = 0
		if fans_count:
			qrcode_friends = fans_count.filter(source=SOURCE_MEMBER_QRCODE).count()
			purchased_fans = get_purchased_fans(fans_count)
			# for follow_member in fans_count:
			# 	if Order.get_orders_from_webapp_user_ids(follow_member.get_webapp_user_ids).filter(status=5).count() >0:
			# 		purchased_fans += 1

		shared_url_lead_number = fans_count.count() - qrcode_friends

		if purchased_fans:
			conversion_rate = "%.2f" % (float(purchased_fans) / float(fans_count.count()) * 100)
		else:
			conversion_rate = 0
		#微众卡使用金额
		if member:
			member.weizoom_card_total_money = weizoom_card_total_money
		if member.fans_count != len(fans_count):
			Member.objects.filter(id=member.id).update(fans_count=len(fans_count))


		c = RequestContext(request, {
			'is_shengjing': is_shengjing,
			'shengjing_register_info': shengjing_register_info,
			'first_nav_name': export.MEMBER_FIRST_NAV,
			'show_member': member,
			'grades': MemberGrade.get_all_grades_list(member.webapp_id),
			'orders': orders,
			'ship_infos': ship_infos,
			'shared_url_infos': shared_url_infos,
			'show_member_info': get_member_info(member),
			'member_browse_records': member_browse_records,
			'member_has_tags': member_has_tags,
			'fans_count': len(fans_count),
			'coupons': coupons,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': export.MEMBERS,
			'shared_url_lead_number':shared_url_lead_number,
			'shared_url_pv':shared_url_pv,
			'qrcode_friends':qrcode_friends,
			'purchased_fans': purchased_fans,
			'conversion_rate': conversion_rate
		})
		return render_to_response('member/editor/member_detail.html', c)

	@login_required
	def api_post(request):
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
			if member_remarks != None:
				member_info_update['member_remarks'] = member_remarks
			if name:
				member_info_update['name'] = name
			if phone_number:
				member_infos = MemberInfo.objects.filter(phone_number=phone_number.strip(), is_binded=True)
				if member_infos:
					member_ids = [member_info.member_id for member_info in member_infos]
					members = Member.objects.filter(webapp_id=webapp_id,id__in=member_ids)
					member_count = members.exclude(id=member_id).count()
					if member_count > 0:
						response = create_response(400)
						response.errMsg = u'该号码已绑定其他微信号'
						return response.get_response()
					else:
						member_info_update['phone_number'] = phone_number.strip()

				else:
					member_info_update['phone_number'] = phone_number.strip()

			if sex != None:
				member_info_update['sex'] = sex
				member.sex = sex
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



class MemberIntegral(resource.Resource):
	app = "member"
	resource = "integral_logs"

	@login_required
	def api_get(request):
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

class Integral(resource.Resource):
	app='member'
	resource='integral'
	@login_required
	def api_post(request):

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
		response.data = {
			'integral': Member.objects.get(webapp_id=webapp_id, id=member_id).integral
		}
		return response.get_response()


class MemberFriends(resource.Resource):
	app='member'
	resource='follow_relations'

	@login_required
	def api_get(request):
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
			elif data_value == 'purchase':
				follow_members=  MemberFollowRelation.get_follow_members_purchase_for(member_id)
			else:
				follow_members = []
		else:
			follow_members = MemberFollowRelation.get_follow_members_for(member_id, only_fans)

		#增加计算follow_members的人数、下单人数、成交金额
		if follow_members:
			population = follow_members.count()
			population_order  = get_purchased_fans(follow_members)
		else:
			population = 0
			population_order = 0
		# for follow_member in follow_members:
		# 	user_orders = Order.get_orders_from_webapp_user_ids(follow_member.get_webapp_user_ids)
		# 	if user_orders and user_orders.filter(status=5).count() > 0:
		# 		population_order += 1
		# #成交金额
		amount = 0
		for follow_member in follow_members:
			amount += follow_member.pay_money

		#增加计算follow_members的人数、下单人数、成交金额

		#进行排序
		if follow_members:
			follow_members = follow_members.order_by(sort_attr)
			if data_value:
				filter_date_follow_members = follow_members
			else:
				filter_date_follow_members = []
		else:
			filter_date_follow_members = []
		#进行分页
		count_per_page = int(request.GET.get('count_per_page', 8))
		cur_page = int(request.GET.get('page', '1'))
		pageinfo, follow_members = paginator.paginate(follow_members, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

		return_follow_members_json_array = []

		# if data_value:
		# 	follow_members = filter_date_follow_members

		for follow_member in follow_members:
			return_follow_members_json_array.append(build_follow_member_basic_json(follow_member, member_id))


		response = create_response(200)
		response.data = {
			'items': return_follow_members_json_array,
			'pageinfo': paginator.to_dict(pageinfo),
			'only_fans':only_fans,
			'sortAttr': request.GET.get('sort_attr', '-created_at'),
			'population': population,
			'population_order': population_order,
			'amount': '%.2f' % amount,
			'data_value': data_value
		}
		return response.get_response()


from weixin2.models import get_opid_from_session
# class MemberExport(resource.Resource):
# 	app = 'member'
# 	resource = 'export'

# 	@login_required
# 	def get(request):
# 		members = get_request_members_list(request, True)

# 		members_info = [
# 			[u'ID', u'昵称',u'性别',u'备注名',
# 			 u'姓名',u'电话',u'QQ',u'微博',u'备注',u'积分',u'经验值',u'会员等级',u'好友数',u'好友关系',
# 			 u'贡献数',u'贡献关系',u'来源',u'加入时间',u'分享总数',u'分享链接',u'链接点击',u'订单数',u'订单号',u'金额',u'状态',u'社交因子']
# 		]

# 		for member in members:

# 			count_list = []
# 			id = member.id
# 			nike_name = member.username
# 			try:
# 				nike_name = nike_name.decode('utf8')
# 			except:
# 				nike_name = member.username_hexstr
# 			remarks_name = member.remarks_name
# 			integral = member.integral
# 			experience = member.experience
# 			grade = member.grade.name


# 			friend_members = MemberFollowRelation.get_follow_members_for(member.id)
# 			friend_count = len(friend_members)
# 			count_list.append(friend_count)

# 			fans_members  = MemberFollowRelation.get_follow_members_for(member.id, '1')
# 			fans_count = len(fans_members)
# 			count_list.append(fans_count)

# 			factor = member.factor
# 			source = member.source
# 			created_at = member.created_at

# 			if source == 0:
# 				source = u'直接关注'

# 			if source == 1:
# 				source = u'推广扫描'

# 			if source == 2:
# 				source = u'会员分享'

# 			if source == -1:
# 				source = u'直接关注'

# 			shared_url_infos = MemberSharedUrlInfo.get_member_share_url_info(member.id)
# 			share_urls_count = len(shared_url_infos)
# 			count_list.append(share_urls_count)

# 			member_orders = get_member_orders(member)

# 			if member_orders != None:
# 				member_orders_count = len(member_orders)
# 			else:
# 				member_orders_count = 0
# 				member_orders = []
# 			count_list.append(member_orders_count)

# 			member_info =  MemberInfo.get_member_info(member.id)
# 			name = u''
# 			sex = u''
# 			phone_number = u''
# 			qq_number = u''
# 			weibo_nickname = u''
# 			member_remarks = u''
# 			if member_info:
# 				name = member_info.name
# 				sex = member_info.sex
# 				if sex != -1:
# 					if sex == 1:
# 						sex = u'男'
# 					elif sex == 2:
# 						sex = u'女'
# 					else:
# 						sex = u'未知'
# 				else:
# 					sex = u'未知'
# 				phone_number = member_info.phone_number
# 				qq_number = member_info.qq_number
# 				weibo_nickname = member_info.weibo_nickname
# 				member_remarks = member_info.member_remarks

# 			max_count = max(count_list)
# 			if max_count == 0:
# 				max_count = 1
# 			for index in range(max_count):
# 				share_url = shared_url_infos[index] if share_urls_count > index else None
# 				if share_url:
# 					share_url_title = share_url.title
# 					pv = share_url.pv
# 				else:
# 					share_url_title = ''
# 					pv = ''

# 				member_order = member_orders[index] if member_orders_count > index else None
# 				if member_order:
# 					order_id = member_order.order_id
# 					status = STATUS2TEXT[member_order.status]
# 					final_price = member_order.final_price
# 				else:
# 					order_id = ''
# 					status = ''
# 					final_price = ''

# 				friend_member = friend_members[index] if friend_count > index else None
# 				if friend_member:
# 					friend_name = friend_member.username
# 					try:
# 						friend_name = friend_name.decode('utf8')
# 					except:
# 						friend_name = friend_member.username_hexstr
# 				else:
# 					friend_name = ''

# 				fans_member = fans_members[index] if fans_count > index else None
# 				if fans_member:
# 					fans_name = fans_member.username
# 					try:
# 						fans_name = fans_name.decode('utf8')
# 					except:
# 						fans_name = fans_member.username_hexstr
# 				else:
# 					fans_name = ''

# 				if index == 0:
# 					info_list = [ id,
# 							nike_name,
# 							sex,
# 							remarks_name,
# 							name,
# 							phone_number,
# 							qq_number,
# 							weibo_nickname,
# 							member_remarks,
# 							integral,
# 							experience,
# 							grade,
# 							friend_count,
# 							friend_name,
# 							fans_count,
# 							fans_name,
# 							source,
# 							created_at,
# 							share_urls_count,
# 							share_url_title,
# 							pv,
# 							member_orders_count,
# 							order_id,
# 							final_price,
# 							status,
# 							factor
# 						]
# 				else:
# 					info_list = ['',
# 							'',
# 							'',
# 							'',
# 							'',
# 							'',
# 							'',
# 							'',
# 							'',
# 							'',
# 							'',
# 							'',
# 							'',
# 							friend_name,
# 							'',
# 							fans_name,
# 							'',
# 							'',
# 							'',
# 							share_url_title,
# 							pv,
# 							'',
# 							order_id,
# 							final_price,
# 							status,
# 							''
# 						]

# 				members_info.append(info_list)

# 		return ExcelResponse(members_info,output_name=u'会员列表'.encode('utf8'),force_csv=False)


class MemberGetFile(resource.Resource):
	"""
	获取参数，构建成文件，上传到u盘运
	"""
	app = "member"
	resource ="export_file_param"
	
	@login_required
	def api_get(request):
		woid = request.webapp_owner_id
		type = int(request.GET.get('type', 0))

		now = datetime.now()
		#判断用户是否存在导出数据任务
		if type == 0:
			param ,sort_attr = get_request_members_list(request, True)
		exportjob = ExportJob.objects.create(
									woid = woid,
									type = type,
									status = 0,
									param = param,
									created_at = now,
									processed_count =0,
									count =0,
									)
		from member.tasks import send_export_job_task
		send_export_job_task.delay(exportjob.id, param, sort_attr, type)

		response = create_response(200)
		response.data = {
			'ok':'ok',
			"exportjob_id":exportjob.id,
		}
		return response.get_response()


class MemberOrders(resource.Resource):
	app='member'
	resource='order_list'

	@login_required
	def api_get(request):
		webapp_id = request.user_profile.webapp_id
		member_id = request.GET.get('id', None)
		cur_page = int(request.GET.get('page', '1'))
		count = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		orders = []
		if member_id:
			member = Member.objects.get(id=member_id, webapp_id=webapp_id)
			webapp_user_ids = member.get_webapp_user_ids
			orders = Order.by_webapp_user_id(webapp_user_ids).order_by("-created_at","-id")

			pay_money = 0
			orders_valid = orders.filter(status=ORDER_STATUS_SUCCESSED)
			for order in orders_valid:
				order_final_price = order.final_price + order.weizoom_card_money
				pay_money += order_final_price
			total_count = orders.count()
			pageinfo, orders = paginator.paginate(orders, cur_page, count)
		
		items = []
		for order in orders:
			items.append({
				"id": order.id,
				"order_id": order.order_id,
				"final_price": float('%.2f' % (order.final_price+order.weizoom_card_money)),
				"created_at": datetime.strftime(order.created_at, '%Y-%m-%d %H:%M:%S'),
				"order_status": order.status,
				})
		response = create_response(200)
		response.data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'pay_money': '%.2f' % pay_money,
		}
		return response.get_response()

#by bert
class MemberSpread(resource.Resource):
	app='member'
	resource='spread'

	@login_required
	def api_get(request):
		webapp_id = request.user_profile.webapp_id
		member_id = request.GET.get('member_id', None)
		cur_page = int(request.GET.get('page', '1'))
		count = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		shared_url_infos = []
		if member_id:
			member = Member.objects.get(id=member_id, webapp_id=webapp_id)
			shared_url_infos = get_member_shared_urls(member)
		pageinfo, shared_url_infos = paginator.paginate(shared_url_infos, cur_page, count)
		items = []
		for shared_url_info in shared_url_infos:
			items.append({
				"id": shared_url_info.id,
				"title": shared_url_info.title,
				"pv": shared_url_info.pv,
				"followers": shared_url_info.followers,
				"leadto_buy_count": shared_url_info.leadto_buy_count,
				})
		response = create_response(200)
		response.data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo)
		}
		return response.get_response()
