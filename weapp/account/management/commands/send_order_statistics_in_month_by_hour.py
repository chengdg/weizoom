# -*- coding: utf-8 -*-
#__auth__='justiing'
import logging
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db.models import Sum

#邮件部分
from core.sendmail import sendmail


import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
from mall.models import *
import xlsxwriter

from utils import dateutil

from datetime import datetime,timedelta,date
DATE_FORMAT="%Y-%m-%d"


class Command(BaseCommand):
	help = "send zypt order statistics in month by hour"
	args = ''
	
	def handle(self,*args, **options):
			print args

			week_day = datetime.now().weekday()
			current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

			first_day = "{}-01 00:00:00".format(current_time.rsplit('-',1)[0])
			first_datetime = dateutil.parse_datetime(first_day)
			file_path = 'order_statistices_in_month_by_hour.xlsx'
			
			workbook   = xlsxwriter.Workbook(file_path)
			table = workbook.add_worksheet()
			alist = [u"日期"]

			date_list = dateutil.get_date_range_list(first_datetime,datetime.now())

			for d in date_list:
				alist.append(dateutil.date2string(d))

			table.write_row('A1',alist)

			for i in range(24):
				table.write(i+1,0,"%s:00 ~ %s:59" % (i,i))

			tmp_line = 1
			for d in date_list:
				tmp_line += 1
				date_str = dateutil.date2string(d)
				end_datetime = "%s 23:59:00" % date_str
				orders = Order.objects.filter(status__in=[2,3,5], payment_time__gte=d, payment_time__lte=end_datetime)

				for i in range(24):
					print "%s %s:00" % (date_str, i), "----", "%s %s:59" % (date_str,i) ,"count()==",orders.filter(payment_time__gte="%s %s:00" % (date_str, i), payment_time__lte="%s %s:59" % (date_str,i)).count()
					total_price = orders.filter(payment_time__gte="%s %s:00" % (date_str, i), payment_time__lte="%s %s:59" % (date_str,i)).aggregate(Sum('product_price'))['product_price__sum']
					if  not total_price:
						total_price = 0
					table.write(i+1,tmp_line-1, total_price)

			workbook.close()

			receivers = ['zhangzhiyong@weizoom.com', 'guoyucheng@weizoom.com']
			mode = ''
			if len(args) == 1:
				if args[0] == 'test':
					mode = 'test'
					receivers = ['guoyucheng@weizoom.com']
			title = u'微众自运营平台当月时间段订单金额{}'.format(current_time)
			content = u'您好，微众自运营平台当月时间段订单金额'

			sendmail(receivers, title, content, mode, file_path)

