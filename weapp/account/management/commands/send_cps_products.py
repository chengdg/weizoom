# -*- coding: utf-8 -*-
#__auth__='justiing'
import logging
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db.models import Sum, F
#邮件部分
from core.sendmail import sendmail


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

			file_path = 'product_cps.xlsx'
			workbook   = xlsxwriter.Workbook(file_path)
			table = workbook.add_worksheet()
			alist = [u'商品', u'供货商', u'开始时间', u'结束时间']
			table.write_row('A1',alist)
			promote_details = PromoteDetail.objects.filter(promote_status=2)

			product_ids = [p.product_id for p in promote_details]
			products = Product.objects.filter(id__in=product_ids)
			productid2name = dict([(p.id, p.name) for p in products])
			supplier_ids = [p.supplier for p in products]
			supplierid2name = dict([(s.id, s.name) for s in Supplier.objects.filter(id__in=supplier_ids)])
			productid2supplierid = dict([(p.id, p.supplier) for p in products])
			tmp_line = 1
			for promote_detail in promote_details:
				tmp_line += 1

				tmp_list = [productid2name[promote_detail.product_id], supplierid2name[ productid2supplierid[promote_detail.product_id] ], promote_detail.promote_time_from.strftime("%Y-%m-%d %H:%M:%S"), promote_detail.promote_time_to.strftime("%Y-%m-%d %H:%M:%S")]
				table.write_row('A{}'.format(tmp_line),tmp_list)
			workbook.close()

			receivers = ['zhangzhiyong@weizoom.com', 'guoyucheng@weizoom.com']
			mode = ''
			if len(args) == 1:
				if args[0] == 'test':
					mode = 'test'
			title = u'微众自运营平台product_cps'
			content = u'您好'

			sendmail(receivers, title, content, mode, file_path)

