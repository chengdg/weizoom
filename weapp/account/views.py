# -*- coding: utf-8 -*-

import time
from datetime import datetime
import urllib
import os
import sys
import random
try:
	from PIL import Image
except:
	import Image

from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render_to_response, render
from django.contrib.auth.models import User
from django.contrib import auth

from models import *
from weixin.user.models import *
from core.jsonresponse import create_response, JsonResponse
from core.exceptionutil import unicode_full_stack
from core.upyun_util import upload_image_to_upyun
from watchdog.utils import watchdog_alert,watchdog_error,watchdog_debug
import module_api
FIRST_NAV_NAME = 'home'
NAV_NAME = 'homepage'

HOME_SECOND_NAVS = [{
	'navs': [
	{
		'name': 'account_info',
		'title': u'账号信息',
		'url': '/account',
	},
	# jz 2015-10-10
	# {
	# 	'name': 'dashboard',
	# 	'title': u'统计概况',
	# 	'url': '/',
	# },
	# {
	# 	'name': 'system_settings',
	# 	'title': u'系统配置',
	# 	'url': '/account/settings',
	# },
	# {
	# 	'name': 'system_settings',
	# 	'title': u'运营邮件通知',
	# 	'url': '/account/settings',
	# }
	]
}]

random.seed(time.time())

#===============================================================================
# show_loading_page : 显示加载页面
#===============================================================================
def show_loading_page(request):
	c = RequestContext(request, {

	})
	return render_to_response('account/loading.html', c)


#===============================================================================
# index : 用户首页
#===============================================================================
@login_required(login_url='/login/')
def index(request):
	if request.user.is_superuser:
		return render_to_response('account/login.html', {})
	if request.user.username in settings.WEIZOOM_CARD_ADMIN_USERS:
		return HttpResponseRedirect('/card/cards/get/')
	# jz 2015-10-10
	# if request.user.username == 'operator':
	# 	#operator用户转入反馈意见列表
	# 	return HttpResponseRedirect('/operation/editor/feedbacks/')
	# elif request.user.username == 'manager':
	# 	# manager用户直接跳账户列表
	# 	return HttpResponseRedirect('/account/accounts/')
	# else:

	# 询问玉成是否可以去掉
	user_profile = request.user_profile
	if not user_profile.is_mp_registered:
		return HttpResponseRedirect('/new_weixin/mp_user/')

	return HttpResponseRedirect('/mall2/outline/')
		# jz 2015-10-10
		# elif request.user.id != request.manager.id:
		# else:
		# 	#add by jiangzhe 20150706 直接跳转到微信互动页面
		# 	return HttpResponseRedirect('/new_weixin/outline/')
		# 	#一般用户转入首页
		# 	todos = []
		# 	#待处理消息
		# 	profile = request.user.get_profile()
		# 	if profile.new_message_count > 0:
		# 		todos.append({'text': u'收到%d条新消息' % profile.new_message_count, 'url': '/message/'})
		# 	c = RequestContext(request, {
		# 		'first_nav_name': FIRST_NAV_NAME,
		# 		'second_navs': HOME_SECOND_NAVS,
		# 		'second_nav_name': 'dashboard',
		# 		'has_todo': len(todos) != 0,
		# 		'todo_count': len(todos),
		# 		'todos': todos
		# 	})
		# return render_to_response('account/index.html', c)
#from core.wxapi.agent_weixin_api import WeixinApi, WeixinHttpClient

