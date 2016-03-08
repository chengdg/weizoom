# -*- coding: utf-8 -*-
from collections import OrderedDict

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from datetime import datetime
import xlwt

from mall.models import Order
from market_tools.tools.weizoom_card.models import WeizoomCardHasOrder, WeizoomCard
from modules.member.models import Member

"""
导出盛景数据，包括 手机号、姓名、公司
"""

class Command(BaseCommand):
	help = "start export data ..."
	args = ''

	def get_export_data(self):
		cards = WeizoomCard.objects.filter(weizoom_card_id__startswith='9')
		card_ids = [card.id for card in cards]

		order_ids = [wcho.order_id for wcho in WeizoomCardHasOrder.objects.filter(card_id__in=card_ids)]
		order_ids = set(order_ids)
		order_id2cards = {}
		user_id2username = {u.id: u.username for u in User.objects.all()}
		orders = Order.objects.filter(order_id__in=order_ids)
		order_id2final_price = {o.order_id: o.final_price for o in orders}
		order_id2webapp_user_id = {o.order_id: o.webapp_user_id for o in orders}

		webappuser2member = Member.members_from_webapp_user_ids(order_id2webapp_user_id.values())


		for order in WeizoomCardHasOrder.objects.filter(order_id__in=list(order_ids)):
			if not order_id2cards.has_key(order.order_id):
				order_id2cards[order.order_id] = [{
					'order_id': order.order_id,
					'card_id': order.card_id,
					'money': order.money,
					'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
					'onwer_id': order.owner_id,
					'owner_username': user_id2username[order.owner_id],
					'final_price': order_id2final_price[order.order_id],
					'member': webappuser2member[order_id2webapp_user_id[order.order_id]].username
				}]
			else:
				order_id2cards[order.order_id].append({
					'order_id': order.order_id,
					'card_id': order.card_id,
					'money': order.money,
					'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
					'onwer_id': order.owner_id,
					'owner_username': user_id2username[order.owner_id],
					'final_price': order_id2final_price[order.order_id],
					'member': webappuser2member[order_id2webapp_user_id[order.order_id]].username
				})
		# order2cards = {}
		# for k,cards in  order_id2cards.items():
		# 	card_money = {}
		# 	for card in cards:
		# 		if not card_money.has_key(card['card_id']):
		# 			card_money[card['card_id']] = {
		# 					'card_id':card['card_id'],
		# 					'order_id' :card['order_id'],
		# 					'use_money': card['money'],
		# 					'created_at': card['created_at'],
		# 					'owner_username': card['owner_username']
		# 				}
		# 		else:
		# 			card_money[card['card_id']]['use_money'] +=card['money']
		# 	order2cards[k] = card_money.values()
		card_ids = set()
		for k,inner_list in order_id2cards.items():
			for order in inner_list:
				card_ids.add(order['card_id'])
		weizoom_cards = {}
		for card in WeizoomCard.objects.filter(id__in=list(card_ids)):
			weizoom_cards[card.id] = {
				'weizoom_card_id': card.weizoom_card_id
			}

		members_info = [
			[u'渠道帐号',u'订单号',u'消费卡号',u'消费金额',u'消费日期',u'现金',u'总消费',u'用户名']
		]
		for order_id,cards in order_id2cards.items():
			for card in cards:
				card_id = card['card_id']
				info_list=[
					card['owner_username'],
					card['order_id'],
					weizoom_cards[card_id]['weizoom_card_id'],
					'%.2f' % card['use_money'],
					card['created_at'],
					'%.2f' % card['final_price'],
					'%.2f' % (card['use_money']+card['final_price']),
					card['member']
				]
				members_info.append(info_list)

		file_name = "card.xls"
		wb = xlwt.Workbook(encoding='utf-8')
		ws = wb.add_sheet(u'微众卡', cell_overwrite_ok=False)
		row = col = 0
		for item in members_info:
			for card in item:
				ws.write(row,col,card)
				col += 1
			row += 1

		print ''
		print '---- file name: {}'.format(file_name)
		wb.save(file_name)

	def handle(self, **options):

		print "----------------start export data ..."

		# 生成xml
		self.get_export_data()

		print '... end'