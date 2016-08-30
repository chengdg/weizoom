# -*- coding: utf-8 -*-
#__auth__='justiing'
import logging
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db.models import Q,F

#邮件部分
from core.sendmail import sendmail

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weapp.settings")

# from django.core.management import execute_from_command_line

# execute_from_command_line(sys.argv)

from tools.regional.models import *
from modules.member.models import Member,MemberHasSocialAccount,MemberIntegralLog,MemberHasTag,MemberGrade,WebAppUser
from mall.models import Order,Product,OrderHasProduct
from member.member_list import get_member_orders,get_member_info,get_member_ship_info

from weixin.user.models import ComponentAuthedAppid,ComponentAuthedAppidInfo
from account.models import UserProfile
import xlsxwriter
from datetime import datetime,timedelta,date
DATE_FORMAT="%Y-%m-%d"

'''
获取上周微众自运营订单数量

订单状态取值：取已支付到已完成状态的订单

ORDER_STATUS_NOT = 0  # 待支付：已下单，未付款
ORDER_STATUS_CANCEL = 1  # 已取消：取消订单(回退销量)
ORDER_STATUS_PAYED_SUCCESSED = 2  # 已支付：已下单，已付款，已不存此状态
ORDER_STATUS_PAYED_NOT_SHIP = 3  # 待发货：已付款，未发货
ORDER_STATUS_PAYED_SHIPED = 4  # 已发货：已付款，已发货
ORDER_STATUS_SUCCESSED = 5  # 已完成：自下单10日后自动置为已完成状态
ORDER_STATUS_REFUNDING = 6  # 退款中
ORDER_STATUS_REFUNDED = 7  # 退款完成(回退销量)
ORDER_STATUS_GROUP_REFUNDING = 8 #团购退款（没有退款完成按钮）
ORDER_STATUS_GROUP_REFUNDED = 9 #团购退款完成
'''


class Command(BaseCommand):
	help = "get weizoom order every week"
	args = ''
	
	def handle(self,*args, **options):
			print args

			week_day = datetime.now().weekday()
			current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

			last_week_days = []
			#获取上周的时间(多取1天的时间，最后1天为本周1)
			for i in xrange(8):
				date = (datetime.now()-timedelta(week_day-i+7)).strftime(DATE_FORMAT)
				last_week_days.append(date)

			heads = [u'总订单', u'总订单金额', u'首单', u'首单金额', u'复购', u'复购金额']
			tmp_line= 1
			head_lists = []
			for last_week_day in last_week_days[:7]:
				for head in heads:
					tmp = last_week_day + head
					head_lists.append(tmp)

			file_path = u'order{}.xlsx'.format(last_week_days[0])
			workbook = xlsxwriter.Workbook(file_path)
			table = workbook.add_worksheet()

			head_lists = [u'平台名称']+head_lists
			table.write_row('A1', head_lists)
			user_profiles = UserProfile.objects.filter(webapp_type = 1).filter(~Q(user_id__in=[968, 930,816, 16,529]))
			for user_profile in user_profiles:
				tmp_line += 1
				user_id = user_profile.user_id
				nick_name = user_profile.store_name
				webapp_id = user_profile.webapp_id
				statistics_days = [nick_name]
				for i in xrange(7):
					orders_total = Order.objects.filter(webapp_id=webapp_id, created_at__gte=last_week_days[i], created_at__lt=last_week_days[i+1], status__in=[2,3,4,5], origin_order_id__lte=0)
					orders_total_count = orders_total.count()
					orders_first = Order.objects.filter(webapp_id=webapp_id, created_at__gte=last_week_days[i], created_at__lt=last_week_days[i+1], status__in=[2,3,4,5], is_first_order=True, origin_order_id__lte=0)
					orders_first_count = orders_first.count()
					orders_not_first= Order.objects.filter(webapp_id=webapp_id, created_at__gte=last_week_days[i], created_at__lt=last_week_days[i+1], status__in=[2,3,4,5], is_first_order=False, origin_order_id__lte=0)
					orders_not_first_count = orders_not_first.count()
					paid_amount_total = 0.0
					paid_amount_total_first = 0.0
					paid_amount_total_not_first = 0.0
					for order in orders_total:
						tmp_paid_amount = order.final_price + order.weizoom_card_money
						paid_amount_total += tmp_paid_amount

					for order in orders_first:
						tmp_paid_amount = order.final_price + order.weizoom_card_money
						paid_amount_total_first += tmp_paid_amount

					for order in orders_not_first:
						tmp_paid_amount = order.final_price + order.weizoom_card_money
						paid_amount_total_not_first += tmp_paid_amount

					statistics_days.extend([orders_total_count, round(paid_amount_total, 2), orders_first_count, round(paid_amount_total_first, 2), orders_not_first_count, round(paid_amount_total_not_first, 2)])

				table.write_row('A{}'.format(tmp_line), statistics_days)

			workbook.close()

			receivers = ['houtingfei@weizoom.com', 'zhangzhiyong@weizoom.com', 'guoyucheng@weizoom.com']
			mode = ''
			if len(args) == 1:
				if args[0] == 'test':
					mode = 'test'
			title = u'微众自运营平台订单数量{}'.format(current_time)
			content = u'您好，这是上周统计的微众自运营平台订单数量'
			from core.sendmail import sendmail
			sendmail(receivers, title, content, mode, file_path)