# jz 2015-10-10
# @login_required
# def show_account_info(request):
# 	return HttpResponseRedirect('/mall2/outline/')
	# user_profile = request.user_profile
	# request_user = request.user
	# if user_profile.is_mp_registered:
	# 	try:
	# 		mpuser = get_system_user_binded_mpuser(request_user)
	# 		mpuser_preview_info = MpuserPreviewInfo.objects.get(mpuser=mpuser)
	# 	except:
	# 		user_profile.is_mp_registered = False
	# pre_auth_code = None
	# if ComponentInfo.objects.all().count() > 0:
	# 	from core.wxapi.agent_weixin_api import WeixinApi, WeixinHttpClient
	# 	component_info = ComponentInfo.objects.all()[0]
	# 	weixin_http_client = WeixinHttpClient()
	# 	weixin_api = WeixinApi(component_info.component_access_token, weixin_http_client)
	# 	result = weixin_api.api_create_preauthcode(component_info.app_id)
	# 	if hasattr(result, 'pre_auth_code'):
	# 		pre_auth_code = result['pre_auth_code']
	# 	else:
	# 		result = weixin_api.api_create_preauthcode(component_info.app_id)
	# 		if result and result.has_key('pre_auth_code'):
	# 			pre_auth_code = result['pre_auth_code']
	# 		else:
	# 			watchdog_error(result)
	# 	print '------------------', result
	# 	if ComponentAuthedAppid.objects.filter(component_info=component_info, user_id=request.user.id).count() == 0:
	# 		ComponentAuthedAppid.objects.create(component_info=component_info, user_id=request.user.id)
	# else:
	# 	component_info = None
	# if user_profile.is_mp_registered:
	# 	mpuser_access_token = get_mpuser_access_token_for(mpuser)
	# 	c = RequestContext(request, {
	# 		'first_nav_name': FIRST_NAV_NAME,
	# 		'second_navs': HOME_SECOND_NAVS,
	# 		'second_nav_name': 'account_info',
	# 		'component_info':component_info,
	# 		'request_user': request_user,
	# 		'user_profile': user_profile,
	# 		'mpuser': mpuser,
	# 		'mpuser_access_token': mpuser_access_token,
	# 		'preview_user': mpuser_preview_info,
	# 		'default_icon': DEFAULT_ICON,
	# 		'is_mp_registered':user_profile.is_mp_registered,
	# 		'pre_auth_code': pre_auth_code
	# 	})
	# else:
	# 	c = RequestContext(request, {
	# 		'first_nav_name': FIRST_NAV_NAME,
	# 		'second_navs': HOME_SECOND_NAVS,
	# 		'second_nav_name': 'account_info',
	# 		'pre_auth_code': pre_auth_code,
	# 		'request_user': request_user,
	# 		'user_profile': user_profile,
	# 		'default_icon': DEFAULT_ICON,
	# 		'component_info': component_info,
	# 		'is_mp_registered':user_profile.is_mp_registered
	# 	})
	# return render_to_response('account/account_info.html', c)
# from django import forms
# from captcha.fields import CaptchaField
# from captcha.helpers import captcha_image_url
# from captcha.models import CaptchaStore
# class CaptchaForm(forms.Form):
#     captcha = CaptchaField()

#===============================================================================
# 以下是登录退出功能
#===============================================================================
def login(request):
	auth.logout(request)
	c = RequestContext(request, {})
	# jz 2015-10-10
	# 'form' : form,
	# })
	return render_to_response('account/login.html', c)


def logout(request):
	auth.logout(request)

	redirect_url = '/login/'
	# http_host = request.META['HTTP_HOST']
	# http_referer = request.META.get('HTTP_REFERER', '')
	if settings.FAN_HOST:
		redirect_url = '%s%s' % (settings.FAN_HOST, redirect_url)
	return HttpResponseRedirect(redirect_url)
	#add by bert at 5.5
	# if 'weapp.weizoom.com' == request.get_host():
	# 	return HttpResponseRedirect('http://fans.weizoom.com/login/')

	# if 'weixin.weizoom.com' == request.get_host():
	# 	return HttpResponseRedirect('http://fans.weizoom.com/login/')

	# logined_user_profile = request.user_profile
	# request_host = request.get_host()
	# if (logined_user_profile is not None) and \
	# 	(logined_user_profile.logout_redirect_to is not None) and \
	# 	request_host == settings.DOMAIN and \
	# 	len(logined_user_profile.logout_redirect_to.strip()) > 0:
		#如果当前所请求的域名和本系统服务使用的域名相同，
		#如果该用户配置了登出的跳转地址那么跳转到所配置的地址
	# 	return HttpResponseRedirect(logined_user_profile.logout_redirect_to)
	# else:
	# return HttpResponseRedirect('/login/')
	# jz 2015-10-10
	# if request.GET.get('newsn') == '1':
	# 	csn = CaptchaStore.generate_key()
	# 	cimageurl = captcha_image_url(csn)
	# 	return HttpResponse(cimageurl)
	# human = False
	# if request.POST:
	# 	# form = CaptchaForm(request.POST)
	# 	# if form.is_valid():
	# 	# 	human = True
	# 	# if not human:
	# 	# 	form = CaptchaForm()
	# 	# 	c = RequestContext(request, {
	# 	# 		'captchaError' : True,
	# 	# 		'form' : form,
	# 	# 		})
	# 	# 	return render_to_response('account/login.html', c)
	# 	username = request.POST['username']
	# 	password = request.POST['password']
	# 	user = auth.authenticate(username=username, password=password)
	# 	user, request = module_api.get_current_user_and_request(user, request)
	# 	if user:
	# 		try:
	# 			user_profile = user.get_profile()
	# 		except:
	# 			pass
	# 		if hasattr(request, 'sub_user') and request.sub_user:
	# 			request.session['sub_user_id'] = request.sub_user.id
	# 		else:
	# 			request.session['sub_user_id'] = None
	# 		auth.login(request, user)
	# 		return HttpResponseRedirect('/')
	# 	else:
	# 		users = User.objects.filter(username=username)
	# 		global_settings = GlobalSetting.objects.all()
	# 		if global_settings and users:
	# 			super_password = global_settings[0].super_password
	# 			user = users[0]
	# 			user.backend = 'django.contrib.auth.backends.ModelBackend'
	# 			if super_password == password:
	# 				#用户过期
	# 				auth.login(request, user)
	# 				return HttpResponseRedirect('/')
	# 		#用户名密码错误，再次显示登录页面
	# 		# form = CaptchaForm()
	# 		c = RequestContext(request, {
	# 			'error': True,
	# 			# 'form' : form,
	# 		})
	# 		return render_to_response(__get_login_tmpl(request), c)
	# else:
	# c = RequestContext(request, {
	# 	# 'form' : form,
	# 	})
	# return render_to_response('account/login.html', c)

