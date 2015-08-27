# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.shortcuts import render_to_response

from models import *
from modules.member import util as member_util


def _is_alert_for_iphone_version_less_6(request):
	http_user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
	http_user_agent = http_user_agent.split('iphone os')
	if len(http_user_agent) > 1:
		try:
			version = int(http_user_agent[1].split('_')[0])
			if version < 6 :
				return True
			else:
				return False
		except:
			return False
	else:
		return False


########################################################################
# get_activity: 获取活动详情
########################################################################
# update by bert chang 已签到 to 1 未签到 to 0
def get_activity(request):
	profile = request.user_profile
	# webapp_id = profile.webapp_id
	webapp_user = request.webapp_user
	# webapp_owner_id = request.project.owner_id
	member = webapp_user.get_member_by_webapp_user_id(webapp_user.id)
	activity_id = request.GET['activity_id']

	is_participated = False #是否已经报名
	members = None
	member_count = 0

	is_alert_img_msg = _is_alert_for_iphone_version_less_6(request)

	hide_non_member_cover = False
	activity_type = 0
	# try:
	activity = Activity.objects.get(id=activity_id)
	activity_type = activity.type
	activity.check_time()
	#是否签到
	is_enable_offline_sign_str = 0
	if activity.is_enable_offline_sign:
		activity_user_code = ActivityUserCode.objects.filter(activity=activity, webapp_user_id=webapp_user.id)
		sign_status = 0
		if activity_user_code:
			sign_status = activity_user_code[0].sign_status
		if sign_status:
			is_enable_offline_sign_str =1
	if activity.is_non_member:
		hide_non_member_cover = True
	# except:
	# 	c = RequestContext(request, {
	# 		'is_deleted_data': True,
	# 		'is_hide_weixin_option_menu':False
	# 	})
	# 	if activity_type == 1:
	# 		return render_to_response('activity/webapp/activity_ph.html', c)
	# 	else:
	# 		return render_to_response('activity/webapp/activity.html', c)

	items = ActivityItem.objects.filter(activity=activity)
	options = {
		'activity' : activity,
		'items' : items,
		'is_alert_img_msg' : is_alert_img_msg,
		'is_enable_offline_sign_str' : is_enable_offline_sign_str
	}
	if activity_type == 1:
		return get_activity_ph(request,options)
	for item in items:
		item.input_name = '{}-{}'.format(item.id, item.type)
		if item.type == ACTIVITYITEM_TYPE_SELECT:
			item.options = item.initial_data.split('|')
		if item.type == ACTIVITYITEM_TYPE_CHECKBOX:
			item.options = item.initial_data.split('|')

		if member:
			if item.title == u'姓名':
				item.value = member.member_info.name if (member is not None) else ''
			elif item.title == u'手机号':
				item.value = member.member_info.phone_number if (member is not None) else ''
		else:
			item.value = ''

		type = 'text'
		if item.type == ACTIVITYITEM_TYPE_SELECT:
			type = 'select'
		elif item.type == ACTIVITYITEM_TYPE_IMAGE:
			type = 'image'
		elif item.type == ACTIVITYITEM_TYPE_CHECKBOX:
			type = 'checkbox'
		item.type = type

	#确定是否已经报名
	is_participated = (ActivityItemValue.objects.filter(activity=activity, webapp_user_id=webapp_user.id).count() > 0)

	is_enable_offline_sign = activity.is_enable_offline_sign
	sign_code = ""
	if is_enable_offline_sign:
		activit_user_code = ActivityUserCode.objects.filter(activity=activity, webapp_user_id=webapp_user.id)
		if activit_user_code:
			sign_code = activit_user_code[0].sign_code
	#获取报名人数
	member_count = ActivityItemValue.objects.filter(activity=activity).values("webapp_user_id").distinct().count()
	#6.19日运营需求，增加参与量
	if int(activity.id) == 75:
		member_count = 268 + member_count

	#参与活动的好友信息
	joined_users_ids = set(ActivityItemValue.objects.filter(activity=activity).values_list("webapp_user_id", flat=True).distinct())
	friend_members = member.friends if member else []
	members = member.members_from_webapp_user_ids(joined_users_ids) if member else []
	joined_member_ids = []
	for m in members:
		joined_member_ids.append(members[m])

	joined_friend_members = []
	for member in friend_members:
		if member.id in joined_member_ids:
			joined_friend_members.append(member)

	request.should_hide_footer = True
	c = RequestContext(request, {
		'page_title': activity.name,
	    'activity': activity,
	    'is_participated': is_participated,
	    'items': items,
	    'sign_code': sign_code,
	    'member_count': member_count,
	    'friend_members': joined_friend_members,
	    'is_alert_img_msg': is_alert_img_msg,
	    'member': member,
	    'hide_non_member_cover': hide_non_member_cover,
	    'is_enable_offline_sign_str': is_enable_offline_sign_str,
	    'is_hide_weixin_option_menu':False
	})
	if activity_type == 1:
		return render_to_response('activity/webapp/activity_ph.html', c)
	else:
		return render_to_response('activity/webapp/activity.html', c)

