# -*- coding: utf-8 -*-

__author__ = 'chuter'

import json

from django.contrib.auth.decorators import login_required
from core.jsonresponse import JsonResponse, create_response
from core import emotion

from models import *
from weixin.message.qa.models import Rule, MENU_TYPE
from tools.customerized_menu import views as menu_tool
import util as menu_util
from account.models import UserProfile


########################################################################
# __create_rule: 创建rule
########################################################################
def __create_rule(owner, menu):
	answer = menu['answer']
	rule = None
	if answer['type'] == 'text':
		rule = Rule.objects.create(
			owner = owner,
			type = MENU_TYPE,
			patterns = 'MENU_QUERY_%s' % menu['id'],
			answer = emotion.change_img_to_emotion(answer['content'])
		)
	elif answer['type'] == 'news':
		rule = Rule.objects.create(
			owner = owner,
			type = MENU_TYPE,
			patterns = 'MENU_QUERY_%s' % menu['id'],
			answer = '',
			material_id = answer['content']
		)
	elif answer['type'] == 'url':
		rule = Rule.objects.create(
			owner = owner,
			type = MENU_TYPE,
			patterns = 'MENU_QUERY_%s' % menu['id'],
			answer = answer['content'],
			is_url = True
		)
	else:
		pass

	return rule


########################################################################
# __update_rule: 更新rule
########################################################################
def __update_rule(owner, menu):
	answer = menu['answer']
	pattern = 'MENU_QUERY_%s' % menu['id']
	if answer['type'] == 'text':
		rule = Rule.objects.filter(owner=owner, patterns=pattern).update(
			type = MENU_TYPE,
			answer = emotion.change_img_to_emotion(answer['content']),
			material_id = 0,
			is_url=False
		)
	elif answer['type'] == 'news':
		rule = Rule.objects.filter(owner=owner, patterns=pattern).update(
			type = MENU_TYPE,
			answer = '',
			material_id = answer['content'],
			is_url=False
		)
	elif answer['type'] == 'url':
		rule = Rule.objects.filter(
			owner = owner,
			patterns = pattern).update(answer = answer['content'], is_url = True, type = MENU_TYPE)
	else:
		pass


########################################################################
# __delete_rules: 删除rules
########################################################################
def __delete_rules(owner, menu_ids):
	if len(menu_ids) == 0:
		return

	patterns = ['MENU_QUERY_%d' % id for id in menu_ids]
	Rule.objects.filter(owner=owner, patterns__in=patterns).delete()


class FakeRequest(object):
	def __init__(self, user, post):
		self.user = user
		self.POST = post

	def __str__(self):
		items = []
		items.append('========== menu FakeRequest =========')
		items.append('user: %s' % self.user.username)
		items.append('post: ')
		items.append(json.dumps(json.loads(self.POST['menu_json']), indent=True))
		return '\n'.join(items)


########################################################################
# __get_menus_json_for_weixin: 获取微信需要的菜单数据
########################################################################
def __get_menus_json_for_weixin(user):
	menus = menu_util.get_menus_json(user)
	menu_json_obj = {'button':[]}
	#处理menu json obj
	for menu in menus:
		if len(menu['items']) == 0:
			if menu['answer']['type'] == 'url':
				menu_json_obj['button'].append({
					'type': 'view',
					'name': menu['name'],
					'url': menu['answer']['content'] if menu['answer']['content'].startswith('http') else 'http://%s' % menu['answer']['content']
				})
			else:
				menu_json_obj['button'].append({
					'type': 'click',
					'name': menu['name'],
					'key': 'MENU_QUERY_%s' % menu['id']
				})
		else:
			menu_sub_buttons = []
			menu_json_obj['button'].append({
				'name': menu['name'],
				'sub_button': menu_sub_buttons,
			})

		for menu_item in menu['items']:
			if menu_item['answer']['type'] == 'url':
				menu_sub_buttons.append({
					'type': 'view',
					'name': menu_item['name'],
					'url': menu_item['answer']['content'] if menu_item['answer']['content'].startswith('http') else 'http://%s' % menu_item['answer']['content']
				})
			else:
				menu_sub_buttons.append({
					'type': 'click',
					'name': menu_item['name'],
					'key': 'MENU_QUERY_%s' % menu_item['id']
				})

	return menu_json_obj


