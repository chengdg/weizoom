# -*- coding: utf-8 -*-

__author__ = 'slzhu'

import time, datetime

from django.conf import settings

from core.jsonresponse import JsonResponse, create_response
from core.exceptionutil import unicode_full_stack
from wglass_dateutil import get_month_range, get_date_range
from core import paginator
from webapp.modules.mall.models import *
from modules.member.models import *
from datetime import datetime, timedelta


COUNT_PER_PAGE = 10
STATUS2TEXT = {
	ORDER_STATUS_NOT: u'等待支付',
	ORDER_STATUS_PAYED_SUCCESSED: u'已支付',
	ORDER_STATUS_PAYED_NOT_SHIP: u'等待发货',
	ORDER_STATUS_PAYED_SHIPED: u'已发货',
	ORDER_STATUS_SUCCESSED: u'已完成',
	ORDER_STATUS_CANCEL: u'已取消',
}
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

def _get_all_order_items(user, date_interval=None, query_string=None):
	webapp_id = user.get_profile().webapp_id
	orders = Order.objects.belong_to(webapp_id)

	#处理 时间区间筛选
	start_time, end_time = get_date_range(date_interval, 6)
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


################################################################################
# get_order_by_pay_type: 获取支付方式统计
################################################################################
def get_order_by_pay_type(request):
	#获取当前页数
	cur_page = int(request.GET.get('page', '1'))
	#获取每页个数
	count = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
	#时间范围
	date_interval = request.GET.get('date_interval', '')

	start_date, end_date = get_date_range(date_interval, 6)
	date_items = get_month_range(6)

	webapp_id = request.user.get_profile().webapp_id
	orders = Order.objects.filter(webapp_id=webapp_id, created_at__gte=start_date, created_at__lte=end_date)

	order_items = {}
	for order in orders:
		pay_interface_name = PAYTYPE2NAME.get(order.pay_interface_type, u'')
		if pay_interface_name == '':
			pay_interface_name = u'积分抵扣'
		if order.pay_interface_type == -1:
			pay_interface_name = u'-'
		order_item = {}
		if order_items.has_key(pay_interface_name):
			order_item = order_items[pay_interface_name]
		else:
			order_items[pay_interface_name] = order_item
			for date in date_items:
				order_item[date] = 0
		incr_dict_by_key(order_item, u'总数量')
		month = order.created_at.strftime('%Y-%m')
		if order_item.has_key(month):
			order_item[month] += 1
	sorted_order_items = sorted(order_items.items (), key=lambda e:e[0], reverse=False)

	data = []
	for order_tuple in sorted_order_items:
		data_item = []
		data_item.append(order_tuple[0])
		data_item.append(get_dict_value_by_key(order_tuple[1], u'总数量'))
		for date in date_items:
			data_item.append(order_tuple[1][date])
		data.append(data_item)
	pageinfo, data = paginator.paginate(data, cur_page, count, query_string=None)
	print paginator.to_dict(pageinfo)
	try:
		column = [{"name":"pay_type", "title":u'支付方式'}, {"name":"order_count", "title":u'总数量'}]
		for date in date_items:
			column.append({"name":"month", "title":date})
		response = create_response(200)
		response.data = {
			'column': column,
			'data': data,
			'page_info': paginator.to_dict(pageinfo),
		}
		return response.get_jsonp_response(request)
	except:
		response = create_response(500)
		response.innerErrMsg = unicode_full_stack()
		return response.get_jsonp_response(request)
################################################################################
# get_order_by_product: 获取商品统计
################################################################################
def get_order_by_product(request):
	#获取当前页数
	cur_page = int(request.GET.get('page', '1'))
	#获取每页个数
	count = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
	#时间范围
	date_interval = request.GET.get('date_interval', '')

	start_date, end_date = get_date_range(date_interval, 6)
	date_items = get_month_range(6)

	orders, product2name, order2products = _get_all_order_items(request.user, date_interval)

	order_items = {}
	for order in orders:
		if not order2products.has_key(order.id):
			continue

