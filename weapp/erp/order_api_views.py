# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response
from django.conf import settings

from core import paginator
from mall import module_api as mall_api
from tools.express import util as express_util

from watchdog.utils import *
from core.jsonresponse import JsonResponse, create_response
import module_api
from util import session_required, arguments_required
import util as erp_util
from core.exceptionutil import unicode_full_stack

MESSAGE_COUNT_PER_PAGE = 50
COUNT_PER_PAGE = 1

DATA_UPDATE_TYPE = 1 #"update_time"
DATA_CREATED_TYPE = 0 #"created_time"
DATA_TYPE = {
	DATA_UPDATE_TYPE : "update_at",
	DATA_CREATED_TYPE : "created_at"
}

def __get_request_order_list(request):
	# 获取当前页数
	cur_page = int(request.GET.get('page', '1'))
	# 获取每页个数
	count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
	# 处理排序
	sort_attr = request.GET.get('sort_attr', '-created_at')
	filter_value = request.GET.get('filter_value', '-1')

	# 处理筛选条件
	filter_value = request.GET.get('filter_value', '-1')
	serach_type = request.GET.get('serach_type', '0')

	# 用户
	user = request.user

	# 时间区间
	start_date = request.GET.get('start_date', None)
	end_date = request.GET.get('end_date', None)

	date_type = int(request.GET.get('date_type', DATA_CREATED_TYPE))
	#处理搜索
	# 填充query
	query = request.GET.get('query', '')
	query_dict = dict()
	if len(query):
		query_dict['order_id'] = query

	if start_date is None and end_date is None:
		dates = None
	else:
		dates = [start_date, end_date]

	query_string = request.META['QUERY_STRING']

	# 查询全部
	if int(serach_type) == 1:
		dates = None
		count_per_page = -1

	user.is_weizoom_mall = False

	orders, pageinfo, order_total_count = mall_api.get_order_list(user, query_dict, filter_value, sort_attr, query_string, 
		count_per_page, cur_page, dates, DATA_TYPE[date_type])

	return pageinfo, list(orders), count_per_page


def __get_request_order(request, order_id):
	return mall_api.get_order_by_order_id(order_id)

def __build_return_order_json(order):
	data = {
		'order_id': order.order_id,
		'status': order.status,
		'status_text': order.get_status_text(),
		'final_price': order.final_price,
		'order_total_price': order.get_total_price(),
		'ship_name': order.ship_name,
		'ship_tel': order.ship_tel,
		'ship_address': order.ship_address,
		'pay_interface_name': order.get_pay_interface_name,
		'created_at': datetime.strftime(order.created_at, '%Y-%m-%d %H:%M:%S'),
		'update_at': datetime.strftime(order.update_at, '%Y-%m-%d %H:%M:%S'),
		# 'product_count': order.product_count,
		'customer_message': order.customer_message,
		'payment_time': datetime.strftime(order.payment_time, '%Y-%m-%d %H:%M:%S'),
		'area': u'{}'.format(order.get_str_area),
		'type': order.type
	}
	products = []
	for has_product in order.get_products:
		product = {
			'id': has_product.product_id,
			'name': has_product.product.name,
			'model_name': has_product.product_model_name,
			'price': has_product.price,
			'total_price': has_product.total_price,
			'count': has_product.number
		}
		model_names = []
		if has_product.get_specific_model:
			for property in has_product.get_specific_model:
				model_names.append(property.get('name')+":"+property.get('property_value'))
		product['model_value'] = u' '.join(model_names)
		products.append(product)
	data['products'] = products
	return data

def __build_return_order_min_json(order):
	return{
		'order_id': order.order_id,
		'status': order.status,
		'status_text': order.get_status_text(),
		'final_price': order.final_price,
		'order_total_price': order.get_total_price(),
		'created_at': datetime.strftime(order.created_at, '%Y-%m-%d %H:%M:%S'),
		'update_at': datetime.strftime(order.update_at, '%Y-%m-%d %H:%M:%S')
	}

########################################################################
# get_orders: 获取订单列表
########################################################################
@arguments_required('token', 'serach_type')
@session_required
def get_orders(request):
	token = request.GET.get('token', '').strip()

	response = erp_util.check_invalid_serach_type(request.GET.get('serach_type', '0'))
	if response:
		return response

	try:
		pageinfo, request_orders, count_per_page = __get_request_order_list(request)
		return_orders_jsonarray = []
		# 构造返回数据
		for order in request_orders:
			return_orders_jsonarray.append(__build_return_order_min_json(order))

		response = create_response(200)
		response.data = {
			'items': return_orders_jsonarray
		}
		if count_per_page == -1:		
			response.data['pageinfo'] = {'object_count':pageinfo['object_count']}
		else:
			response.data['pageinfo'] = paginator.to_dict(pageinfo)

	except:
		response = create_response(590)
		response.errMsg = u'内部异常'
		error_msg = u"erp获取订单列表 token={}, cause:\n{}".format(token, unicode_full_stack())
		response.innerErrMsg = error_msg
		watchdog_error(error_msg)

	return response.get_response()


########################################################################
# get_order: 获取订单
########################################################################
@arguments_required('token', 'order_id')
@session_required
def get_order(request):
	token = request.GET.get('token', '').strip()
	order_id = request.GET.get('order_id', '').strip()

	response = erp_util.check_invalid_order(request.user, order_id)
	if response:
		return response

	try:
		order = __get_request_order(request, order_id)

		# 构造返回数据
		response = create_response(200)
		response.data =  __build_return_order_json(order)
	except:
		response = create_response(590)
		response.errMsg = u'内部异常'
		error_msg = u"erp获取订单 token={}, order_id={}, cause:\n{}".format(token, order_id, unicode_full_stack())
		response.innerErrMsg = error_msg

	return response.get_response()


########################################################################
# create_order_express_info: 创建订单物流信息
########################################################################
@arguments_required('token', 'order_id', 'express_company_id', 'express_id')
@session_required
def create_order_express_info(request):
	order_id = request.POST.get('order_id', '').strip()
	express_company_id = request.POST.get('express_company_id', '').strip()
	express_id = request.POST.get('express_id', '').strip()

	response = erp_util.check_invalid_order(request.user, order_id)
	if response:
		return response

	express_company_name = erp_util.get_express_company_name(express_company_id)
	if not express_company_name:
		response = create_response(511)
		response.errMsg = u'无效物流公司'
		return response.get_response()

	try:
		mall_api.update_order_express_info(order_id, express_company_name, express_id)
	except:
		response = create_response(590)
		response.errMsg = u'内部异常'
		return response.get_response()

	response = create_response(200)
	return response.get_response()


########################################################################
# update_product_stock: 更新商品库存信息
########################################################################
@arguments_required('token', 'product_id', 'product_model_id', 'stock')
@session_required
def update_product_stock(request):
	product_id = request.POST.get('product_id', '').strip()
	product_model_id = request.POST.get('product_model_id', '').strip()
	stock = request.POST.get('stock', '').strip()

	response = erp_util.check_invalid_product(request.user, product_id)
	if response:
		return response

	response = erp_util.check_invalid_product_model(request.user, product_id, product_model_id)
	if response:
		return response

	try:
		stock = int(stock)
	except:
		response = create_response(552)
		response.errMsg = u'无效库存'
		return response.get_response()

	try:
		mall_api.update_product_stock(product_id, product_model_id, stock)
	except:
		response = create_response(590)
		response.errMsg = u'内部异常'
		return response.get_response()

	response = create_response(200)
	return response.get_response()