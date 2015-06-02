# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json

from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission
from django.contrib import auth

from core.paginator import paginate
from core import paginator
from core.jsonresponse import JsonResponse, create_response

from models import *

########################################################################
# delete_news: 删除一条图文
########################################################################
@login_required
def delete_news(request):
	Material.objects.filter(owner=request.user, id=request.GET['id']).update(is_deleted=True)
	return create_response(200).get_response()


########################################################################
# create_material: 创建素材
########################################################################
@login_required
def create_material(request):
	newses = json.loads(request.POST['data'])
	if len(newses) == 1:
		material = Material.objects.create(owner=request.user, type=SINGLE_NEWS_TYPE)
	else:
		material = Material.objects.create(owner=request.user, type=MULTI_NEWS_TYPE)

	for news in newses:
		News.objects.create(
			material = material,
			display_index = news['display_index'],
			title = news['title'].strip(),
			summary = news['summary'].strip(),
			text = news['text'],
			pic_url = news['pic_url'],
			url = news['url'],
			link_target = news['link_target'],
			is_show_cover_pic = True if (news.get('is_show_cover_pic', True) in ('true', 'yes', 'True', 'Yes', True)) else False
		)

	response = create_response(200)
	response.data.id = material.id
	return response.get_response()


########################################################################
# update_material: 修改素材
########################################################################
@login_required
def update_material(request):
	newses = json.loads(request.POST['data'])
	material_id = int(request.POST['material_id'])
	
	delete_ids = request.POST.get('delete_ids', None)
	if delete_ids:
		News.objects.filter(id__in=delete_ids.split(',')).delete()

	if material_id == -1:
		if len(newses) == 1:
			material = Material.objects.create(owner=request.user, type=SINGLE_NEWS_TYPE)
		else:
			material = Material.objects.create(owner=request.user, type=MULTI_NEWS_TYPE)
	else:
		material = Material.objects.get(id=material_id)

	for index, news in enumerate(newses):
		link_target = news['link_target']
		if type(link_target) != unicode:
			link_target = json.dumps(link_target)

		if int(news['id']) > 0:
			new = News.objects.get(id=news['id'])
			new.display_index = index+1
			new.title = news['title'].strip()
			new.summary = news['summary'].strip()
			if news['url']:
				new.text = ''
				new.url = news['url']
				new.link_target = link_target
			else:
				new.text = news['text']
				new.url = ''
				new.link_target = ''
			new.pic_url = news['pic_url']
			
			new.is_show_cover_pic = True if (news.get('is_show_cover_pic', True) in ('true', 'yes', 'True', 'Yes', True)) else False
			new.save()
		else:
			News.objects.create(
				material = material,
				display_index = index+1,
				title = news['title'].strip(),
				summary = news['summary'].strip(),
				text = news['text'],
				pic_url = news['pic_url'],
				url = news['url'],
				link_target = link_target,
				is_show_cover_pic = True if (news.get('is_show_cover_pic', True) in ('true', 'yes', 'True', 'Yes', True)) else False
			)

	response = create_response(200)
	response.data.id = material.id
	return response.get_response()


########################################################################
# get_material: 获取素材
########################################################################
@login_required
def get_material(request):
	material = Material.objects.get(id=request.GET['id'])
	response = create_response(200)
	newses = []
	for news in News.objects.filter(material=material):
		data = dict()
		data['id'] = news.id
		data['title'] = news.title
		data['summary'] = news.summary
		data['text'] = news.text
		data['pic_url'] = news.pic_url
		data['date'] = news.created_at.strftime('%m月%d日').strip('0')
		data['url'] = news.url
		data['link_target'] = news.link_target
		data['is_show_cover_pic'] = news.is_show_cover_pic
		newses.append(data)

	response.data.items = newses
	return response.get_response()


########################################################################
# get_newses: 获图文消息列表
########################################################################
@login_required
def get_newses(request):
	materials = Material.objects.filter(owner=request.user, is_deleted=False).order_by('-created_at')
	cur_page = request.GET.get('page', 1)
	count_per_page = request.GET.get('count_per_page', 20)
	response = create_response(200)
	if not cur_page == "0":
		pageinfo, materials = paginator.paginate(materials, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
		response.data.pageinfo = paginator.to_dict(pageinfo)
	else:
		pass
	
	material_ids = [m.id for m in materials]
	id2material = __get_materials(material_ids)
	newses = []
	for id in material_ids:
		data = dict()
		data['id'] = id
		data['newses'] = id2material[id]
		if len(data['newses']) == 0:
			#空素材，略过
			pass
		else:
			newses.append(data)

	response.data.items = newses
	
	return response.get_response()


def __get_materials(material_ids):
	id2material = dict([(material_id, []) for material_id in material_ids])
	for news in News.objects.filter(material_id__in=material_ids):
		material_id = news.material_id
		data = {}
		data['id'] = news.id
		data['display_index'] = news.display_index
		data['title'] = news.title
		data['summary'] = news.summary
		data['text'] = news.text
		data['pic_url'] = news.pic_url
		data['url'] = news.url
		data['link_target'] = news.link_target
		data['is_show_cover_pic'] = news.is_show_cover_pic
		id2material[material_id].append(data)

	return id2material