# 		d = order.created_at.strftime('%Y-%m-%d')
# 		if not order_items.has_key(d):
# 			order_items[d] = {}
# 		o = order_items[d]
# 		if STATUS2TEXT.get(order.status, u'') in ORDER_PAYED_STATUS :
# 			incr_dict_by_key(o, u'总订单金额', order.final_price)
# 		else :
# 			if not o.has_key(u'总订单金额'):
# 				o[u'总订单金额'] = 0
# 		order_items = {}

		order_has_products = order2products[order.id]
		product_items = []
		for order_has_product in order_has_products:
			product_id = order_has_product.product_id
			order_item = {}
			if order_items.has_key(product_id):
				order_item = order_items[product_id]
			else:
				order_items[product_id] = order_item
				for date in date_items:
					order_item[date] = 0
			product_name = product2name[product_id]
			order_item[u'商品名'] = product_name
			incr_dict_by_key(order_item, u'商品数量', order_has_product.number)
			incr_dict_by_key(order_item, u'总金额', order_has_product.total_price)
			try:
				product_items.index(product_id)
			except:
				product_items.append(product_id)
		for key in product_items:
			product_item = order_items[key]
			product_item[u'类型'] = order.type
			incr_dict_by_key(product_item, u'订单数')
			status = STATUS2TEXT.get(order.status, u'')
			incr_dict_by_key(product_item, status)
			month = order.created_at.strftime('%Y-%m')
			if product_item.has_key(month):
				product_item[month] += 1
	sorted_order_items = sorted(order_items.items (), key=lambda e:e[0], reverse=False)

	data = []
	for order_tuple in sorted_order_items:
		data_item = []
		data_item.append(order_tuple[0])
		data_item.append(get_dict_value_by_key(order_tuple[1], u'商品名'))
		data_item.append(get_dict_value_by_key(order_tuple[1], u'订单数'))
		data_item.append(get_dict_value_by_key(order_tuple[1], u'商品数量'))
		data_item.append('%.2f' % (get_dict_value_by_key(order_tuple[1], u'总金额')))
		payed_count = 0
		for status in ORDER_PAYED_STATUS:
			payed_count += get_dict_value_by_key(order_tuple[1], status)
		data_item.append(payed_count)
		data_item.append(order_tuple[1][u'订单数'] - payed_count)
		payed_ratio = 0.00
		if order_tuple[1][u'订单数'] <> 0:
			payed_ratio = '%.2f' % (payed_count / float(order_tuple[1][u'订单数']))
		data_item.append(payed_ratio)
		# for date in date_items:
		# 	data_item.append(order_tuple[1][date])
		data.append(data_item)
	pageinfo, data = paginator.paginate(data, cur_page, count, query_string=None)
	try:
		column = [{"name":"product_id", "title":u'商品ID'}, {"name":"product_name", "title":u'商品名'},
				 {"name":"order_count", "title":u'订单数'}, {"name":"product_count", "title":u'商品总数'}, {"name":"total_price", "title":u'总金额'}, {"name":"payed", "title":u'已付款'},
				 {"name":"not_payed", "title":u'未付款'}, {"name":"pay_ratio", "title":u'支付率'}]
		# for date in date_items:
		# 	column.append({"name":"month", "title":date})
		response = create_response(200)
		response.data = {
			'column': column,
			'data': data,
			'page_info': paginator.to_dict(pageinfo),
		}
		return response.get_jsonp_response(request)
	except:
		response = create_response(500)
		response.innerErrMsg = unicode_full_stack()
		return response.get_jsonp_response(request)


