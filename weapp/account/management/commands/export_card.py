# -*- coding: utf-8 -*-
import os
import smtplib
from collections import OrderedDict

import sys
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from datetime import datetime
import xlwt

from account.models import UserProfile
from mall.models import Order, ORDER_STATUS_REFUNDED,Product, OrderHasProduct, STATUS2TEXT
from market_tools.tools.weizoom_card.models import WeizoomCardHasOrder, WeizoomCard
from modules.member.models import Member
from email.mime.text import MIMEText

from weapp import settings

"""
导出
"""

mail_host = "smtp.mxhichina.com"
mail_user = "noreply@weizoom.com"
mail_pass = "#weizoom2013"
mail_postfix = "weizoom.com"

class Command(BaseCommand):
	help = "start export data ..."
	args = ''

	def get_export_card_data(self):
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
		id2products = {}
		for op in OrderHasProduct.objects.filter(order_id__in=order_id2id.values()):
			if not id2products.has_key(op.order_id):
				id2products[op.order_id] = [op]
			else:
				id2products[op.order_id].append(op)
		product_ids = []
		for products in id2products.values():
			for p in products:
				product_ids.append(p.product_id)
		prduct_id2producr_name = {p.id: p.name for p in Product.objects.filter(id__in=product_ids)}

		order_id2product_name = {}
		for order_id, products in id2products.items():
			for p in products:
				number = u''
				if p.number != 1:
					number = u'(%d)' % p.number
				if not order_id2product_name.has_key(order_id):
					order_id2product_name[order_id] = [u'%s%s' % (prduct_id2producr_name[p.product_id], number)]
				else:
					order_id2product_name[order_id].append(u'%s%s' % (prduct_id2producr_name[p.product_id], number))

		webappuser2member = Member.members_from_webapp_user_ids(order_id2webapp_user_id.values())


		for order in WeizoomCardHasOrder.objects.filter(order_id__in=list(order_id2price.keys())):
			if order_id2price.get(order.order_id,None) != None:
				try:
					name = webappuser2member[order_id2webapp_user_id[order.order_id]].username.decode('utf8')
				except:
					name = webappuser2member[order_id2webapp_user_id[order.order_id]].username_hexstr
				member_created_at = webappuser2member[order_id2webapp_user_id[order.order_id]].created_at.strftime('%Y-%m-%d %H:%M:%S')
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
						'status': order_id2price[order.order_id]['status'],
						'member_created_at': member_created_at
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
						'status': order_id2price[order.order_id]['status'],
						'member_created_at': member_created_at
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
			[u'订单号', u'用户名', u'消费卡号', u'渠道帐号', u'商品名', u'消费总额', u'微众卡消费消费', u'现金', u'订单的状态',u'消费时间',u'关注时间']
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
					card['status'].encode('utf-8'),
					card['created_at'],
					card['member_created_at']
				]
				members_info.append(info_list)

		file_name = os.path.join(settings.UPLOAD_DIR, 'card.xls')

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

	def send_mail(self, to_list, sub, content):

		me = "noreply@weizoom.com"
		msg = MIMEMultipart()
		msg['Subject'] = sub
		msg['From'] = me
		msg['To'] = ';'.join(to_list)
		msg.attach(MIMEText(content, 'plain', 'utf-8'))

		with open(settings.UPLOAD_DIR+'/card.xls', 'rb') as f:
			mime = MIMEBase('application', 'xls', filename='card.xls')
			mime.add_header('Content-Disposition', 'attachment', filename='card.xls')
			mime.set_payload(f.read())
			encoders.encode_base64(mime)
			msg.attach(mime)
		with open(settings.UPLOAD_DIR+'/product.xls', 'rb') as f:
			other = MIMEBase('application', 'xls', filename='product.xls')
			other.add_header('Content-Disposition', 'attachment', filename='product.xls')
			other.set_payload(f.read())
			encoders.encode_base64(other)
			msg.attach(other)
		try:
			server = smtplib.SMTP()
			server.connect(mail_host)
			server.login(mail_user, mail_pass)
			server.sendmail(me, to_list, msg.as_string())

			server.close()
			print 'send mail success'
			return True
		except	Exception,e:
			print 'send mail fail'
			return False

	def handle(self, **options):

		print "----------------start export data ..."

		# 生成xml
		self.get_export_card_data()
		self.get_export_pruduct_data()
		today = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
		receivers = ['likunlun@weizoom.com', 'youdongdong@weizoom.com', 'liunan@weizoom.com', 'linan@weizoom.com', 'chenlei@weizoom.com']
		self.send_mail(receivers, u"微众卡%s" % today, u"微众卡")

		print '... end'

	def get_export_pruduct_data(self):
		cards = WeizoomCard.objects.filter(weizoom_card_id__startswith='9')
		card_ids = [card.id for card in cards]

		order_ids = [wcho.order_id for wcho in WeizoomCardHasOrder.objects.filter(card_id__in=card_ids).exclude(order_id='-1')]
		order_ids = set(order_ids)
		orders = Order.objects.filter(order_id__in=list(order_ids)).exclude(status=ORDER_STATUS_REFUNDED)
		order_id2webapp_id = {o.id: o.webapp_id for o in orders}
		weapp_id2store_name = {u.webapp_id: u.store_name for u in UserProfile.objects.filter(webapp_id__in=order_id2webapp_id.values())}

		order_id2id = {o.order_id: o.id for o in orders}
		product_id2product = {}
		for op in OrderHasProduct.objects.filter(order_id__in=order_id2id.values()):
			if not product_id2product.has_key(op.product_id):
				product_id2product[op.product_id] = {
					'store_name': weapp_id2store_name[order_id2webapp_id[op.order_id]],
					'product_name': op.product_name,
					'number': op.number,
					'price': op.price
				}
			else:
				product_id2product[op.product_id]['number'] += op.number
		product_ids = [p_id for p_id in product_id2product.keys()]

		prduct_id2producr_name = {p.id: p.name for p in Product.objects.filter(id__in=product_ids)}

		members_info = [
			[u'商品名', u'单价', u'数量', u'供货商']
		]
		for product_id, product in product_id2product.items():
			product_name = product['product_name'] if product['product_name'] != '' else prduct_id2producr_name[product_id]
			info_list = [
				product_name.encode('utf-8'),
				product['price'],
				product['number'],
				product['store_name']
			]
			members_info.append(info_list)

		file_name = os.path.join(settings.UPLOAD_DIR, 'product.xls')
		wb = xlwt.Workbook(encoding='utf-8')
		ws = wb.add_sheet(u'微众卡--商品', cell_overwrite_ok=False)
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