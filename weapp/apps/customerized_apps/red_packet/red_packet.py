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
			"""
			每次拼手气红包都是取固定金额：总金额/个数，再加上随机的浮动值，得到拼手气红包最终的金额，这里需要在生成拼红包活动时，
			跟着生成一个随机数的List存到数据库中，随机数数量是红包个数，所有随机数的总和为0

			"""
			random_random_number_list = []
			random_number_range = float(data['random_total_money']) * 0.05 #拼手气红包随机数浮动范围为5%
			random_packets_number = int(data['random_packets_number'])  #拼手气红包红包个数
			for _ in range(random_packets_number): #在正负浮动范围内生成红包个数个随机数
				random_random_number_list.append('%.2f'% random.uniform(-random_number_range, random_number_range))
			total_random = 0 #总随机金额
			for r in random_random_number_list:
				total_random += float(r) #计算总随机金额
			if total_random != 0: #如果总随机金额不等于0，将随机出来的总随机金额与0的差额除以红包个数，分别加到每个随机数上，使之最终总和趋向为0
				total_random_average = (-total_random) / random_packets_number
				i = 0
				total_random = 0 #再次初始化总随机金额
				for r in random_random_number_list:
					random_random_number_list[i] = '%.2f'% (float(r) + float(total_random_average))
					total_random += float(random_random_number_list[i]) #计算平均分配过差额后的总随机金额
					i += 1
				if total_random != 0: #如果因为total_random_average产生了0.01上的差别，取反数加到第一个随机数上，使之最终总和为0
					random_random_number_list[0] = '%.2f'% (float(-total_random) + float(random_random_number_list[0]))
			data['random_random_number_list'] = random_random_number_list#拼手气红包随机数List
		red_packet = app_models.RedPacket(**data)
		red_packet.save()
		error_msg = None
		
		data = json.loads(red_packet.to_json())
		data['id'] = data['_id']['$oid']
		if error_msg:
			data['error_msg'] = error_msg
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
				update_data['set__regular_packets_number'] = ''
				update_data['set__regular_per_money'] = ''
				page['component']['components'][0]['model']['regular_packets_number'] = ''
				page['component']['components'][0]['model']['regular_per_money'] = ''
			if key == "type" and value == "regular":
				update_data['set__random_total_money'] = ''
				update_data['set__random_packets_number'] = ''
				page['component']['components'][0]['model']['random_total_money'] = ''
				page['component']['components'][0]['model']['random_packets_number'] = ''
		app_models.RedPacket.objects(id=request.POST['id']).update(**update_data)
		pagestore.save_page(real_project_id, 1, page['component'])
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

