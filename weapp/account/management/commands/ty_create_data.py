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
会员4	1星	会员2	2017-01-19

订单	下单时间	状态	支付时间	金额
会员1	2017-01-08	完成	2017-01-08	10
会员1	2017-01-19	待发货	2017-01-19	90
会员1	2017-01-20	取消	2017-01-20	30
会员1	2017-01-21	已发货	2017-01-21	90
会员2	2017-01-11	完成	2017-01-11	99
会员2	2017-01-16	完成	2017-01-16	1
会员3	2017-02-18	完成	2017-02-18	40
会员3	2017-02-19	待发货	2017-02-19	30
会员3	2017-02-20	完成	2017-02-20	80
会员4	2017-02-16	待发货	2017-02-16	30
会员4	2017-02-18	取消	2017-02-18	80

周期：
会员1	2017-01-01	2017-01-31
会员1	2017-01-31	2017-03-02
会员2	2017-01-09	2017-02-08
会员3	2017-01-15	2017-02-14
会员3	2017-02-14	2017-03-16
会员4	2017-01-19	2017-02-18
会员4	2017-02-18	2017-03-20

2017-01-23
无发放
2017-01-24
会员2发放40 购物返利
2017-01-27
会员1发放20 购物返利
2017-01-31
无发放
2017-02-01
会员1发放10 推荐返利 推荐的会员2
2017-02-08
无发放
2017-02-26
无发放
2017-02-27
会员3发放20 购物返利
2017-03-02
无发放
2017-03-03
会员1发放10 推荐返利 推荐的会员3
2017-03-04
无发放
'''


class Command(BaseCommand):
	help = "json.dumps cached value"
	args = ''
	
	def handle(self, **options):
		



		#清除旧数据
		MemberGrade.objects.all().delete()
		Member.objects.all().delete()
		WebAppUser.objects.all().delete()
		Order.objects.all().delete()
		OrderStatusLog.objects.all().delete()
		TengyiMember.objects.all().delete()
		TengyiMemberRebateCycle.objects.all().delete()

		grade = MemberGrade.objects.create(webapp_id=1,name='grade1')

		member = Member.objects.create(grade=grade,token=10,username_hexstr='会员1')
		member1 = member
		webapp_user = WebAppUser.objects.create(token=10,webapp_id='0',member_id=member.id)
		order = Order.objects.create(webapp_user_id=webapp_user.id,order_id='00001', status=5,final_price=120)
		order.created_at='2017-06-15 08:08:08'
		order.save()
		l = OrderStatusLog.objects.create(order_id=order.order_id,from_status=0,to_status=2,remark='')
		l.created_at='2017-06-15 08:08:08'
		l.save()
		l = OrderStatusLog.objects.create(order_id=order.order_id,from_status=0,to_status=5,remark='')
		l.created_at='2017-01-16 08:08:08'
		l.save()
		order = Order.objects.create(webapp_user_id=webapp_user.id,order_id='00002', status=3,final_price=100)
		order.created_at='2017-06-28 08:08:08'
		order.save()
		l = OrderStatusLog.objects.create(order_id=order.order_id,from_status=0,to_status=2,remark='')
		l.created_at='2017-06-28 08:08:08'
		l.save()
		l = OrderStatusLog.objects.create(order_id=order.order_id,from_status=0,to_status=3,remark='')
		l.created_at='2017-01-20 08:08:08'
		l.save()
		order = Order.objects.create(webapp_user_id=webapp_user.id,order_id='00003', status=7,final_price=30)
		order.created_at='2017-07-20 08:08:08'
		order.save()
		l = OrderStatusLog.objects.create(order_id=order.order_id,from_status=0,to_status=2,remark='')
		l.created_at='2017-07-20 08:08:08'
		l.save()
		l = OrderStatusLog.objects.create(order_id=order.order_id,from_status=0,to_status=7,remark='')
		l.created_at='2017-01-22 08:08:08'
		l.save()
		order = Order.objects.create(webapp_user_id=webapp_user.id,order_id='00004', status=4,final_price=100)
		order.created_at='2017-07-21 08:08:08'
		order.save()
		l = OrderStatusLog.objects.create(order_id=order.order_id,from_status=0,to_status=2,remark='')
		l.created_at='2017-07-21 08:08:08'
		l.save()
		l = OrderStatusLog.objects.create(order_id=order.order_id,from_status=0,to_status=4,remark='')
		l.created_at='2017-01-23 08:08:08'
		l.save()
		m = TengyiMember.objects.create(member_id=member.id,recommend_by_member_id=0,level=2)
		m.created_at='2017-01-01 08:08:08'
		m.save()
		

		member2 = Member.objects.create(grade=grade,token=20,username_hexstr='会员2')
		member = member2
		webapp_user = WebAppUser.objects.create(token=20,webapp_id='0',member_id=member.id)
		order = Order.objects.create(webapp_user_id=webapp_user.id,order_id='00005', status=5,final_price=200)
		order.created_at='2017-06-02 08:08:08'
		order.save()
		l = OrderStatusLog.objects.create(order_id=order.order_id,from_status=0,to_status=2,remark='')
		l.created_at='2017-06-02 08:08:08'
		l.save()
		order = Order.objects.create(webapp_user_id=webapp_user.id,order_id='00006', status=5,final_price=100)
		order.created_at='2017-07-16 08:08:08'
		order.save()
		l = OrderStatusLog.objects.create(order_id=order.order_id,from_status=0,to_status=2,remark='')
		l.created_at='2017-07-16 08:08:08'
		l.save()
		m = TengyiMember.objects.create(member_id=member.id,recommend_by_member_id=member1.id,level=2)
		m.created_at='2017-01-09 08:08:08'
		m.save()

		member = Member.objects.create(grade=grade,token=30,username_hexstr='会员3')
		webapp_user = WebAppUser.objects.create(token=30,webapp_id='0',member_id=member.id)
		order = Order.objects.create(webapp_user_id=webapp_user.id,order_id='00007', status=5,final_price=40)
		order.created_at='2017-06-05 08:08:08'
		order.save()
		l = OrderStatusLog.objects.create(order_id=order.order_id,from_status=0,to_status=2,remark='')
		l.created_at='2017-06-05 08:08:08'
		l.save()
		order = Order.objects.create(webapp_user_id=webapp_user.id,order_id='00008', status=3,final_price=30)
		order.created_at='2017-06-15 08:08:08'
		order.save()
		l = OrderStatusLog.objects.create(order_id=order.order_id,from_status=0,to_status=2,remark='')
		l.created_at='2017-06-15 08:08:08'
		l.save()
		order = Order.objects.create(webapp_user_id=webapp_user.id,order_id='00009', status=5,final_price=80)
		order.created_at='2017-07-15 08:08:08'
		order.save()
		l = OrderStatusLog.objects.create(order_id=order.order_id,from_status=0,to_status=2,remark='')
		l.created_at='2017-07-15 08:08:08'
		l.save()
		m = TengyiMember.objects.create(member_id=member.id,recommend_by_member_id=member1.id,level=1)
		m.created_at='2017-01-15 08:08:08'
		m.save()

		member = Member.objects.create(grade=grade,token=40,username_hexstr='会员4')
		webapp_user = WebAppUser.objects.create(token=40,webapp_id='0',member_id=member.id)
		order = Order.objects.create(webapp_user_id=webapp_user.id,order_id='00010', status=3,final_price=30)
		order.created_at='2017-02-16 08:08:08'
		order.save()
		l = OrderStatusLog.objects.create(order_id=order.order_id,from_status=0,to_status=2,remark='')
		l.created_at='2017-02-16 08:08:08'
		l.save()
		order = Order.objects.create(webapp_user_id=webapp_user.id,order_id='00011', status=7,final_price=80)
		order.created_at='2017-02-18 08:08:08'
		order.save()
		l = OrderStatusLog.objects.create(order_id=order.order_id,from_status=0,to_status=2,remark='')
		l.created_at='2017-02-18 08:08:08'
		l.save()
		m = TengyiMember.objects.create(member_id=member.id,recommend_by_member_id=member2.id,level=1)
		m.created_at='2017-01-19 08:08:08'
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

