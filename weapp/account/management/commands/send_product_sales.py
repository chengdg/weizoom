# -*- coding: utf-8 -*-
#__auth__='justiing'
import logging
from django.core.management.base import BaseCommand, CommandError

#邮件部分
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.utils import parseaddr, formataddr
import smtplib


import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
from django.contrib.auth.models import User
from tools.regional.models import *
from modules.member.models import Member,MemberHasSocialAccount,MemberIntegralLog,MemberHasTag,MemberGrade
from mall.models import *
from mall.promotion.models import *
from member.member_list import get_member_orders,get_member_info,get_member_ship_info
from weixin.user.models import ComponentAuthedAppid,ComponentAuthedAppidInfo
from account.models import UserProfile
from mall.product import utils
import xlsxwriter

from datetime import datetime,timedelta,date
DATE_FORMAT="%Y-%m-%d"
sales_order_status = [ORDER_STATUS_PAYED_NOT_SHIP, ORDER_STATUS_PAYED_SHIPED, ORDER_STATUS_SUCCESSED, ORDER_STATUS_REFUNDING, ORDER_STATUS_GROUP_REFUNDING]


class Command(BaseCommand):
	help = "send product sales email"
	args = ''
	
	def handle(self,*args, **options):
			print args

			week_day = datetime.now().weekday()
			current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

			first_day = "{}-01".format(current_time.rsplit('-',1)[0])

			file_path = 'product_pool_sales.xlsx'
			workbook   = xlsxwriter.Workbook(file_path)
			table = workbook.add_worksheet()
			alist = [u'商品', u'供货商', u'销量', u'微众卡', u'微众优惠券', u'微众积分', u'现金', u'总金额']
			table.write_row('A1',alist)
			pool_weapp_profile = UserProfile.objects.filter(webapp_type=2).first()
			owner_pool = User.objects.get(id=pool_weapp_profile.user_id)

			product_ids = Product.objects.filter(owner=owner_pool, shelve_type__in=(PRODUCT_SHELVE_TYPE_ON,PRODUCT_SHELVE_TYPE_OFF)).values_list('id', flat=True)
			manager_supplier_ids2name = dict([(s.id, s.name) for s in Supplier.objects.filter(owner_id=pool_weapp_profile.user_id)])

			supplier_ids2name = {}
			product_id2store_name, product_id2sync_time = utils.get_sync_product_store_name(product_ids)
			tmp_line = 1
			for product_id in product_ids:
				tmp_line += 1
				product = Product.objects.get(id=product_id)
				product_name = product.name

				store_name = manager_supplier_ids2name.get(product.supplier, "")
				if store_name:
					is_sync = True
				if not store_name:
					store_name = supplier_ids2name[product.supplier] if product.supplier and supplier_ids2name.has_key(product.supplier) else product_id2store_name.get(product.id, "")
					is_sync = product_id2store_name.has_key(product.id)
				if store_name:
					if is_sync:
						supplier_name_export = u'同[{}]'.format(store_name)
					else:
						supplier_name_export = u'自[{}]'.format(store_name)
				else:
					supplier_name_export = ''

				product_sales= 0 
				weizoom_card = 0.0
				coupon_money = 0.0
				integral_money = 0.0
				cash = 0.0
				total = 0.0

				order_has_products = OrderHasProduct.objects.filter(product_id=product_id, order__origin_order_id__lte=0, order__status__in=sales_order_status, order__payment_time__gte='2016-08-01')
				for order_has_product in order_has_products:
					product_sales += order_has_product.number
					weizoom_card += order_has_product.order.weizoom_card_money
					if order_has_product.order.coupon_money > 0:
						coupon =  Coupon.objects.get(id=order_has_product.order.coupon_id)
						if coupon.coupon_rule.limit_product:
							product_ids = coupon.coupon_rule.limit_product_id.split(',')
							if product_id in product_ids:
								coupon_money += order_has_product.order.coupon_money
						else:
							coupon_money += order_has_product.order.coupon_money

					integral_money += order_has_product.order.integral_money
					cash += order_has_product.order.final_price
					total += order_has_product.price* order_has_product.number

				tmp_list = [product_name, supplier_name_export, product_sales, weizoom_card, coupon_money, integral_money, cash, total]
				table.write_row('A{}'.format(tmp_line),tmp_list)

			workbook.close()

			#邮件部分
			#msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')
			# 输入Email地址和口令:
			MAIL_NOTIFY_USERNAME = u'postmaster@noreply.itoldme.net'
			MAIL_NOTIFY_PASSWORD = u'db344fef68af413a5fa8502cbebd02f4'
			MAIL_NOTIFY_ACCOUNT_SMTP = u'smtp.mailgun.org'

			from_addr = MAIL_NOTIFY_USERNAME
			password = MAIL_NOTIFY_PASSWORD
			# 输入SMTP服务器地址:
			smtp_server = MAIL_NOTIFY_ACCOUNT_SMTP
			# 输入收件人地址:
			receivers = ['891470084@qq.com', 'houtingfei@weizoom.com', 'zhangzhiyong@weizoom.com', 'guoyucheng@weizoom.com']
			if len(args) == 1:
				if args[0] == 'test':
					receivers = ['houtingfei@weizoom.com']

			to_addr = ';'.join(receivers)

			#msg = MIMEText(u'hello, 每周报表', 'plain', 'utf-8')
			#邮件对象
			msg = MIMEMultipart()
			msg['From'] = from_addr
			msg['To'] = to_addr
			msg['Subject'] = Header(u'微众自运营平台商品销量{}'.format(current_time) , 'utf-8').encode()

			#邮件正文是MIMETEXT
			msg.attach(MIMEText(u'您好，这是本月统计的微众自运营平台商品销量', 'plain', 'utf-8'))

			#添加附件
			filename = file_path.split('.')[0]
			with open(file_path ,'rb') as f:
				#设置福建的mime和文件名，这里是py类型
				mime = MIMEBase('txt', 'xlsx', filename=filename)
				#加上头信息
				mime.add_header('Content-Disposition', 'attachment', filename=file_path)
				mime.add_header('Content-ID', '<0>')
				mime.add_header('X-Attachment-Id', '0')

				#把附件的内容读进来
				mime.set_payload(f.read())

				#用Base64编码
				encoders.encode_base64(mime)

				#添加到MIMEMultipart
				msg.attach(mime)

			import smtplib

			#server = smtplib.SMTP(smtp_server, 25) # SMTP协议默认端口是25
			server = smtplib.SMTP_SSL(smtp_server, 465)
			server.set_debuglevel(1)
			server.login(from_addr, password)
			server.sendmail(from_addr, receivers, msg.as_string())
			server.quit()

