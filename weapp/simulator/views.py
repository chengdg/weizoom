# -*- coding: utf-8 -*-
"""
微信模拟器

"""

import time
from datetime import timedelta, datetime, date
import os
import json
import hashlib
from core.jsonresponse import create_response

from BeautifulSoup import BeautifulSoup

from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.test import Client

from account.models import UserProfile
from weixin.user import module_api
from weixin.user.models import WeixinMpUser, MpuserPreviewInfo, get_system_user_binded_mpuser
from weixin.message import generator
from weixin.manage.customerized_menu import util as menu_util
from models import *


def start_simulator(request):
	"""
	启动微信模拟器
	"""
	if settings.MODE == 'develop' or settings.MODE == 'test':
		is_in_dev_mode = True
	else:
		is_in_dev_mode = False

	if request.user.is_authenticated():
		# 如果已经登录过
		mpuser = get_system_user_binded_mpuser(request.user)

		if mpuser:
			try:
				mpuser_preview_info = MpuserPreviewInfo.objects.get(mpuser=mpuser)
			except:
				mpuser_preview_info = None
		else:
			mpuser_preview_info = None

		c = RequestContext(request, {
			'title': mpuser_preview_info.name if (mpuser_preview_info and mpuser_preview_info.name) else u'信息预览',
			'is_logined': True,
			'is_in_dev_mode': is_in_dev_mode,
			'mp_users': json.dumps([]),
			'menus_json': menu_util.get_menus_json(request.user)
		})
		return render_to_response('simulator/simulator.html', c)
	else:
		user2profile = dict([(p.user_id, p) for p in list(UserProfile.objects.all())])
		id2user = dict([(u.id, u) for u in list(User.objects.all())])
		id2mpuser = dict([(u.id, u) for u in WeixinMpUser.objects.all()])
		mp_users = []
		for mp_user in id2mpuser.values():
			user_id = mp_user.owner_id
			user_name = id2user[user_id].username
			profile = user2profile[user_id]
			mp_users.append({
				'webapp_id': profile.webapp_id,
				'mp_user_name': user_name
			})

		c = RequestContext(request, {
	    	'is_logined': False,
	    	'mp_users': json.dumps(mp_users),
	    	'is_in_dev_mode': is_in_dev_mode,
	    	'menus_json': "[]"
		})
		return render_to_response('simulator/simulator.html', c)


########################################################################
# start_advance_simulator: 启动高级微信模拟器
########################################################################
def start_advance_simulator(request):
	if settings.MODE == 'develop' or settings.MODE == 'test':
		is_in_dev_mode = True
	else:
		is_in_dev_mode = False

	if request.user.is_authenticated():
		c = RequestContext(request, {
		})
		return render_to_response('simulator/not_allowed_advance_simulator.html', c)
	else:
		user2profile = dict([(p.user_id, p) for p in list(UserProfile.objects.all())])
		id2user = dict([(u.id, u) for u in list(User.objects.all())])
		id2mpuser = dict([(u.id, u) for u in WeixinMpUser.objects.all()])
		mp_users = []
		for mp_user in id2mpuser.values():
			user_id = mp_user.owner_id
			user_name = id2user[user_id].username
			profile = user2profile.get(user_id, None)
			if not profile:
				continue
			mp_users.append({
				'webapp_id': profile.webapp_id,
				'mp_user_name': user_name
			})
		mp_users.sort(lambda x,y:cmp(x['webapp_id'], y['webapp_id']))

		simulator_users = []
		for simulator_user in SimulatorUser.objects.all():
			simulator_users.append({
				'name': simulator_user.name,
				'display_name': simulator_user.display_name
			})

		c = RequestContext(request, {
	    	'is_logined': False,
	    	'mp_users': mp_users,
	    	'simulator_users': simulator_users,
	    	'is_in_dev_mode': is_in_dev_mode,
	    	'menus_json': "[]"
		})
		return render_to_response('simulator/advance_simulator.html', c)


########################################################################
# render_text_response: 渲染文本类消息回复
########################################################################
def render_text_response(xml_response):
	beg_tag = '<Content><![CDATA['
	beg = xml_response.find(beg_tag) + len(beg_tag)
	end = xml_response.find(']]>', beg)
	content = xml_response[beg:end]

	c = Context({'content':content})
	http_response = render_to_response('weixin/text_content.html', c)
	return http_response.content.decode('utf-8')