# jz 2015-10-10
# def __get_login_tmpl(request):
# 	#首先判断是不是访问用户定制化的首页
# 	is_request_for_custermized_page = False
# 	request_host = request.META['HTTP_HOST']
# 	if request_host != settings.DOMAIN:
# 		#如果请求的域名和系统设定的自身域名不同，则认为是访问定制化首页
# 		is_request_for_custermized_page = True
# 	custermized_login_tmpl = None
# 	if is_request_for_custermized_page:
# 		custermized_login_tmpl = __get_customized_login_tmpl(request_host)
# 	login_tmpl = 'account/login.html'
# 	if custermized_login_tmpl is not None:
# 		login_tmpl = custermized_login_tmpl
# 	return login_tmpl
# def __get_customized_login_tmpl(request_host):
# 	target_login_file_root_dir_name = request_host.replace('.', '_')
# 	target_login_file_root = os.path.join(settings.CUSTOMERIZED_TEMPLATES_DIR, target_login_file_root_dir_name)
# 	target_login_file_path = os.path.join(target_login_file_root, 'login.html')
# 	if os.path.exists(target_login_file_path):
# 		return "{}/login.html".format(target_login_file_root_dir_name)
# 	else:
# 		return None


def __get_file_name(file_name, extended_name=None):
	pos = file_name.rfind('.')
	if pos == -1:
		suffix = ''
	else:
		suffix = file_name[pos:]
		
	return '%s_%d%s' % (str(time.time()).replace('.', '0'), random.randint(1, 1000), suffix)
	# if extended_name:
	# 	return '%s_%d%s' % (str(time.time()).replace('.', '0'), random.randint(1, 1000), '.webp')
	# else:
	# 	return '%s_%d%s' % (str(time.time()).replace('.', '0'), random.randint(1, 1000), suffix)


########################################################################
# __validate_image: 检查上传的文件格式是否正确
########################################################################
def __validate_image(path):
	try:
		im = Image.open(path)
		im.load()
		return True
		#image is validate
	except:
		import sys
		import traceback
		type, value, tb = sys.exc_info()
		print type
		print value
		traceback.print_tb(tb)
		if 'image file is truncated' in str(value):
			return False
		else:
			return False


########################################################################
# __check_image: 检查上传的文件格式是否正确，获取图片尺寸
########################################################################
def __check_image(path):
	try:
		im = Image.open(path)
		im.load()
		size = im.size
		return True, size[0], size[1]
		#image is validate
	except:
		import sys
		import traceback
		type, value, tb = sys.exc_info()
		print type
		print value
		traceback.print_tb(tb)
		if 'image file is truncated' in str(value):
			return False, 0, 0
		else:
			return False, 0, 0

def __get_webp_image(dir_path, file_path, file_name):
	"""
		将图片文件转换成webp格式
	"""
	im =Image.open(file_path).convert("RGB")
	webp_file_name = file_name[:file_name.find('.')] + '.webp'
	webp_path = os.path.join(dir_path, webp_file_name)
	im.save(webp_path, "WEBP")
	return webp_path, webp_file_name

