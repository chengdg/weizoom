# -*- coding: utf-8 -*-

__author__ = 'bert'

import export

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.db.models import Q
#import sys
from mall.models import Order, STATUS2TEXT

from modules.member.models import *
from watchdog.utils import watchdog_error
from weixin.user.models import DEFAULT_ICON, get_system_user_binded_mpuser
from excel_response import ExcelResponse
from market_tools.tools.coupon.util import get_coupon_rules, get_my_coupons
from market_tools.tools.member_qrcode.models import *
from apps.customerized_apps.shengjing.models import *

# from models import *
from core.restful_url_route import *

# import module_api as mall_api


@view(app='member', resource='members', action='get')
@login_required
def get_members(request):
	"""
	get_memers: 会员列表
	"""
	mpuser = get_system_user_binded_mpuser(request.user)
	webapp_id  = request.user_profile.webapp_id
	#处理来自“数据罗盘-会员分析-关注会员链接”过来的查看关注会员的请求
	#add by duhao 2015-07-13
	status = request.GET.get('status' , '1')
	c = RequestContext(request, {
		'first_nav_name': export.MEMBER_FIRST_NAV,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': export.MEMBERS,
		'should_show_authorize_cover' : get_should_show_authorize_cover(request),
		'user_tags': MemberTag.get_member_tags(webapp_id),
		'grades': MemberGrade.get_all_grades_list(webapp_id),
		'counts': Member.objects.filter(webapp_id=webapp_id,is_for_test=0, status__in= [SUBSCRIBED, CANCEL_SUBSCRIBED]).count(),
		'status': status
	})

	return render_to_response('member/editor/members.html', c)

def get_should_show_authorize_cover(request):
	mpuser = get_system_user_binded_mpuser(request.user)

	if (mpuser is None) or (not mpuser.is_certified) or (not mpuser.is_service):
		return True
	else:
		return False

@view(app='member', resource='member_tags', action='get')
@login_required
def list_tags(request):
	webapp_id = request.user_profile.webapp_id
	default_tag_id = MemberTag.get_default_tag(webapp_id).id
	member_tags = MemberTag.get_member_tags(webapp_id)
	#调整排序，将为分组放在最前面
	tags = []
	for tag in member_tags:
		if tag.name == '未分组':
			tags = [tag] + tags
		else:
			tags.append(tag)
	member_tags = tags
	if request.method == "GET":
		is_can_send = False
		from weixin.user.models import WeixinMpUser
		try:
			mp_user = WeixinMpUser.objects.get(owner_id=request.user_profile.user_id)
			if mp_user and mp_user.is_certified:
				is_can_send = True
		except:
			pass


		for member_tag in member_tags:
			member_tag.count = MemberHasTag.get_tag_has_member_count(member_tag)
		c = RequestContext(request, {
			'first_nav_name': export.MEMBER_FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': export.MEMBER_TAG,
			'member_tags': member_tags,
			'should_show_authorize_cover': get_should_show_authorize_cover(request),
			'success_count': UserSentMassMsgLog.success_count(webapp_id),
			'is_can_send': is_can_send
			#'pageinfo': json.dumps(paginator.to_dict(pageinfo))
			})
		return render_to_response('member/editor/member_tags.html', c)
	else:
		member_tag_ids = [member_tag.id for member_tag in member_tags]
		for tag in member_tags:
			print tag.name, "0000"
		print member_tag_ids, "11111"
		id_values = {}
		for key, value in request.POST.dict().items():
			id = key.split('_')[2]
			id_values[int(id)] = value
		for id in id_values.keys():
			value = id_values[id]
			print value
			#不能添加和更新名为‘未分组’的组名
			if value != '未分组':
				if MemberTag.objects.filter(id=id, webapp_id=webapp_id).count() > 0:
					MemberTag.objects.filter(id=id, webapp_id=webapp_id).update(name=value)
				else:
					print "^^^^^^^"
					MemberTag.objects.create(id=id, name=value, webapp_id=webapp_id)
		delete_ids = list(set(member_tag_ids).difference(set(id_values.keys())))
		if default_tag_id in delete_ids:
			delete_ids.remove(default_tag_id)
		print delete_ids, "2222"
		members = [m.member for m in MemberHasTag.objects.filter(member_tag_id__in=delete_ids)]
		MemberTag.objects.filter(id__in=delete_ids).delete()
		for m in members:
			if MemberHasTag.objects.filter(member=m).count() == 0:
				MemberHasTag.objects.create(member=m, member_tag_id=default_tag_id)
		for tag in MemberTag.objects.filter(webapp_id=webapp_id):
			print tag.name, "333"
		return HttpResponseRedirect('/member/member_tags/get/')


