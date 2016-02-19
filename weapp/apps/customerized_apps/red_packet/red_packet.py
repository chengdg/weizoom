# -*- coding: utf-8 -*-

import json
import random
from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required

from core import resource
from core import paginator
from core.jsonresponse import create_response
from utils.cache_util import delete_cache

import models as app_models
import export
from apps import request_util
from mall import export as mall_export
from modules.member import integral as integral_api
from mall.promotion import utils as mall_api
import termite.pagestore as pagestore_manager

FIRST_NAV = mall_export.MALL_PROMOTION_AND_APPS_FIRST_NAV
COUNT_PER_PAGE = 20

class RedPacket(resource.Resource):
	app = 'apps/red_packet'
	resource = 'red_packet'
	
	@login_required
	def get(request):
		"""
		响应GET
		"""
		if 'id' in request.GET:
			project_id = 'new_app:red_packet:%s' % request.GET.get('related_page_id', 0)
			try:
				red_packet = app_models.RedPacket.objects.get(id=request.GET['id'])
			except:
				c = RequestContext(request, {
					'first_nav_name': FIRST_NAV,
					'second_navs': mall_export.get_promotion_and_apps_second_navs(request),
					'second_nav_name': mall_export.MALL_APPS_SECOND_NAV,
					'third_nav_name': mall_export.MALL_APPS_REDPACKET_NAV,
					'is_deleted_data': True,
				})

				return render_to_response('red_packet/templates/editor/workbench.html', c)
			is_create_new_data = False

			name = red_packet.name
		else:
			red_packet = None
			is_create_new_data = True
			project_id = 'new_app:red_packet:0'
			name = u'拼红包'

		_, app_name, real_project_id = project_id.split(':')
		if real_project_id != '0':
			pagestore = pagestore_manager.get_pagestore('mongo')
			pages = pagestore.get_page_components(real_project_id)
			if not pages:
				c = RequestContext(request, {
					'first_nav_name': FIRST_NAV,
					'second_navs': mall_export.get_promotion_and_apps_second_navs(request),
					'second_nav_name': mall_export.MALL_APPS_SECOND_NAV,
					'third_nav_name': mall_export.MALL_APPS_REDPACKET_NAV,
					'is_deleted_data': True,
				})

				return render_to_response('red_packet/templates/editor/workbench.html', c)
		
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': mall_export.get_promotion_and_apps_second_navs(request),
			'second_nav_name': mall_export.MALL_APPS_SECOND_NAV,
			'third_nav_name': mall_export.MALL_APPS_REDPACKET_NAV,
			'red_packet': red_packet,
			'title_name': name,
			'is_create_new_data': is_create_new_data,
			'project_id': project_id,
		})
		
		return render_to_response('red_packet/templates/editor/workbench.html', c)
	
	@login_required
	def api_put(request):
		"""
		响应PUT
		"""
		data = request_util.get_fields_to_be_save(request)
		data['qrcode'] = json.loads(request.POST['qrcode'])
		if request.POST['type'] == 'random':
			data['random_random_number_list'] = create_pop_list(data['random_total_money'],data['random_packets_number']) #拼手气红包随机数List
			data['red_packet_remain_amount'] = data['random_packets_number']
		else:
			data['red_packet_remain_amount'] = data['regular_packets_number']
		red_packet = app_models.RedPacket(**data)
		red_packet.save()
		error_msg = None
		
		data = json.loads(red_packet.to_json())
		data['id'] = data['_id']['$oid']
		if error_msg:
			data['error_msg'] = error_msg

		#并发问题临时解决方案 ---start
		# control_data = {}
		# control_data['belong_to'] = data['id']
		# control_data['red_packet_amount'] = 0
		# control = app_models.RedPacketAmountControl(**control_data)
		# control.save()
		# default_data = {}
		# default_data['belong_to'] = data['id']
		# default_data['red_packet_amount'] = int(red_packet_amount) + 1
		# default = app_models.RedPacketAmountControl(**default_data)
		# default.save()
		#并发问题临时解决方案 ---end

		response = create_response(200)
		response.data = data
		return response.get_response()
	
	@login_required
	def api_post(request):
		"""
		响应POST
		"""
		data = request_util.get_fields_to_be_save(request)
		data['qrcode'] = json.loads(request.POST['qrcode'])
		pagestore = pagestore_manager.get_pagestore('mongo')
		project_id = request.GET.get('project_id', 0)
		_, app_name, real_project_id = project_id.split(':')
		page = pagestore.get_page(real_project_id, 1)
		update_data = {}
		update_fields = set(['name', 'start_time', 'end_time', 'timing', 'type', 'random_total_money','random_packets_number','regular_packets_number','regular_per_money','money_range','reply_content', 'material_image','share_description', 'qrcode'])
		for key, value in data.items():
			if key in update_fields:
				update_data['set__'+key] = value
				print key,value,"$$$$$$$$$"
			#清除红包类型选项下不需要再保存的两个字段
			if key == "type" and value == "random":
				update_data['set__random_random_number_list'] = create_pop_list(data['random_total_money'],data['random_packets_number'])
				data['red_packet_remain_amount'] = data['random_packets_number']
				update_data['set__regular_packets_number'] = ''
				update_data['set__regular_per_money'] = ''
				page['component']['components'][0]['model']['regular_packets_number'] = ''
				page['component']['components'][0]['model']['regular_per_money'] = ''
			if key == "type" and value == "regular":
				data['red_packet_remain_amount'] = data['regular_packets_number']
				update_data['set__random_total_money'] = ''
				update_data['set__random_packets_number'] = ''
				page['component']['components'][0]['model']['random_total_money'] = ''
				page['component']['components'][0]['model']['random_packets_number'] = ''
		app_models.RedPacket.objects(id=request.POST['id']).update(**update_data)

		#并发问题临时解决方案 ---start
		# app_models.RedPacketAmountControl.objects(belong_to=request.POST['id']).delete()
		# control_data = {}
		# control_data['belong_to'] = data['id']
		# control_data['red_packet_amount'] = 0
		# control = app_models.RedPacketAmountControl(**control_data)
		# control.save()
		# default_data = {}
		# default_data['belong_to'] = data['id']
		# default_data['red_packet_amount'] = int(red_packet_amount) + 1
		# default = app_models.RedPacketAmountControl(**default_data)
		# default.save()
		#并发问题临时解决方案 ---end

		pagestore.save_page(real_project_id, 1, page['component'])
		#更新后清除缓存
		cache_key = 'apps_red_packet_%s_html' % request.POST['id']
		delete_cache(cache_key)
		response = create_response(200)
		return response.get_response()
	
	@login_required
	def api_delete(request):
		"""
		响应DELETE
		"""
		app_models.RedPacket.objects(id=request.POST['id']).delete()
		
		response = create_response(200)
		return response.get_response()

