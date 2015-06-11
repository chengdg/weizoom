# -*- coding: utf-8 -*-

import time, datetime

from django.conf import settings

from core.jsonresponse import JsonResponse, create_response
from core import paginator

from account.models import *
from mall.models import *
from wglass_dateutil import get_date_range

COUNT_PER_PAGE = 10
MIQIER_MONTH_BEFORE = 6

STATUS2TEXT = {
	ORDER_STATUS_NOT: u'等待支付',
	ORDER_STATUS_PAYED_SUCCESSED: u'已支付',
	ORDER_STATUS_PAYED_NOT_SHIP: u'等待发货',
	ORDER_STATUS_PAYED_SHIPED: u'已发货',
	ORDER_STATUS_SUCCESSED: u'已完成',
	ORDER_STATUS_CANCEL: u'已取消',
}
ORDER_PAYED_STATUS = [
	u'已支付',
	u'等待发货',
	u'已发货',
	u'已完成'
]

def create_table_response(request, column_names, data_lines, pageinfo=None, sortAttr=None):
	"""
	创建表格数据的response
	@param column_names 表格列的描述
		例如：
		[{
			"name": "date",
			"title": "日期",
		}, {
			"name": "url",
			"title": "访问地址",
		}, {
			"name": "user",
			"title": "用户",
		}]
	@param data_lines 所有行的数据
		例如：
		[
			['2014-10-17', '/app/demo', '用户1'],
			['2014-10-18', '/app/demo', '用户2'],
			['2014-10-19', '/app/demo', '用户2'],
			['2014-10-19', '/app/demo', '用户1'],
			['2014-10-20', '/app/demo', '用户1'],
		]
	"""

	response_data = {}
	response_data['cols'] = column_names
	response_data['lines'] = data_lines
	response_data['pageinfo'] = pageinfo
	response_data['sortAttr'] = sortAttr

	response = create_response(200)
	response.data = response_data

	return response.get_jsonp_response(request)

def _get_all_order_items(user, date_interval=None, query_string=None):
	webapp_id = user.get_profile().webapp_id
	orders = Order.objects.belong_to(webapp_id)

	#处理 时间区间筛选
	start_time, end_time = get_date_range(date_interval, MIQIER_MONTH_BEFORE)
	orders = orders.filter(created_at__gte=start_time, created_at__lt=end_time)
	#orders = Order.objects.using('weapp').filter(webapp_id=webapp_id, created_at__gte=start_time, created_at__lt=end_time)


	#获得商品信息
	product2name = {}
	products = Product.objects.filter(owner=user)
	for p in products:
		product2name[p.id] = p.name

	#获得订单包含商品信息
# 	order_ids = [o.id for o in orders]
	#去掉已取消和未付款的订单
	order_ids = []
	for o in orders:
		if o.status >= 2:
			order_ids.append(o.id)

		###############################################################################
		#临时特殊处理老商城的订单，2014年12月底老商城下线，此处逻辑即可去掉
		if o.webapp_id == '3194':
			o.final_price = o.integral_money + o.final_price
			if o.pay_interface_type == 10:
				o.pay_interface_type = 3 #变更为微众卡支付
		###############################################################################

	order_has_products = OrderHasProduct.objects.filter(order_id__in=order_ids)
	order2products = {}
	for r in order_has_products:
		order_id = r.order_id
		if not order2products.has_key(order_id):
			order2products[order_id] = []
		products = order2products[order_id]
		products.append(r)

	return orders, product2name, order2products

def incr_dict_by_key(dict, key, value=1):
	if not dict.has_key(key):
		dict[key] = 0
	dict[key] += value


def get_dict_value_by_key(dict, key, val=0):
	value = val
	if (dict.has_key(key)):
		value = dict[key]
	return value


