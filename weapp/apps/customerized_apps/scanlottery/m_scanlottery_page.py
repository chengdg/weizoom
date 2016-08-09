# -*- coding: utf-8 -*-
import random
import StringIO

from django.conf import settings
from datetime import datetime

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.template.loader import render_to_string

from core import resource
from core.jsonresponse import create_response
from core.exceptionutil import unicode_full_stack
from watchdog.utils import watchdog_error

from apps.customerized_apps.exlottery.image import *

import models as app_models

COLOR_LIST = ['#1b4da0', '#0e3e20', '#eb6139', '#730f0f', '#0c1532', '#eb6139', '#000000']

class Mexlottery(resource.Resource):
	app = 'apps/scanlottery'
	resource = 'm_scanlottery_page'

	def get(request):
		"""
		响应GET
		"""
		id = request.GET.get('id', '')
		share_page_desc = ''
		try:
			scanlottery = app_models.Scanlottery.objects.get(id=id)
			share_page_desc = scanlottery.name
		except:
			pass

		member = request.member
		is_pc = False if member else True
		thumbnails_url = '/static_v2/img/thumbnails_lottery.png'

		c = RequestContext(request, {
			'record_id': id,
			'page_title': u'扫码抽奖',
			'app_name': "scanlottery",
			'resource': "scanlottery",
			'hide_non_member_cover': True, #非会员也可使用该页面
			'isPC': is_pc,
			'share_img_url': thumbnails_url,
			'share_page_desc': share_page_desc,
			'is_hide_weixin_option_menu': True
		})
		response = render_to_string('scanlottery/templates/webapp/m_scanlottery_page.html', c)

		return HttpResponse(response)

	def api_get(request):
		"""
        响应GET
        """
		owner_id = request.webapp_owner_id
		member = request.member
		record_id = request.GET.get('id', None)
		verify = request.GET['verify_code'].encode('utf8')
		_code = request.session['checkcode']

		# BDD专用
		# verify_for_bdd = request.GET.get('verify_code_for_bdd', None)
		# if verify_for_bdd:
		# 	_code = verify_for_bdd

		response = create_response(500)
		# 检查验证码是否正确
		if _code.lower() != str(verify).lower():
			response.errMsg = u'验证码输入有误'
			return response.get_response()

		if not record_id or not member:
			response.errMsg = u'活动信息出错'
			return response.get_response()

		response = create_response(200)
		return response.get_response()

class MscanlotteryCodeTest(resource.Resource):
	app = 'apps/scanlottery'
	resource = 'scan_code_test'

	def api_get(request):
		"""
		响应GET
		"""
		scan_code = request.GET.get('scan_code', '')
		if not scan_code or len(scan_code) != 20 or not scan_code.isdigit():
			response = create_response(500)
			response.errMsg = u'您的二维码有误'
			return response.get_response()

		scanlottery_record = app_models.ScanlotteryRecord.objects(code=scan_code)
		if scanlottery_record:
			response = create_response(500)
			response.errMsg = u'该码已经参与'
		else:
			response = create_response(200)

		return response.get_response()


class MscanlotteryCaptcha(resource.Resource):
	app = 'apps/scanlottery'
	resource = 'm_captcha'

	def api_get(request):
		"""
		响应GET
		"""
		try:
			cur_color = random.choice(COLOR_LIST)
			captcha_image = captcha(
				drawings=[background('#FFFFFF'),
						  text(fonts=['ARLRDBD.TTF'], font_sizes=[30],
							   drawings=[
								   offset(dx_factor=0.1, dy_factor=0.1)
							   ],
							   color=cur_color,
							   squeeze_factor=1.2),
						  curve(cur_color),
						  noise(),
						  # smooth()
						  ], width=120, height=45)
			code_dict = init_check_code()
			rand_list = code_dict['clist']
			rand_str = code_dict['cstr']
			image = captcha_image(rand_list)
			# 将验证码转换成小写，并保存到session中
			request.session['checkcode'] = rand_str.lower()
			buf = StringIO.StringIO()
			image.save(buf, 'png')
			return HttpResponse(buf.getvalue(), 'image/png')
		except:
			error_msg = u"生成扫码抽奖验证码失败, cause:\n{}".format(unicode_full_stack())
			watchdog_error(error_msg)
			return HttpResponse('')

# 创建随机码
def init_check_code(length=4):
	codes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
			 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

	code_list = random.sample(codes, 4)
	code_str = ''.join(code_list)
	return {'clist': code_list, 'cstr': code_str}