################################################################################
# get_order_by_source: 获取来源统计
################################################################################
def get_order_by_source(request):
	#获取当前页数
	cur_page = int(request.GET.get('page', '1'))
	#获取每页个数
	count = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
	#时间范围
	date_interval = request.GET.get('date_interval', '')

	start_date, end_date = get_date_range(date_interval, 6)
	date_items = get_month_range(6)
	webapp_id = request.user.get_profile().webapp_id
	orders = Order.objects.filter(webapp_id=webapp_id, created_at__gte=start_date, created_at__lte=end_date)

	order_items = {}
	for order in orders:
		order_source = order.order_source
		order_item = {}
		if order_items.has_key(order_source):
			order_item = order_items[order_source]
		else:
			order_items[order_source] = order_item
			for date in date_items:
				order_item[date] = 0
		incr_dict_by_key(order_item, u'总数量')
		status = STATUS2TEXT.get(order.status, u'')
		incr_dict_by_key(order_item, status)
		month = order.created_at.strftime('%Y-%m')
		if order_item.has_key(month):
			order_item[month] += 1
	sorted_order_items = sorted(order_items.items (), key=lambda e:e[0], reverse=False)

	data = []
	for order_tuple in sorted_order_items:
		data_item = []
		data_item.append(order_tuple[0])
		data_item.append(get_dict_value_by_key(order_tuple[1], u'总数量'))
		payed_count = 0
		for status in ORDER_PAYED_STATUS:
			payed_count += get_dict_value_by_key(order_tuple[1], status)
		data_item.append(payed_count)
		data_item.append(order_tuple[1][u'总数量'] - payed_count)
		payed_ratio = 0.00
		if order_tuple[1][u'总数量'] <> 0:
			payed_ratio = '%.2f' % (payed_count / float(order_tuple[1][u'总数量']))
		data_item.append(payed_ratio)
		for date in date_items:
			data_item.append(order_tuple[1][date])
		data.append(data_item)
	pageinfo, data = paginator.paginate(data, cur_page, count, query_string=None)
	try:
		column = [{"name":"pay_type", "title":u'支付方式'}, {"name":"order_count", "title":u'总数量'},
				{"name":"payed", "title":u'已付款'}, {"name":"not_payed", "title":u'未付款'}, {"name":"pay_ratio", "title":u'支付率'}]
		for date in date_items:
			column.append({"name":"month", "title":date})
		response = create_response(200)
		response.data = {
			'column': column,
			'data': data,
			'page_info': paginator.to_dict(pageinfo),
		}
		return response.get_jsonp_response(request)
	except:
		response = create_response(500)
		response.innerErrMsg = unicode_full_stack()
		return response.get_jsonp_response(request)

def get_user_source_by_day(request):
	#获取当前页数
	cur_page = int(request.GET.get('page', '1'))
	#获取每页个数
	num = int(request.GET.get('count_per_page', COUNT_PER_PAGE))

	date_range = request.GET.get('date_interval', '')
	start_date, end_date = get_date_range(date_range, 6)

	data = []

	#计算发起扫码和分享的会员数
	#从relation表中取出通过关注关系进来的会员id
	member_list = MemberFollowRelation.objects.filter(created_at__gte=start_date,
									created_at__lte=end_date,
									is_fans=1).values_list('follower_member_id')

	#取出米琦尔的会员
	webapp_id = request.user.get_profile().webapp_id
	ori_users = Member.objects.filter(webapp_id=webapp_id,
												is_for_buy_test=False,
												is_for_test=False,
												source__in=[SOURCE_MEMBER_QRCODE, SOURCE_BY_URL],
												id__in=member_list)#.values_list('id')
	#保存各个会员的来源
	member_id2source = {}
	for user in ori_users:
		member_id2source[user.id] = user.source

	#取出会员的上一级会员id
	orilist = MemberFollowRelation.objects.filter(created_at__gte=start_date,
									created_at__lte=end_date,
									is_fans=1,
									follower_member_id__in=ori_users.values_list('id'))#.values_list('member_id')

	ori_qrcode_date2member_id = {}
	ori_url_date2member_id = {}
	for user in orilist:
		created_at = user.created_at.strftime('%Y-%m-%d')

		if not ori_qrcode_date2member_id.has_key(created_at):
			ori_qrcode_date2member_id[created_at] = {}
		if not ori_url_date2member_id.has_key(created_at):
			ori_url_date2member_id[created_at] = {}

		if member_id2source[user.follower_member_id] == SOURCE_MEMBER_QRCODE:
			ori_qrcode_date2member_id[created_at][user.member_id] = 1
		elif member_id2source[user.follower_member_id] == SOURCE_BY_URL:
			ori_url_date2member_id[created_at][user.member_id] = 1

	users = Member.objects.filter(webapp_id=webapp_id,
												created_at__gte=start_date,
												created_at__lte=end_date,
												is_for_buy_test=False,
												is_for_test=False,
												source__in=[SOURCE_MEMBER_QRCODE, SOURCE_BY_URL])

	#计算新增会员
	qrcode_date2count = {}
	url_date2count = {}
	for user in users:
		created_at = user.created_at.strftime('%Y-%m-%d')
		if not qrcode_date2count.has_key(created_at):
			qrcode_date2count[created_at] = 0
		if not url_date2count.has_key(created_at):
			url_date2count[created_at] = 0

		if user.source == SOURCE_MEMBER_QRCODE:
			qrcode_date2count[created_at] += 1
		elif user.source == SOURCE_BY_URL:
			url_date2count[created_at] += 1

	date2data = {}

	for date in qrcode_date2count:
		#date = item[0]
		ori_qrcode_count = 0
		ori_url_count = 0

		if ori_qrcode_date2member_id.has_key(date):
			ori_qrcode_count = len(ori_qrcode_date2member_id[date])

		if ori_url_date2member_id.has_key(date):
			ori_url_count = len(ori_url_date2member_id[date])

		_data = [ori_qrcode_count, qrcode_date2count[date], ori_url_count, url_date2count[date]]
		date2data[date] = _data
