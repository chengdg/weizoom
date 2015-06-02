# -*- coding: utf-8 -*-
__author__ = 'liupeiyu'

from core.jsonresponse import create_response
from order.account.order_decorators import project_freight_required
from core import paginator
from tools.regional.views import get_str_value_by_string_ids

from webapp.modules.mall.models import *
from modules.member.models import *
from webapp.modules.mall.module_api import ship_order
from tools.express.util import get_value_by_name

########################################################################
# list_orders: 显示订单列表
########################################################################
@project_freight_required
def get_orders(request):
	#获取当前页数
	cur_page = int(request.GET.get('page', '1'))
	#获取每页个数
	count = int(request.GET.get('count_per_page', 25))

	webapp_id = request.freight_user.get_profile().webapp_id
	status = [ORDER_STATUS_PAYED_SUCCESSED, ORDER_STATUS_PAYED_NOT_SHIP, ORDER_STATUS_PAYED_SHIPED]
	orders = Order.objects.belong_to(webapp_id)
	orders = orders.filter(status__in=status)

	#处理搜索
	query = request.GET.get('query', None)
	if query:
		orders = orders.filter(order_id=query)
	#处理过滤
	filter_attr = request.GET.get('filter_attr', None)
	filter_value = int(request.GET.get('filter_value', -1))
	source = None
	if filter_attr and (filter_value != -1):
		if filter_attr == 'source':
			if filter_value == 1:
					source = 'weizoom_mall'
			else:
					source = 'mine_mall'
		else:
			params = {filter_attr: filter_value}
			orders = orders.filter(**params)

	#处理排序
	sort_attr = request.GET.get('sort_attr', 'created_at')

	# 排序
	orders = orders.extra(order_by = ['status', sort_attr])

	pageinfo, orders = paginator.paginate(orders, cur_page, count, query_string=request.META['QUERY_STRING'])

	#获取order关联的product集合
	order_ids = [order.id for order in orders]
	product_ids = []
	order2products = {}
	order_product_relations = list(OrderHasProduct.objects.filter(order_id__in=order_ids))
	for relation in order_product_relations:
		product_ids.append(relation.product_id)
		order2products.setdefault(relation.order_id, []).append({
			'count': relation.number, #商品数量
			'id': relation.product_id, #商品id
			'total_price': relation.total_price #商品总价
		})
	id2product = dict([(product.id, product) for product in Product.objects.filter(id__in=product_ids)])

	#获取order对应的会员
	webapp_user_ids = set([order.webapp_user_id for order in orders])
	webappuser2member = Member.members_from_webapp_user_ids(webapp_user_ids)

	orders_json = []
	for order in orders:
		order_info = __get_order_info_json(order, webappuser2member, order2products, id2product)
		if order_info:
			orders_json.append(order_info)

	response = create_response(200)
	response.data.items = orders_json
	response.data.pageinfo = paginator.to_dict(pageinfo)
	response.data.sortAttr = sort_attr
	return response.get_response()


def __get_order_info_json(order, webappuser2member, order2products, id2product):
	#获取order对应的member的显示名
	member = webappuser2member.get(order.webapp_user_id, None)
	if member is not None:
		order.buyer_name = member.username_for_html
	else:
		order.buyer_name = u'未知'

	product_items = []
	#added by chuter, 是否是操作订单删除逻辑的时候有问题？
	if not order2products.has_key(order.id):
		return None

	product_infos = order2products[order.id]
	for product_info in product_infos:
		try:
			product_id = product_info['id']
			product = id2product[product_id]
			product_items.append({
				'name': product.name,
				'thumbnails_url': product.thumbnails_url,
				'count': product_info['count'],
				'total_price': '%.2f' % product_info['total_price']
			})
		except:
			pass

	try:
		ship_address = u'{}{}'.format(get_str_value_by_string_ids(order.area), order.ship_address)
	except:
		ship_address = ''

	# 付款时间
	order.payment_time = ''
	log = get_order_payment_time(order.order_id)
	if log:
		order.payment_time = datetime.strftime(log.created_at, '%Y-%m-%d %H:%M')

	order_info = {
		'id': order.id,
		'order_id': order.order_id,
		'status': order.status,
		'total_price': order.final_price,
		'ship_name': order.ship_name,
		'ship_tel': order.ship_tel,
	    'ship_address': ship_address,
		'buyer_name': order.buyer_name,
	    'payment_time': order.payment_time,
		'pay_interface_name': PAYTYPE2NAME.get(order.pay_interface_type, u''),
		'created_at': datetime.strftime(order.created_at, '%m-%d %H:%M'),
		'product_count': len(product_items),
		'products': product_items,
		'customer_message': order.customer_message
	}

	return order_info

########################################################################
# get_order_status_logs: 获得订单的付款日期
########################################################################
def get_order_payment_time(order_id):
	logs = OrderStatusLog.objects.filter(order_id=order_id, to_status=ORDER_STATUS_PAYED_NOT_SHIP)
	if logs.count() > 0:
		return logs[0]

	return None

########################################################################
# add_waybill: 订单添加运单号
########################################################################
@project_freight_required
def add_waybill(request):
	order_id = request.POST.get('order_id', '')
	waybill = request.POST.get('waybill', '')
	express_name = request.POST.get('express_name', '')	
	leader_name = request.POST.get('leader_name', 'aaa')
	is_update_express = request.POST.get('is_update_express',False)

	express_value = get_value_by_name(express_name)
	# 调用订单的发货处理
	if ship_order(order_id, express_value, waybill, request.freight_user.username, leader_name=leader_name):
		response = create_response(200)
		response.data.message = u'成功！'
		return response.get_response()

	response = create_response(500)
	response.data.message = u'失败！'
	return response.get_response()

