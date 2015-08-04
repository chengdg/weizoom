# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required

from core import apiview_util
from core import paginator
from core.jsonresponse import JsonResponse, create_response

from modules.member.module_api import get_member_by_id_list
from models import *


########################################################################
# get_store: 门店信息
########################################################################
@login_required
def get_store(request):
	count_per_page = int(request.GET.get('count_per_page', '1'))
	cur_page = int(request.GET.get('page', '1'))

	filter_attr = request.GET.get('filter_attr')
	if filter_attr == 'city':
		stores =Store.objects.filter(owner=request.user, city=request.GET.get('filter_value')).order_by('-created_at')
	else:
		stores = Store.objects.filter(owner=request.user).order_by('-created_at')
	
	pageinfo, stores = paginator.paginate(stores, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])	
	
	cur_stores = []
	for c in stores:
		cur_store = JsonResponse()
		cur_store.id = c.id
		cur_store.name = c.name
		cur_store.city = c.city
		cur_store.created_at = datetime.strftime(c.created_at, '%Y-%m-%d %H:%M')
		cur_stores.append(cur_store)

	cur_citys = list(Store.objects.filter(owner=request.user).values('city').distinct())

	response = create_response(200)
	response.data.items = cur_stores
	response.data.all_city = cur_citys
	response.data.sortAttr = request.GET.get('sort_attr', '-created_at')
	response.data.pageinfo = paginator.to_dict(pageinfo)
	
	return response.get_response()


########################################################################
# delete_store: 删除门店信息
########################################################################
@login_required
def delete_store(request):
	store_id = request.POST['store_id']
	Store.objects.filter(id=store_id).delete()
	
	response = create_response(200)
	return response.get_response()


def call_api(request):
	api_function = apiview_util.get_api_function(request, globals())
	return api_function(request)