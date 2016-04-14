# -*- coding: utf-8 -*-
import json

from django.shortcuts import render_to_response
from django.template import RequestContext
from core.jsonresponse import JsonResponse, create_response
from django.contrib.auth.decorators import login_required

from core import resource
from core.jsonresponse import create_response
from core import paginator
import nav
from card.models import *
from weapp.models import *
FIRST_NAV = 'rule_order'
SECOND_NAV = 'rule_order'

class RuleOrder(resource.Resource):
	app = 'order'
	resource = 'rule_order'

	@login_required
	def get(request):
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': SECOND_NAV,
		})
		return render_to_response('order/rule_order.html', c)

	@login_required
	def api_get(request):
		cur_page = request.GET.get('page', 1)
		weizoom_card_orders = WeizoomCardOrder.objects.all().order_by('-order_number')
		weizoom_card_order_items = WeizoomCardOrderItem.objects.all()
		w_cards = WeizoomCard.objects.filter(weizoom_card_order_item_id__gte=1)
		order_item_id2weizoom_card_id = {}
		for w_card in w_cards:
			if w_card.weizoom_card_order_item_id in order_item_id2weizoom_card_id:
				order_item_id2weizoom_card_id[w_card.weizoom_card_order_item_id].append(w_card.weizoom_card_id)
			else:
				order_item_id2weizoom_card_id[w_card.weizoom_card_order_item_id] = [w_card.weizoom_card_id]
		rule_ids = set([w_card.weizoom_card_rule_id for w_card in w_cards])
		card_rules = WeizoomCardRule.objects.filter(id__in=rule_ids)
		card_order_id2id = {}
		for order_item in weizoom_card_order_items:
			if order_item.weizoom_card_order_id in card_order_id2id:
				card_order_id2id[order_item.weizoom_card_order_id].append(order_item.id)
			else:
				card_order_id2id[order_item.weizoom_card_order_id] = [order_item.id]
		order_id2rule_id = {order_item.id:order_item.weizoom_card_rule_id for order_item in weizoom_card_order_items}
		id2weizoom_card_order_item = {weizoom_card_order_item.id:weizoom_card_order_item for weizoom_card_order_item in weizoom_card_order_items}
		id2card_rule = {card_rule.id:card_rule for card_rule in card_rules}
		order2is_activation={}
		weizoom_card_orders_ids =[W.id for W in weizoom_card_orders]
		for cur_weizoom_card_orders_id in weizoom_card_orders_ids:
			order2cards =w_cards.filter(weizoom_card_order_id=cur_weizoom_card_orders_id,operate_status=1)
			if order2cards:
				order2is_activation[cur_weizoom_card_orders_id] =1
			else:
				order2is_activation[cur_weizoom_card_orders_id] =0
		
		pageinfo, weizoom_card_orders = paginator.paginate(weizoom_card_orders, cur_page, 10, query_string=request.META['QUERY_STRING'])	
		
		user_ids = []
		for r in card_rules:
			shop_limit_list = str(r.shop_limit_list).split(',')
			for a in shop_limit_list:
				if a != '-1':
					user_ids.append(a)
		user_id2store_name = {}
		user_profiles = UserProfile.objects.using('weapp').filter(user_id__in=user_ids)
		for user_profile in user_profiles:
			if user_profile.store_name:
				user_id2store_name[user_profile.user_id] = user_profile.store_name

		card_order_list = []
		for card_order in weizoom_card_orders:
			card_order_dic = {}
			print card_order.id
			if card_order.id in card_order_id2id:
				order_items = card_order_id2id[card_order.id]
				order_item_list = []
				order_money = 0
				for order_item_id in order_items:
					if order_item_id in order_item_id2weizoom_card_id:
						order_item_dic = {}
						rule_id = order_id2rule_id[order_item_id]
						name = '' if rule_id not in id2card_rule else id2card_rule[rule_id].name
						if name:
							name = name
						else:
							name = u'%.f元卡' % id2card_rule[rule_id].money

						shop_limit_list = id2card_rule[rule_id].shop_limit_list.split(',')
						shop_limit_list_name = []
						for user_id in shop_limit_list:
							if user_id != "-1" and user_id2store_name.has_key(int(user_id)):
								shop_limit_list_name.append(user_id2store_name[int(user_id)])

						weizoom_card_ids = sorted(order_item_id2weizoom_card_id[order_item_id])
						weizoom_card_id_first = weizoom_card_ids[0]
						weizoom_card_id_last = weizoom_card_ids[-1]
						valid_restrictions = id2card_rule[rule_id].valid_restrictions
						count = 0 if order_item_id not in id2weizoom_card_order_item else id2weizoom_card_order_item[order_item_id].weizoom_card_order_item_num
						order_money += id2card_rule[rule_id].money * count
						order_item_dic['weizoom_card_id_first'] = weizoom_card_id_first
						order_item_dic['weizoom_card_id_last'] = weizoom_card_id_last
						order_item_dic['name'] =name
						order_item_dic['id'] =rule_id
						order_item_dic['money'] = u'%.2f' %id2card_rule[rule_id].money
						order_item_dic['total_money'] = u'%.2f' %(id2card_rule[rule_id].money * count)
						order_item_dic['weizoom_card_order_item_num'] = count
						order_item_dic['card_kind'] = WEIZOOM_CARD_KIND2TEXT[id2card_rule[rule_id].card_kind]
						order_item_dic['card_class'] = WEIZOOM_CARD_CLASS2TEXT[id2card_rule[rule_id].card_class]
						order_item_dic['shop_limit_list'] = shop_limit_list_name
						order_item_dic['valid_restrictions'] = u'满%.f使用' % valid_restrictions if valid_restrictions != -1 else u'不限制'
						order_item_list.append(order_item_dic)
				if order_item_list:
					if card_order.order_attribute == WEIZOOM_CARD_ORDER_ATTRIBUTE_INTERNAL:
						apply_people = card_order.use_persion
						apply_departent = card_order.use_departent
					else:
						apply_people = card_order.responsible_person
						apply_departent = card_order.company
					card_order_dic['id'] = card_order.id
					card_order_dic['status'] = card_order.status
					card_order_dic['order_number'] = card_order.order_number
					card_order_dic['order_attribute'] = WEIZOOM_CARD_ORDER_ATTRIBUTE2TEXT[card_order.order_attribute]
					card_order_dic['responsible_person'] = card_order.responsible_person
					card_order_dic['company'] = card_order.company
					card_order_dic['use_departent'] = card_order.use_departent
					card_order_dic['project_name'] = card_order.project_name
					card_order_dic['appliaction'] = card_order.appliaction
					card_order_dic['use_persion'] = card_order.use_persion
					card_order_dic['apply_people'] = apply_people
					card_order_dic['apply_departent'] = apply_departent
					card_order_dic['order_money'] = '%s' %order_money
					card_order_dic['created_at'] = card_order.created_at.strftime("%Y-%m-%d")
					card_order_dic['is_activation'] =u'' if card_order.id not in order2is_activation else order2is_activation[card_order.id]
					card_order_dic['order_item_list'] = json.dumps(order_item_list)
					card_order_list.append(card_order_dic)
		data = {
			'card_order_list': json.dumps(card_order_list)
		}
		response = create_response(200)
		response.data = data
		response.data['rows'] = card_order_list
		response.data['pagination_info'] = pageinfo.to_dict()
		return response.get_response()

	@login_required
	def api_post(request):
		status_orderId = request.POST.get('orderId','')
		status_is_activation = request.POST.get('is_activation','')
		status_status = request.POST.get('status','')
		if status_orderId and status_is_activation:
			cur_cards = WeizoomCard.objects.filter(storage_status=WEIZOOM_CARD_STORAGE_STATUS_OUT,weizoom_card_order_id=status_orderId)
			
			if int(status_is_activation) ==1:			
				for cur_card in cur_cards:
					cur_card.operate_status=WEIZOOM_CARD_OPERATE_STATUS_INACTIVE
					cur_card.save()
			elif int(status_is_activation) ==0:
				for cur_card in cur_cards:
					cur_card.operate_status=WEIZOOM_CARD_OPERATE_STATUS_ACTIVED
					cur_card.save()
		if status_status:
			if int(status_status) ==0:
				WeizoomCard.objects.filter(weizoom_card_order_id=status_orderId).update(storage_status=WEIZOOM_CARD_STORAGE_STATUS_IN)
				WeizoomCardOrder.objects.filter(id=status_orderId).update(status=WEIZOOM_CARD_ORDER_STATUS_CANCLED)
		response = create_response(200)
		return response.get_response()