########################################################################
# list_grades: 获取会员等级分类
########################################################################
@view(app='member', resource='member_grades', action='get')
@login_required
def list_grades(request):
	webapp_id = request.user_profile.webapp_id
	default_grade = MemberGrade.get_default_grade(webapp_id)

	member_grades = MemberGrade.get_all_grades_list(webapp_id)
	if request.method == "GET":
		c = RequestContext(request, {
			'first_nav_name': export.MEMBER_FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': export.MEMBER_GRADE,
			'member_grades': member_grades,
			'shop_discounts': [1]*100,
			'should_show_authorize_cover' : get_should_show_authorize_cover(request)
		})
		return render_to_response('member/editor/member_grades.html', c)
	else:
		member_grade_ids = [grade.id for grade in member_grades]

		post_ids = []
		for key, value in request.POST.dict().items():
			if key.startswith('grade_id_'):
				post_ids.append(int(key.split('_')[2]))
		post_ids.sort()
		for id in post_ids:
			grade_name = request.POST.get('grade_id_%s' % id , 'get none value')
			grade_integral_term = request.POST.get('grade_integral_term_%s' % id , 0)
			grade_money_term = request.POST.get('grade_money_term_%s' % id , 0)
			grade_paytimes_term = request.POST.get('grade_paytimes_term_%s' % id , 0)
			shop_discount = request.POST.get('shop_discount_%s' % id , 100)
			if id == default_grade.id:
				MemberGrade.objects.filter(id=id).update(shop_discount=shop_discount, name=grade_name)
			elif id in member_grade_ids:
				MemberGrade.objects.filter(id=id).update(pay_money=grade_money_term, pay_times=grade_paytimes_term, integral=grade_integral_term, name=grade_name, shop_discount=shop_discount,)
			else:
				MemberGrade.objects.create(pay_money=grade_money_term, pay_times=grade_paytimes_term, integral=grade_integral_term, name=grade_name, webapp_id=webapp_id, upgrade_lower_bound=0, shop_discount=shop_discount,)

		delete_ids = list(set(member_grade_ids).difference(set(post_ids)))
		MemberGrade.objects.filter(id__in=delete_ids).delete()
		if delete_ids:
			from mall.module_api import update_promotion_status_by_member_grade
			update_promotion_status_by_member_grade(delete_ids)
		return HttpResponseRedirect('/member/member_grades/get/')

########################################################################
# member_qrocde: 推广扫描
########################################################################
@view(app='member', resource='member_qrcode', action='get')
@login_required
def member_qrocde(request):
	mpuser = get_system_user_binded_mpuser(request.user)

	if (mpuser is None) or (not mpuser.is_certified) or (not mpuser.is_service):
		should_show_authorize_cover = True
	else:
		should_show_authorize_cover = False

	coupon_rules = get_coupon_rules(request.user)
	member_qrcode_settings = MemberQrcodeSettings.objects.filter(owner=request.user)
	member_qrcode_setting = member_qrcode_settings[0] if member_qrcode_settings.count() > 0 else None
	if member_qrcode_setting:
		award_contents = MemberQrcodeAwardContent.objects.filter(member_qrcode_settings=member_qrcode_setting)
		if award_contents.count() > 0:
			award_content = award_contents[0] if member_qrcode_setting.award_member_type == 1 else None
		else:
			award_content = None
	else:
		award_contents = None
		award_content = None
	member_grades = MemberGrade.get_all_grades_list(request)

	if member_grades and award_contents:

		for member_grade in member_grades:
			content = award_contents.filter(member_level=member_grade.id)[0] if award_contents.filter(member_level=member_grade.id).count() > 0 else None
			if content:
				member_grade.award_type = content.award_type
				member_grade.award_content = content.award_content

	c = RequestContext(request, {
		'first_nav_name': export.MEMBER_FIRST_NAV,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': export.MEMBER_QRCODE,
		'member_grades': member_grades,
		'member_qrcode_settings': member_qrcode_setting,
		'coupon_rules': coupon_rules,
		'award_content': award_content,
		'member_grades': member_grades,
		'should_show_authorize_cover': should_show_authorize_cover,
		'is_hide_weixin_option_menu': True
	})

	return render_to_response('member/editor/member_qrcode.html', c)