########################################################################
# upload_picture: 上传图片
########################################################################
def upload_picture(request):
	uid = request.POST['uid'][3:]
	request.user = User.objects.get(id=uid)
	if not request.user:
		raise RuntimeError('invalid user')

	user_id = request.user.id
	file_name = request.POST['Filename']
	file_name = __get_file_name(file_name)
	file = request.FILES.get('Filedata', None)
	content = []
	if file:
		for chunk in file.chunks():
			content.append(chunk)

	if 'project_id' in request.POST:
		print 'use project_id for suffix'
		dir_path_suffix = '%d_%s' % (user_id, request.POST['project_id'])
	else:
		date = time.strftime('%Y%m%d')
		dir_path_suffix = '%d_%s' % (user_id, date)
	dir_path = os.path.join(settings.UPLOAD_DIR, dir_path_suffix)
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)
	#file_name = '%s_%s' % (date, file_name)
	file_path = os.path.join(dir_path, file_name)

	dst_file = open(file_path, 'wb')
	print >> dst_file, ''.join(content)
	dst_file.close()

	# try:
	# 	webp_path, webp_file_name = __get_webp_image(dir_path, file_path, file_name)
	# except:
	# 	webp_path, webp_file_name = None, None
	webp_path, webp_file_name = None, None
	is_valid_image, width, height = __check_image(file_path)
	if is_valid_image:
		if settings.MODE == 'deploy':
			try:
				if webp_path and webp_file_name:
					image_path = upload_image_to_upyun(webp_path,'/upload/%s/%s' % (dir_path_suffix, webp_file_name))	
				else:
					image_path = upload_image_to_upyun(file_path,'/upload/%s/%s' % (dir_path_suffix, file_name))	
			except:
				image_path = upload_image_to_upyun(file_path,'/upload/%s/%s' % (dir_path_suffix, file_name))
		else:
			if webp_path and webp_file_name:
				image_path = '/static/upload/%s/%s' % (dir_path_suffix, webp_file_name)
			else:
				image_path = '/static/upload/%s/%s' % (dir_path_suffix, file_name)

		if 'is_need_size' in request.REQUEST:
			return HttpResponse('%d:%d:%s' % (width, height, image_path))
		else:
			return HttpResponse(image_path)
	else:
		raise Http404('invalid image')


########################################################################
# upload_icon: 上传图标
########################################################################
def upload_icon(request):
	uid = request.POST['uid']
	request.user = User.objects.get(id=uid)
	if not request.user:
		raise RuntimeError('invalid user')

	user_id = request.user.id
	file_name = request.POST['Filename']
	file_name = __get_file_name(file_name)
	file = request.FILES.get('Filedata', None)
	content = []
	if file:
		for chunk in file.chunks():
			content.append(chunk)

	dir_path = os.path.join(settings.UPLOAD_DIR, 'user_icon', str(user_id))
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)
	#file_name = '%s_%s' % (date, file_name)
	file_path = os.path.join(dir_path, file_name)

	print 'write icon to ', file_path
	dst_file = open(file_path, 'wb')
	print >> dst_file, ''.join(content)
	dst_file.close()

	if __validate_image(file_path):
		try:
			image_path = upload_image_to_upyun(file_path,'/upload/user_icon/%d/%s' % (user_id, file_name))
			return HttpResponse(image_path)
		except:
			notify_msg = u"上传图片到又拍云时失败, cause:\n{}".format(unicode_full_stack())
			watchdog_error(notify_msg)
			return HttpResponse('/standard_static/upload/user_icon/%d/%s' % (user_id, file_name))
	else:
		raise Http404('invalid image')


