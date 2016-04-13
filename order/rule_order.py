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
		weizoom_card_orders = WeizoomCardOrder.objects.all().order_by('-order_number')
		print weizoom_card_orders[0].status,999999999999999111111111111111111
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
		pageinfo, weizoom_card_orders = paginator.paginate(weizoom_card_orders, 1, 10, query_string=request.META['QUERY_STRING'])	
		card_order_list = []
		for card_order in weizoom_card_orders:
			print card_order.status,988888888888888888888888888888889
			card_order_dic = {}
			print card_order.id
			if card_order.id in card_order_id2id:
				print 'sssssssssssssssss'
				order_items = card_order_id2id[card_order.id]
				order_item_list = []
				for order_item_id in order_items:
					if order_item_id in order_item_id2weizoom_card_id:
						print 'ddddddddddddddddd'
						order_item_dic = {}
						rule_id = order_id2rule_id[order_item_id]
						weizoom_card_ids = sorted(order_item_id2weizoom_card_id[order_item_id])
						weizoom_card_id_first = weizoom_card_ids[0]
						weizoom_card_id_last = weizoom_card_ids[-1]
						valid_restrictions = id2card_rule[rule_id].valid_restrictions

						count = 0 if order_item_id not in id2weizoom_card_order_item else id2weizoom_card_order_item[order_item_id].weizoom_card_order_item_num
						order_item_dic['weizoom_card_id_first'] = weizoom_card_id_first
						order_item_dic['weizoom_card_id_last'] = weizoom_card_id_last
						order_item_dic['name'] =u'' if rule_id not in id2card_rule else id2card_rule[rule_id].name
						order_item_dic['money'] = u'%.2f' %id2card_rule[rule_id].money
						order_item_dic['total_money'] = u'%.2f' %(id2card_rule[rule_id].money * count)
						order_item_dic['weizoom_card_order_item_num'] = count
						order_item_dic['card_kind'] = WEIZOOM_CARD_KIND2TEXT[id2card_rule[rule_id].card_kind]
						order_item_dic['card_class'] = WEIZOOM_CARD_CLASS2TEXT[id2card_rule[rule_id].card_class]
						order_item_dic['shop_limit_list'] = id2card_rule[rule_id].shop_limit_list
						order_item_dic['valid_restrictions'] = u'满%.f使用' % valid_restrictions if valid_restrictions != -1 else u'不限制'
						order_item_list.append(order_item_dic)
				# if order_item_id in order_item_id2weizoom_card_id:
				# 	weizoom_card_ids = sorted(order_item_id2weizoom_card_id[order_item_id])
				# 	weizoom_card_id_first = weizoom_card_ids[0]
				# 	weizoom_card_id_last = weizoom_card_ids[-1]
				# 	count = 0 if card_order.id not in id2weizoom_card_order_item else id2weizoom_card_order_item[card_order.id].weizoom_card_order_item_num
				# 	card_order_dic['id'] = card_order.id
				# 	card_order_dic['weizoom_card_id_first'] = weizoom_card_id_first
				# 	card_order_dic['weizoom_card_id_last'] = weizoom_card_id_last
				# 	card_order_dic['order_number'] = card_order.order_number
					# card_order_dic['name'] ='' if rule_id not in id2card_rule else id2card_rule[rule_id].name
					# card_order_dic['money'] = '%.2f' %id2card_rule[rule_id].money
					# card_order_dic['total_money'] = '%.2f' %(id2card_rule[rule_id].money * count)
					# card_order_dic['weizoom_card_order_item_num'] = count
					# card_order_dic['card_kind'] = WEIZOOM_CARD_KIND2TEXT[id2card_rule[rule_id].card_kind]
					# card_order_dic['card_class'] = WEIZOOM_CARD_CLASS2TEXT[id2card_rule[rule_id].card_class]
				if order_item_list:
					print card_order.status,989898989898989
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
					card_order_dic['created_at'] = card_order.created_at.strftime("%Y-%m-%d")
					card_order_dic['is_activation'] =u'' if card_order.id not in order2is_activation else order2is_activation[card_order.id]
					card_order_dic['order_item_list'] = json.dumps(order_item_list)
					card_order_list.append(card_order_dic)
		data = {
			'card_order_list': json.dumps(card_order_list)
		}
		print card_order_list,55555555555555555555555555
		response = create_response(200)
		response.data = data

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
					cur_card.operate_status=2
					cur_card.save()
			elif int(status_is_activation) ==0:
				for cur_card in cur_cards:
					cur_card.operate_status=1
					cur_card.save()
		if status_status:
			if int(status_status) ==0:
				WeizoomCard.objects.filter(weizoom_card_order_id=status_orderId).update(storage_status=0)
				WeizoomCardOrder.objects.filter(id=status_orderId).update(status=1)
		response = create_response(200)
		return response.get_response()