# 		data.append([date, ori_qrcode_count, item[1], ori_url_count, url_date2count[date]])

	#遍历各个日期，按时间倒序排列载入数据
	_start_date = datetime.strptime(start_date,'%Y-%m-%d %H:%M:%S')
	_end_date = datetime.strptime(end_date,'%Y-%m-%d %H:%M:%S')
	delta = _end_date - _start_date

	while delta.days >= 0:
		date = _end_date.strftime('%Y-%m-%d')
		if date2data.has_key(date):
			items = date2data[date]
			data.append([date, items[0], items[1], items[2], items[3]])
		else:
			data.append([date, 0, 0, 0, 0])

		_end_date = _end_date - timedelta(days = 1)
		delta = _end_date - _start_date

	try:
		column = [{"name":"date", "title":u'日期'},{"name":"ori_qrcode_count", "title":u'发起扫码会员数'},{"name":"qrcode_count", "title":u'通过扫码新增会员数'},
				{"name":"ori_url_count", "title":u'发起线上分享会员数'},
				{"name":"url_count", "title":u'通过线上分享新增会员数'}]
		pageinfo, data = paginator.paginate(data, cur_page, num, query_string=None)
		response = create_response(200)
		response.data = {
			'column': column,
			'data': data,
			'page_info': paginator.to_dict(pageinfo),
		}
		return response.get_jsonp_response(request)
	except:
		response = create_response(500)
		response.innerErrMsg = unicode_full_stack()
		return response.get_jsonp_response(request)





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