def process_sale_item(order2products, item, order):
	incr_dict_by_key(item, u'总订单数')
	status = STATUS2TEXT.get(order.status, u'')
	incr_dict_by_key(item, status)
	pay_interface_name = PAYTYPE2NAME.get(order.pay_interface_type, u'')

	#去掉已取消的订单
	if order.status >= 2:
		incr_dict_by_key(item, u'支付:' + pay_interface_name)

	if STATUS2TEXT.get(order.status, u'') in ORDER_PAYED_STATUS :
		incr_dict_by_key(item, u'总订单金额', order.final_price)
	else :
		if not item.has_key(u'总订单金额'):
			item[u'总订单金额'] = 0

	order_product_count = 0
	if order2products.has_key(order.id):
		order_has_products = order2products[order.id]
		for order_has_product in order_has_products:
			order_product_count += order_has_product.number
	incr_dict_by_key(item, u'总商品数量', order_product_count)


def add_sale_item(data, data_item, item):
	data_item.append(item[u'总订单数'])
	if (item.has_key(u'购买人数')):
		data_item.append(get_dict_value_by_key(item, u'购买人数'))
	if (item.has_key(u'新用户数')):
		data_item.append(get_dict_value_by_key(item, u'新用户数'))
	if (item.has_key(u'老用户数')):
		data_item.append(get_dict_value_by_key(item, u'老用户数'))
	payed_count = 0
	for status in ORDER_PAYED_STATUS:
		payed_count += get_dict_value_by_key(item, status)
	payed_ratio = 0.00
	if item[u'总订单数'] <> 0:
		payed_ratio = '%.2f' % (payed_count / float(item[u'总订单数']))

	wait_to_pay_count = get_dict_value_by_key(item, u'等待支付')
	cancel_count = get_dict_value_by_key(item, u'已取消')
	data_item.append(payed_count)
	#data_item.append(item[u'总订单数'] - payed_count)
	data_item.append(wait_to_pay_count)
	data_item.append(cancel_count)
	data_item.append(payed_ratio)
	data_item.append('%.2f' % item[u'总订单金额'])
	data_item.append(item[u'总商品数量'])
	data_item.append(get_dict_value_by_key(item, u'支付:支付宝'))
	data_item.append(get_dict_value_by_key(item, u'支付:微信支付'))
	data_item.append(get_dict_value_by_key(item, u'支付:货到付款'))
	data_item.append(get_dict_value_by_key(item, u'支付:微众卡支付'))
	data_item.append(get_dict_value_by_key(item, u'支付:优惠抵扣'))
	data_item.append(get_dict_value_by_key(item, u'支付:积分抵扣'))
	data.append(data_item)

def get_day_begin(ts = time.time(),N = 0):
    """
    N为0时获取时间戳ts当天的起始时间戳，N为负数时前数N天，N为正数是后数N天
    """
    return int(time.mktime(time.strptime(time.strftime('%Y-%m-%d',time.localtime(ts)),'%Y-%m-%d'))) + 86400*N


def get_week_begin(ts = time.time(),N = 0):
    """
    N为0时获取时间戳ts当周的开始时间戳，N为负数时前数N周，N为整数是后数N周，此函数将周一作为周的第一天
    """
    w = int(time.strftime('%w',time.localtime(ts)))
    if w == 0:
    	w = 7
    return get_day_begin(int(ts - (w-1)*86400)) + N*604800


def get_week_end(ts = time.time(),N = 0):
    """
    N为0时获取时间戳ts当周的开始时间戳，N为负数时前数N周，N为整数是后数N周，此函数将周一作为周的第一天
    """
    w = int(time.strftime('%w',time.localtime(ts)))
    if w == 0:
    	w = 7
    return get_day_begin(int(ts - (w-7)*86400)) + N*604800

def create_doughnut_chart_response(request, type, item):
	response = create_response(200)
	response.data.type = type

	dataPoints = []
	for key, value in item.items():
		dataPoint = {}
		dataPoint['label'] = key+":"+str(value)
		dataPoint['y'] = value
		dataPoint['legendText'] = key
		dataPoints.append(dataPoint)

	response.data.dataPoints = dataPoints

	return response.get_jsonp_response(request)


