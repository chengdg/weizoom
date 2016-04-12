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
import random

#创建微众卡
def create_weizoom_card_rule(card_class,request):
	name = request.POST.get('name', '')
	weizoom_card_id_prefix = request.POST.get('weizoom_card_id_prefix', '')
	money = request.POST.get('money', '')
	remark = request.POST.get('remark', '')
	count = int(request.POST.get('count', ''))
	card_kind = int(request.POST.get('card_kind', 0))  #卡的类型
	shop_limit_list = request.POST.get('shop_limit_list','-1')
	is_new_member_special = int(request.POST.get('is_new_member_special', 0))
	valid_restrictions = request.POST.get('valid_restrictions', -1)
	
	if weizoom_card_id_prefix not in [card_rule.weizoom_card_id_prefix for card_rule in WeizoomCardRule.objects.all()]:
		rule = WeizoomCardRule.objects.create(
			owner_id=request.user.id,
			name=name,
			weizoom_card_id_prefix=weizoom_card_id_prefix,
			money=money,
			remark=remark,
			count=count,
			card_class=card_class,
			card_kind=card_kind,
			shop_limit_list=shop_limit_list,
			is_new_member_special=is_new_member_special,
			valid_restrictions=valid_restrictions if valid_restrictions else -1
			)
		#生成微众卡
		create_weizoom_card(rule, count, request)


def create_weizoom_card(rule,count,request,is_append=False):
	"""
	生成微众卡
	"""
	count = int(count)
	weizoom_cards = WeizoomCard.objects.filter(weizoom_card_rule_id=rule.id).order_by('-id')
	if weizoom_cards:
		card_number = int(weizoom_cards[0].weizoom_card_id[:3])
	else:
		card_number = int(u'000000')

	passwords = set([w.password for w in WeizoomCard.objects.filter(owner=request.user)])
	create_list = []
	for i in range(count):
		card_number = int(card_number) + 1
		card_number = '%06d' % card_number
		weizoom_card_id = '%s%s' % (str(rule.weizoom_card_id_prefix), card_number)
		password = create_weizoom_card_password(passwords)
		create_list.append(WeizoomCard(
			owner_id=request.user.id,
			weizoom_card_rule_id=rule.id,
			weizoom_card_id=weizoom_card_id,
			money=rule.money,
			password=password,
			active_card_user_id=0
		))
		passwords.add(password)
	WeizoomCard.objects.bulk_create(create_list)


def create_weizoom_card_password(passwords):
	"""
	生成微众卡密码
	"""
	random_args_value = ['1','2','3','4','5','6','7','8','9','0']
	while True:
		password = '%s' % ''.join(random.sample(random_args_value, 7))
		if password not in passwords:
			break

	return password


#获取卡规则的信息
def get_rule_list(card_class, cur_page, count_per_page, request):
	weizoom_card_rules = WeizoomCardRule.objects.filter(card_class=card_class).order_by('-id')
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
			weizoom_card_ids = [weizoom_cards[0].weizoom_card_id, weizoom_cards[::-1][0].weizoom_card_id]
			rule_id2card_ids[r_id] = weizoom_card_ids

	cur_weizoom_card_rules = []
	for rule in weizoom_card_rules:
		shop_limit_list = rule.shop_limit_list.split(',')
		shop_limit_list_name = []
		for user_id in shop_limit_list:
			if user_id != "-1" and user_id2store_name.has_key(int(user_id)):
				shop_limit_list_name.append(user_id2store_name[int(user_id)])
		cur_weizoom_card_rule = {
			"id": rule.id,
			"name": rule.name if rule.name else '%.f元卡' % rule.money,
			"count": rule.count,
			"remark": rule.remark,
			"money": '%.2f' % rule.money,
			"card_kind": WEIZOOM_CARD_KIND2TEXT[rule.card_kind],
			"is_new_member_special": u"新会员" if rule.is_new_member_special else "",
			"card_class": rule.card_class,
			"shop_limit_list": shop_limit_list_name,
			"valid_restrictions": '满%.f使用' % rule.valid_restrictions if rule.valid_restrictions != -1 else u'不限制'
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