def create_pop_list(random_total_money,random_packets_number):
	"""
	每次拼手气红包都是取固定金额：总金额/个数，再加上随机的浮动值，得到拼手气红包最终的金额，这里需要在生成拼红包活动时，
	跟着生成一个随机数的List存到数据库中，随机数数量是红包个数，所有随机数的总和为0

	"""
	random_random_number_list = []
	random_total_money = float(random_total_money)#拼手气红包总额
	random_packets_number = int(random_packets_number)  #拼手气红包红包个数
	random_number_range = (random_total_money / random_packets_number) * 0.1 #拼手气红包随机范围
	for _ in range(random_packets_number): #在正负浮动范围内生成红包个数个随机数
		random_random_number_list.append(round(random.uniform(-random_number_range, random_number_range),2))
	total_random = 0 #总随机金额
	for r in random_random_number_list:
		total_random += float(r) #计算总随机金额
	if total_random != 0: #如果总随机金额不等于0，将随机出来的总随机金额与0的差额除以红包个数，分别加到每个随机数上，使之最终总和趋向为0
		total_random_average = (-total_random) / random_packets_number
		i = 0
		total_random = 0 #再次初始化总随机金额
		for r in random_random_number_list:
			random_random_number_list[i] = round((float(r) + float(total_random_average)),2)
			total_random += float(random_random_number_list[i]) #计算平均分配过差额后的总随机金额
			i += 1
		if total_random != 0: #如果因为total_random_average产生了0.01上的差别，取反数加到第一个随机数上，使之最终总和为0
			random_random_number_list[0] = round((float(-total_random) + float(random_random_number_list[0])),2)

	return random_random_number_list