########################################################################
# get_activity_ph: 获取ph活动,方便html页面组织标签顺序
########################################################################
def get_activity_ph(request,options):
	request.should_hide_footer = True
	items = options['items']
	type_dict = {}
	ph_dict = {}
	img_dict = {}
	comment_dict = {}
	for item in items:
		item.input_name = '{}-{}'.format(item.id, item.type)
		if item.type == ACTIVITYITEM_TYPE_SELECT:
			item.options = item.initial_data.split('|')
			item.type = 'select'
			type_dict = item
		elif item.type == ACTIVITYITEM_TYPE_CHECKBOX:
			item.options = item.initial_data.split('|')
			item.type = 'checkbox'
			type_dict = item
		elif item.type == ACTIVITYITEM_TYPE_IMAGE:
			item.type = 'image'
			img_dict = item
		else:
			item.type = 'text'
			# is_mandatory用来区分是ph值还是评论，所以必须要在配置页面加以限制
			if item.is_mandatory:
				print 'ph'
				ph_dict = item
			else:
				comment_dict = item
				print 'com'
	c = RequestContext(request, {
		'page_title': u'生活PH值大检测',
	    'activity': options['activity'],
	    'type_dict': type_dict,
		'ph_dict': ph_dict,
		'img_dict': img_dict,
		'comment_dict': comment_dict,
	    'is_alert_img_msg': options['is_alert_img_msg'],
	    'is_enable_offline_sign_str': options['is_enable_offline_sign_str'],
	    'is_hide_weixin_option_menu':False,
		'hide_non_member_cover': True,
		'webapp_user_id':request.webapp_user.id,
		'webapp_owner_id': request.project.owner_id
	})
	return render_to_response('activity/webapp/activity_ph.html', c)
########################################################################
# get_usage: 获取“我的”活动列表
########################################################################
def get_usage(request):
	profile = request.user_profile
	webapp_user = request.webapp_user

	activities = Activity.get_activites(webapp_user)

	c = RequestContext(request, {
		'page_title': u'我的活动列表',
		'activities': activities,
		'is_hide_weixin_option_menu':False
	})
	return render_to_response('activity/webapp/my_activities.html', c)


########################################################################
# get_member_activites: 获取“我参与的活动”列表
########################################################################
from apps.customerized_apps.event import models as event_models
from apps.customerized_apps.vote import models as vote_models
from apps.customerized_apps.survey import models as survey_models
from apps.customerized_apps.lottery import models as lottery_models

def get_member_activites(request):
	profile = request.user_profile
	webapp_user = request.webapp_user
	member = member_util.get_member(request)

	#活动
	events = event_models.eventParticipance.objects.filter(member_id=member.id)
	events_items = []
	for event in events:
		print event.belong_to
		print '1111111111111'
		event_id = event.belong_to
		event_details = event_models.event.objects.get(id=event_id )
		print event_details
		print event_details.name
		events_items.append({
			'id': str(event_id),
			'name': event_details.name
		})
	#投票
	votes = vote_models.voteParticipance.objects.filter(member_id=member.id)
	votes_items = []
	for vote in votes:
		vote_id = vote.belong_to
		vote_details = vote_models.vote.objects.get(id=vote_id )
		votes_items.append({
			'id': str(vote_id),
			'name': vote_details.name
		})
	#调研
	surveies = survey_models.surveyParticipance.objects.filter(member_id=member.id)
	surveies_items = []
	for survey in surveies:
		survey_id = survey.belong_to
		survey_details = survey_models.survey.objects.get(id=survey_id )
		surveies_items.append({
			'id': str(survey_id),
			'name': survey_details.name
		})
	#抽奖
	lotteres = lottery_models.lotteryParticipance.objects.filter(member_id=member.id)
	lotteres_items = []
	for lottery in lotteres:
		lottery_id = lottery.belong_to
		lottery_details = lottery_models.lottery.objects.get(id=lottery_id )
		lotteres_items.append({
			'id': str(lottery_id),
			'name': lottery_details.name
		})

	c = RequestContext(request, {
		'page_title': u'我的活动列表',
		'events_items': events_items,
		'votes_items': votes_items,
		'surveies_items': surveies_items,
		'lotteres_items': lotteres_items,
		'is_hide_weixin_option_menu':False
	})
	return render_to_response('activity/webapp/my_activities.html', c)


########################################################################
# activity_share_ph:
########################################################################
def share_activity(request):
	webapp_user_id = request.GET.get('memberId')
	webapp_user = request.webapp_user
	curr_webapp_user_id = webapp_user.id
	webapp_owner_id = request.project.owner_id
	member = webapp_user.get_member_by_webapp_user_id(curr_webapp_user_id)
	is_member = True if member else False
	is_visitor = True if int(webapp_user_id) != curr_webapp_user_id else False
	activity_id = request.GET['act_id']
	# activity = Activity.objects.get(id=activity_id)
	# if is_visitor:
	# 	items = ActivityItem.objects.filter(activity=activity)
	# 	is_alert_img_msg = _is_alert_for_iphone_version_less_6(request)
	# 	options = {
	# 		'activity' : activity,
	# 		'items' : items,
	# 		'is_alert_img_msg' : is_alert_img_msg,
	# 		'is_enable_offline_sign_str' : 0
	# 	}
	# 	return get_activity_ph(request,options)

	ids = request.GET['ids']
	ids = ids.split(',')
	del ids[0]
	ids = map(eval,ids)
	items = ActivityItemValue.objects.filter(id__in = ids)
	values = []
	for iterm in items:
		values.append(iterm.value)
	c = RequestContext(request,{
		'ph' : values[0],
		'comment' : values[1],
		'type' : values[2],
		'img' : values[3],
		'is_visitor':is_visitor,
		'is_member':is_member,
		'activity_id':activity_id,
		'webapp_owner_id':webapp_owner_id
	})
	return render_to_response('activity/webapp/my_activitie_ph.html',c)