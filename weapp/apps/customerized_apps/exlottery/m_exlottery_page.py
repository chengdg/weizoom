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
from utils.cache_util import GET_CACHE, SET_CACHE

import models as app_models
from termite2 import pagecreater
from modules.member.module_api import get_member_by_openid
from image import *
from m_exlottery import check_exlottery_code

COLOR_LIST = ['#1b4da0', '#0e3e20', '#eb6139', '#730f0f', '#0c1532', '#eb6139', '#000000']

class Mexlottery(resource.Resource):
	app = 'apps/exlottery'
	resource = 'm_exlottery_page'

	def get(request):
		"""
		响应GET
		"""
		id = request.GET['id']

		member = request.member
		is_pc = False if member else True

		try:
			record = app_models.Exlottery.objects.get(id=id)
			homepage_image = record.homepage_image
		except:
			c = RequestContext(request,{
				'is_deleted_data': True
			})
			return render_to_response('exlottery/templates/webapp/m_exlottery_page.html', c)

		c = RequestContext(request, {
			'record_id': id,
			'page_title': u'专项抽奖',
			'app_name': "exlottery",
			'resource': "exlottery",
			'hide_non_member_cover': True, #非会员也可使用该页面
			'isPC': is_pc,
			'homepage_image': homepage_image
		})
		response = render_to_string('exlottery/templates/webapp/m_exlottery_page.html', c)

		return HttpResponse(response)

	def api_get(request):
		"""
		响应GET
		"""
		owner_id = request.webapp_owner_id
		member = request.member
		record_id = request.GET.get('id',None)
		ex_code = request.GET['excode']
		verify = request.GET['verify_code'].encode('utf8')
		_code = request.session['checkcode']
		# request.session['checkcode'] = ''

		response = create_response(500)
		# 检查验证码是否正确
		if _code.lower() != str(verify).lower():
			response.errMsg = u'验证码输入有误'
			return response.get_response()

		if not record_id or not member:
			response.errMsg = u'活动信息出错'
			return response.get_response()

		# 检查抽奖码是否可用
		resp = check_exlottery_code(ex_code, member.id)

		if resp is not True and (resp != 'is_member_self'):
			response.errMsg = resp
			return response.get_response()

		if resp != 'is_member_self':
			#抽奖码可用，将抽奖码与会员绑定
			exlottery_participance = app_models.ExlotteryParticipance(
				member_id=member.id,
				belong_to=record_id,
				created_at=datetime.now(),
				code=ex_code,
				status=app_models.NOT_USED
			)
			try:
				exlottery_participance.save()
			except:
				response.errMsg = u'活动信息出错'
				return response.get_response()

		response = create_response(200)
		return response.get_response()

class MexlotteryCaptcha(resource.Resource):
	app = 'apps/exlottery'
	resource = 'm_captcha'

	def api_get(request):
		"""
		响应GET
		"""
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

# 创建随机码
def init_check_code(length=4):
	codes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
			 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

	code_list = random.sample(codes, 4)
	code_str = ''.join(code_list)
	return {'clist': code_list, 'cstr': code_str}