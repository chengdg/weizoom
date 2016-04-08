# -*- coding: utf-8 -*-
import json

from django.shortcuts import render_to_response
from django.template import RequestContext
from core import resource
from core.jsonresponse import JsonResponse, create_response
from django.contrib.auth.decorators import login_required
from core import paginator
from models import *
from weapp.models import *


def get_rule_list(card_class, cur_page, count_per_page, request):
	print cur_page,count_per_page
	weizoom_card_rules = WeizoomCardRule.objects.filter(card_class=card_class).order_by('-created_at')
	#分页的数据
	pageinfo, weizoom_card_rules = paginator.paginate(weizoom_card_rules, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

	card_rule_ids = []
	user_ids = []

	for r in weizoom_card_rules:
		card_rule_ids.append(int(r.id))
		shop_limit_list = str(r.shop_limit_list).split(',')
		for a in shop_limit_list:
			if a != '-1':
				user_ids.append(a)

	user_id2store_name = {}
	user_profiles = UserProfile.objects.using('weapp').filter(user_id__in=user_ids)
	print user_profiles,"ggggggggggggg"
	for user_profile in user_profiles:
		if user_profile.store_name:
			user_id2store_name[user_profile.user_id] = user_profile.store_name
	all_cards = WeizoomCard.objects.filter(weizoom_card_rule_id__in=card_rule_ids)

	rule_id2card_ids = {}
	rule_id2cards = {}

	for c in all_cards:
		card_rule_id = c.weizoom_card_rule_id
		if card_rule_id not in rule_id2cards:
			rule_id2cards[card_rule_id] = [c]
		else:
			rule_id2cards[card_rule_id].append(c)

	for r_id in card_rule_ids:
		if r_id in rule_id2cards:
			weizoom_cards = rule_id2cards[r_id]
			weizoom_card_ids = [int(weizoom_cards[0].weizoom_card_id), int(weizoom_cards[::-1][0].weizoom_card_id)]
			rule_id2card_ids[r_id] = weizoom_card_ids

	cur_weizoom_card_rules = []
	for rule in weizoom_card_rules:
		shop_limit_list = str(rule.shop_limit_list).split(',')
		shop_limit_list = [user_id2store_name.get(int(i),None) for i in shop_limit_list]
		cur_weizoom_card_rule = {
			"id": rule.id,
			"name": rule.name if rule.name else '%.f元卡' % rule.money,
			"count": rule.count,
			"remark": rule.remark,
			"money": '%.2f' % rule.money,
			"card_kind": WEIZOOM_CARD_KIND2TEXT[rule.card_kind],
			"is_new_member_special": rule.is_new_member_special,
			"card_class": rule.card_class,
			"shop_limit_list": shop_limit_list,
			"valid_restrictions": ('满%.f使用' % rule.valid_restrictions) if rule.valid_restrictions != -1 else u'不限制'
		}

		#卡号区间
		try:
			weizoom_card_ids = rule_id2card_ids[cur_weizoom_card_rule["id"]]
			weizoom_card_id_start = weizoom_card_ids[0]
			weizoom_card_id_end = weizoom_card_ids[1]
			card_num_range = '%s-%s'%(weizoom_card_id_start,weizoom_card_id_end)
			cur_weizoom_card_rule["card_range"] = card_num_range
		except:
			pass
		cur_weizoom_card_rules.append(cur_weizoom_card_rule)
	return pageinfo, cur_weizoom_card_rules