########################################################################
# render_news_response: 渲染图文类消息回复
########################################################################
def render_news_response(html_response):
	message = BeautifulSoup(html_response.content)
	items = message.articles.findAll('item')

	#处理第一条消息
	main_message = items[0]
	params = {
		'main_message': {
			'title': main_message.title.text,
			'description': main_message.description.text,
			'pic_url': main_message.picurl.text,
			'url': main_message.url.text
		},
	    'sub_messages': []
	}

	#处理后续的消息
	sub_messages = items[1:]
	for sub_message in sub_messages:
		message = {
			'title': sub_message.title.text,
			'description': sub_message.description.text,
			'pic_url': sub_message.picurl.text,
			'url': sub_message.url.text
		}
		params['sub_messages'].append(message)

	c = Context(params)
	if len(sub_messages) == 0:
		http_response = render_to_response('weixin/single_news_content.html', c)
	else:
		http_response = render_to_response('weixin/news_content.html', c)
	return http_response.content.decode('utf-8')


########################################################################
# send_from_simulator: 启动微信模拟器
########################################################################
def send_from_simulator(request):
	content = request.POST['content']
	webapp_id = request.POST['webapp_id']
	weixin_user_name = request.POST['weixin_user_name']
	weixin_user_fakeid = request.POST['weixin_user_fakeid']

	#构造传递给message handler的参数
	profile = UserProfile.objects.get(webapp_id=webapp_id)
	try:
		mp_user = WeixinMpUser.objects.get(owner_id=profile.user_id)
	except:
		mp_user = WeixinMpUser()
		mp_user.username = 'empty_weixin_mp_user_name'

	#
	#根据输入的文本内容 构造不同的消息 方便测试
	#
	if content == 'voice':
		data = generator.get_voice_request(mp_user.username, weixin_user_name, content)
	elif content == 'startaduio' or content == '__built_in:homepage':
		data = generator.get_text_test_event_request(mp_user.username, weixin_user_name, content)
	elif content == 'image_message_test':
		data = generator.get_image_message_test_request(mp_user.username, weixin_user_name, content)
	else:
		data = generator.get_text_request(mp_user.username, weixin_user_name, content)


	params = {
		'weizoom_test_data': data,
		'receiver_fake_id': '',
		'sender_fake_id': weixin_user_fakeid,
		'is_user_logined': 0
	}

	if request.user.is_authenticated():
		params['is_user_logined'] = 1

	#模拟POST，获得response
	authed_appid_info = module_api.authed_appid(profile.user_id)
	appid = authed_appid_info.authorizer_appid
	client = Client()
	html_response = client.post('/weixin/appid/%s/?weizoom_test_data=1' % appid, params)

	#从response中抽取返回的文本
	xml_response = html_response.content.decode('utf-8')
	if settings.DUMP_DEBUG_MSG == True:
		print '========== start response =========='
		if settings.IS_UNDER_BDD:
			print xml_response.replace('<', '{').replace('>', '}')
		else:
			print xml_response
		print '========== finish response =========='

	if '<MsgType><![CDATA[text]]></MsgType>' in xml_response:
		return_content = render_text_response(xml_response)
	elif '<MsgType><![CDATA[news]]></MsgType>' in xml_response:
		return_content = render_news_response(html_response)
	else:
		return_content = 'unknown_type'

	response = create_response(200)
	response.data = return_content
	return response.get_response()


########################################################################
# get_menu_event_response: 获得点击菜单事件的响应
########################################################################
def get_menu_event_response(request):
	content = request.POST['content']
	webapp_id = request.POST['webapp_id']
	from_user = request.POST.get('from_user', 'weizoom')
	profile = UserProfile.objects.get(webapp_id=webapp_id)
	#模拟POST，获得response
	authed_appid_info = module_api.authed_appid(profile.user_id)
	appid = authed_appid_info.authorizer_appid
	client = Client()
	html_response = client.post('/weixin/appid/%s/?weizoom_test_data=1' % appid, {
		'weizoom_test_data': generator.get_text_test_event_request(webapp_id, from_user, content)
	})

	#从response中抽取返回的文本
	xml_response = html_response.content.decode('utf-8')
	if settings.DUMP_DEBUG_MSG:
		print '========== start xml response =========='
		if settings.IS_UNDER_BDD:
			print xml_response.replace('<', '{').replace('>', '}')
		else:
			print xml_response
		print '========== finish xml response =========='
	if '<MsgType><![CDATA[text]]></MsgType>' in xml_response:
		return_content = render_text_response(xml_response)
	elif '<MsgType><![CDATA[news]]></MsgType>' in xml_response:
		return_content = render_news_response(html_response)
	else:
		return_content = 'unknown_type'

	response = create_response(200)
	response.data = return_content
	return response.get_response()


