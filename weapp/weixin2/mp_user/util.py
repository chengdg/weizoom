# -*- coding: utf-8 -*-

__author__ = 'slzhu'

import json

from django.conf import settings

from core import emotion
from weixin.manage.customerized_menu.models import *
from weixin2.models import Rule, MENU_TYPE


########################################################################
# get_menus_json: 获取自定义菜单json数据
########################################################################
def get_menus_json(user):
	id2menu = dict()
	menu_models = list(CustomerMenuItem.objects.filter(owner=user))
	#使father_id为0的menu排在最前面，menu item排在其后
	menu_models.sort(lambda x,y: cmp(x.father_id, y.father_id))

	rule_ids = [menu_model.rule_id for menu_model in menu_models]
	id2rule = dict([(rule.id, rule) for rule in Rule.objects.filter(id__in=rule_ids)])

	for menu_model in menu_models:
		if not id2rule.has_key(menu_model.rule_id):
			#TODO 如果自定义菜单关联的规则被删除之后的处理？？
			continue

		if len(menu_model.name) == 0:
			#如果菜单项的名称长度为0，删除该菜单项
			try:
				menu_model.delete()
			except:
				pass
			continue

		rule = id2rule[menu_model.rule_id]
		if rule.is_url:
			answer = {
				'type': 'url',
				'content': rule.answer
			}
		elif rule.is_news_type:
			answer = {
				'type': 'news',
				'content': rule.material_id
			}
		else:
			answer = {
				'type': 'text',
				'content':  emotion.change_emotion_to_img(rule.answer)
			}

		if menu_model.father_id == 0:
			id2menu[menu_model.id] = {
				'id': menu_model.id,
				'name': menu_model.name,
				'index': menu_model.display_index,
				'answer': answer,
				'items': []
			}
		else:
			menu_item_model = menu_model
			rule = id2rule[menu_item_model.rule_id]
			menu = id2menu[menu_item_model.father_id]
			menu['items'].append({
				'id': menu_item_model.id,
				'name': menu_item_model.name,
				'index': menu_item_model.display_index,
				'answer': answer
			})

	menus = id2menu.values()
	menus.sort(lambda x,y: cmp(x['index'], y['index']))
	for menu in menus:
		if len(menu['items']) == 0:
			continue

		menu['items'].sort(lambda x,y: cmp(y['index'], x['index']))

	return menus


########################################################################
# create_rule: 创建rule
########################################################################
def create_rule(owner, menu):
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
# update_rule: 更新rule
########################################################################
def update_rule(owner, menu):
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
# _delete_rules: 删除rules
########################################################################
def delete_rules(owner, menu_ids):
	if len(menu_ids) == 0:
		return

	patterns = ['MENU_QUERY_%d' % id for id in menu_ids]
	Rule.objects.filter(owner=owner, patterns__in=patterns).delete()
	

def get_url(url):
	if url.startswith('http'):
		return url
	elif url.startswith('./?'):
		domain = 'http://%s/workbench/jqm/preview/?' % settings.DOMAIN
		return url.replace('./?', domain)
	elif url.startswith('/'):
		return 'http://%s%s' % (settings.DOMAIN, url)
	else:
		return 'http://%s' % url
	
########################################################################
# get_menus_json_for_weixin: 获取微信需要的菜单数据
########################################################################
def get_menus_json_for_weixin(user):
	menus = get_menus_json(user)
	menu_json_obj = {'button':[]}
	#处理menu json obj
	for menu in menus:
		if len(menu['items']) == 0:
			if menu['answer']['type'] == 'url':
				try:
					answer_content = json.loads(menu['answer']['content'])['data']
				except:
					answer_content = menu['answer']['content']
				menu_json_obj['button'].append({
					'type': 'view',
					'name': menu['name'],
					'url': get_url(answer_content)
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
				try:
					answer_content = json.loads(menu_item['answer']['content'])['data']
				except:
					answer_content = menu_item['answer']['content']
				menu_sub_buttons.append({
					'type': 'view',
					'name': menu_item['name'],
					'url': get_url(answer_content)
				})
			else:
				menu_sub_buttons.append({
					'type': 'click',
					'name': menu_item['name'],
					'key': 'MENU_QUERY_%s' % menu_item['id']
				})

	return menu_json_obj


class FakeRequest(object):
	"""
	构造更新微信自定义菜单请求
	"""
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
	
	
def get_fake_request(user, post_data):
	return FakeRequest(user, post_data)