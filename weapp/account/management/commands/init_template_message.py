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
#IT  订单标记发货通知 orderProductPrice:final_price,orderProductName:product_name,orderAddress:ship_address,orderName:order_id 5RoTMtfXqGas8j39VoRDDmINyLVOOJ6p1BOJ2gVMMBY
template_message_dict = [[1, u'TM00247-购买成功通知' ,'product:product_name,price:final_price,time:payment_time', PAY_ORDER_SUCCESS], 
						[1,  u'OPENTM200303341-商品发货通知' ,'keyword1: express_company_name, keyword2:express_number, keyword3:product_name,keyword4:number',PAY_DELIVER_NOTIFY],
						[0,  u'TM00398-付款成功通知' ,'orderProductPrice:final_price,orderProductName:product_name,orderAddress:ship_address,orderName:order_id', PAY_ORDER_SUCCESS],
						[0,  u'TM00505-订单标记发货通知' ,'orderProductPrice:final_price,orderProductName:product_name,orderAddress:ship_address,orderName:order_id', PAY_DELIVER_NOTIFY]
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
