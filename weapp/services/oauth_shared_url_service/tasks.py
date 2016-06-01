# -*- coding: utf-8 -*-
"""@package services.oauth_shared_url_service.tasks

"""
from django.db.models import F
from watchdog.utils import watchdog_fatal
from core.exceptionutil import unicode_full_stack
from modules.member import member_settings

from modules.member import integral_new
from modules.member.models import Member, MemberFollowRelation, SOURCE_BY_URL, NOT_SUBSCRIBED
from utils import url_helper

from celery import task


def process_shared_url(request, args):
	is_new_created_member = False
	if args.has_key('is_new_created_member'):
		is_new_created_member = args['is_new_created_member']

	fmt = request.GET.get(member_settings.FOLLOWED_MEMBER_TOKEN_URL_QUERY_FIELD, None)

	if fmt and fmt.find(',') > -1:
		fmt = fmt.split(',')[0]

	member = request.member

	try:
		if fmt and member and fmt != member.token and fmt != "undefined":
			#建立关系，更新会员来源
			integral_friend_count = False
			follow_member = Member.objects.get(token=fmt)
			if is_new_created_member:
				MemberFollowRelation.objects.create(member_id=follow_member.id, follower_member_id=member.id, is_fans=is_new_created_member)
				Member.objects.filter(id=follow_member.id).update(fans_count=F('fans_count')+1)
				MemberFollowRelation.objects.create(member_id=member.id, follower_member_id=follow_member.id, is_fans=False)
				member.source = SOURCE_BY_URL
				member.save()
				integral_friend_count = True
			elif MemberFollowRelation.objects.filter(member_id=member.id,follower_member_id=follow_member.id).count() == 0:
				MemberFollowRelation.objects.create(member_id=follow_member.id, follower_member_id=member.id, is_fans=is_new_created_member)
				MemberFollowRelation.objects.create(member_id=member.id, follower_member_id=follow_member.id, is_fans=False)
				integral_friend_count = True
			try:
				if integral_friend_count and (follow_member.status!=NOT_SUBSCRIBED and member.status!=NOT_SUBSCRIBED):
					Member.objects.filter(id__in = [member.id, follow_member.id]).update(friend_count=F('friend_count')+1)
			except:
				notify_message = u"process_shared_url integral_friend_count error:('member_id':{}, follower_member_id: {}), cause:\n{}".format(member.id, follow_member.id, unicode_full_stack())
				watchdog_fatal(notify_message)
			
			#点击分享链接给会员增加积分
			try:
				integral_new.increase_for_click_shared_url(follow_member, member, request.get_full_path())
			except:
				notify_message = u"process_shared_url increase_for_click_shared_url:('member_id':{}), cause:\n{}".format(member.id, unicode_full_stack())
				watchdog_fatal(notify_message)

	except:
		notify_message = u"('fmt':{}), 处理分享信息,request_path{} cause:\n{}".format(
				fmt, request.get_full_path(),unicode_full_stack())
		watchdog_fatal(notify_message)

#@register('oautu_shared_url')
def serve(request, args):
	process_shared_url(request, args)


@task
def oauth_shared_url(request0, args):
	from services.service_manager import create_request
	request = create_request(args)
	serve(request, args)
	return 'OK'

	