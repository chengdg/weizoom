# -*- coding: utf-8 -*-

__author__ = 'chuter'

import urllib2
import os
from datetime import timedelta, datetime

from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib import auth

from models import *
from core.jsonresponse import create_response, decode_json_str
from core.exceptionutil import unicode_full_stack
from account.models import UserProfile
from account.social_account.models import SocialAccount
from core.wxapi import get_weixin_api

from watchdog.utils import watchdog_fatal, watchdog_error
from modules.member.models import Member
from weixin.user.models import WeixinUser, WeixinMpUser, WeixinMpUserAccessToken, DEFAULT_ICON, MpuserPreviewInfo, get_system_user_binded_mpuser

#===============================================================================
# create_weixin_mp_user_temp_message : 创建公众账号接收的消息
#===============================================================================
def create_weixin_mp_user_temp_message(request):
	TempReceivedMessage.objects.create(
		mp_user_name = request.GET['sender_name'],
		weixin_user_name = request.GET['receiver_name'],
		content = request.GET['content']
	)

	return create_response(200).get_response()


#===============================================================================
# get_weixin_mp_user_temp_messages : 获取公众账号发来的消息
#===============================================================================
def get_weixin_mp_user_temp_messages(request):
	try:
		if request.user_profile:
			profile = request.user_profile
		else:
			if request.app:
				profile = UserProfile.objects.get(webapp_id=request.app.webapp_id)
			else:
				profile = None
		mp_user = WeixinMpUser.objects.get(owner_id=profile.user_id)
		mp_user_name = mp_user.username
		weixin_user_name = request.GET['weixin_user_name']

		response = create_response(200)
		
		message = TempReceivedMessage.objects.filter(mp_user_name=mp_user_name, 
			weixin_user_name=weixin_user_name,
			is_processed = False)[0]
		html_response = render_to_response('weixin/text_content.html', {'content':message.content})
		response.data = html_response.content

		message.is_processed = True
		message.save();
		return response.get_response()
	except:
		import sys
		import traceback
		type, value, tb = sys.exc_info()
		#print type
		#print value
		#traceback.print_tb(tb)
		response = create_response(200)
		response.data = ''
		return response.get_response()

########################################################################
# bind_mpuser: 绑定公众号
########################################################################
@login_required
def bind_mpuser(request):
	user_profile = request.user_profile
	user_profile.is_mp_registered = True
	user_profile.save()

	return create_response(200).get_response()

########################################################################
# update_binded_mpuser: 更新绑定账号信息
########################################################################
@login_required
def update_binded_mpuser(request):
	try:
		mpuser = WeixinMpUser.objects.filter(id=int(request.POST['mpid'])).update(
			# username = request.POST['username'].strip(),
			is_service = True if request.POST['is_service'] == 'true' else False,
			is_certified = True if request.POST['is_certified'] == 'true' else False,
			aeskey = request.POST.get('aeskey', '0'),
			encode_aeskey = request.POST.get('encode_aeskey', ''),
			)

		MpuserPreviewInfo.objects.filter(id=int(request.POST['mpprid'])).update(
			image_path = request.POST['pic_url'],
			name = request.POST['mpuser_nickname'].strip(),
			)

		response = create_response(200)
	except:
		response = create_response(500)
		response.errMsg = u"更新公众号信息失败"
		response.innerErrMsg = unicode_full_stack()

	return response.get_response()

########################################################################
# delete_binded_mpuser: 解除绑定
########################################################################
@login_required
def delete_binded_mpuser(request):
	user_profile = request.user_profile

	response = create_response(200)
	try:
		mpuser = get_system_user_binded_mpuser(request.user)
		if mpuser:
			mpuser.delete()
			
			user_profile.is_mp_registered = False
			user_profile.save()

		#删除所有之前的会员
		Member.objects.filter(webapp_id=user_profile.webapp_id).delete()
		#删除所有之前的微信用户
		WeixinUser.objects.filter(webapp_id=user_profile.webapp_id).delete()
	except:
		notify_msg = u"解除绑定操作失败, cause:\n{}".format(unicode_full_stack())
		watchdog_fatal(notify_msg)

	return response.get_response()

########################################################################
# get_bind_status: 获取公众号绑定信息
########################################################################
@login_required
def get_bind_status(request):
	user_profile = request.user_profile

	response = create_response(200)
	if user_profile.is_mp_registered:
		mpusers = WeixinMpUser.objects.filter(owner=request.user)

		if mpusers.count() == 0:
			mpuser = WeixinMpUser.objects.create(
				owner = request.user,
				username = request.GET.get('mpusername', request.user_profile.webapp_id),
				is_certified = request.GET.get('is_certified', 'false') == 'true',
				is_service = request.GET.get('mp_type', 'normal') == 'service',
				is_active = True,
				aeskey = request.POST.get('aeskey', '0'),
				encode_aeskey = request.POST.get('encode_aeskey', '')
			)

			MpuserPreviewInfo.objects.create(
				mpuser = mpuser,
				name = mpuser.username,
				image_path = DEFAULT_ICON
			)
		else:
			WeixinMpUser.objects.filter(owner=request.user).update(
				is_certified = request.GET.get('is_certified', 'false') == 'true',
				is_service = request.GET.get('mp_type', 'normal') == 'service',
				is_active = True,
				aeskey = request.POST.get('aeskey', '0'),
				encode_aeskey = request.POST.get('encode_aeskey', '')
				)

		response.data.is_binded = True
	else:
		response.data.is_binded = False

	return response.get_response()

