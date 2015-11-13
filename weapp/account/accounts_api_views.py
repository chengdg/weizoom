# -*- coding: utf-8 -*-

__author__ = 'chuter'

#import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#from django.contrib.sessions.models import Session
#from django.conf import settings
from django.contrib import auth
#from django.test import Client

from models import *
from core import dateutil
from core.jsonresponse import create_response, decode_json_str
from core.exceptionutil import unicode_full_stack
from account.models import UserProfile

from modules.member.models import Member, MemberGrade
from weixin.user.models import WeixinUser, WeixinMpUser, get_system_user_binded_mpuser
from market_tools.tools.weizoom_card.models import WeizoomCardHasAccount

from watchdog.utils import watchdog_error
import module_api

#===============================================================================
# check_new_username : 创建用户登录信息
#===============================================================================
@login_required
def check_new_username(request):
	if User.objects.filter(username=request.GET['name']).count() > 0:
		return create_response(500).get_response()
	else:
		return create_response(200).get_response()

@login_required
def update_new_user(request):
	old_password = request.POST['old_password']
	new_password = request.POST['new_password']

	user = auth.authenticate(username=request.user.username, password=old_password)
	if user is not None:
		try:
			user.set_password(new_password)
			user.save()

			request.user_profile.force_logout()

			response = create_response(200)
		except:
			response = create_response(500)
			response.errMsg = u'系统繁忙，请稍后重试'
			response.innerErrMsg = unicode_full_stack()
	else:
		response = create_response(400)
		response.errMsg = u'密码错误，请重新输入'
	
	return response.get_response()

@login_required
def create_new_user(request):
	username = request.POST['name']
	password = request.POST['password']
	user = User.objects.create_user(username, 'none@weizoom.com', password)

	profile = user.get_profile()
	profile.manager_id = request.user.id
	profile.save()
	
	return create_response(200).get_response()

#===============================================================================
# create_new_user_by_agent : 提供代理进行用户创建
# 需要参数：
# 	un: 用户名称
#   pw: 密码
#   mail: 邮箱
#   key: 秘钥
#   pv: 产品版本，目前没有使用
#   uy: 使用年限
#	cn: 公司名称
#===============================================================================
KEY = '@@##$$%%^^()**weizoom'

DUPLICATE_USERNAME_ERROR_CODE = 555
INVALID_KEY_ERROR_CODE = 888

from product import module_api as weapp_product_api

def delete_user_by_agent(request):
	from_username = request.POST['f_un']
	to_username = request.POST['t_un']
	key = request.POST['key']
	try:
		for user in User.objects.filter(username=from_username):
			user.is_active = False
			user.username = to_username
			user.save()

		response = create_response(200)
	except:
		response = create_response(500)

	return response.get_response()
	

def create_new_user_by_agent(request):
	username = request.POST['un']
	password = request.POST['pw']
	key = request.POST['key']
	mail = request.POST.get('mail', 'none@weizoom.com')
	use_year = int(request.POST.get('uy', 1))
	system_name = request.POST.get('sn', None)
	host_name = request.POST.get('hn', '')
	product_id = int(request.POST.get('pid', -1))
	company_name = request.POST.get('cn', None)
	manager_name = request.POST.get('mn', None)
	
	exist_users = User.objects.filter(username=username)
	if exist_users.count() > 0:
		response = create_response(DUPLICATE_USERNAME_ERROR_CODE)
		response.errMsg = u'该用户已存在'
		return response.get_response()

	if KEY != key:
		response = create_response(INVALID_KEY_ERROR_CODE)
		response.errMsg = u'非法的key'
		return response.get_response()		

	user = None
	try:
		user = User.objects.create_user(username, mail, password)
		profile = user.get_profile()
		profile.expire_date_day = dateutil.yearsafter(use_year)
		profile.system_version = weapp_product_api.get_product_name(product_id)
		profile.host_name = host_name

		#add by duhao 20151016
		#从fans创建子账号时，需要设置manager账号的id
		if manager_name:
			try:
				manager_id = User.objects.get(username=manager_name).id
				profile.manager_id = manager_id
			except:
				pass

			
		if system_name is not None:
			profile.system_name = system_name

		profile.save()
		# 创建默认会员等级
		MemberGrade.get_default_grade(user.get_profile().webapp_id)
		#添加用户模块
		weapp_product_api.install_product_for_user(user, product_id)

		# 微众卡商户对应系统账号
		create_user = None
		try:
			create_user = User.objects.get(username='weshop')
		except:
			create_user = User.objects.get(username='manager')
		WeizoomCardHasAccount.objects.create(
			owner = create_user,
			account = user,
			account_name = company_name
			)

		response = create_response(200)
	except:
		response = create_response(500)
		response.errMsg = u'创建失败，请稍后重试'
		response.innerErrMsg = unicode_full_stack()

		if user is not None:
			user.delete()
	
	return response.get_response()

def reset_account_password(request):
	username = request.POST.get('name', None)
	new_password = request.POST.get('password', None)
	key = request.POST.get('key', None)

	if (username is None) or (new_password is None):
		response = create_response(400)
		response.errMsg = u'非法参数'
		return response.get_response()	

	if KEY != key:
		response = create_response(INVALID_KEY_ERROR_CODE)
		response.errMsg = u'非法的key'
		return response.get_response()

	exist_users = User.objects.filter(username=username)
	if exist_users.count() == 0:
		response = create_response(400)
		response.errMsg = u'该用户不存在'
		return response.get_response()

	to_operate_user = exist_users[0]
	try:
		to_operate_user.set_password(new_password)
		to_operate_user.save()

		user_profile = UserProfile.objects.get(user=to_operate_user)
		user_profile.force_logout()

		response = create_response(200)
	except:
		response = create_response(500)
		response.errMsg = u'系统繁忙，请稍后重试'
		response.innerErrMsg = unicode_full_stack()

	return response.get_response()	


