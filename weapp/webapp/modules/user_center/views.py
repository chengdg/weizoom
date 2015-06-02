# -*- coding: utf-8 -*-

__author__ = 'chuter'

import export

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.db.models import Q
import sys
from webapp.modules.mall.models import Order, STATUS2TEXT

from modules.member.models import *
from watchdog.utils import watchdog_error
from weixin.user.models import DEFAULT_ICON, get_system_user_binded_mpuser
from excel_response import ExcelResponse
from market_tools.tools.member_qrcode.models import *
from apps.customerized_apps.shengjing.models import *
from market_tools.tools.coupon.util import get_my_coupons

FIRST_NAV_NAME = 'webapp'
WEAPP_USER_CENTER_NAV_NAME = 'usercenter-memberlist'
WEAPP_USER_CENTER_OTHER_OPTIONS_NAV_NAME = 'usercenter-grades'

########################################################################
# get_user_center: 用户中心
########################################################################
@login_required
def list_memers(request):
	mpuser = get_system_user_binded_mpuser(request.user)
	webapp_id  = request.user_profile.webapp_id
	
	
	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV_NAME,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': WEAPP_USER_CENTER_NAV_NAME,
		'should_show_authorize_cover' : get_should_show_authorize_cover(request),
		'user_tags': MemberTag.get_member_tags(webapp_id),
		'grades': MemberGrade.get_all_grades_list(webapp_id),
		'counts': Member.objects.filter(webapp_id=webapp_id,is_for_test=0).count()
	})

	return render_to_response('user_center/editor/user_center.html', c)

def get_should_show_authorize_cover(request):
	mpuser = get_system_user_binded_mpuser(request.user)

	if (mpuser is None) or (not mpuser.is_certified) or (not mpuser.is_service):
		return True
	else:
		return False

def __get_member_orders(member):
	if member is None:
		return None

	webapp_user = WebAppUser.from_member(member)
	if webapp_user is None:
		notify_message = u"获取会员对应webappuser失败，member id:{}".format(member.id)
		watchdog_error(notify_message)
		return None
	
	return Order.objects.filter(webapp_user_id=webapp_user.id).order_by("-created_at")

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
	return MemberInfo.objects.get(member_id=member.id)

def __count_member_follow_relations(member):
	return MemberFollowRelation.objects.filter(member_id=member.id).count()	

########################################################################
# show_member: 会员详情信息
########################################################################
@login_required
def show_member(request, member_id):
	try:
		member = Member.objects.get(id=member_id)
		member.friend_count = __count_member_follow_relations(member)
		member.save()
	except:
		raise Http404(u"不存在该会员")

	#完善会员的基本信息
	if member.user_icon:
		member.user_icon = member.user_icon if len(member.user_icon.strip()) > 0 else DEFAULT_ICON
	else:
		member.user_icon = DEFAULT_ICON
	member_browse_records = MemberBrowseRecord.objects.filter(~Q(title=''), member=member).order_by('-created_at')
	
	#会员标签
	webapp_id  = request.user_profile.webapp_id
	member_tags = []
	notmemer_tags = []
	for tag in MemberTag.get_member_tags(webapp_id):
		if MemberHasTag.is_member_tag(member, tag):
			tag.is_member_tag = True
			member_tags.append(tag)
		else:
			tag.is_member_tag = False
			notmemer_tags.append(tag)

	member_tags.extend(notmemer_tags)
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
			watchdog_error(u'该用户已解除绑定或信息不存在， member_id = %s' % member_id, 'WEB', request.user.id)
	else:
		is_shengjing = False

	c = RequestContext(request, {
		'is_shengjing': is_shengjing,
		'shengjing_register_info': shengjing_register_info,
		'first_nav_name': FIRST_NAV_NAME,
		'show_member': member,
		'grades': MemberGrade.get_all_grades_list(member.webapp_id),
		'orders': __get_member_orders(member),
		'shipInfo': __get_member_ship_info(member),
		'shared_url_infos': __get_member_shared_urls(member),
		'show_member_info': __get_member_info(member),
		'member_browse_records': member_browse_records,
		'member_tags': member_tags,
		'fans_count': len(fans_count),
		'coupons': coupons
	})
	return render_to_response('user_center/editor/detail_user.html', c)


########################################################################
# update_member: 更新会员
########################################################################
@login_required
def update_member(request, member_id):
	if request.POST:
		Member.objects.filter(id=member_id).update(
			integral = request.POST.get('integral', '').strip(),
			grade = MemberGrade.objects.get(id=int(request.POST.get('grade_id'))),
			remarks_name = request.POST.get('remarks_name', '').strip(),
			remarks_extra = request.POST.get('remarks_extra', '').strip()
		)

		MemberInfo.objects.filter(member_id=member_id).update(
			name = request.POST.get('name', '').strip(),
			sex = int(request.POST.get('sex', SEX_TYPE_UNKOWN).strip()),
			phone_number = request.POST.get('phone_number', '').strip()
			)

		

		return HttpResponseRedirect('/webapp/user_center/')
	else:
		return HttpResponseRedirect('/webapp/user_center/editor/detail/{}/'.format(member_id))

