# -*- coding: utf-8 -*-

__author__ = 'paco bert'

import os

from django.conf import settings
from core.jsonresponse import create_response

from core.exceptionutil import unicode_full_stack

from modules.member import util as member_util
from modules.member.models import Member, BRING_NEW_CUSTOMER_VIA_QRCODE

from models import *

from account.views import save_base64_img_file_local_for_webapp

from modules.member.integral import increase_member_integral
# from market_tools.tools.coupon.util import get_coupon_rules, consume_coupon
########################################################################
# join_activity:
########################################################################
def join_complain(request):
	complain_id = request.POST.get('complain_id', '0')
	
	try:
		member_complain_settings = MemberComplainSettings.objects.get(id=complain_id)
	except:
		response = create_response(500)
		response.errMsg = u'当前不可反馈'
		response.innerErrMsg = unicode_full_stack()
		return response.get_response()	

	username = ''
	phone_number = ''
	webapp_user_id = -1
	if request.webapp_user:
		webapp_user_id = request.webapp_user.id
	if request.POST:
		try:
			content = request.POST.get('content', '')

			if content.strip() == '':
				response = create_response(500)
				response.errMsg = u'请输入反馈内容'
				return response.get_response()

			# file = request.POST.get('pic_url','')
			# if file:
			# 	value = save_base64_img_file_local_for_webapp(request, file)
			# else:
			# 	value = ''
			
			MemberComplainRecord.objects.create(
				complain_settings_id=complain_id,
				pic_url='',
				content=content,
				webapp_user_id=request.webapp_user.id
				)
			# if member_complain_settings.prize_type == AWARD_INTEGRAL:
			# 	increase_member_integral(member, member_complain_settings.prize_content, u'反馈获取积分')
			# elif member_complain_settings.prize_type == AWARD_COUPON:
			# 	create_coupons(member_complain_settings.owner, member_complain_settings.prize_content, 1, member)
			response = create_response(200)
		except:
			response = create_response(500)
			response.errMsg = u'提交错误'
			response.innerErrMsg = unicode_full_stack()
			return response.get_response()
	else:
		response = create_response(500)
		response.errMsg = u'is not POST method'

	return response.get_response()