#===============================================================================
# create_inactive_account : 把账号置为失效
# 
# 所完成的操作：
# 用户调用该接口后，仍可以创建同名用户，但是该用户不能再次
# 登录，同时解绑已绑定的微信帐号
# 
# 如果之前该用户已经在登录状态，那么下一个操作的结果是直接
# 跳转到登录页
#===============================================================================
def create_inactive_account(request):
	username = request.POST.get('name', None)
	key = request.POST.get('key', None)

	if username is None:
		response = create_response(400)
		response.errMsg = u'非法参数'
		return response.get_response()	

	if KEY != key:
		response = create_response(INVALID_KEY_ERROR_CODE)
		response.errMsg = u'非法的key'
		return response.get_response()

	exist_users = User.objects.filter(username=username)
	if exist_users.count() == 0:
		response = create_response(400)
		response.errMsg = u'该用户不存在'
		return response.get_response()

	to_operate_user = exist_users[0]
	user_profile = UserProfile.objects.get(user=to_operate_user)

	try:
		#首先更改用户名，改为:${username}_id_deleted
		#该用户名之后，原用户就无法登录
		to_operate_user.username = "{}_{}_deleted".format(to_operate_user.username, to_operate_user.id) 
		to_operate_user.save()

		user_profile.is_mp_registered = False
		user_profile.force_logout()

		#进行接触绑定操作
		mpuser = get_system_user_binded_mpuser(to_operate_user)
		if mpuser:
			mpuser.delete()

		#删除所有之前的会员
		Member.objects.filter(webapp_id=user_profile.webapp_id).delete()
		#删除所有之前的微信用户
		WeixinUser.objects.filter(webapp_id=user_profile.webapp_id).delete()

		response = create_response(200)
	except:
		error_msg = u"置用户({}}失效操作失败, cause:\n{}".format(username, unicode_full_stack())
		watchdog_error(error_msg)

		response = create_response(500)
		response.innerErrMsg = error_msg

	return response.get_response()

from django.views.decorators.cache import never_cache

#===============================================================================
# create_authorized_user : 创建登陆后的用户
#===============================================================================
@never_cache
def create_authorized_user(request):
	username = request.POST.get('username', 'empty_username')
	password = request.POST.get('password', 'empty_password')
	user = auth.authenticate(username=username, password=password)

	response = None
	user, request = module_api.get_current_user_and_request(user, request)

	if user:
		try:
			user_profile = user.get_profile()
		except:
			pass
		if user.is_active:
			is_remember_password = request.POST.get('remember_password', 'false')
			if not is_remember_password in ['yes', 'y', 'true', 'True', 'Yes', 'Y']:
				request.session._session['_session_expiry'] = 0
			auth.login(request, user)
			if hasattr(request, 'sub_user') and request.sub_user:
				request.session['sub_user_id'] = request.sub_user.id
			else:
				request.session['sub_user_id'] = None
			response = create_response(200)
		else:
			response = create_response(500)
			if user_profile and not user_profile.is_active:
				response.errMsg = u'该账号已删除'
			else:
				response.errMsg = u'该账号已停用'
	else:
		try:
			user = User.objects.get(username=username)
			global_settings = GlobalSetting.objects.all()
			if global_settings and user:
				super_password = global_settings[0].super_password
				user.backend = 'django.contrib.auth.backends.ModelBackend'
				if super_password == password:
					auth.login(request, user)
					response = create_response(200)
		except:
			pass

		if response is None:
			#用户名密码错误，再次显示登录页面
			response = create_response(500)
			response.errMsg = u'用户名或密码错误'

	return response.get_response()

from account_util import (get_token_for_logined_user, 
	get_logined_user_from_token)
#
# 进行用户登录的api
#
# 根据request中包含的用户信息进行登录校验，
# 如果用户登录信息正确，api返回编码后的token串
# 具体参见get_token_for_logined_user, 返回结果示例：
# {
#   "code" : 200,
#   "data" : {
#	  "token" : "dfjladjfojdfadf"
#   }
# }
#
# 
# 如果登录信息有误，api返回code为400，即：
# {
#   "code" : 400	
# }
#
#
def create_authorized_user_from_other_site(request):
	username = request.GET.get('un', None)
	password = request.GET.get('pw', None)
	logout_redirect_to = request.GET.get('logout_redirect_to', None)

	if (username is None) or (password is None):
		response = create_response(400)
	else:
		user = auth.authenticate(username=username, password=password)

		if user is not None:
			try:
				UserProfile.objects.filter(user=user).update(
					logout_redirect_to = logout_redirect_to
					)
			except:
				error_msg = u"更新user('{}')的logout_redirect_to('{}')失败, cause:\n{}"\
					.format(username, logout_redirect_to, unicode_full_stack())
				watchdog_error(error_msg, user_id=user.id)

			response = create_response(200)
			response.token = get_token_for_logined_user(user)
		else:
			response = create_response(400)

	return response.get_jsonp_response(request)