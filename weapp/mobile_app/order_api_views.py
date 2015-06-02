# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required

from core import apiview_util
from core import paginator
from core.jsonresponse import JsonResponse, create_response

from account.models import *
from webapp.modules.mall.models import *
from modules.member.models import Member,MemberHasSocialAccount
from webapp.modules.mall import module_api as mall_api
from tools.regional import views as regional_util
from tools.express.util import *
from market_tools.tools.weizoom_card.models import AccountHasWeizoomCardPermissions
from webapp.modules.mall.templatetags.mall_filter import *
from tools.express import util

order_status2text = {
	ORDER_STATUS_NOT: u'待支付',
	ORDER_STATUS_CANCEL: u'已取消',
	ORDER_STATUS_PAYED_SUCCESSED: u'已支付',
	ORDER_STATUS_PAYED_NOT_SHIP: u'待发货',
	ORDER_STATUS_PAYED_SHIPED: u'已发货',
	ORDER_STATUS_SUCCESSED: u'已完成'
}
DEFAULT_CREATE_TIME = '2000-01-01 00:00:00'
def get_order_status_text(status):
	return order_status2text[status]


def __data_format(datetime):
	if type(datetime) == unicode:
		datetime = __parse_datetime_raw_string(datetime)
	# return str(datetime.strftime('%Y-%m-%d %H:%M:%S'))
	year = datetime.strftime('%Y')
	month = datetime.strftime('%m')
	day = datetime.strftime('%d')
	month_day = '%s-%s-%s' % (year, month, day)
	hour_minute = datetime.strftime('%H:%M:%S')
	return '%s %s' % (month_day, hour_minute)

def _get_order_items(user, query, filter_value, sort_attr, query_string, count_per_page=15, cur_page=1):
	webapp_id = user.get_profile().webapp_id
	orders = Order.objects.belong_to(webapp_id)
	# # 统计订单总数
	# order_total_count = _get_orders_total_count(orders)
	###################################################
	#处理搜索
	if query:
		orders = orders.filter(order_id__icontains=query)
	###################################################
	# 处理筛选条件
	source = None
	if filter_value and (filter_value != '-1'):
		params, source_value = UserHasOrderFilter.get_filter_params_by_value(filter_value)
		orders = orders.filter(**params)
		orders = orders.filter(order_source=source_value)
	# 	if source_value == 1:
	# 		source = 'weizoom_mall'
	# 	elif source_value == 0:
	# 		source = 'mine_mall'
	# ###################################################
	# if user.is_weizoom_mall:
	# 	weizoom_mall_order_ids = WeizoomMallHasOtherMallProductOrder.get_orders_weizoom_mall_for_other_mall(webapp_id)
	# else:
	# 	weizoom_mall_order_ids = WeizoomMallHasOtherMallProductOrder.get_order_ids_for(webapp_id)

	# order_id_list = []
	# if source:
	# 	for order in orders:
	# 		if weizoom_mall_order_ids:
	# 			if order.order_id in weizoom_mall_order_ids:
	# 				if user.is_weizoom_mall:
	# 					order.come = 'weizoom_mall'
	# 				else:
	# 					order.come = 'weizoom_mall'
	# 			else:
	# 				order.come = 'mine_mall'
	# 		else:
	# 			order.come = 'mine_mall'
	# 		if source and order.come != source:
	# 			continue
	# 		order_id_list.append(order.id)

	# if order_id_list:
	# 	orders = orders.filter(id__in=order_id_list)
	###################################################
	#处理排序
	if sort_attr != 'created_at':
		orders = orders.order_by(sort_attr)
	###################################################
	#进行分页
	pageinfo, orders = paginator.paginate(orders, cur_page, count_per_page, query_string=query_string)

	#获取order对应的会员
	webapp_user_ids = set([order.webapp_user_id for order in orders])
	webappuser2member = Member.members_from_webapp_user_ids(webapp_user_ids)

	#获得order对应的商品数量
	order_ids = [order.id for order in orders]

	order2productcount = {}
	for relation in OrderHasProduct.objects.filter(order_id__in=order_ids):
		order_id = relation.order_id
		if order_id in order2productcount:
			order2productcount[order_id] = order2productcount[order_id] + 1
		else:
			order2productcount[order_id] = 1

	#构造返回的order数据
	items = []
	today = datetime.today()

	for order in  orders:
		#获取order对应的member的显示名
		member = webappuser2member.get(order.webapp_user_id, None)
		if member:
			order.buyer_name = member.username_for_html
			order.member_id = member.id
		else:
			order.buyer_name = u'未知'
			order.member_id = 0

		payment_time = None

		if order.payment_time is None:
			payment_time = ''
		elif __data_format(order.payment_time) == DEFAULT_CREATE_TIME:
			payment_time = ''
		else:
			payment_time = __data_format(order.payment_time)

		# if weizoom_mall_order_ids:
		# 	if order.order_id in weizoom_mall_order_ids:
		# 		if user.is_weizoom_mall:
		# 			order.come = 'weizoom_mall'
		# 		else:
		# 			order.come = 'weizoom_mall'
		# 	else:
		# 		order.come = 'mine_mall'
		# else:
		# 	order.come = 'mine_mall'
		# if source and order.come != source:
		# 	continue
		if order.order_source:
			order.come = 'weizoom_mall'
		else:
			order.come = 'mine_mall'

		# liupeiyu 该订单中的会员是否可点击
		# 来自本店的订单,会员不可点击
		# 或者改用户是 微众商城，会员都可点击
		if order.come is 'weizoom_mall' and user.is_weizoom_mall is False:
			order.member_id = 0

		#order_id_list.append(order.id)
		items.append({
			'id': order.id,
			'order_id': order.order_id,
			'status': get_order_status_text(order.status),
			'total_price': '%.2f' % order.final_price,
			'ship_name': order.ship_name,
			'buyer_name': order.buyer_name,
			'pay_interface_name': PAYTYPE2NAME.get(order.pay_interface_type, u''),
			'created_at': __data_format(order.created_at),
			'product_count': order2productcount.get(order.id, 0),
			'customer_message': order.customer_message,
			'payment_time': payment_time,
			'come': order.come,
			'member_id': order.member_id,
			'type': order.type,
			'reason': order.reason
		})
	return items, pageinfo