########################################################################
# show_member_integral_log: 用户积分日志
########################################################################
@login_required
def show_member_integral_log(request, member_id):
	member_logs = MemberIntegralLog.objects.filter(member_id=member_id).order_by('-created_at')
	for member_log in member_logs:
		if member_log.member:
			try:
				member = Member.objects.get(token=member_log.follower_member_token)
			except:
				member = None
			member_log.follower_member = member
			
	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV_NAME,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': WEAPP_USER_CENTER_NAV_NAME,

		'member_logs': member_logs,
		'member_id': member_id
	})
	return render_to_response('user_center/editor/user_integral_log.html', c)

########################################################################
# list_grades: 获取会员等级分类
########################################################################
@login_required
def list_grades(request):
	webapp_id = request.user_profile.webapp_id
	MemberGrade.get_default_grade(webapp_id)

	member_grades = MemberGrade.get_all_grades_list(webapp_id)

	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV_NAME,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': WEAPP_USER_CENTER_OTHER_OPTIONS_NAV_NAME,
		'member_grades': member_grades,
		'should_show_authorize_cover' : get_should_show_authorize_cover(request)
	})
	return render_to_response('user_center/editor/grades.html', c)


########################################################################
# add_grade: 添加会员等级
########################################################################
@login_required
def add_grade(request):
	show_alert = False
	try:
		member_qrcode_settings = MemberQrcodeSettings.objects.filter(owner=request.user)
		if member_qrcode_settings.count() > 0 and AWARD_MEMBER_TYPE_LEVEL == member_qrcode_settings[0].award_member_type:
			show_alert = True
	except:
		pass
	if request.POST:
		is_auto_upgrade = int(request.POST['is_auto_upgrade'])
		if is_auto_upgrade > 0:
			upgrade_lower_bound = int(request.POST['upgrade_lower_bound'].strip())
		else:
			upgrade_lower_bound = 0

		usable_integral_percentage_in_order = int(request.POST.get('usable_integral_percentage_in_order', '100'))

		grade = MemberGrade.objects.create(
			webapp_id = request.user_profile.webapp_id,
			name = request.POST.get('name', '').strip(),
			is_auto_upgrade = True if is_auto_upgrade > 0 else False,
			upgrade_lower_bound = upgrade_lower_bound,
			shop_discount = int(request.POST['shop_discount'].strip()),
			usable_integral_percentage_in_order = usable_integral_percentage_in_order
		)

		member_ids = request.POST.get('member_ids', '').strip()
		member_ids_list = [int(member_id.strip()) for member_id in member_ids.split(',') if len(member_id.strip()) > 0]
		if len(member_ids_list) > 0:
			Member.objects.filter(id__in=member_ids_list).update(grade=grade)

		if show_alert and MemberGrade.objects.filter(webapp_id=request.user_profile.webapp_id,name=MemberGrade.DEFAULT_GRADE_NAME).count() > 0:
			member_arcode_contents = MemberQrcodeAwardContent.objects.filter(member_level=MemberGrade.objects.filter(webapp_id=request.user_profile.webapp_id,name=MemberGrade.DEFAULT_GRADE_NAME)[0].id)
			if member_arcode_contents.count() > 0:
				MemberQrcodeAwardContent.objects.create(
					member_qrcode_settings=member_arcode_contents[0].member_qrcode_settings,
					member_level=grade.id,
					award_type=member_arcode_contents[0].award_type,
					award_content=member_arcode_contents[0].award_content
					)

		return HttpResponseRedirect('/webapp/user_center/grades/')
	else:
		
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV_NAME,
			'shop_discounts': [1]*100,
			'default_grade': MemberGrade.get_default_grade(request.user_profile.webapp_id),
			'show_alert':show_alert
		})
		return render_to_response('user_center/editor/edit_grade.html', c)

########################################################################
# update_grade: 更新会员等级
########################################################################
@login_required
def update_grade(request, grade_id):
	try:
		grade = MemberGrade.objects.get(id=grade_id)
	except:
		raise Http404(u'不存在该会员等级')
	show_alert = False
	if request.POST:
		is_auto_upgrade = int(request.POST.get('is_auto_upgrade', '0'))
		if is_auto_upgrade > 0:
			upgrade_lower_bound = int(request.POST['upgrade_lower_bound'].strip())
		else:
			upgrade_lower_bound = 0
		usable_integral_percentage_in_order = int(request.POST.get('usable_integral_percentage_in_order', '100'))
		MemberGrade.objects.filter(id=grade_id).update(
			name = request.POST.get('name', '').strip(),
			is_auto_upgrade = True if is_auto_upgrade > 0 else False,
			upgrade_lower_bound = upgrade_lower_bound,
			shop_discount = int(request.POST['shop_discount'].strip()),
			usable_integral_percentage_in_order = usable_integral_percentage_in_order
			)

		member_ids = request.POST.get('member_ids', '').strip()
		if len(member_ids) > 0:
			member_ids = member_ids.split(',')
			# 删除此分组member_ids不包含的会员
			Member.objects.filter(grade=grade).\
				filter(~Q(id__in = member_ids)).\
				update(grade = MemberGrade.get_default_grade(request.user_profile.webapp_id))

			# 保存此分组member_ids包含的会员
			Member.objects.filter(id__in=member_ids).update(grade=grade)
		else:
			Member.objects.filter(grade=grade).update(grade=grade.get_default_grade(request.user_profile.webapp_id))

		return HttpResponseRedirect('/webapp/user_center/grades/')
	else:
		default_grade = grade if grade.is_default_grade else MemberGrade.get_default_grade(request.user_profile.webapp_id)

		try:
			member_qrcode_settings = MemberQrcodeSettings.objects.filter(owner=request.user)
			if member_qrcode_settings.count() > 0 and AWARD_MEMBER_TYPE_LEVEL == member_qrcode_settings[0].award_member_type:
				show_alert = True
		except:
			pass

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV_NAME,
			'shop_discounts': [1]*100,
			'grade': grade,
			'default_grade': default_grade,
			'show_alert':show_alert
		})
		return render_to_response('user_center/editor/edit_grade.html', c)

