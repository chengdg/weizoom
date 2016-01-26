# -*- coding: utf-8 -*-

import os
import subprocess
from datetime import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from market_tools import ToolModule
from market_tools.settings import TOOLS_ORDERING
from apps.models import CustomizedApp, CustomizedAppInfo, CustomizedappStatus
from market_tools.tools.template_message.models import *

#消费品 购买成功通知 product:product_name,price:final_price,time:payment_time    CzaZLpoF-5haKH4LSRPmsR9JceFmqG7aVNF7Fx2xlt0
#消费品 商品发货通知 keyword1: express_company_name, keyword2:express_number, keyword3:product_name,keyword4:number             e345uC49Y_e3R8cSFzc8AdQW25BD0hRAd5aw-wa1_KI
#IT 付款成功通知 orderProductPrice:final_price,orderProductName:product_name,orderAddress:ship_address,orderName:order_id       8qH_wwt3PieaaZVBVIkgP9EgLhpPETkZGRYSfh9i8X4
#IT 订单标记发货通知 orderProductPrice:final_price,orderProductName:product_name,orderAddress:ship_address,orderName:order_id 5RoTMtfXqGas8j39VoRDDmINyLVOOJ6p1BOJ2gVMMBY
#IT 优惠券领取成功通知 keyword1:coupon_name,keyword3:invalid_date
#IT 优惠券过期提醒 orderTicketStore: coupon_store, orderTicketRule: coupon_rule
template_message_dict = [[1, u'TM00247-购买成功通知' ,'product:product_name,price:final_price,time:payment_time', PAY_ORDER_SUCCESS], 
						[1,  u'OPENTM200303341-商品发货通知' ,'keyword1: express_company_name, keyword2:express_number, keyword3:product_name,keyword4:number',PAY_DELIVER_NOTIFY],
						[0,  u'TM00398-付款成功通知' ,'orderProductPrice:final_price,orderProductName:product_name,orderAddress:ship_address,orderName:order_id', PAY_ORDER_SUCCESS],
						[0,  u'TM00505-订单标记发货通知' ,'orderProductPrice:final_price,orderProductName:product_name,orderAddress:ship_address,orderName:order_id', PAY_DELIVER_NOTIFY],
						[0,  u'OPENTM200474379-优惠券领取成功通知' ,'keyword1:coupon_name,keyword3:invalid_date', COUPON_ARRIVAL_NOTIFY],
						[0,  u'TM00853-优惠券过期提醒' ,'orderTicketStore:coupon_store,orderTicketRule:coupon_rule', COUPON_EXPIRED_REMIND],
						[0,  u'OPENTM207449727-任务完成通知' ,'keyword1:task_name,keyword2:prize,keyword3:finish_time', MISSION_ACCOMPLISHED_NOTIFY]
						]
class Command(BaseCommand):
	help = "init tempalte message"
	args = ''
	
	def handle(self, **options):
		for key in TYPE2INDUSTRY.keys():
			if MarketToolsIndustry.objects.filter(industry_type=key).count() == 0:
				MarketToolsIndustry.objects.create(industry_type=key, industry_name=TYPE2INDUSTRY[key])


		for template_message in template_message_dict:			
			if MarketToolsTemplateMessage.objects.filter(title = template_message[1].strip()).count() == 0:
				MarketToolsTemplateMessage.objects.create(industry=template_message[0],  title=template_message[1], attribute=template_message[2], send_point=template_message[3])

		self._set_new_template()
		# self.__abc()


	def _set_new_template(self):
		print 'set_new_template-------------start'

		MarketToolsTemplateMessage.objects.filter(title=u'TM00851-优惠券到账通知').delete()
		
		users = User.objects.all()
		for user in users:
			industries = MarketToolsTemplateMessageDetail.objects.filter(owner=user).values('industry', 'type').distinct()
			industry = {}
			for indus in industries:
				industry_name = TYPE2INDUSTRY.get(indus['industry'], '')
				if indus['type'] == MAJOR_INDUSTRY_TYPE:
					industry['major'] = indus['industry']
				elif indus['type'] == DEPUTY_INDUSTRY_TYPE:
					industry['deputy'] = indus['industry']

			if industry.get('major', '') == INDUSTR_IT or industry.get('deputy', '') == INDUSTR_IT:
				print u'IT科技 user_name={}, user_id={}'.format(user.username, user.id)
				for template_message in template_message_dict:
					message = MarketToolsTemplateMessage.objects.get(title = template_message[1].strip())
					if MarketToolsTemplateMessageDetail.objects.filter(owner=user, template_message_id=message.id).count() == 0:
						print u'	需要补充{}'.format(template_message[1])
						MarketToolsTemplateMessageDetail.objects.create(
							owner = user,
							template_message = message,
							industry = template_message[0],
							template_id = "",
							first_text = "",
							remark_text = "",
							type = MAJOR_INDUSTRY_TYPE if industry.get('major') == INDUSTR_IT else DEPUTY_INDUSTRY_TYPE 
						)


		print 'set_new_template-------------start'


	def __abc(self):
		user = User.objects.get(username='ceshi01')
		from market_tools.tools.template_message import module_api as template_module_api
		webapp_owner_id = user.id
		webapp_user_id = 6
		member_id = 2184797
		send_point = COUPON_ARRIVAL_NOTIFY
		model = {
			"coupon_name": u'全部可用',
			"invalid_date": u'2015-09-07至2015-09-15有效'
		}
		message = template_module_api.send_weixin_template_message(webapp_owner_id, member_id, model, send_point)
		print message
