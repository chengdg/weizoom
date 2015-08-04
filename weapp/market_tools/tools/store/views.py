# -*- coding: utf-8 -*-

import json

from django.template import Context, RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from core import paginator
from models import *
from market_tools import export
from account.models import *


MARKET_TOOLS_NAV = 'market_tools'
SECOND_NAV_NAME = 'store'

########################################################################
# list_store: 显示门店列表
########################################################################
@login_required
def list_stores(request):
	c = RequestContext(request, {
		'first_nav_name': MARKET_TOOLS_NAV,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': SECOND_NAV_NAME,
	})
	return render_to_response('store/editor/stores.html', c)

########################################################################
# add_store: 添加门店信息
########################################################################
@login_required
def add_store(request):
	if request.POST:
		zone = request.POST.get('zone', '').strip()
		num = request.POST.get('num', '').strip()
		tel = "%s-%s" % (zone, num)
		store = Store.objects.create(
			owner = request.user,
			name = request.POST.get('name', '').strip(),
			thumbnails_url = request.POST.get('thumbnails_url', '').strip(),
			store_intro = request.POST.get('store_intro', '').strip(),
			city = request.POST.get('city', '').strip(),
			address = request.POST.get('address', '').strip(),
			location = request.POST.get('location', '').strip(),
			bus_line = request.POST.get('bus_line', '').strip(),
			tel = tel,
			detail = request.POST.get('detail', '').strip(),
		)

		#处理轮播图
		swipe_images = json.loads(request.POST.get('swipe_images', '[]'))
		for swipe_image in swipe_images:
			StoreSwipeImage.objects.create(
				store = store,
				url = swipe_image['url']
			)
		return HttpResponseRedirect('/market_tools/store/')
	else:
		c = RequestContext(request, {
		'first_nav_name': MARKET_TOOLS_NAV,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': SECOND_NAV_NAME,
		})
		return render_to_response('store/editor/edit_store.html', c)


########################################################################
# update_store: 更新门店信息
########################################################################
@login_required
def update_store(request, store_id):
	is_can_update_store = Store.can_update_by(request.user.id, store_id)
	if request.POST:
		if is_can_update_store is False:
			return HttpResponseRedirect('/market_tools/store/')

		zone = request.POST.get('zone', '').strip()
		num = request.POST.get('num', '').strip()
		tel = "%s-%s" % (zone, num)
		Store.objects.filter(owner=request.user, id=store_id).update(
			owner = request.user,
			name = request.POST.get('name', '').strip(),
			thumbnails_url = request.POST.get('thumbnails_url', '').strip(),
			store_intro = request.POST.get('store_intro', '').strip(),
			city = request.POST.get('city', '').strip(),
			address = request.POST.get('address', '').strip(),
			location = request.POST.get('location', '').strip(),
			bus_line = request.POST.get('bus_line', '').strip(),
			tel = tel,
			detail = request.POST.get('detail', '').strip(),
		)

		StoreSwipeImage.objects.filter(store_id=store_id).delete()
		swipe_images = json.loads(request.POST.get('swipe_images', '[]'))
		for swipe_image in swipe_images:
			StoreSwipeImage.objects.create(
				store_id = store_id,
				url = swipe_image['url']
			)

		return HttpResponseRedirect('/market_tools/store/')
	else:
		store = Store.objects.get(id=store_id)
		store.zone,store.num = store.tel.split("-")
		#获取轮播图
		store.swipe_images = []
		for swipe_image in StoreSwipeImage.objects.filter(store_id=store_id):
			store.swipe_images.append({
				'url': swipe_image.url
			})
		store.swipe_images_json = json.dumps(store.swipe_images)
		store.is_can_update_store = is_can_update_store
		c = RequestContext(request, {
		'store': store,
		'first_nav_name': MARKET_TOOLS_NAV,
		'second_navs': export.get_second_navs(request),
		'second_nav_name': SECOND_NAV_NAME,
		})
		return render_to_response('store/editor/edit_store.html', c)
