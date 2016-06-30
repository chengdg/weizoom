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

		# try:
		# 	record = app_models.Exlottery.objects.get(id=id)
		# except:
		# 	c = RequestContext(request,{
		# 		'is_deleted_data': True
		# 	})
		# 	return render_to_response('exlottery/templates/webapp/m_exlottery.html', c)
		# activity_status, record = update_exlottery_status(record)


		c = RequestContext(request, {
			'record_id': id,
			# 'activity_status': activity_status,
			'page_title': u'专项抽奖',
			'app_name': "exlottery",
			'resource': "exlottery",
			'hide_non_member_cover': True, #非会员也可使用该页面
			'isPC': is_pc,
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

		# 检查抽奖码是否存在
		exlottery_code = app_models.ExlotteryCode.objects(owner_id=owner_id, belong_to=record_id, code=ex_code)
		if exlottery_code.count() == 0:
			response.errMsg = u'请输入正确抽奖码'
			return response.get_response()

		if not record_id or not member:
			response.errMsg = u'活动信息出错'
			return response.get_response()

		exlottery = app_models.Exlottery.objects(owner_id=owner_id, id=record_id)
		if exlottery.count() <= 0:
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

def update_exlottery_status(lottery):
	activity_status = lottery.status_text
	now_time = datetime.today().strftime('%Y-%m-%d %H:%M')
	data_start_time = lottery.start_time.strftime('%Y-%m-%d %H:%M')
	data_end_time = lottery.end_time.strftime('%Y-%m-%d %H:%M')
	data_status = lottery.status
	if data_status <= 1:
		if data_start_time <= now_time and now_time < data_end_time:
			lottery.update(set__status=app_models.STATUS_RUNNING)
			activity_status = u'进行中'
		elif now_time >= data_end_time:
			lottery.update(set__status=app_models.STATUS_STOPED)
			activity_status = u'已结束'
		lottery.reload()
	return activity_status, lottery

def check_keyword(data):
	"""
	匹配用户的消息
	@param data: {
		'webapp_owner_id': 0,
		'keyword': 0,
		'openid': 0,
		'webapp_id': 0
	}
	@return: return_html string
	"""
	webapp_owner_id = data['webapp_owner_id']
	keyword = data['keyword']
	member = get_member_by_openid(data['openid'], data['webapp_id'])

	if not member:
		return None

	resp, exlottery= check_exlottery_code(keyword, member.id)

	if resp is not True and (resp != 'is_member_self'):
		return resp

	if resp != 'is_member_self':
		#将用户与抽奖码绑定
		exlottery_participance = app_models.ExlotteryParticipance(
			member_id = member.id,
			belong_to = str(exlottery.id),
			created_at = datetime.now(),
			code = keyword,
			status = app_models.NOT_USED
		)
		try:
			exlottery_participance.save()
		except:
			return None

	reply = exlottery.reply
	reply_link = exlottery.reply_link
	host = settings.DOMAIN
	return_html = u"{}, <a href='http://{}/m/apps/exlottery/m_exlottery/?webapp_owner_id={}&id={}&ex_code={}'>{}</a>".format(reply, host, webapp_owner_id, str(exlottery.id), keyword ,reply_link)

	return return_html

def check_exlottery_code(keyword,member_id):
	if len(keyword) != 10:
		return None
	if not keyword.startswith('el'):
		return None
	code = app_models.ExlotteryCode.objects(code=keyword).order_by('-created_at')
	if code.count() == 0:
		return u'请输入正确的抽奖码', None

	code = code.first()
	belong_to = code.belong_to
	exlottery = app_models.Exlottery.objects(id=belong_to)
	if exlottery.count() == 0:
		return None, None
	exlottery = exlottery.first()
	exlottery_status = exlottery.status
	exlottery_participance = app_models.ExlotteryParticipance.objects(code=keyword,belong_to=belong_to)
	exlottery_participance_count = exlottery_participance.count()

	if exlottery_status == app_models.STATUS_NOT_START:
		return u'该抽奖码尚未生效', None
	elif exlottery_status == app_models.STATUS_STOPED:
		if exlottery_participance_count > 0:
			return u'该抽奖码已使用', None
		else:
			return u'该抽奖码已过期', None
	elif exlottery_status == app_models.STATUS_RUNNING:
		if exlottery_participance_count > 0:
			if app_models.ExlotteryParticipance.objects(code=keyword,belong_to=belong_to,member_id=member_id).count() == 1:
				if exlottery_participance.first().status == app_models.NOT_USED:
					return 'is_member_self', exlottery
				else:
					return u'该抽奖码已使用', None
			else:
				return u'该抽奖码已使用', None

	return True, exlottery