def get_user_source_by_week(request):
	#获取当前页数
	cur_page = int(request.GET.get('page', '1'))
	#获取每页个数
	num = int(request.GET.get('count_per_page', COUNT_PER_PAGE))

	date_range = request.GET.get('date_interval', '')
	start_date, end_date = get_date_range(date_range, 6)

	#获取起始日期所在周的第一天
	start_date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(get_week_begin(time.mktime(time.strptime(start_date,'%Y-%m-%d %H:%M:%S')))))
	#获取结束日期所在周的最后一天,最后一天必须以23:59:59结尾，不然会丢一天数据
	end_date = time.strftime('%Y-%m-%d 23:59:59',time.localtime(get_week_end(time.mktime(time.strptime(end_date,'%Y-%m-%d %H:%M:%S')))))
	print 'start',start_date
	print 'end',end_date

	data = []

	#计算发起扫码和分享的会员数
	#从relation表中取出通过关注关系进来的会员id
	member_list = MemberFollowRelation.objects.filter(created_at__gte=start_date,
									created_at__lte=end_date,
									is_fans=1).values_list('follower_member_id')

	#取出米琦尔的会员
	webapp_id = request.user.get_profile().webapp_id
	ori_users = Member.objects.filter(webapp_id=webapp_id,
												is_for_buy_test=False,
												is_for_test=False,
												source__in=[SOURCE_MEMBER_QRCODE, SOURCE_BY_URL],
												id__in=member_list)#.values_list('id')
	#保存各个会员的来源
	member_id2source = {}
	for user in ori_users:
		member_id2source[user.id] = user.source

	#取出会员的上一级会员id
	orilist = MemberFollowRelation.objects.filter(created_at__gte=start_date,
									created_at__lte=end_date,
									is_fans=1,
									follower_member_id__in=ori_users.values_list('id'))#.values_list('member_id')

	ori_qrcode_date2member_id = {}
	ori_url_date2member_id = {}
	week_info = {}
	for user in orilist:
		week = user.created_at.strftime('%W')

		if not week_info.has_key(week):
			week_info[week] = {}
			week_info[week]['start_date'] = time.strftime('%Y-%m-%d',time.localtime(get_week_begin(time.mktime(user.created_at.timetuple()))))
			week_info[week]['end_date'] = time.strftime('%Y-%m-%d',time.localtime(get_week_end(time.mktime(user.created_at.timetuple()))))

		if not ori_qrcode_date2member_id.has_key(week):
			ori_qrcode_date2member_id[week] = {}
		if not ori_url_date2member_id.has_key(week):
			ori_url_date2member_id[week] = {}

		if member_id2source[user.follower_member_id] == SOURCE_MEMBER_QRCODE:
			ori_qrcode_date2member_id[week][user.member_id] = 1
		elif member_id2source[user.follower_member_id] == SOURCE_BY_URL:
			ori_url_date2member_id[week][user.member_id] = 1

	users = Member.objects.filter(webapp_id=webapp_id,
												created_at__gte=start_date,
												created_at__lte=end_date,
												is_for_buy_test=False,
												is_for_test=False,
												source__in=[SOURCE_MEMBER_QRCODE, SOURCE_BY_URL])

	#计算新增会员
	qrcode_date2count = {}
	url_date2count = {}
	for user in users:
		week = user.created_at.strftime('%W')

		if not week_info.has_key(week):
			week_info[week] = {}
			week_info[week]['start_date'] = time.strftime('%Y-%m-%d',time.localtime(get_week_begin(time.mktime(user.created_at.timetuple()))))
			week_info[week]['end_date'] = time.strftime('%Y-%m-%d',time.localtime(get_week_end(time.mktime(user.created_at.timetuple()))))

		if not qrcode_date2count.has_key(week):
			qrcode_date2count[week] = 0
		if not url_date2count.has_key(week):
			url_date2count[week] = 0

		if user.source == SOURCE_MEMBER_QRCODE:
			qrcode_date2count[week] += 1
		elif user.source == SOURCE_BY_URL:
			url_date2count[week] += 1

	date2data = {}

	for week in qrcode_date2count:
		ori_qrcode_count = 0
		ori_url_count = 0

		if ori_qrcode_date2member_id.has_key(week):
			ori_qrcode_count = len(ori_qrcode_date2member_id[week])

		if ori_url_date2member_id.has_key(week):
			ori_url_count = len(ori_url_date2member_id[week])

		_data = [week_info[week]['start_date'], week_info[week]['end_date'], ori_qrcode_count, qrcode_date2count[week], ori_url_count, url_date2count[week]]
		date2data[week] = _data

	#遍历各个日期，按时间倒序排列载入数据
	_start_date = datetime.strptime(start_date,'%Y-%m-%d %H:%M:%S')
	_end_date = datetime.strptime(end_date,'%Y-%m-%d %H:%M:%S')
	delta = _end_date - _start_date

	_week_info = {}

	while delta.days >= 0:
		week = _end_date.strftime('%W')

		if date2data.has_key(week):
			items = date2data[week]
			data.append([week, items[0], items[1], items[2], items[3], items[4], items[5]])
		else:
			start = time.strftime('%Y-%m-%d',time.localtime(get_week_begin(time.mktime(_end_date.timetuple()))))
			end = time.strftime('%Y-%m-%d',time.localtime(get_week_end(time.mktime(_end_date.timetuple()))))
			data.append([week, start, end, 0, 0, 0, 0])

		_end_date = _end_date - timedelta(days = 7)
		delta = _end_date - _start_date

	try:
		column = [{"name":"week", "title":u'周数'},
				{"name":"start_date", "title":u'起始日期'},
				{"name":"end_date", "title":u'结束日期'},
				{"name":"ori_qrcode_count", "title":u'发起扫码会员数'},
				{"name":"qrcode_count", "title":u'通过扫码新增会员数'},
				{"name":"ori_url_count", "title":u'发起线上分享会员数'},
				{"name":"url_count", "title":u'通过线上分享新增会员数'}]
		pageinfo, data = paginator.paginate(data, cur_page, num, query_string=None)
		response = create_response(200)
		response.data = {
			'column': column,
			'data': data,
			'page_info': paginator.to_dict(pageinfo),
		}
		return response.get_jsonp_response(request)
	except:
		response = create_response(500)
		response.innerErrMsg = unicode_full_stack()
		return response.get_jsonp_response(request)