########################################################################
# delete_grade: 删除会员等级
########################################################################
@login_required
def delete_grade(request, grade_id):
	webapp_id = request.user_profile.webapp_id
	default_grade = MemberGrade.get_default_grade(webapp_id)

	try:
		grade = MemberGrade.objects.get(id=grade_id)
	except:
		raise Http404(u"不存在该会员等级")

	if grade_id != default_grade.id:
		Member.objects.filter(webapp_id=webapp_id, grade=grade).update(grade=default_grade)
		grade.delete()

	return HttpResponseRedirect('/webapp/user_center/grades/')

########################################################################
# export_orders:  导出订单列表
########################################################################
@login_required
def export_member(request):
	webapp_id = request.user_profile.webapp_id
	members = Member.objects.filter(webapp_id=webapp_id, is_for_test=False)
	
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
				info_list = [
						'', '', '', '', '', '', '',
						'', '', 
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


COUNT_PER_PAGE = 20
MEMBER_TAGS = 'usercenter-tags'
########################################################################
# list_tags: 会员分组列表
########################################################################
@login_required
def list_tags(request):
	webapp_id = webapp_id = request.user_profile.webapp_id
	member_tags = MemberTag.get_member_tags(webapp_id)

	# #获取当前页数
	# cur_page = int(request.GET.get('page', '1'))
	# #获取每页个数
	# count = int(request.GET.get('count', COUNT_PER_PAGE))

	# pageinfo, member_tags = paginator.paginate(member_tags, cur_page, count, query_string=request.META['QUERY_STRING'])

	for member_tag in member_tags:
		member_tag.count = MemberHasTag.get_tag_has_member_count(member_tag)

	c = RequestContext(request, {
		'first_nav_name': FIRST_NAV_NAME,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': MEMBER_TAGS,
		'member_tags': member_tags,
		'should_show_authorize_cover': get_should_show_authorize_cover(request),
		'success_count': UserSentMassMsgLog.success_count(webapp_id)
		#'pageinfo': json.dumps(paginator.to_dict(pageinfo))
	})
	return render_to_response('user_center/editor/user_tags.html', c)

########################################################################
# add_tag: 添加会员分组
########################################################################
@login_required
def add_tag(request):
	if request.POST:
		name = request.POST.get('name','')
		webapp_id = webapp_id = request.user_profile.webapp_id
		if name and webapp_id:
			MemberTag.objects.create(name=name,webapp_id=webapp_id)

		return HttpResponseRedirect('/webapp/user_center/tags/')
	else:
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV_NAME,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': MEMBER_TAGS,
			#'pageinfo': json.dumps(paginator.to_dict(pageinfo))
		})
		return render_to_response('user_center/editor/edit_tag.html', c)


########################################################################
# update_tag: 修改会员分组
########################################################################
@login_required
def update_tag(request, tag_id):
	if request.POST:
		name = request.POST.get('name','')
		webapp_id = webapp_id = request.user_profile.webapp_id
		if name and webapp_id:
			MemberTag.objects.filter(id=tag_id).update(name=name)

		return HttpResponseRedirect('/webapp/user_center/tags/')
	else:
		member_tag = MemberTag.objects.get(id=tag_id)
		member_has_tags = MemberHasTag.objects.filter(member_tag=member_tag)
		is_shengjing = False
		if request.user.username == 'shengjing360' and (member_tag.name == u'注册未绑定CRM' or member_tag.name == u'注册绑定CRM'):
			is_shengjing = True
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV_NAME,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': MEMBER_TAGS,
			'tag': member_tag,
			'member_has_tags': member_has_tags,
			'is_shengjing': is_shengjing
			#'pageinfo': json.dumps(paginator.to_dict(pageinfo))
		})
		return render_to_response('user_center/editor/edit_tag.html', c)


########################################################################
# delete_tag: 修改会员分组
########################################################################
@login_required
def delete_tag(request, tag_id):
	MemberTag.objects.filter(id=tag_id).delete()
	return HttpResponseRedirect('/webapp/user_center/tags/')