########################################################################
# update_customer_menu: 更新本地存储的自定义菜单项
########################################################################
@login_required
def update_customer_menu(request):
	menus = json.loads(request.POST['data'])

	ids = set()
	for menu in menus:
		ids.add(menu['id'])
		for item in menu['items']:
			ids.add(item['id'])

	existed_ids = set([item.id for item in CustomerMenuItem.objects.filter(owner=request.user)])
	need_add_ids = ids - existed_ids
	need_delete_ids = existed_ids - ids

	need_update_ids = ids.intersection(existed_ids)

	owner = request.user
	for menu in menus:
		menu_id = menu['id']
		#处理CustomerMenuItem
		if menu_id in need_add_ids:
			menu_model = CustomerMenuItem.objects.create(
				owner = owner,
				name = menu['name'],
				type = MENU_ITEM_TYPE_KEYWORD,
				rule_id = 0,
				father_id = 0,
				url = '',
				is_active = True,
				display_index = menu['index']
			)
			menu_id = menu_model.id
			menu['id'] = menu_id
			rule = __create_rule(owner, menu)
			CustomerMenuItem.objects.filter(id=menu_id).update(rule_id=rule.id)
		elif menu_id in need_update_ids:
			CustomerMenuItem.objects.filter(id=menu_id).update(
				name = menu['name'],
				display_index = menu['index']
			)
			__update_rule(owner, menu)
		for menu_item in menu['items']:
			menu_item_id = menu_item['id']
			#处理CustomerMenuItem
			if menu_item_id in need_add_ids:
				menu_item_model = CustomerMenuItem.objects.create(
					owner = owner,
					name = menu_item['name'],
					type = MENU_ITEM_TYPE_KEYWORD,
					rule_id = 0,
					father_id = menu_id,
					url = '',
					is_active = True,
					display_index = menu_item['index']
				)
				menu_item_id = menu_item_model.id
				menu_item['id'] = menu_item_model.id
				rule = __create_rule(owner, menu_item)
				CustomerMenuItem.objects.filter(id=menu_item_id).update(rule_id=rule.id)
			elif menu_item_id in need_update_ids:
				__update_rule(owner, menu_item)
				CustomerMenuItem.objects.filter(id=menu_item_id).update(
					name = menu_item['name'],
					display_index = menu_item['index']
				)

	#删除需要删除的菜单
	__delete_rules(request.user, need_delete_ids)
	CustomerMenuItem.objects.filter(id__in=need_delete_ids).delete()

	#调用微信api
	menu_json_obj = __get_menus_json_for_weixin(request.user)
	post = {
		'menu_json': json.dumps(menu_json_obj, ensure_ascii=False)
	}
	fake_request = FakeRequest(request.user, post)
	response = menu_tool.update_customerized_menu(fake_request)


	#返回结果
	#response = create_response(200)
	#return response.get_response()
	return response