def _update_local_mpuser_access_token(mpuser, appid, app_secret, access_token, expires_span):
	assert (mpuser and access_token)

	next_expire_time = datetime.now() + timedelta(seconds=expires_span)

	access_tokens = WeixinMpUserAccessToken.objects.filter(mpuser=mpuser)
	if access_tokens.count() == 0:
		
		return WeixinMpUserAccessToken.objects.create(
			mpuser = mpuser,
			app_id = appid,
			app_secret = app_secret,
			access_token = access_token,
			expire_time = next_expire_time
		)
	else:
		WeixinMpUserAccessToken.objects.filter(mpuser=mpuser).update(
			mpuser = mpuser,
			app_id = appid,
			app_secret = app_secret,
			access_token = access_token,
			expire_time = next_expire_time
			)
		return access_tokens[0]


from weixin.user.access_token import get_new_access_token
@login_required
def create_mpuser_access_token(request):
	from modules.member.util import create_member_group, get_all_group
	appid = request.GET.get('appid', None)
	secret = request.GET.get('secret', None)

	if appid is None or secret is None:
		response = create_response(400)
		response.errMsg = u'appid或secret输入不正确'
	else:
		new_access_token, expires_span, error_response = get_new_access_token(appid, secret)
		if (new_access_token is None) and (error_response is None):
			response = create_response(500)
			response.errMsg = u'服务繁忙请稍后重试'
		else:
			if new_access_token is None:
				response = create_response(500)
				response.errMsg = error_response.get_errormsg_in_zh()
			else:
				#访问api成功, 需要创建本地mpser对应的授权信息
				try:
					mpuser = get_system_user_binded_mpuser(request.user)
					access_token = _update_local_mpuser_access_token(mpuser, appid, secret, new_access_token, expires_span)
					try:
						user_profile = request.user_profile
						groups = get_all_group(user_profile)
						create_member_group(groups, user_profile.webapp_id)
					except:
						notify_msg = u"更新分组失败, cause:\n{}".format(unicode_full_stack())
						watchdog_fatal(notify_msg)

					response = create_response(200)
				except:
					notify_msg = u"获取或存储access_token失败, appid:'{}', secret:'{}', cause:\n{}".format(appid, secret, unicode_full_stack())
					watchdog_error(notify_msg)

					response = create_response(500)
					response.errMsg = u'服务繁忙请稍后重试'

	return response.get_response()

########################################################################
# jz 2015-10-10
# get_preview_info: 获得预览信息
########################################################################
# @login_required
# def get_preview_info(request):
# 	try:
# 		info = PreviewInfo.objects.get(owner=request.user)
# 		response = create_response(200)
# 		data = {}
# 		if len(info.name) > 6:
# 			data['name'] = u'%s...' % info.name[:6]
# 		else:
# 			data['name'] = info.name
# 		data['image_path'] = info.image_path
# 		response.data = data;
# 		return response.get_response()
# 	except:
# 		response = create_response(200)
# 		data = {}
# 		data['name'] = ''
# 		data['image_path'] = DEFAULT_ICON
# 		response.data = data;
# 		return response.get_response()


########################################################################
# get_session_id: 获取sessionid，用于支持预览
########################################################################
@login_required
def get_session_id(request):
	response = create_response(200)
	response.data = request.COOKIES['sessionid'];
	return response.get_response()


########################################################################
# get_social_account_token: 获取social account token，用于支持预览
########################################################################
@login_required
def get_social_account_token(request):
	openid = request.GET['openid']
	social_account = SocialAccount.objects.get(openid=openid)

	response = create_response(200)
	response.data = social_account.token
	return response.get_response()


########################################################################
# get_user_icons: 获得用户icon
########################################################################
@login_required
def get_user_icons(request):
	response = create_response(200)
	data = {}
	icon_names = {
		'icon_color': u'颜色',
	    'icon_my': u'我上传的'
	}
	icons_dir = os.path.join(settings.PROJECT_HOME, '../static/img/system_icons')
	for dir_name in os.listdir(icons_dir):
		if 'icon_' in  dir_name:
			icon_dir_path = os.path.join(icons_dir, dir_name)
			if os.path.isdir(icon_dir_path):
				dir_name_key = icon_names[dir_name]
				data[dir_name_key] = []
				for file_name in os.listdir(icon_dir_path):
					icon_file_path = os.path.join(icon_dir_path, file_name)
					if os.path.isfile(icon_file_path) and '.png' in file_name:
						data[dir_name_key].append('/standard_static/img/system_icons/%s/%s' % (dir_name, file_name))

	user_icon_dir = os.path.join(settings.UPLOAD_DIR, 'user_icon', str(request.user.id))
	data[u'我上传的'] = []
	if os.path.exists(user_icon_dir):
		for file in os.listdir(user_icon_dir):
			data[u'我上传的'].append('/standard_static/upload/user_icon/%d/%s' % (request.user.id, file))

	response.data = data
	return response.get_response()