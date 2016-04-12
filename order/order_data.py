# -*- coding: utf-8 -*-
import json
import datetime

from django.shortcuts import render_to_response
from django.template import RequestContext
from core.jsonresponse import JsonResponse, create_response
from django.contrib.auth.decorators import login_required

from core import resource
from core.jsonresponse import create_response
from core import paginator
from card.models import *

class RuleOrder(resource.Resource):
	app = 'order'
	resource = 'order_data'

	@login_required
	def api_post(request):
		"""
		显示卡规则列表
		"""
		post = request.POST
		rule_order = post.get('rule_order',[])
		card_rule_num = post.get('card_rule_num',0)
		valid_time_from = post.get('valid_time_from','')
		valid_time_to = post.get('valid_time_to','')
		company_info = post.get('company_info','')
		responsible_person = post.get('responsible_person','')
		contact = post.get('contact','')
		sale_name = post.get('sale_name','')
		sale_departent = post.get('sale_departent','')
		order_attributes = post.get('order_attributes','')
		remark = post.get('remark','')
		rule_order = json.loads(rule_order)
		now_day = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").replace('-','').replace(':','').replace(' ','')
		weizoom_card_order = WeizoomCardOrder.objects.create(
			owner_id = request.user.id,
			order_number = now_day,
			order_attribute = order_attributes,
			company = company_info,
			responsible_person = responsible_person,
			contact = contact,
			sale_name = sale_name,
			sale_departent = sale_departent,
			remark=remark
		)

		for rule in rule_order:
			rule_id = int(rule['rule_id'])
			if not valid_time_from:
				valid_time_from = rule['valid_time_from']
				valid_time_to = rule['valid_time_to']
			if not card_rule_num:
				card_rule_num = rule['card_rule_num']
			print card_rule_num,7777777777777777
			weizoom_card_order_items = WeizoomCardOrderItem.objects.create(
				weizoom_card_rule_id = rule_id,
				valid_time_from = valid_time_from,
				valid_time_to = valid_time_to,
				weizoom_card_order_item_num = card_rule_num,
				weizoom_card_order = weizoom_card_order
			)
			weizoom_cards = WeizoomCard.objects.filter(weizoom_card_rule=rule_id,storage_status=WEIZOOM_CARD_STORAGE_STATUS_IN)[:card_rule_num]
			for weizoom_card in weizoom_cards:
				weizoom_card.storage_status = WEIZOOM_CARD_STORAGE_STATUS_OUT
				weizoom_card.weizoom_card_order_item_id = weizoom_card_order_items
				weizoom_card.weizoom_card_order_id = weizoom_card_order
				weizoom_card.storage_time = weizoom_card_order_items.created_at
				weizoom_card.activated_to = responsible_person
				weizoom_card.department = company_info
				weizoom_card.save()
			# WeizoomCard.objects.filter(weizoom_card_rule=rule_id,storage_status=WEIZOOM_CARD_STORAGE_STATUS_IN).update(
			# 	storage_status = WEIZOOM_CARD_STORAGE_STATUS_OUT,
			# 	weizoom_card_order_item_id = weizoom_card_order_items,
			# 	weizoom_card_order_id = weizoom_card_order,
			# 	storage_time = weizoom_card_order_items.created_at
			# )
			card_rule_num = 0
		response = create_response(200)
		return response.get_response()