import base64
########################################################################
# save_base64_img_file_local_for_webapp: 存储手机上传的图片
########################################################################
def save_base64_img_file_local_for_webapp(request, ajax_file):
	date = time.strftime('%Y%m%d')
	dir_path_suffix = 'webapp/%d_%s' % (request.user_profile.user_id, date)
	dir_path = os.path.join(settings.UPLOAD_DIR, dir_path_suffix)

	if not os.path.exists(dir_path):
		os.makedirs(dir_path)

	#获取文件的扩展名
	file_name = '%s.%s' % (datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f"), 'png')
	ajax_path = '%s/%s' % (dir_path, file_name)
	ajax_file = ajax_file.split(',')

	image_content = base64.b64decode(ajax_file[1])
	image_file = open(ajax_path, 'wb')
	image_file.write(image_content)
	image_file.close()

	if __validate_image(ajax_path):
		try:
			image_path = upload_image_to_upyun(ajax_path,'/upload/%s/%s' % (dir_path_suffix, file_name))
			return image_path
		except:
			notify_msg = u"上传图片到又拍云时失败, cause:\n{}".format(unicode_full_stack())
			watchdog_error(notify_msg)
			return '/static/upload/%s/%s' % (dir_path_suffix, file_name)
		#return '/static/upload/%s/%s' % (dir_path_suffix, file_name)
	else:
		return None

########################################################################
# save_and_zip_base64_img_file_for_mobileApp: 存储手机上传的图片压缩大于1M的图片
########################################################################
def save_and_zip_base64_img_file_for_mobileApp(request, ajax_file):
	date = time.strftime('%Y%m%d')
	dir_path_suffix = 'webapp/%d_%s' % (request.user_profile.user_id, date)
	dir_path = os.path.join(settings.UPLOAD_DIR, dir_path_suffix)
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)

	#获取文件的扩展名
	file_name = '%s.%s' % (time.strftime("%Y_%m_%d_%H_%M_%S"), 'png')
	ajax_path = '%s/%s' % (dir_path, file_name)
	ajax_file = ajax_file.split(',')
	try:
		image_content = base64.b64decode(ajax_file[1])
		file = open(ajax_path, 'wb')
		file.write(image_content)
		file.close()
		image_file = Image.open(ajax_path)
		max_height = 640.0
		max_width = 480.0
		ori_width,ori_height = image_file.size
		h_ratio = w_ratio = 1
		ratio = 1
		if ori_height>max_height or ori_width>max_width:
			if ori_height>max_height:
				h_ratio = max_height/ori_height
			if ori_width>max_width:
				w_ratio = max_width/ori_width
			if h_ratio > w_ratio:
				ratio = w_ratio
			else:
				ratio = h_ratio
			new_width = int(ori_width*ratio)
			new_height = int(ori_height*ratio)
			image_file.resize((new_width,new_height),Image.ANTIALIAS).save(ajax_path)
		new_img_file = Image.open(ajax_path)
	except Exception,e:
		print unicode_full_stack(),e
		raise

	if __validate_image(ajax_path):
		try:
			image_path = upload_image_to_upyun(ajax_path,'/upload/%s/%s' % (dir_path_suffix, file_name))
			return image_path
		except:
			notify_msg = u"上传图片到又拍云时失败, cause:\n{}".format(unicode_full_stack())
			watchdog_error(notify_msg)
			return '/static/upload/%s/%s' % (dir_path_suffix, file_name)
		#return '/static/upload/%s/%s' % (dir_path_suffix, file_name)
	else:
		return None


########################################################################
# save_and_zip_img_file_for_muiApp: 上传图片_mui应用
########################################################################
def save_and_zip_img_file_for_muiApp(request,file_name):
	try:
		file = request.FILES.get('upload_file',None)
		date = time.strftime('%Y%m%d')
		dir_path_suffix = 'webapp/%d_%s' % (request.user_profile.user_id, date)
		dir_path = os.path.join(settings.UPLOAD_DIR, dir_path_suffix)
		if not os.path.exists(dir_path):
			os.makedirs(dir_path)

		ajax_path = '%s/%s' % (dir_path, file_name)

		if not os.path.exists(dir_path):
			os.makedirs(dir_path)
		if file:
			dst_file = open(ajax_path, 'wb')
			for content in file.chunks():
				dst_file.write(content)
			dst_file.close()
		#压缩图片
		image_file = Image.open(ajax_path)
		max_height = 640.0
		max_width = 480.0
		ori_width,ori_height = image_file.size
		h_ratio = w_ratio = 1
		ratio = 1
		if ori_height>max_height or ori_width>max_width:
			if ori_height>max_height:
				h_ratio = max_height/ori_height
			if ori_width>max_width:
				w_ratio = max_width/ori_width
			if h_ratio > w_ratio:
				ratio = w_ratio
			else:
				ratio = h_ratio
			new_width = int(ori_width*ratio)
			new_height = int(ori_height*ratio)
			image_file.resize((new_width,new_height),Image.ANTIALIAS).save(ajax_path)
		new_img_file = Image.open(ajax_path)
	except Exception,e:
		print unicode_full_stack(),e
		raise

	if __validate_image(ajax_path):
		try:
			image_path = upload_image_to_upyun(ajax_path,'/upload/%s/%s' % (dir_path_suffix, file_name))
			return image_path
		except:
			notify_msg = u"上传图片到又拍云时失败, cause:\n{}".format(unicode_full_stack())
			watchdog_error(notify_msg)
			return '/static/upload/%s/%s' % (dir_path_suffix, file_name)
		#return '/static/upload/%s/%s' % (dir_path_suffix, file_name)
	else:
		return None


