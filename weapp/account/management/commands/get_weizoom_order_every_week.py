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

			nick_names = [u'微众商城', u'微众家', u'微众妈妈', u'微众学生', u'微众白富美', u'微众俱乐部']
			# nick_names = [u'微众商城']

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

			for nick_name in nick_names:
				tmp_line += 1

				user_id = ComponentAuthedAppidInfo.objects.get(nick_name=nick_name).auth_appid.user_id
				webapp_id = UserProfile.objects.filter(user_id=user_id)[0].webapp_id
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

					statistics_days.extend([orders_total_count, paid_amount_total, orders_first_count, paid_amount_total_first, orders_not_first_count, paid_amount_total_not_first])

				table.write_row('A{}'.format(tmp_line), statistics_days)

			workbook.close()

			#邮件部分
			#msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')
			# 输入Email地址和口令:

			from_addr = '903214406@qq.com'
			password = 'opfengexhapqbfae'
			# 输入SMTP服务器地址:
			smtp_server = 'smtp.qq.com'
			# 输入收件人地址:
			receivers = ['891470084@qq.com', 'houtingfei@weizoom.com', 'zhangzhiyong@weizoom.com', 'guoyucheng@weizoom.com']
			if len(args) == 1:
				if args[0] == 'test':
					receivers = ['891470084@qq.com']

			to_addr = ';'.join(receivers)

			#msg = MIMEText(u'hello, 每周报表', 'plain', 'utf-8')
			#邮件对象
			msg = MIMEMultipart()
			msg['From'] = from_addr
			msg['To'] = to_addr
			msg['Subject'] = Header(u'微众自运营平台订单数量{}'.format(current_time) , 'utf-8').encode()

			#邮件正文是MIMETEXT
			msg.attach(MIMEText(u'您好，这是上周统计的微众自运营平台订单数量', 'plain', 'utf-8'))

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

