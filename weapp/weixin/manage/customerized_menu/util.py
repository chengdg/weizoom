# -*- coding: utf-8 -*-

__author__ = 'chuter'


import json
import weixin

from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from models import *
from utils.json_util import string_json
from weixin.message.qa.models import Rule, TEXT_TYPE, NEWS_TYPE
from core import emotion


########################################################################
# edit_customerized_menu: 编辑自定义菜单
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