########################################################################
# update_customer_menu: 更新本地存储的自定义菜单项
########################################################################
@login_required
def update_customer_menu_bak(request):
	menus = json.loads(request.POST['data'])

	ids = set()
	for menu in menus:
		ids.add(menu['id'])
		for item in menu['items']:
			ids.add(item['id'])

	existed_ids = set([item.id for item in CustomerMenuItem.objects.filter(owner=request.user)])
	need_add_ids = ids - existed_ids
	need_delete_ids = existed_ids - ids
	need_update_ids = ids.intersection(existed_ids)

	owner = request.user
	menu_json_obj = {'button':[]}
	for menu in menus:
		menu_id = menu['id']

		#处理menu json obj
		if len(menu['items']) == 0:
			if menu['answer']['type'] == 'url':
				menu_json_obj['button'].append({
					'type': 'view',
					'name': menu['name'],
					'url': menu['answer']['content'] if menu['answer']['content'].startswith('http') else 'http://%s' % menu['answer']['content']
				})
			else:
				menu_json_obj['button'].append({
					'type': 'click',
					'name': menu['name'],
					'key': 'MENU_QUERY_%s' % menu['id']
				})
		else:
			menu_sub_buttons = []
			menu_json_obj['button'].append({
				'name': menu['name'],
				'sub_button': menu_sub_buttons,
			})

		#处理CustomerMenuItem
		if menu_id in need_add_ids:
			menu_model = CustomerMenuItem.objects.create(
				owner = owner,
				name = menu['name'],
				type = MENU_ITEM_TYPE_KEYWORD,
				rule_id = 0,
				father_id = 0,
				url = '',
				is_active = True,
				display_index = menu['index']
			)
			menu_id = menu_model.id
			menu['id'] = menu_id
			rule = __create_rule(owner, menu)
			CustomerMenuItem.objects.filter(id=menu_id).update(rule_id=rule.id)
		elif menu_id in need_update_ids:
			CustomerMenuItem.objects.filter(id=menu_id).update(
				name = menu['name'],
				display_index = menu['index']
			)
			__update_rule(owner, menu)

		for menu_item in menu['items']:
			menu_item_id = menu_item['id']

			#处理menu json object
			# menu_sub_buttons.append({
			# 	'type': 'click',
			# 	'name': menu_item['name'],
			# 	'key': 'MENU_QUERY_%s' % menu_item_id
			# })

			if menu_item['answer']['type'] == 'url':
				menu_sub_buttons.append({
					'type': 'view',
					'name': menu_item['name'],
					'url': menu_item['answer']['content'] if menu_item['answer']['content'].startswith('http') else 'http://%s' % menu_item['answer']['content']
				})
			else:
				menu_sub_buttons.append({
					'type': 'click',
					'name': menu_item['name'],
					'key': 'MENU_QUERY_%s' % menu_item['id']
				})
			#处理CustomerMenuItem
			if menu_item_id in need_add_ids:
				menu_item_model = CustomerMenuItem.objects.create(
					owner = owner,
					name = menu_item['name'],
					type = MENU_ITEM_TYPE_KEYWORD,
					rule_id = 0,
					father_id = menu_id,
					url = '',
					is_active = True,
					display_index = menu_item['index']
				)
				menu_item_id = menu_item_model.id
				menu_item['id'] = menu_item_model.id
				rule = __create_rule(owner, menu_item)
				CustomerMenuItem.objects.filter(id=menu_item_id).update(rule_id=rule.id)
			elif menu_item_id in need_update_ids:
				__update_rule(owner, menu_item)
				CustomerMenuItem.objects.filter(id=menu_item_id).update(
					name = menu_item['name'],
					display_index = menu_item['index']
				)

	#删除需要删除的菜单
	__delete_rules(request.user, need_delete_ids)
	CustomerMenuItem.objects.filter(id__in=need_delete_ids).delete()

	#调用微信api
	post = {
		'menu_json': json.dumps(menu_json_obj, ensure_ascii=False)
	}
	fake_request = FakeRequest(request.user, post)
	response = menu_tool.update_customerized_menu(fake_request)

	#返回结果
	#response = create_response(200)
	#return response.get_response()
	return response


########################################################################
# get_menus: 获得菜单数据
########################################################################
def get_menus(request):
	if request.user.is_authenticated():
		user = request.user
	else:
		webapp_id = request.GET.get('webapp_id', None)
		if not webapp_id:
			response = create_response(500)
			response.errMsg = u'invalid webapp_id'
			return response.get_response()
			
		user_profile = UserProfile.objects.get(webapp_id=request.GET['webapp_id'])
		user = user_profile.user
		
	menus = menu_util.get_menus_json(user)

	response = create_response(200)
	response.data = menus
	return response.get_response()