# -*- coding: utf-8 -*-
from collections import OrderedDict

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from datetime import datetime
import xlwt

from mall.models import Order, ORDER_STATUS_REFUNDED,Product, OrderHasProduct, STATUS2TEXT
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

		order_ids = [wcho.order_id for wcho in WeizoomCardHasOrder.objects.filter(card_id__in=card_ids).exclude(order_id='-1')]
		order_ids = set(order_ids)
		order_id2cards = {}
		user_id2username = {u.id: u.username for u in User.objects.all()}
		orders = Order.objects.filter(order_id__in=list(order_ids)).exclude(status=ORDER_STATUS_REFUNDED)
		order_id2price = {o.order_id: {
			"final_price": o.final_price,
			"price": o.final_price + o.weizoom_card_money,
			"status": STATUS2TEXT[o.status]
		} for o in orders}
		order_id2webapp_user_id = {o.order_id: o.webapp_user_id for o in orders}
		order_id2id = {o.order_id: o.id for o in orders}
		id2product_id = {}
		for op in OrderHasProduct.objects.filter(order_id__in=order_id2id.values()):
			if not id2product_id.has_key(op.order_id):
				id2product_id[op.order_id] = [op.product_id]
			else:
				id2product_id[op.order_id].append(op.product_id)
		product_ids = []
		for p_id_list in id2product_id.values():
			for p_id in p_id_list:
				product_ids.append(p_id)
		prduct_id2producr_name = {p.id: p.name for p in Product.objects.filter(id__in=product_ids)}

		order_id2product_name = {}
		for order_id, p_id_list in id2product_id.items():
			for p_id in p_id_list:
				if not order_id2product_name.has_key(order_id):
					order_id2product_name[order_id] = [prduct_id2producr_name[p_id]]
				else:
					order_id2product_name[order_id].append(prduct_id2producr_name[p_id])

		webappuser2member = Member.members_from_webapp_user_ids(order_id2webapp_user_id.values())


		for order in WeizoomCardHasOrder.objects.filter(order_id__in=list(order_id2price.keys())):
			if order_id2price.get(order.order_id,None) != None:
				try:
					name = webappuser2member[order_id2webapp_user_id[order.order_id]].username.decode('utf8')
				except:
					name = webappuser2member[order_id2webapp_user_id[order.order_id]].username_hexstr
				if not order_id2cards.has_key(order.order_id):
					order_id2cards[order.order_id] = [{
						'order_id': order.order_id,
						'card_id': order.card_id,
						'money': order.money,
						'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
						'onwer_id': order.owner_id,
						'owner_username': user_id2username[order.owner_id],
						'final_price': order_id2price[order.order_id]['final_price'],
						'price': order_id2price[order.order_id]['price'],
						'member': name,
						'product_name': order_id2product_name[order_id2id[order.order_id]],
						'status': order_id2price['status']
					}]
				else:
					order_id2cards[order.order_id].append({
						'order_id': order.order_id,
						'card_id': order.card_id,
						'money': order.money,
						'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
						'onwer_id': order.owner_id,
						'owner_username': user_id2username[order.owner_id],
						'final_price': order_id2price[order.order_id]['final_price'],
						'price': order_id2price[order.order_id]['price'],
						'member': name,
						'product_name': order_id2product_name[order_id2id[order.order_id]],
						'status': order_id2price['status']
					})
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
			[u'订单号', u'用户名', u'消费卡号', u'渠道帐号', u'商品名', u'消费总额', u'微众卡消费消费', u'现金', u'订单的状态']
		]
		for order_id,cards in order_id2cards.items():
			for card in cards:
				card_id = card['card_id']
				info_list=[
					card['order_id'],
					card['member'],
					weizoom_cards[card_id]['weizoom_card_id'],
					card['owner_username'],
					','.join(card['product_name']),

					'%.2f' % card['price'],
					'%.2f' % card['money'],
					'%.2f' % card['final_price'],
					card['status'].encode('utf-8')
				]
				members_info.append(info_list)

		file_name = "card.xls"
		wb = xlwt.Workbook(encoding='utf-8')
		ws = wb.add_sheet(u'微众卡', cell_overwrite_ok=False)
		row = col = 0
		for item in members_info:
			col = 0
			for card in item:
				ws.write(row, col, card)
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