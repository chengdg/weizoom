# -*- coding: utf-8 -*-

import json
from datetime import datetime

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from core import resource
from mall import export
from core.jsonresponse import JsonResponse, create_response
from core import paginator
from mall.promotion.string_util import byte_to_hex, hex_to_byte
from models import (CouponRule, Coupon, CouponRecord, COUPON_STATUS_USED,
					COUPONSTATUS, COUPON_STATUS_EXPIRED)
from . import models as promotion_models
from mall import models as mall_models
from modules.member.module_api import get_member_by_id_list
from modules.member.models import (MemberGrade, MemberTag, WebAppUser)
from core import search_util
from market_tools.tools.coupon.tasks import send_message_to_member
from market_tools.tools.weizoom_card import models as card_models
from excel_response import ExcelResponse


FIRST_NAV_NAME = export.MALL_PROMOTION_AND_APPS_FIRST_NAV


class CardExchange(resource.Resource):
	app = "mall2"
	resource = "card_exchange"

	@login_required
	def get(request):
		"""
		卡兑换配置页
		"""
		webapp_id = request.user_profile.webapp_id  
		card_exchange_dic = CardExchange.get_can_exchange_cards(request,webapp_id)
		
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV_NAME,
			'second_navs': export.get_promotion_and_apps_second_navs(request),
			'second_nav_name': export.MALL_PROMOTION_SECOND_NAV,
			'third_nav_name': export.MALL_PROMOTION_CARD_EXCHANGE_NAV,
			'card_exchange_dic': card_exchange_dic
		})
		return render_to_response('mall/editor/promotion/card_exchange.html', c)

	@login_required
	def api_get(request):
		s_num = request.GET.get('snum','')
		end_num = request.GET.get('endnum','')
		owner_id = request.webapp_owner_id

		can_exchange_card_count = len(get_can_exchange_cards_list(s_num,end_num,owner_id))
		
		response = create_response(200)
		response.data = can_exchange_card_count
		return response.get_response()

	@login_required
	def api_post(request):
		"""
		卡兑换配置
		"""
		is_bind = request.POST.get('isBind',0)
		prize = request.POST.get('prize','')
		reward_type = request.POST.get('reward',0)

		webapp_id = request.user_profile.webapp_id
		
		prize_list = json.loads(prize)
		card_exchange_rule_list = []
		try:
			cur_webapp_card_exchange = promotion_models.CardExchange.objects.get(webapp_id = webapp_id)
			cur_webapp_card_exchange_id = cur_webapp_card_exchange.id
			promotion_models.CardExchangeRule.objects.filter(exchange_id = cur_webapp_card_exchange_id).delete()
			cur_webapp_card_exchange.delete()
		except:
			pass
		card_exchange = promotion_models.CardExchange.objects.create(
			webapp_id = webapp_id,
			require = is_bind,
			reward_type = reward_type
		)
		for prize in prize_list:
			card_number = prize['snum'] + '-' + prize['endnum']
			card_exchange_rule_list.append(promotion_models.CardExchangeRule(
				integral = prize['integral'],
				money = prize['money'],
				card_number = card_number,
				exchange = card_exchange
			))
		promotion_models.CardExchangeRule.objects.bulk_create(card_exchange_rule_list)	

		response = create_response(200)
		return response.get_response()

	@staticmethod
	def get_can_exchange_cards(request,webapp_id):
		try:
			owner_id = request.webapp_owner_id
			card_exchange_dic = {}
			card_exchange = promotion_models.CardExchange.objects.get(webapp_id = webapp_id)
			require = card_exchange.require
			card_exchange_dic['is_bind'] = require
			card_exchange_id = card_exchange.id
			card_exchange_rules = promotion_models.CardExchangeRule.objects.filter(exchange_id = card_exchange_id)
			card_number2count = get_useful_card_count(owner_id,card_exchange_rules)
			prize_list = []
			for rule in card_exchange_rules:
				card_number = rule.card_number
				s_num = card_number.split('-')[0]
				end_num = card_number.split('-')[1]
				count = card_number2count.get(card_number,0)
				prize_list.append({
					'integral': rule.integral,
					'money': int(rule.money),
					's_num': s_num,
					'end_num': end_num,
					'count': count				 
				})
			card_exchange_dic['prize'] = prize_list
			return card_exchange_dic
		except:
			return {}