def get_user_static(request):
	#获取当前页数
	cur_page = int(request.GET.get('page', '1'))
	#获取每页个数
	num = int(request.GET.get('count_per_page', COUNT_PER_PAGE))

	date_range = request.GET.get('date_interval', '')
	start_date, end_date = get_date_range(date_range, 6)
	data = []
	webapp_id = request.user.get_profile().webapp_id
	users = Member.objects.filter(webapp_id=webapp_id,
												created_at__gte=start_date,
												created_at__lte=end_date,
												is_subscribed=True,
												is_for_buy_test=False,
												is_for_test=False)
	date2count = {}
	for user in users:
		created_at = user.created_at.strftime('%Y-%m-%d')
		if(date2count.has_key(created_at)):
			count = date2count[created_at]
		else:
			count = 0
		date2count[created_at] = count + 1

	sorted_date2count = sorted(date2count.items(), key=lambda e:e[0], reverse=False)

	date2static = {}
	total_count = Member.objects.filter(webapp_id=webapp_id,
													created_at__lt=start_date,
													is_subscribed=True,
													is_for_buy_test=False,
													is_for_test=False).count()

	#初始化真实会员信息，排除测试账号
	real_member_id_list = []
	for real_user in Member.objects.filter(webapp_id=webapp_id,
														is_for_buy_test=False,
														is_for_test=False):
		real_member_id_list.append(real_user.id)

	#初始化webapp_user_id和member_id的对应关系
	webapp_user_id2member_id = {}
	for webapp_user in WebAppUser.objects.filter(webapp_id=webapp_id):
		if webapp_user.member_id in real_member_id_list and webapp_user.member_id != 0:
			webapp_user_id2member_id[webapp_user.id] = webapp_user.member_id

	#处理订单信息
	date2member_id = {}
	for order in Order.objects.filter(webapp_id=webapp_id, status__gte=2):
		date = order.created_at.strftime('%Y-%m-%d')
		if not date2member_id.has_key(date):
			date2member_id[date] = {}
		if webapp_user_id2member_id.has_key(order.webapp_user_id):
			member_id = webapp_user_id2member_id[order.webapp_user_id]
			date2member_id[date][member_id] = 1

	cur_date = datetime.strptime('2014-01-24', '%Y-%m-%d')
	raw_date = cur_date
	d1 = datetime.strptime(datetime.strftime(datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S'), '%Y-%m-%d'), '%Y-%m-%d')
	delta = d1 - cur_date
	days = delta.days

	date2data = {}
# 	all_member_id = {}
	while delta.days >= 0:
		date2data[datetime.strftime(cur_date, '%Y-%m-%d')] = {}
		#计算4周前数据
# 		four_weeks_ago = cur_date - timedelta(days = 28)
# 		_cur_date = cur_date
		_raw_date = raw_date
		four_weeks_ago = cur_date - timedelta(days = 28)
		_delta = four_weeks_ago - _raw_date
# 		_delta = _raw_date - four_weeks_ago
		_days = _delta.days
		member_id_dict1 = {}
		while _days > 0:
			if date2member_id.has_key(datetime.strftime(_raw_date, '%Y-%m-%d')):
				dict = date2member_id[datetime.strftime(_raw_date, '%Y-%m-%d')]
				tuple = dict.keys()
				if len(tuple) > 0:
					for member_id in tuple:
						member_id_dict1[member_id] = 1

			_raw_date = _raw_date + timedelta(days = 1)
			_delta = four_weeks_ago - _raw_date
			_days = _delta.days

		count = len(member_id_dict1)
		date2data[datetime.strftime(cur_date, '%Y-%m-%d')]['four_week_ago'] = count

		#计算4周内数据
		_delta = cur_date - four_weeks_ago
		member_id_dict2 = {}
		_days = _delta.days
		while _days >= 0:
			if date2member_id.has_key(datetime.strftime(four_weeks_ago, '%Y-%m-%d')):
				dict = date2member_id[datetime.strftime(four_weeks_ago, '%Y-%m-%d')]
				tuple = dict.keys()
				if len(tuple) > 0:
					for member_id in tuple:
						member_id_dict2[member_id] = 1

# 				member_id_dict2[date2member_id[four_weeks_ago]] = 1
			four_weeks_ago = four_weeks_ago + timedelta(days = 1)
			_delta = cur_date - four_weeks_ago
			_days = _delta.days
		count = len(member_id_dict2)
		date2data[datetime.strftime(cur_date, '%Y-%m-%d')]['four_week_to_now'] = count

		cur_date = cur_date + timedelta(days = 1)
		delta = d1 - cur_date
		days = delta.days

	date2total_data = {}
	total_count_yesterday = 0
	for tuple in sorted_date2count:
		total_count += tuple[1]
		new_add = tuple[1]
		if total_count_yesterday != 0:
			rate = '%.6f' % (new_add / float(total_count_yesterday))
		else:
			rate = '%.6f' % 1.00
		total_count_yesterday = total_count
# 		rate = '%.6f' % rate

		date_str = tuple[0]
		four_week_ago = 0
		four_week_to_now = 0
		if date2data.has_key(date_str):
			four_week_ago = date2data[date_str]['four_week_ago']
			four_week_to_now = date2data[date_str]['four_week_to_now']

# 		item = [date_str, total_count, new_add, rate, four_week_ago, four_week_to_now]
		item = [total_count, new_add, rate, four_week_ago, four_week_to_now]
		print item
		date2total_data[date_str] = item
# 		data.append(item)

	_end_date = end_date
	while start_date <= _end_date:
		temp_date = _end_date[:10]
		if date2total_data.has_key(temp_date):
			item = date2total_data[temp_date]
			data.append([temp_date, item[0], item[1], item[2], item[3], item[4]])

		_end_date = (datetime.strptime(_end_date, '%Y-%m-%d %H:%M:%S') - timedelta(days = 1)).strftime('%Y-%m-%d %H:%M:%S')

	try:
		column = [{"name":"date", "title":u'日期'},{"name":"total", "title":u'会员总数'},{"name":"new", "title":u'当日新增'},{"name":"rate", "title":u'会员增长率'},
				{"name":"four_week_ago", "title":u'4周前购买会员数'},	{"name":"four_week_to_now", "title":u'4周内购买会员数'}]
		pageinfo, data = paginator.paginate(data, cur_page, num, query_string=None)
		x_value2y_value = {}
		for d in data:
			x_value2y_value[d[0]] = [d[3], d[1]]
		x_values = x_value2y_value.keys()
		x_values.sort()
		y_values_rate = []
		y_values_count = []
		for x_value in x_values:
			y_values_rate.append(x_value2y_value[x_value][0])
			y_values_count.append(x_value2y_value[x_value][1])
		if len(x_values) == 0:
			x_values.append(u'无')
			y_values_rate.append(0)
			y_values_count.append(0)
		table_data = {}
		table_data['column_names'] = column
		table_data['data_lines'] = data
		table_data['pageinfo'] = paginator.to_dict(pageinfo)
		table_data['sortAttr'] = None


		response_pic_data = {}
		y_values = [{
			'name': u'增长率',
			'values': y_values_rate
		 }, {
			'name': u'会员总数',
			'values': y_values_count
		}]
		response_pic_data['x_unit_label'] = ''
		response_pic_data['y_unit_label'] = ''
		response_pic_data['x_values'] = x_values
		response_pic_data['y_values_list'] = y_values
		response_pic_data['type'] = 'line'

		response = create_response(200)
		response.data = {
			'table_data': table_data,
			# 'response_pic_data': response_pic_data,
		}
		return response.get_jsonp_response(request)
	except:
		response = create_response(500)
		response.innerErrMsg = unicode_full_stack()
		return response.get_jsonp_response(request)