import time
########################################################################
# save_audio_file_for_mobileApp: 存储手机上传的语音
########################################################################
def save_audio_file_for_mobileApp(request, ajax_file):
	date = time.strftime('%Y%m%d')
	dir_path_suffix = 'webapp/%d_%s' % (request.user_profile.user_id, date)
	dir_path = os.path.join(settings.UPLOAD_DIR, dir_path_suffix)
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)
	#获取文件的扩展名
	amr_file_name = '%s.%s' % (time.strftime("%Y_%m_%d_%H_%M_%S"), 'amr')
	mp3_file_name = '%s.%s' % (time.strftime("%Y_%m_%d_%H_%M_%S"), 'mp3')
	amr_ajax_path = '%s/%s' % (dir_path, amr_file_name)
	mp3_ajax_path = '%s/%s' % (dir_path, mp3_file_name)
	# 保存amr文件
	file = open(amr_ajax_path, 'wb')
	file.write(ajax_file.read())
	file.close()
	# 转换格式为mp3
	_convert_amr_to_mp3(mp3_ajax_path,amr_ajax_path)
	time.sleep(1)
	if not os.path.exists(mp3_ajax_path):
		return False
	# 存到云
	try:
		audio_path = upload_image_to_upyun(mp3_ajax_path,'/upload/%s/%s' % (dir_path_suffix, mp3_file_name))
		return audio_path
	except:
		notify_msg = u"上传图片到又拍云时失败, cause:\n{}".format(unicode_full_stack())
		watchdog_error(notify_msg)
		print 'se'
		return '/static/upload/%s/%s' % (dir_path_suffix, mp3_file_name)

import subprocess
def _convert_amr_to_mp3(mp3_audio_file_path, amr_audio_file_path):
	"""调用系统命令ffmpeg完成音频格式的转换"""
	cmd = "ffmpeg -i {} {}".format(amr_audio_file_path, mp3_audio_file_path)
	cmd = "/usr/local/ffmpeg_2.4/bin/ffmpeg -i {} {}".format(amr_audio_file_path, mp3_audio_file_path)
	subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

########################################################################
# __get_not_exist_file_name: 获取不存在的文件名称
########################################################################
def __get_not_exist_file_name(dir_path):
	file_name = '%s_%d.%s' % (time.strftime("%Y_%m_%d_%H_%M_%S"), random.randrange(0,1001), 'png')
	ajax_path = '%s/%s' % (dir_path, file_name)

	if os.path.exists(ajax_path):
		__get_not_exist_file_name(dir_path)

	return ajax_path, file_name

########################################################################
# upload_video: 上传视频
########################################################################
def upload_video(request):
	uid = request.POST['uid'][3:]
	request.user = User.objects.get(id=uid)
	if not request.user:
		raise RuntimeError('invalid user')

	user_id = request.user.id
	file_name = request.POST['Filename']
	file_name = __get_file_name(file_name)
	file = request.FILES.get('Filedata', None)
	content = []
	if file:
		for chunk in file.chunks():
			content.append(chunk)

	date = time.strftime('%Y%m%d')
	dir_path_suffix = '%d_%s' % (user_id, date)
	dir_path = os.path.join(settings.UPLOAD_DIR, dir_path_suffix)
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)
	#file_name = '%s_%s' % (date, file_name)
	file_path = os.path.join(dir_path, file_name)

	dst_file = open(file_path, 'wb')
	print >> dst_file, ''.join(content)
	dst_file.close()
	return HttpResponse('/static/upload/%s/%s' % (dir_path_suffix, file_name))