########################################################################
# edit_member: 会员详情信息
########################################################################
@view(app='member', resource='member_detail', action='edit')
@login_required
def edit_member(request):
	webapp_id = request.user_profile.webapp_id
	member_id = request.GET.get('id', None)
	ship_infos = None
	orders = []
	#try:
	if member_id:
		member = Member.objects.get(id=member_id, webapp_id=webapp_id)
		orders = __get_member_orders(member)
		pay_money = 0
		pay_times = 0
		for order in orders:
			order.final_price = order.final_price + order.weizoom_card_money
			if order.status > 2:
				pay_money += order.final_price
				pay_times += 1

		member.pay_times = pay_times
		member.pay_money = pay_money
		try:
			member.unit_price = pay_money/pay_times
		except:
			member.unit_price = 0

		try:
			member.friend_count = __count_member_follow_relations(member)
		except:
			notify_message = u"更新会员好友数量失败:cause:\n{}".format(unicode_full_stack())
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
	coupons = get_my_coupons(member.id)

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

	shared_url_infos = __get_member_shared_urls(member)

	numbers = shared_url_infos.aggregate(Sum("followers"))
	# shared_url_lead_number = 0
	# if numbers["followers__sum"] is not None:
	# 	shared_url_lead_number = numbers["followers__sum"]

	numbers = shared_url_infos.aggregate(Sum("pv"))
	shared_url_pv = 0
	if numbers["pv__sum"] is not None:
		shared_url_pv = numbers["pv__sum"]

	qrcode_friends = 0
	if fans_count:
		qrcode_friends = fans_count.filter(source=SOURCE_MEMBER_QRCODE).count()

	shared_url_lead_number = fans_count.count() - qrcode_friends


	c = RequestContext(request, {
		'is_shengjing': is_shengjing,
		'shengjing_register_info': shengjing_register_info,
		'first_nav_name': export.MEMBER_FIRST_NAV,
		'show_member': member,
		'grades': MemberGrade.get_all_grades_list(member.webapp_id),
		'orders': orders,
		'ship_infos': ship_infos,
		'shared_url_infos': shared_url_infos,
		'show_member_info': __get_member_info(member),
		'member_browse_records': member_browse_records,
		'member_has_tags': member_has_tags,
		'fans_count': len(fans_count),
		'coupons': coupons,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': export.MEMBERS,
		'shared_url_lead_number':shared_url_lead_number,
		'shared_url_pv':shared_url_pv,
		'qrcode_friends':qrcode_friends,
	})
	return render_to_response('member/editor/member_detail.html', c)

def __count_member_follow_relations(member):
	count = 0
	for member_follow_relation in MemberFollowRelation.objects.filter(member_id=member.id):
		try:
			follower_member = Member.objects.get(id=member_follow_relation.follower_member_id)
			if follower_member.status != NOT_SUBSCRIBED:
				count = count + 1
		except:
			continue

	return count

def __get_member_orders(member):
	if member is None:
		return None
	webapp_user_ids = member.get_webapp_user_ids
	return Order.objects.filter(webapp_user_id__in=webapp_user_ids).order_by("-created_at")

def __get_member_shared_urls(member):
	return MemberSharedUrlInfo.objects.filter(member_id=member.id)

def __get_member_ship_info(member):
	if member is None:
		return None

	webapp_user = WebAppUser.from_member(member)
	if webapp_user is None:
		notify_message = u"获取会员对应webappuser失败，member id:{}".format(member.id)
		watchdog_error(notify_message)
		return None

	return webapp_user.ship_info

def __get_member_info(member):
	try:
		return MemberInfo.objects.get(member_id=member.id)
	except:
		return None


