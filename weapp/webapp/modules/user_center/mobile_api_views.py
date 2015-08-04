# -*- coding: utf-8 -*-

__author__ = 'bert'

from django.conf import settings

from account.social_account.models import SocialAccount, SOCIAL_PLATFORM_WEIXIN

from weixin.message.handler.message_handler import MessageHandler
from weixin.user.models import get_token_for

from core.exceptionutil import unicode_full_stack

from modules.member.models import WebAppUser
from modules.member.integral_new import increase_for_click_shared_url
from modules.member.util import (get_member_by_binded_social_account, 
	create_member_by_social_account, create_social_account)

from watchdog.utils import watchdog_error, watchdog_fatal
from core.jsonresponse import JsonResponse, create_response

from webapp.modules.user_center import request_api_util
# ########################################################################
# # get_sct: 个人信息
# ########################################################################
# import urllib2
# import urllib 
# import json
# import hashlib
# from BeautifulSoup import BeautifulSoup
# def get_sct(request):
# 	code = request.POST.get('code', '')
# 	appid = request.POST.get('appid', '')
# 	secret = request.POST.get('secret', '')
# 	fmt = request.POST.get('fmt', '')
# 	request_uri = request.POST.get('request_uri', '')
# 	data = {
# 		'appid': appid,
# 		'secret': secret,
# 		'code': code,
# 		'grant_type': 'authorization_code'
# 	}

# 	url = 'https://api.weixin.qq.com/sns/oauth2/access_token?'
# 	try:
# 		req = urllib2.urlopen(url, urllib.urlencode(data))
# 		response_data = req.read()
# 	except:
# 		notify_message = u"get_sct: cause:\n{}".format(unicode_full_stack())
# 		watchdog_fatal(notify_message)
# 		response = create_response(201)
# 		return response.get_response()

# 	response_data = eval(response_data)
# 	watchdog_fatal(response_data)
# 	if response_data.has_key('openid'):
# 		weixin_user_name = response_data['openid']
# 		token = get_token_for(request.user_profile.webapp_id, weixin_user_name)
# 		social_accounts = SocialAccount.objects.filter(token=token)
# 		if social_accounts.count() > 0:
# 			social_account = social_accounts[0]
# 		else:
# 			social_account = create_social_account(request.user_profile.webapp_id, weixin_user_name, token, SOCIAL_PLATFORM_WEIXIN)

# 		member = get_member_by_binded_social_account(social_account)
# 		is_new_created_member = False
# 		if member is None:
# 			#创建会员信息
# 			try:
# 				member = create_member_by_social_account(request.user_profile, social_account)
# 				#之后创建对应的webappuser
# 				_create_webapp_user(member)
# 				is_new_created_member = True
# 			except:
# 				notify_message = u"MemberHandler中创建会员信息失败，社交账户信息:('openid':{}), cause:\n{}".format(
# 					social_account.openid, unicode_full_stack())
# 				watchdog_fatal(notify_message)

# 		try:
# 			if fmt and member and fmt != member.token:
# 				#建立关系，更新会员来源
# 				follow_member = Member.objects.get(token=fmt)
# 				if is_new_created_member:
# 					MemberFollowRelation.objects.create(member_id=follow_member.id, follower_member_id=member.id, is_fans=is_new_created_member)
# 					MemberFollowRelation.objects.create(member_id=member.id, follower_member_id=follow_member.id, is_fans=False)
# 					member.source = SOURCE_BY_URL
# 					member.save()
# 				elif MemberFollowRelation.objects.objects.filter(member_id=member.id,follower_member_id=follow_member.id).count() == 0:
# 					MemberFollowRelation.objects.create(member_id=follow_member.id, follower_member_id=member.id, is_fans=is_new_created_member)
# 					MemberFollowRelation.objects.create(member_id=member.id, follower_member_id=follow_member.id, is_fans=False)

# 				#点击分享链接给会员增加积分
# 				try:
# 					if request_uri:
# 						increase_for_click_shared_url(follow_member, member, request_uri)
# 				except:
# 					notify_message = u"increase_for_click_shared_url:('openid':{}), cause:\n{}".format(social_account.openid, unicode_full_stack())
# 					watchdog_fatal(notify_message)

# 		except:
# 			notify_message = u"get_sct:('openid':{}), 处理分享信息 cause:\n{}".format(
# 					social_account.openid, unicode_full_stack())
# 			watchdog_fatal(notify_message)

# 		if social_account:
# 			response = create_response(200)
# 			data = {}
# 			data['sct'] = social_account.token
# 			data['webapp_id'] = social_account.webapp_id
# 			data['open_id'] = weixin_user_name
# 			data['member_token'] = member.token

# 			response.data = data
		

# 		else:
# 			watchdog_fatal(u'social_account is None')
# 			response = create_response(201)
# 			response.data = {}
# 	else:
# 		response = create_response(201)
# 		watchdog_fatal(u'response_data do not has openid')
# 		response.data = {}

# 	return response.get_response()
# 	#return request_util.get_user_info(request)


# def _create_webapp_user(self, member):
# 	try:
# 		if WebAppUser.objects.filter(token = member.token, webapp_id = member.webapp_id, member_id = member.id).count() == 0:
# 			WebAppUser.objects.create(
# 				token = member.token,
# 				webapp_id = member.webapp_id,
# 				member_id = member.id
# 				)
# 	except:
# 		pass


########################################################################
# send_phone_msg: 发送手机验证码
########################################################################
def send_captcha(request):
	return request_api_util.send_captcha(request)

def binding_phone(request):
	return request_api_util.binding_phone(request)

def record_shared_url(request):
	return request_api_util.record_shared_url(request)	

def record_refueling_log(request):
	return request_api_util.record_refueling_log(request)	