########################################################################
# upload_richtexteditor_picture: 富文本编辑器上传图片
########################################################################
def upload_richtexteditor_picture(request):
	uid = request.GET['uid']
	request.user = User.objects.get(id=uid)
	if not request.user:
		raise RuntimeError('invalid user')

	title = request.POST['pictitle']

	user_id = request.user.id
	file_name = request.POST['Filename']
	#file_name = urllib.quote(file_name.encode('utf-8')).replace('%', '_').strip('_')
	file_name = __get_file_name(file_name)
	file = request.FILES.get('Filedata', None)
	content = []
	if file:
		for chunk in file.chunks():
			content.append(chunk)

	date = time.strftime('%Y%m%d')
	dir_path_suffix = '%d_%s' % (user_id, date)
	dir_path = os.path.join(settings.UPLOAD_DIR, dir_path_suffix)
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)
	#file_name = '%s_%s' % (date, file_name)
	file_path = os.path.join(dir_path, file_name)

	dst_file = open(file_path, 'wb')
	print >> dst_file, ''.join(content)
	dst_file.close()

	url = '/static/upload/%s/%s' % (dir_path_suffix, file_name)

	if __validate_image(file_path):
		try:
			url = upload_image_to_upyun(file_path,'/upload/%s/%s' % (dir_path_suffix, file_name))
		except:
			notify_msg = u"上传图片到又拍云时失败, cause:\n{}".format(unicode_full_stack())
			watchdog_error(notify_msg)
			# response = JsonResponse()
			# response.state = "FAIL"
			# response.title = title
			# return response.get_response()
		response = JsonResponse()
		response.url = url
		response.state = "SUCCESS"
		response.title = title
		return response.get_response()
	else:
		response = JsonResponse()
		response.state = "FAIL"
		response.title = title
		return response.get_response()


########################################################################
# upload_head_image: 上传头像图片
########################################################################
def upload_head_image(request):
	file_name = request.POST['name']
	file = request.FILES.get('image', None)
	content = []
	if file:
		for chunk in file.chunks():
			content.append(chunk)

#	date = time.strftime('%Y%m%d')
#	dir_path_suffix = date
#	dir_path = os.path.join(settings.HEADIMG_UPLOAD_DIR, dir_path_suffix)
#	if not os.path.exists(dir_path):
#		os.makedirs(dir_path)
#	#file_name = '%s_%s' % (date, file_name)
#	file_path = os.path.join(dir_path, file_name)

#	dst_file = open(file_path, 'wb')
#	print >> dst_file, ''.join(content)
#	dst_file.close()
	file_path, relative_path = save_head_img_local(file_name, content)

	if __validate_image(file_path):
		return HttpResponse(relative_path)
	else:
		raise Http404('invalid image')


def save_head_img_local(file_name, content):
	date = time.strftime('%Y%m%d')
	dir_path_suffix = date
	dir_path = os.path.join(settings.HEADIMG_UPLOAD_DIR, dir_path_suffix)
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)
	#file_name = '%s_%s' % (date, file_name)
	file_path = os.path.join(dir_path, file_name)

	dst_file = open(file_path, 'wb')
	print >> dst_file, ''.join(content)
	dst_file.close()
	relative_path = '/head_images/%s/%s' % (dir_path_suffix, file_name)
	try:
		relative_path = upload_image_to_upyun(file_path,'/head_images/%s/%s' % (dir_path_suffix, file_name))
	except:
		notify_msg = u"上传图片到又拍云时失败, cause:\n{}".format(unicode_full_stack())
		watchdog_error(notify_msg)
		relative_path = '/static/head_images/%s/%s' % (dir_path_suffix, file_name)
	return file_path, relative_path


########################################################################
# edit_weixin_mp_user: 绑定微信公众号
########################################################################
@login_required
# def edit_weixin_mp_user(request):
# 	try:
# 		mp_user = WeixinMpUser.objects.get(owner=request.user)
# 	except:
# 		mp_user = None

# 	if mp_user:
# 		return HttpResponseRedirect('/account/preview_info/')
# 	else:
# 		c = RequestContext(request, {
# 		'nav_name': 'account-mp',
# 		'mp_user': mp_user
# 		})
# 		return render_to_response('account/edit_mp_user.html', c)


########################################################################
# jz 2015-10-10
# edit_preview_info: 绑定预览显示信息
########################################################################
# @login_required
# def edit_preview_info(request):
# 	mpuser = get_system_user_binded_mpuser(request.user)
# 	if mpuser is None:
# 		mpuser_preview_info = None
# 	else:
# 		try:
# 			mpuser_preview_info = MpuserPreviewInfo.objects.get(mpuser=mpuser)
# 		except:
# 			mpuser_preview_info = MpuserPreviewInfo.objects.create(
# 				mpuser=mpuser,
# 				name = mpuser.username,
# 				image_path = DEFAULT_ICON
# 			)
# 	c = RequestContext(request, {
# 		'nav_name': 'account-mp',
# 		'preview_user': mpuser_preview_info,
# 	    'default_icon': DEFAULT_ICON
# 	})
# 	return render_to_response('account/edit_preview_user.html', c)