########################################################################
# show_member: 会员详情信息
########################################################################
from weixin2.models import get_opid_from_session
@view(app='member', resource='members', action='export')
@login_required
def export_members(request):
	filter_value = request.GET.get('filter_value', None)
	filter_data_args = {}
	filter_data_args['webapp_id'] = request.user_profile.webapp_id
	filter_data_args['is_for_test'] = False
	filter_data_args['status__in'] = [SUBSCRIBED, CANCEL_SUBSCRIBED]

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
				elif value in ['0','1']:
					filter_data_args['source__in'] = [0,-1]
				else:
					filter_data_args["source"] = value

			if key in ['pay_times', 'pay_money', 'friend_count', 'unit_price']:
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

			if key in ['first_pay', 'sub_date', 'integral'] :
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

	members = Member.objects.filter(**filter_data_args)

	members_info = [
		[u'ID', u'昵称',u'性别',u'备注名',
		 u'姓名',u'电话',u'QQ',u'微博',u'备注',u'积分',u'经验值',u'会员等级',u'好友数',u'好友关系',
		 u'贡献数',u'贡献关系',u'来源',u'加入时间',u'分享总数',u'分享链接',u'链接点击',u'订单数',u'订单号',u'金额',u'状态',u'社交因子']
	]

	for member in members:

		count_list = []
		id = member.id
		nike_name = member.username
		try:
			nike_name = nike_name.decode('utf8')
		except:
			nike_name = member.username_hexstr
		remarks_name = member.remarks_name
		integral = member.integral
		experience = member.experience
		grade = member.grade.name


		friend_members = MemberFollowRelation.get_follow_members_for(member.id)
		friend_count = len(friend_members)
		count_list.append(friend_count)

		fans_members  = MemberFollowRelation.get_follow_members_for(member.id, '1')
		fans_count = len(fans_members)
		count_list.append(fans_count)

		factor = member.factor
		source = member.source
		created_at = member.created_at

		if source == 0:
			source = u'直接关注'

		if source == 1:
			source = u'推广扫描'

		if source == 2:
			source = u'会员分享'

		if source == -1:
			source = u'直接关注'

		shared_url_infos = MemberSharedUrlInfo.get_member_share_url_info(member.id)
		share_urls_count = len(shared_url_infos)
		count_list.append(share_urls_count)

		member_orders = __get_member_orders(member)

		if member_orders != None:
			member_orders_count = len(member_orders)
		else:
			member_orders_count = 0
			member_orders = []
		count_list.append(member_orders_count)

		member_info =  MemberInfo.get_member_info(member.id)
		name = u''
		sex = u''
		phone_number = u''
		qq_number = u''
		weibo_nickname = u''
		member_remarks = u''
		if member_info:
			name = member_info.name
			sex = member_info.sex
			if sex != -1:
				if sex == 1:
					sex = u'男'
				elif sex == 2:
					sex = u'女'
				else:
					sex = u'未知'
			else:
				sex = u'未知'
			phone_number = member_info.phone_number
			qq_number = member_info.qq_number
			weibo_nickname = member_info.weibo_nickname
			member_remarks = member_info.member_remarks

		max_count = max(count_list)
		if max_count == 0:
			max_count = 1
		for index in range(max_count):
			share_url = shared_url_infos[index] if share_urls_count > index else None
			if share_url:
				share_url_title = share_url.title
				pv = share_url.pv
			else:
				share_url_title = ''
				pv = ''

			member_order = member_orders[index] if member_orders_count > index else None
			if member_order:
				order_id = member_order.order_id
				status = STATUS2TEXT[member_order.status]
				final_price = member_order.final_price
			else:
				order_id = ''
				status = ''
				final_price = ''

			friend_member = friend_members[index] if friend_count > index else None
			if friend_member:
				friend_name = friend_member.username
				try:
					friend_name = friend_name.decode('utf8')
				except:
					friend_name = friend_member.username_hexstr
			else:
				friend_name = ''

			fans_member = fans_members[index] if fans_count > index else None
			if fans_member:
				fans_name = fans_member.username
				try:
					fans_name = fans_name.decode('utf8')
				except:
					fans_name = fans_member.username_hexstr
			else:
				fans_name = ''

			if index == 0:
				info_list = [ id,
						nike_name,
						sex,
						remarks_name,
						name,
						phone_number,
						qq_number,
						weibo_nickname,
						member_remarks,
						integral,
						experience,
						grade,
						friend_count,
						friend_name,
						fans_count,
						fans_name,
						source,
						created_at,
						share_urls_count,
						share_url_title,
						pv,
						member_orders_count,
						order_id,
						final_price,
						status,
						factor
					]
			else:
				info_list = ['',
						'',
						'',
						'',
						'',
						'',
						'',
						'',
						'',
						'',
						'',
						'',
						'',
						friend_name,
						'',
						fans_name,
						'',
						'',
						'',
						share_url_title,
						pv,
						'',
						order_id,
						final_price,
						status,
						''
					]

			members_info.append(info_list)

	return ExcelResponse(members_info,output_name=u'会员列表'.encode('utf8'),force_csv=False)
