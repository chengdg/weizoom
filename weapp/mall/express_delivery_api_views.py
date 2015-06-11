# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import MySQLdb
import random
import string

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth
from django.db.models import Q, F
from django.db.models.aggregates import Sum, Count

from models import *
import export
from core.restful_url_route import *
from core.jsonresponse import create_response
from core import paginator
from tools.express import util as tools_express_util

########################################################################
# get_init_express_deliverys: 获得下拉列表中的快递公司信息
########################################################################
@api(app='mall', resource='init_express_deliverys', action='get')
@login_required
def get_init_express_deliverys(request):
	data = tools_express_util.get_express_company_json()
	express_deliverys = ExpressDelivery.objects.filter(owner_id=request.manager.id)

	# 过滤已有的快递公司
	result_express_deliverys = []
	if express_deliverys.count() == 0:
		result_express_deliverys = data
	else:
		express_values = [e.express_value for e in express_deliverys]
		for item in data:
			if item['value'] in express_values:
				continue				
			result_express_deliverys.append(item)

	response = create_response(200)
	response.data = result_express_deliverys
	return response.get_response()


########################################################################
# update_express_delivery_display_index: 修改排列顺序
########################################################################
@api(app='mall', resource='express_delivery_display_index', action='update')
@login_required
def update_express_delivery_display_index(request):
	src_id = request.REQUEST.get('src_id', None)
	dst_id = request.REQUEST.get('dst_id', None)

	if not src_id or not dst_id:
		response = create_response(500)
		response.errMsg = u'invalid arguments: src_id(%s), dst_id(%s)' % (src_id, dst_id)
		return response.get_response()		

	src_id = int(src_id)
	dst_id = int(dst_id)
	if dst_id == 0:
		#dst_id = 0, 将src_product的display_index设置得比第一个product的display_index大即可
		first_delivery = ExpressDelivery.objects.filter(owner=request.manager).order_by('-display_index')[0]
		if first_delivery.id != src_id:
			ExpressDelivery.objects.filter(id=src_id).update(display_index=first_delivery.display_index+1)
	else:
		#dst_id不为0，交换src_product, dst_product的display_index
		id2delivery = dict([(p.id, p) for p in ExpressDelivery.objects.filter(id__in=[src_id, dst_id])])
		ExpressDelivery.objects.filter(id=src_id).update(display_index=id2delivery[dst_id].display_index)
		ExpressDelivery.objects.filter(id=dst_id).update(display_index=id2delivery[src_id].display_index)

	response = create_response(200)
	return response.get_response()


########################################################################
# get_express_deliverys: 获得快递公司
########################################################################
@api(app='mall', resource='express_deliverys', action='get')
@login_required
def get_express_deliverys(request):
	cur_page = int(request.GET.get('page', '1'))
	count_per_page = 50
	#处理排序
	sort_attr = request.GET.get('sort_attr', None);
	if not sort_attr:
		sort_attr = '-display_index'

	express_deliverys = list(ExpressDelivery.objects.filter(owner_id=request.manager.id).order_by('-display_index'))

	pageinfo, express_deliverys = paginator.paginate(express_deliverys, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
	result_express_deliverys = []
	for express_delivery in express_deliverys:
		result_express_deliverys.append({
			"id": express_delivery.id,
			"name": express_delivery.name,
			"express_number": express_delivery.express_number,
			"express_value": express_delivery.express_value,
			"display_index": express_delivery.display_index,
			"remark": express_delivery.remark
		})

	response = create_response(200)
	response.data = {
		'items': result_express_deliverys,
		'pageinfo': paginator.to_dict(pageinfo),
		'sortAttr': sort_attr
	}
	return response.get_response()


########################################################################
# create_express_delivery: 创建物流信息
########################################################################
@api(app='mall', resource='express_delivery', action='create')
@login_required
def create_express_delivery(request):
	express_deliverys = ExpressDelivery.objects.filter(owner_id=request.manager.id).order_by('-display_index')
	if express_deliverys.count() > 0:
		display_index = express_deliverys[0].display_index + 1
	else:
		display_index = 1

	express_delivery = ExpressDelivery.objects.create(
		owner = request.manager,
		name = request.POST.get('name'),
		express_number = request.POST.get('express_number'),
		express_value = request.POST.get('express_value'),
		remark = request.POST.get('remark'),
		display_index = display_index
	)
	response = create_response(200)
	return response.get_response()


########################################################################
# update_express_delivery: 修改物流信息
########################################################################
@api(app='mall', resource='express_delivery', action='update')
@login_required
def update_express_delivery(request):
	try:		
		ExpressDelivery.objects.filter(id=request.POST.get('id')).update(
			name = request.POST.get('name'),
			express_number = request.POST.get('express_number'),
			express_value = request.POST.get('express_value'),
			remark = request.POST.get('remark')
		)
		response = create_response(200)
	except:
		response = create_response(500)

	return response.get_response()


########################################################################
# delete_express_delivery: 删除物流
########################################################################
@api(app='mall', resource='express_delivery', action='delete')
@login_required
def delete_express_delivery(request):
	express_delivery_id = request.POST['id']
	ExpressDelivery.objects.filter(id=express_delivery_id).delete()

	response = create_response(200)
	return response.get_response()


########################################################################
# get_shipping_express_companies: 获得发货时的下拉列表中快递公司信息
########################################################################
@api(app='mall', resource='shipping_express_companies', action='get')
@login_required
def get_shipping_express_companies(request):
	express_deliverys = list(ExpressDelivery.objects.filter(owner_id=request.manager.id).order_by('-display_index'))
	if len(express_deliverys) > 0:
		# 获取 物流名称管理  中的物流信息
		result_express_deliverys = []
		for express_delivery in express_deliverys:
			result_express_deliverys.append({
				"name": express_delivery.name,
				"id": express_delivery.express_number,
				"value": express_delivery.express_value,
			})
	else:
		# 获取 全部的物流信息
		result_express_deliverys = tools_express_util.get_express_company_json()

	response = create_response(200)
	response.data = result_express_deliverys
	return response.get_response()