def get_order_by_status(request):
	date_interval = request.GET.get('date_interval', '')
	start_date, end_date = get_date_range(date_interval, MIQIER_MONTH_BEFORE)

	user_profile = UserProfile.objects.get(user=request.user)
	orders = Order.objects.filter(webapp_id=user_profile.webapp_id, created_at__gte=start_date, created_at__lte=end_date)
	item = {}
	for order in orders:
		order_id = order.order_id
		status = STATUS2TEXT.get(order.status, u'')
		incr_dict_by_key(item, status)
	try:
		return create_doughnut_chart_response(request, 'doughnut', item)
	except:
		response = create_response(500)
		return response.get_jsonp_response(request)

def get_order_by_day(request):
	#获取当前页数
	cur_page = int(request.GET.get('page', '1'))
	#获取每页个数
	count = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
	#时间范围
	date_interval = request.GET.get('date_interval', '')

	user = request.user

	orders, product2name, order2products = _get_all_order_items(user, date_interval)

	order_items = {}
	for order in orders:
		date = order.created_at.strftime('%Y-%m-%d')
		if not order_items.has_key(date):
			order_items[date] = {}
		order_item = order_items[date]
		process_sale_item(order2products, order_item, order)
	sorted_order_items = sorted(order_items.items(), key=lambda e:e[0], reverse=True)

	data = []
	for order_tuple in sorted_order_items:
		data_item = []
		data_item.append(order_tuple[0])
		add_sale_item(data, data_item, order_tuple[1])
	pageinfo, data = paginator.paginate(data, cur_page, count, query_string=None)
	try:
		column = [{"name":"date", "title":u'日期'}, {"name":"total_order_count", "title":u'总订单数'},
			{"name":"payed", "title":u'已付款'},{"name":"not_payed", "title":u'未付款'},{"name":"cancel", "title":u'已取消'},{"name":"pay_ratio", "title":u'支付率'},
			{"name":"order_price", "title":u'总订单金额'},{"name":"total_product_count", "title":u'总商品数量'},
			{"name":"pay_ali", "title":u'支付:支付宝'},{"name":"pay_winxin", "title":u'支付:微信支付'},{"name":"pay_cod", "title":u'支付:货到付款'},
			{"name":"pay_weizoom_coin", "title":u'支付:微众卡支付'},{"name":"pay_preference", "title":u'支付:优惠抵扣'},{"name":"pay_ten", "title":u'支付:积分抵扣'}]
		response = create_response(200)
		response.data = {
			'column': column,
			'data': data,
			'page_info': paginator.to_dict(pageinfo),
		}
		return response.get_jsonp_response(request)
	except:
		response = create_response(500)
		return response.get_jsonp_response(request)