#===============================================================================
# get_order_list: 获取订单列表
#===============================================================================
def get_order_list(request):

	#处理订单号的搜索
	query = request.GET.get('query', None).strip()

	#处理订单状态筛选
	filter_value = request.GET.get('filter_value', '-1')

	#进行分页
	cur_page = int(request.GET.get('cur_page', '1'))
	count_per_page = int(request.GET.get('count', '10'))

	user = request.user
	query_string = request.META['QUERY_STRING']
	sort_attr = "-created_at"

	items, pageinfo = _get_order_items(user, query, filter_value, sort_attr, query_string, count_per_page, cur_page)
	if not items:
		response = create_response(500)
		response.errMsg = u'没有订单'
		return response.get_jsonp_response(request)
	page_json = JsonResponse()
	page_json.has_next = paginator.to_dict(pageinfo)['has_next']

	existed_pay_interfaces = mall_api.get_pay_interfaces_by_user(user)

	is_weizoom_mall_partner = AccountHasWeizoomCardPermissions.is_can_use_weizoom_card_by_owner_id(request.user.id)
	if request.user.is_weizoom_mall:
		is_weizoom_mall_partner = False
	if is_weizoom_mall_partner or request.user.is_weizoom_mall:
		is_show_source = True
	else:
		is_show_source = False
	response = create_response(200)
	response.data = {
		'orders': items,
		'page_info': paginator.to_dict(pageinfo),
		'is_show_source': is_show_source,
		'existed_pay_interfaces' : existed_pay_interfaces,
	}
	return response.get_jsonp_response(request)


#===============================================================================
# get_order: 获取订单详情
#===============================================================================
def get_order(request):
	id = request.GET.get('id')
	order = Order.objects.get(id=id)
	order_has_products = OrderHasProduct.objects.filter(order=order)

	number = 0
	cur_order = JsonResponse()
	for order_has_product in order_has_products :
		number += order_has_product.number

	cur_order.number = number
	cur_order.statu = get_order_status_text(order.status)
	cur_order.express_company_name = get_name_by_value(order.express_company_name)
	cur_order.type = order.type
	cur_order.express_number = order.express_number
	cur_order.leader_name = order.leader_name
	cur_order.integral = order.integral
	cur_order.bill_type = order.bill_type
	cur_order.bill = order.bill
	cur_order.order_id = order.order_id
	cur_order.final_price = '%.2f' % order.final_price
	cur_order.postage = '%.2f' % order.postage
	cur_order.ship_name = order.ship_name
	cur_order.ship_tel = order.ship_tel
	cur_order.area = regional_util.get_str_value_by_string_ids(order.area)
	cur_order.ship_address = order.ship_address
	cur_order.customer_message= order.customer_message
	cur_order.created_at = __data_format(order.created_at)
	cur_order.action = get_order_actions(order)
	cur_order.reason = order.reason
	#关联的优惠券
	coupon =  order.get_coupon()
	if coupon:
		cur_coupon = JsonResponse()
		cur_coupon.coupon_id = coupon.coupon_id
		cur_coupon.coupon_rule_name = coupon.coupon_rule.name
		cur_coupon.money = str(coupon.money)
		cur_order.coupon = cur_coupon
	else:
		cur_order.coupon = None



	products = mall_api.get_order_products(order.id)
	#商品
	cur_product_json = []
	for product in products:
		cur_product = JsonResponse()
		cur_product.name = product['name']
		cur_product.count = product['count']
		cur_product.total_price = product['total_price']
		cur_product.thumbnails_url = product['thumbnails_url']
		cur_product.is_deleted = product['is_deleted']
		properties = product['custom_model_properties']
		if properties:
			for product_property in properties:
				cur_product.property_name = product_property['name']
				cur_product.property_value = product_property['property_value']

		cur_product_json.append(cur_product)

	response = create_response(200)
	response.data.order = cur_order
	response.data.products = cur_product_json
	return response.get_jsonp_response(request)


########################################################################
# get_order_express_name: 获取物流快递名称
########################################################################
def get_order_express_name(request):
	express_name= util.get_express_company_json()
	response = create_response(200)
	response.data = express_name
	return response.get_jsonp_response(request)


########################################################################
# add_express_info: 增加物流信息
########################################################################
def add_express_info(request):
	order_id = request.GET['order_id']
	express_company_name = request.GET['express_company_name']
	express_number = request.GET['express_number']
	leader_name = request.GET['leader_name']
	is_update_express = request.GET['is_update_express']
	is_update_express = True if is_update_express == 'true' else False
	mall_api.ship_order(order_id, express_company_name, express_number, request.user.username, leader_name=leader_name, is_update_express=is_update_express)

	response = create_response(200)
	response.data.message=u'成功'
	return response.get_jsonp_response(request)

########################################################################
# update_order_status: 更新订单状态
########################################################################
def update_order_status(request):
	order_id = request.GET['order_id']
	action = request.GET['action']
	order = Order.objects.get(id=order_id)

	mall_api.update_order_status(request.user, action, order,request)

	response = create_response(200)
	response.data.message=u'成功'
	return response.get_jsonp_response(request)