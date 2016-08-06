# -*- coding: utf-8 -*-
from core import api_resource
from wapi.decorators import auth_required
from mall import module_api as mall_api
from mall import models
from datetime import datetime
from core import paginator
from tools.regional import views as regional_util

DEFAULT_CREATE_TIME = '2000-01-01 00:00:00'

class Orders(api_resource.ApiResource):

	app = 'open'
	resource = 'orders'



	@auth_required
	def get(args):
		"""

		"""
		user = args['user']
		found_begin_time = args['found_begin_time']
		found_end_time = args['found_end_time']
		pay_begin_time = args['pay_begin_time']
		pay_end_time = args['pay_end_time']
		order_status = args['order_status']
		order_id = args['order_id']
		cur_page = args['cur_page']
		result,pageinfo,count = Orders.get_order_items(user,order_id,cur_page,order_status,found_begin_time,found_end_time,pay_begin_time,pay_end_time)

		return result,pageinfo,count

	# get_orders_response调用
	@staticmethod
	def get_order_items(user,order_id,cur_page,order_status=None,found_begin_time=None,found_end_time=None,pay_begin_time=None,pay_end_time=None):
		if order_id != '':
			order_list = models.Order.objects.filter(order_id = order_id.strip().split('-')[0])

		else:
			webapp_id = user.get_profile().webapp_id
			order_list = models.Order.objects.belong_to(webapp_id).order_by('-id')
			if order_status!='':
				order_list = order_list.filter(status=order_status)
			# 1 下单时间，2 付款时间
			if found_begin_time !='' and found_end_time !='':
				order_list = order_list.filter(created_at__gte=found_begin_time, created_at__lt=found_end_time)
			if pay_begin_time !='' and pay_end_time !='':
				order_list = order_list.filter(payment_time__gte=pay_begin_time, payment_time__lt=pay_end_time)
		# 返回订单的数目
		order_return_count = order_list.count()

		pageinfo, order_list = paginator.paginate(order_list, cur_page, 10)


		if order_return_count==0:
			items = []
			return items,pageinfo,order_return_count
		# 获取order对应的会员
		webapp_user_ids = set([order.webapp_user_id for order in order_list])
		from modules.member.models import Member
		webappuser2member = Member.members_from_webapp_user_ids(webapp_user_ids)

		# 获得order对应的商品数量
		order_ids = [order.id for order in order_list]

		order2productcount = {}
		for relation in models.OrderHasProduct.objects.filter(order_id__in=order_ids).order_by('id'):
			order_id = relation.order_id
			if order_id in order2productcount:
				order2productcount[order_id] = order2productcount[order_id] + 1
			else:
				order2productcount[order_id] = 1
		# 构造返回的order数据
		for order in order_list:
			# 获取order对应的member的显示名
			member = webappuser2member.get(order.webapp_user_id, None)
			if member:
				order.buyer_name = member.username_for_html
				#过滤掉表情
				if '<span' in order.buyer_name:
					order.buyer_name = u'未知'

			else:
				order.buyer_name = u'未知'

			if order.payment_time is None:
				payment_time = ''
			elif datetime.strftime(order.payment_time, '%Y-%m-%d %H:%M:%S') == DEFAULT_CREATE_TIME:
				payment_time = ''
			else:
				payment_time = datetime.strftime(order.payment_time, '%Y-%m-%d %H:%M:%S')

			order.product_count = order2productcount.get(order.id, 0)
			order.payment_time = payment_time

		# 构造返回的order数据
		items = []
		for order in order_list:
			products = mall_api.get_order_products(order)
			products_result = []
			for inner_product in products:
				product_model_properties = []
				if 'custom_model_properties' in inner_product and inner_product['custom_model_properties']:
					for model in inner_product['custom_model_properties']:
						return_model = {}
						return_model['property_value'] = model['property_value']
						return_model['name'] = model['name']
						product_model_properties.append(return_model)
				product = {
					# 'total_price':inner_product['total_price'] if 'total_price' in inner_product else inner_product['price']*inner_product['count'] ,
					'goods_pic':inner_product['thumbnails_url'],
					'count':inner_product['count'],
					# 'unit_price':inner_product['price'],
					'goods_name':inner_product['name'],
					'goods_number':inner_product['user_code'],
					'custom_model_properties': product_model_properties
				}
				products_result.append(product)
			regions = regional_util.get_str_value_by_string_ids(order.area).split(" ")
			items.append({
				'order_id': order.order_id,
				'order_status': order.status,
				# 'order_price': float(
				# 	'%.2f' % order.final_price) if order.pay_interface_type != 9 or order.status == 5 else 0,
				"express_info": {
					"logistics_number": order.express_number,
					"buyer_message": order.customer_message,
					"buyer_name":order.buyer_name,
					"receiver_name": order.ship_name,
					"receiver_mobile": order.ship_tel,
					"receiver_province": regions[0] if len(regions)==3 else "未知",
					"receiver_city": regions[1] if len(regions)==3 else "未知",
					"receiver_district": regions[2] if len(regions)==3 else "未知",
					"receiver_address": order.ship_address,
					"logistics_name": order.express_company_name
				},
				'invoice_title': order.bill,
				'found_time': datetime.strftime(order.created_at, '%Y-%m-%d %H:%M:%S'),
				'num': order.product_count,
				'payment_time': order.payment_time,
				'pay_mode': order.pay_interface_type,
				'store_message': order.remark,
				'freight': '%.2f' % order.postage,
				# 'p_price': float(models.Order.get_order_has_price_number(order)) + float(order.postage) - float(
				# 	order.final_price) - float(order.weizoom_card_money),
				# 'weizoom_card_money': float('%.2f' % order.weizoom_card_money),
				# 'cash': '%.2f' % (order.final_price + order.weizoom_card_money),
				'products':products_result,
				'order_total_price': float(models.Order.get_order_has_price_number(order)) + float(order.postage)

			})
		return items,pageinfo,order_return_count