########################################################################
# subscribe: 关注公众账号
########################################################################
def subscribe(request):
	webapp_id = request.POST['webapp_id']
	from_user = request.POST.get('from_user', 'weizoom')
	profile = UserProfile.objects.get(webapp_id=webapp_id)
	#模拟POST，获得response
	authed_appid_info = module_api.authed_appid(profile.user_id)
	appid = authed_appid_info.authorizer_appid
	client = Client()
	html_response = client.post('/weixin/appid/%s/?weizoom_test_data=1' % appid, {
		'weizoom_test_data': generator.get_subscribe_event(webapp_id, from_user)
	})

	#从response中抽取返回的文本
	xml_response = html_response.content.decode('utf-8')
	if settings.DUMP_DEBUG_MSG:
		print '========== start xml response =========='
		if settings.IS_UNDER_BDD:
			print xml_response.replace('<', '{').replace('>', '}')
		else:
			print xml_response
		print '========== finish xml response =========='
	if '<MsgType><![CDATA[text]]></MsgType>' in xml_response:
		return_content = render_text_response(xml_response)
	elif '<MsgType><![CDATA[news]]></MsgType>' in xml_response:
		return_content = render_news_response(html_response)
	else:
		return_content = 'unknown_type'

	response = create_response(200)
	response.data = return_content
	return response.get_response()


########################################################################
# unsubscribe: 取消关注公众账号
########################################################################
def unsubscribe(request):
	webapp_id = request.POST['webapp_id']
	from_user = request.POST.get('from_user', 'weizoom')
	profile = UserProfile.objects.get(webapp_id=webapp_id)
	#模拟POST，获得response
	authed_appid_info = module_api.authed_appid(profile.user_id)
	appid = authed_appid_info.authorizer_appid
	client = Client()
	html_response = client.post('/weixin/appid/%s/?weizoom_test_data=1' % appid, {
		'weizoom_test_data': generator.get_unsubscribe_event(webapp_id, from_user)
	})

	#从response中抽取返回的文本
	xml_response = html_response.content.decode('utf-8')
	if settings.DUMP_DEBUG_MSG:
		print '========== start xml response =========='
		if settings.IS_UNDER_BDD:
			print xml_response.replace('<', '{').replace('>', '}')
		else:
			print xml_response
		print '========== finish xml response =========='
	if '<MsgType><![CDATA[text]]></MsgType>' in xml_response:
		return_content = render_text_response(xml_response)
	elif '<MsgType><![CDATA[news]]></MsgType>' in xml_response:
		return_content = render_news_response(html_response)
	else:
		return_content = 'unknown_type'

	response = create_response(200)
	response.data = return_content
	return response.get_response()

########################################################################
# subscribe: 关注公众账号
########################################################################
def qr_subscribe(request):
	webapp_id = request.POST['webapp_id']
	ticket = request.POST['ticket']
	from_user = request.POST.get('from_user', 'weizoom')
	profile = UserProfile.objects.get(webapp_id=webapp_id)
	#模拟POST，获得response
	authed_appid_info = module_api.authed_appid(profile.user_id)
	appid = authed_appid_info.authorizer_appid
	client = Client()
	html_response = client.post('/weixin/appid/%s/?weizoom_test_data=1' % appid, {
		'weizoom_test_data': generator.get_qrcode_subscribe_event(webapp_id, ticket, from_user)
	})
	#从response中抽取返回的文本
	xml_response = html_response.content.decode('utf-8')
	if settings.DUMP_DEBUG_MSG:
		print '========== start xml response =========='
		if settings.IS_UNDER_BDD:
			print xml_response.replace('<', '{').replace('>', '}')
		else:
			print xml_response
		print '========== finish xml response =========='
	if '<MsgType><![CDATA[text]]></MsgType>' in xml_response:
		return_content = render_text_response(xml_response)
	elif '<MsgType><![CDATA[news]]></MsgType>' in xml_response:
		return_content = render_news_response(html_response)
	else:
		return_content = 'unknown_type'

	response = create_response(200)
	response.data = return_content
	return response.get_response()