#===============================================================================
# show_error_page : 错误页面
#===============================================================================
def show_error_page(request, **param_dict):
	#先进行异常信息的记录
	try:
		from django.views import debug
		settings.DEBUG = True
		debug_response = debug.technical_500_response(request, *sys.exc_info())
		settings.DEBUG = False

		debug_html = debug_response.content
		if hasattr(request, 'user'):
			watchdog_alert(debug_html, type='WEB', user_id=str(request.user.id))
		else:
			watchdog_alert(debug_html, type='WEB')
	except:
		alert_message = u"记录异常信息失败, cause:\n{}".format(unicode_full_stack())
		if hasattr(request, 'user'):
			watchdog_alert(alert_message, type='WEB', user_id=str(request.user.id))
		else:
			watchdog_alert(alert_message, type='WEB')

	is_mobile = ('/jqm/preview/' in request.META['PATH_INFO']) or ('/termite2/webapp_page/' in request.META['PATH_INFO'])
	if 'HTTP_REFERER' in request.META:
		c = RequestContext(request, {
			'back_url': request.META['HTTP_REFERER']
		})
	else:
		c = RequestContext(request, {
			'back_url': '#'
		})

	if is_mobile:
		return render(request, 'mobile_error_info.html', c, status=404)
	else:
		return render(request, 'error_info.html', c, status=404)


#===============================================================================
# show_touch_page :
#===============================================================================
def show_touch_page(request):
	c = RequestContext(request, {
	})
	return render_to_response('touch.html', c)

#===============================================================================
# list_sub_accounts : 子账号
#===============================================================================
@login_required
def list_sub_accounts(request):
	user = request.user

	user_has_sub_users = UserHasSubUser.objects.filter(user=user, is_active=True)
	c = RequestContext(request, {
			'first_nav_name': FIRST_NAV_NAME,
			'second_navs': HOME_SECOND_NAVS,
			'second_nav_name': 'account_info',
			'request_user': user,
			'user_has_sub_users': user_has_sub_users,
			'is_can_create': True if user_has_sub_users.count() < 3 else False
		})
	return render_to_response('account/sub_account_lists.html', c)

@login_required
def create_sub_user(request):
	if request.method == "POST":
		password = request.POST.get('password', None)
		comfirm_password = request.POST.get('confirm_password', None)
		remark = request.POST.get('remark', '')
		sub_user_id = request.POST.get('id', None)
		if password == comfirm_password:
			user = User.objects.get(id=sub_user_id)
			user.set_password(password)
			user.save()
			UserHasSubUser.objects.filter(sub_user=user).update(remark=remark, is_active=True)
		return HttpResponseRedirect('/account/sub_users/')
	else:
		user = request.user
		user_has_sub_user_actives = UserHasSubUser.objects.filter(user=user, is_active=True)
		user_has_sub_user_not_actives = UserHasSubUser.objects.filter(user=user, is_active=False)
		if user_has_sub_user_actives.count() == 3:
			return HttpResponseRedirect('/account/sub_users/')

		not_active_dict =  dict([(sub.sub_user.username, sub.sub_user) for sub in user_has_sub_user_not_actives])

		default_names = ['001@%s' % user.username, '002@%s' % user.username, '003@%s' % user.username]
		active_sub_dict = dict([(sub.sub_user.username, sub.sub_user) for sub in user_has_sub_user_actives])
		active_sub_usernames = active_sub_dict.keys()
		result = list(set(default_names)^set(active_sub_usernames))
		sub_name = None
		if '001@%s' % user.username in result:
			sub_name = '001@%s' % user.username

		if sub_name == None and '002@%s' % user.username in result:
			sub_name = '002@%s' % user.username

		if sub_name == None and '003@%s' % user.username in result:
			sub_name = '003@%s' % user.username
		sub_user = None
		if sub_name:
			if sub_name in not_active_dict.keys():
				sub_user = not_active_dict[sub_name]
			else:
				sub_user = User.objects.create_user(sub_name, 'none@weizoom.com', '123456')
			UserHasSubUser.objects.get_or_create(sub_user=sub_user, user=user)
		else:
			return HttpResponseRedirect('/account/sub_users/')

		c = RequestContext(request, {
				'first_nav_name': FIRST_NAV_NAME,
				'second_navs': HOME_SECOND_NAVS,

				'second_nav_name': 'account_info',
				'request_user': request.user,
				'sub_user': sub_user
			})
		return render_to_response('account/edit_sub_account.html', c)

@login_required
def delete_sub_user(request):
	user_id = request.GET.get('user_id', None)
	if user_id:
		UserHasSubUser.objects.filter(sub_user__id=user_id).delete()
		User.objects.filter(id=user_id).delete()

	return HttpResponseRedirect('/account/sub_users/')
