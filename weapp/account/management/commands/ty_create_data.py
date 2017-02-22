# -*- coding: utf-8 -*-

__author__ = 'jiangzhe'

import time
from datetime import datetime, timedelta
import array

from django.core.management.base import BaseCommand, CommandError

from utils import cache_util
from bson import json_util
import json

from mall.models import *
from modules.member.models import *

'''
会员	星级	推荐人	加入日期
会员1	1星	无	2017-01-01
会员2	2星	会员1	2017-01-09
会员3	1星	会员1	2017-01-15


会员1	2017-01-08	完成	2017-01-16	10
会员1	2017-01-19	完成	2017-01-21	30
会员1	2017-01-20	取消	2017-01-22	30
会员1	2017-01-21	已发货	2017-01-23	90
会员2	2017-01-11	完成	2017-01-19	99
会员2	2017-01-16	完成	2017-01-24	1
会员3	2017-02-18	完成	2017-02-20	40
会员3	2017-02-19	完成	2017-02-22	30
会员3	2017-02-17	完成	2017-02-25	80
'''


class Command(BaseCommand):
	help = "json.dumps cached value"
	args = ''
	
	def handle(self, **options):
		grade = MemberGrade.objects.get(id=1)

		#清除旧数据
		Member.objects.all().delete()
		WebAppUser.objects.all().delete()
		Order.objects.all().delete()
		OrderStatusLog.objects.all().delete()
		TengyiMember.objects.all().delete()
		TengyiMemberRebateCycle.objects.all().delete()


		member = Member.objects.create(grade=grade,token=10,username_hexstr='会员1')
		member1 = member
		webapp_user = WebAppUser.objects.create(token=10,webapp_id='0',member_id=member.id)
		order = Order.objects.create(webapp_user_id=webapp_user.id,order_id='00001', status=5,final_price=10)
		order.created_at='2017-01-08 08:08:08'
		order.save()
		l = OrderStatusLog.objects.create(order_id=order.order_id,from_status=0,to_status=5,remark='')
		l.created_at='2017-01-16 08:08:08'
		l.save()
		order = Order.objects.create(webapp_user_id=webapp_user.id,order_id='00002', status=5,final_price=30)
		order.created_at='2017-01-19 08:08:08'
		order.save()
		l = OrderStatusLog.objects.create(order_id=order.order_id,from_status=0,to_status=5,remark='')
		l.created_at='2017-01-21 08:08:08'
		l.save()
		order = Order.objects.create(webapp_user_id=webapp_user.id,order_id='00003', status=7,final_price=30)
		order.created_at='2017-01-20 08:08:08'
		order.save()
		l = OrderStatusLog.objects.create(order_id=order.order_id,from_status=0,to_status=7,remark='')
		l.created_at='2017-01-16 08:08:08'
		l.save()
		order = Order.objects.create(webapp_user_id=webapp_user.id,order_id='00004', status=3,final_price=90)
		order.created_at='2017-01-21 08:08:08'
		order.save()
		l = OrderStatusLog.objects.create(order_id=order.order_id,from_status=0,to_status=3,remark='')
		l.created_at='2017-01-23 08:08:08'
		l.save()
		m = TengyiMember.objects.create(member_id=member.id,recommend_by_member_id=0,level=1)
		m.created_at='2017-01-01 08:08:08'
		m.save()
		

		member = Member.objects.create(grade=grade,token=20,username_hexstr='会员2')
		webapp_user = WebAppUser.objects.create(token=20,webapp_id='0',member_id=member.id)
		order = Order.objects.create(webapp_user_id=webapp_user.id,order_id='00005', status=5,final_price=99)
		order.created_at='2017-01-11 08:08:08'
		order.save()
		l = OrderStatusLog.objects.create(order_id=order.order_id,from_status=0,to_status=5,remark='')
		l.created_at='2017-01-19 08:08:08'
		l.save()
		order = Order.objects.create(webapp_user_id=webapp_user.id,order_id='00006', status=5,final_price=1)
		order.created_at='2017-01-16 08:08:08'
		order.save()
		l = OrderStatusLog.objects.create(order_id=order.order_id,from_status=0,to_status=5,remark='')
		l.created_at='2017-01-24 08:08:08'
		l.save()
		m = TengyiMember.objects.create(member_id=member.id,recommend_by_member_id=member1.id,level=2)
		m.created_at='2017-01-09 08:08:08'
		m.save()

		member = Member.objects.create(grade=grade,token=30,username_hexstr='会员3')
		webapp_user = WebAppUser.objects.create(token=30,webapp_id='0',member_id=member.id)
		order = Order.objects.create(webapp_user_id=webapp_user.id,order_id='00007', status=5,final_price=40)
		order.created_at='2017-02-18 08:08:08'
		order.save()
		l = OrderStatusLog.objects.create(order_id=order.order_id,from_status=0,to_status=5,remark='')
		l.created_at='2017-02-20 08:08:08'
		l.save()
		order = Order.objects.create(webapp_user_id=webapp_user.id,order_id='00008', status=5,final_price=30)
		order.created_at='2017-02-19 08:08:08'
		order.save()
		l = OrderStatusLog.objects.create(order_id=order.order_id,from_status=0,to_status=5,remark='')
		l.created_at='2017-02-22 08:08:08'
		l.save()
		order = Order.objects.create(webapp_user_id=webapp_user.id,order_id='00009', status=5,final_price=80)
		order.created_at='2017-02-17 08:08:08'
		order.save()
		l = OrderStatusLog.objects.create(order_id=order.order_id,from_status=0,to_status=5,remark='')
		l.created_at='2017-02-25 08:08:08'
		l.save()
		m = TengyiMember.objects.create(member_id=member.id,recommend_by_member_id=member1.id,level=1)
		m.created_at='2017-01-15 08:08:08'
		m.save()

		#创建会员周期
		tengyi_members = TengyiMember.objects.all()
		for tengyi_member in tengyi_members:
			if tengyi_member.level == 1:
				cycle = range(6)
			else:
				cycle = range(12)
			for i in cycle:
				recommend_member_rebate_money = 10
				if i > 5:
					recommend_member_rebate_money = 20
				
				start_time = tengyi_member.created_at.date() + timedelta(30*i)
				end_time = start_time + timedelta(30)
				
				TengyiMemberRebateCycle.objects.create(
					member_id = tengyi_member.member_id,
					start_time = start_time,
					end_time = end_time,
					recommend_member_rebate_money = recommend_member_rebate_money,
				)