def get_order_by_week(request):
	#获取当前页数
	cur_page = int(request.GET.get('page', '1'))
	#获取每页个数
	count = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
	#时间范围
	date_interval = request.GET.get('date_interval', '')

	user = request.user
	orders, product2name, order2products = _get_all_order_items(user, date_interval)

	order_items = {}
	week_customers = []
	week_old_customers = []
	week_new_customers = []
	for order in orders:
		week = order.created_at.strftime('%W')
		order_item = {}
		if not order_items.has_key(week):
			order_item[u'起始日期'] = time.strftime('%Y-%m-%d',time.localtime(get_week_begin(time.mktime(order.created_at.timetuple()))))
			order_item[u'结束日期'] = time.strftime('%Y-%m-%d',time.localtime(get_week_end(time.mktime(order.created_at.timetuple()))))
			order_items[week] = order_item
			week_customers = []
			week_old_customers = []
			week_new_customers = []
		else:
			order_item = order_items[week]
		process_sale_item(order2products, order_item, order)
		if order.webapp_user_id not in week_customers:
			week_customers.append(order.webapp_user_id)
			incr_dict_by_key(order_item, u'购买人数')
			if order.webapp_user_id not in week_old_customers:
				if Order.objects.filter(webapp_user_id=order.webapp_user_id, webapp_id=order.webapp_id, created_at__lt=order_item[u'起始日期']).exists():
					week_old_customers.append(order.webapp_user_id)
					incr_dict_by_key(order_item, u'老用户数')
				else:
					week_new_customers.append(order.webapp_user_id)
					incr_dict_by_key(order_item, u'新用户数')
	sorted_order_items = sorted(order_items.items(), key=lambda e:e[0], reverse=True)

	data = []
	for order_tuple in sorted_order_items:
		data_item = []
		data_item.append(order_tuple[0])
		data_item.append(order_tuple[1][u'起始日期'])
		data_item.append(order_tuple[1][u'结束日期'])
		add_sale_item(data, data_item, order_tuple[1])
	pageinfo, data = paginator.paginate(data, cur_page, count, query_string=None)
	try:
		column = [{"name":"week", "title":u'周数'}, {"name":"begin", "title":u'起始日期'}, {"name":"end", "title":u'结束日期'}, {"name":"total_order_count", "title":u'总订单数'},
				{"name":"customers_count", "title":u'下单人数'},{"name":"new_customers_count", "title":u'新用户'},{"name":"old_customers_count", "title":u'老用户'},
			{"name":"payed", "title":u'已付款'},{"name":"not_payed", "title":u'未付款'},{"name":"cancel", "title":u'已取消'},{"name":"pay_ratio", "title":u'支付率'},
			{"name":"order_price", "title":u'总订单金额'},{"name":"total_product_count", "title":u'总商品数量'},
			{"name":"pay_ali", "title":u'支付:支付宝'},{"name":"pay_winxin", "title":u'支付:微信支付'},{"name":"pay_cod", "title":u'支付:货到付款'},
			{"name":"pay_weizoom_coin", "title":u'支付:微众卡支付'},{"name":"pay_preference", "title":u'支付:优惠抵扣'},{"name":"pay_jifen", "title":u'支付:积分抵扣'}]
		response = create_response(200)
		response.data = {
			'column': column,
			'data': data,
			'page_info': paginator.to_dict(pageinfo),
		}
		return response.get_jsonp_response(request)
	except:
		response = create_response(500)
		return response.get_jsonp_response(request)

def get_order_by_month(request):
	#获取当前页数
	cur_page = int(request.GET.get('page', '1'))
	#获取每页个数
	count = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
	#时间范围
	date_interval = request.GET.get('date_interval', '')

	user = request.user
	orders, product2name, order2products = _get_all_order_items(user, date_interval)

	order_items = {}
	for order in orders:
		month = order.created_at.strftime('%Y-%m')
		if not order_items.has_key(month):
			order_items[month] = {}
		order_item = order_items[month]
		process_sale_item(order2products, order_item, order)
	sorted_order_items = sorted(order_items.items(), key=lambda e:e[0], reverse=True)

	data = []
	for order_tuple in sorted_order_items:
		data_item = []
		data_item.append(order_tuple[0])
		add_sale_item(data, data_item, order_tuple[1])
	pageinfo, data = paginator.paginate(data, cur_page, count, query_string=None)
	try:
		column = [{"name":"month", "title":u'月份'}, {"name":"total_order_count", "title":u'总订单数'},
			{"name":"payed", "title":u'已付款'},{"name":"not_payed", "title":u'未付款'},{"name":"cancel", "title":u'已取消'},{"name":"pay_ratio", "title":u'支付率'},
			{"name":"order_price", "title":u'总订单金额'},{"name":"total_product_count", "title":u'总商品数量'},
			{"name":"pay_ali", "title":u'支付:支付宝'},{"name":"pay_winxin", "title":u'支付:微信支付'},{"name":"pay_cod", "title":u'支付:货到付款'},
			{"name":"pay_weizoom_coin", "title":u'支付:微众卡支付'},{"name":"pay_preference", "title":u'支付:优惠抵扣'},{"name":"pay_ten", "title":u'支付:积分抵扣'}]
		response = create_response(200)
		response.data = {
			'column': column,
			'data': data,
			'page_info': paginator.to_dict(pageinfo),
		}
		return response.get_jsonp_response(request)
	except:
		response = create_response(500)
		return response.get_jsonp_response(request)