class CardExchangeDetail(resource.Resource):
	app = "mall2"
	resource = "card_exchange_details"

	@login_required
	def get(request):
		"""
		卡兑换详情页
		"""		
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV_NAME,
			'second_navs': export.get_promotion_and_apps_second_navs(request),
			'second_nav_name': export.MALL_PROMOTION_SECOND_NAV,
			'third_nav_name': export.MALL_PROMOTION_CARD_EXCHANGE_NAV,
		})
		return render_to_response('mall/editor/promotion/card_exchange_details.html', c)

	@login_required
	def api_get(request):
		"""
		卡兑换查看微众卡使用详情
		"""
		cur_page = int(request.GET.get('page',1))
		count_per_page = int(request.GET.get('count_per_page',10))

		cards = card_models.WeizoomCard.objects.all()
		exchanged_cards = CardExchangeDetail.get_exchanged_cards(request,cards)
		pageinfo, exchanged_cards = paginator.paginate(exchanged_cards, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
		card_rules = card_models.WeizoomCardRule.objects.all()
		exchanged_cards_list = []
		for card in exchanged_cards:
			card_id = card.card_id
			try:
				cur_card = cards.get(id = card_id)
				weizoom_card_id = cur_card.weizoom_card_id
				weizoom_card_rule_id = cur_card.weizoom_card_rule_id
				cur_card_rule = card_rules.get(id = weizoom_card_rule_id)
				money = cur_card_rule.money
				remainder = cur_card.money
				user = hex_to_byte(card.owner_name)
				used_money = money - remainder
				exchanged_cards_list.append({
					'card_id': weizoom_card_id,
					'money': '%.2f' % money,
					'remainder': '%.2f' % remainder,
					'used_money': '%.2f' % used_money,
					'user': user  
				})
			except:
				pass
		
		response = create_response(200)
		response.data.items = exchanged_cards_list
		response.data.pageinfo = paginator.to_dict(pageinfo)
		return response.get_response()

	@staticmethod
	def get_exchanged_cards(request,cards):
		card_number = request.GET.get('cardNumber',None)
		card_user = request.GET.get('cardUser',None)

		webapp_id = request.user_profile.webapp_id
		#查询
		exchanged_cards = promotion_models.CardHasExchanged.objects.filter(webapp_id = webapp_id).order_by('-created_at')
		if card_number:
			cur_cards = cards.filter(weizoom_card_id__contains = card_number)
			card_id_list = []
			for card in cur_cards:
				card_id_list.append(card.id)
			exchanged_cards = exchanged_cards.filter(card_id__in = card_id_list)	
		if card_user:
			exchanged_cards = exchanged_cards.filter(owner_name__contains=byte_to_hex(card_user))

		return exchanged_cards

class CardExchangeDetailExport(resource.Resource):
	app = 'mall2'
	resource = 'export_card_exchange_details'

	@login_required
	def api_get(request):
		"""
		微众卡兑换详情导出
		"""
		cards = card_models.WeizoomCard.objects.all()
		exchanged_cards = CardExchangeDetail.get_exchanged_cards(request,cards)
		card_rules = card_models.WeizoomCardRule.objects.all()

		members_info = [
			[u'卡号', u'面值',u'卡内余额',u'使用金额',u'使用者']
		]

		for card in exchanged_cards:
			card_id = card.card_id
			try:
				cur_card = cards.get(id = card_id)
				weizoom_card_id = cur_card.weizoom_card_id
				weizoom_card_rule_id = cur_card.weizoom_card_rule_id
				cur_card_rule = card_rules.get(id = weizoom_card_rule_id)
				money = cur_card_rule.money
				remainder = cur_card.money
				user = hex_to_byte(card.owner_name)
				used_money = money - remainder
				info_list = [
					weizoom_card_id,
					'%.2f' % money,
					'%.2f' % remainder,
					'%.2f' % used_money,
					user
				]
				members_info.append(info_list)
			except:
				pass

		filename = u'微众卡兑换详情'
		return ExcelResponse(members_info, output_name=filename.encode('utf8'), force_csv=False)

def get_can_exchange_cards_list(s_num,end_num,owner_id):
	s_card_id = 0
	end_card_id = 0
	all_cards = card_models.WeizoomCard.objects.all().order_by('id')
	cards = all_cards.exclude(status = card_models.WEIZOOM_CARD_STATUS_INACTIVE)
	card_id_min = int(cards.first().weizoom_card_id)
	card_id_max = int(cards.last().weizoom_card_id)
	weizoom_card_id2id = {card.weizoom_card_id:card.id for card in cards}
	card_id_list = sorted(weizoom_card_id2id.values())
	if len(card_id_list) <= 0:
		return []
	flag_count = 0
	try:
		s_card_id = all_cards.get(weizoom_card_id = s_num).id
	except:
		flag_count += 1
		s_card_id = card_id_list[0]
	try:
		end_card_id = all_cards.get(weizoom_card_id = end_num).id
	except:
		flag_count += 1
		end_card_id = card_id_list[-1]
	if flag_count == 2 and int(s_num) > card_id_min and int(end_num) > card_id_max:
		return []
	if flag_count == 2 and int(s_num) < card_id_min and int(end_num) < card_id_max:
		return []
	if s_card_id > end_card_id:
		return []
	card_range_list = [i for i in range(s_card_id,end_card_id+1)]
	card_id2ruleid = {c.id: c.weizoom_card_rule_id for c in cards.filter(id__in=card_range_list)}
	card_rule_ids = card_id2ruleid.values()
	
	belong_card_rules = card_models.WeizoomCardRule.objects.filter(card_attr = card_models.WEIZOOM_CARD_SPECIAL,id__in=card_rule_ids)
	for rule in belong_card_rules:
		if str(owner_id) not in rule.shop_limit_list.split(','):
			card_rule_ids.remove(rule.id)
	card_ids = []
	for k,v in card_id2ruleid.items():
		if v in card_rule_ids:
			card_ids.append(k)
	card_ids_tmp = []
	card_has_orders = card_models.WeizoomCardHasOrder.objects.exclude(order_id__in = [-1])
	card_id2order = {order.card_id: order for order in card_has_orders}
	for card_id in card_ids:
		if not card_id2order.get(card_id,None):
			card_ids_tmp.append(card_id)
	card_has_exchanged = promotion_models.CardHasExchanged.objects.all()
	card_id2exchange = {exchange.card_id: exchange for exchange in card_has_exchanged}
	card_ids = card_ids_tmp
	card_ids_tmp = []
	for card_id in card_ids:
		if not card_id2exchange.get(card_id,None):
			card_ids_tmp.append(card_id)

	return card_ids_tmp

###########################
#卡号区间对应的可兑换卡数量
###########################
def get_useful_card_count(owner_id,card_exchange_rules):
	all_cards = card_models.WeizoomCard.objects.all().order_by('id')
	cards = all_cards.exclude(status = card_models.WEIZOOM_CARD_STATUS_INACTIVE)
	belong_card_rules = card_models.WeizoomCardRule.objects.filter(card_attr = card_models.WEIZOOM_CARD_SPECIAL)
	card_has_orders = card_models.WeizoomCardHasOrder.objects.exclude(order_id__in = [-1])
	card_id2order = {order.card_id: order for order in card_has_orders}
	card_has_exchanged = promotion_models.CardHasExchanged.objects.all()
	card_id2exchange = {exchange.card_id: exchange for exchange in card_has_exchanged}
	card_id_min = int(cards.first().weizoom_card_id)
	card_id_max = int(cards.last().weizoom_card_id)
	weizoom_card_id2id = {card.weizoom_card_id:card.id for card in cards}
	card_id_list = sorted(weizoom_card_id2id.values())
	if len(card_id_list) <= 0:
		return [] 
	card_num_list = [rule.card_number for rule in card_exchange_rules]
	card_number2count = {}
	for num in card_num_list:
		s_num = num.split('-')[0]
		end_num = num.split('-')[1]
		flag_count = 0
		try:
			s_card_id = all_cards.get(weizoom_card_id = s_num).id
		except:
			flag_count += 1
			s_card_id = card_id_list[0]
		try:
			end_card_id = all_cards.get(weizoom_card_id = end_num).id
		except:
			flag_count += 1
			end_card_id = card_id_list[-1]
		if flag_count == 2 and int(s_num) > card_id_min and int(end_num) > card_id_max:
			return []
		if flag_count == 2 and int(s_num) < card_id_min and int(end_num) < card_id_max:
			return []
		if s_card_id > end_card_id:
			return []
		card_range_list = [i for i in range(s_card_id,end_card_id+1)]
		card_id2ruleid = {c.id: c.weizoom_card_rule_id for c in cards.filter(id__in=card_range_list)}
		card_rule_ids = card_id2ruleid.values()
		cur_belong_card_rules = belong_card_rules.filter(id__in=card_rule_ids)
		for rule in belong_card_rules:
			if str(owner_id) not in rule.shop_limit_list.split(','):
				card_rule_ids.remove(rule.id)
		card_ids = []
		for k,v in card_id2ruleid.items():
			if v in card_rule_ids:
				card_ids.append(k)
		card_ids_tmp = []
		for card_id in card_ids:
			if not card_id2order.get(card_id,None):
				card_ids_tmp.append(card_id)
		card_ids = card_ids_tmp
		card_ids_tmp = []
		for card_id in card_ids:
			if not card_id2exchange.get(card_id,None):
				card_ids_tmp.append(card_id)
		card_number2count[num] = len(card_ids_tmp)

	return card_number2count