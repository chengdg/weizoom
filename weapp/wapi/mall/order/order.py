# -*- coding: utf-8 -*-

from core import api_resource, paginator
from wapi.decorators import param_required

from mall import models as mall_models
from mall import module_api as mall_api
from modules.member import models as member_models
from tools.regional.views import get_str_value_by_string_ids_new

from utils import dateutil as utils_dateutil

class Order(api_resource.ApiResource):
	"""
	订单
	"""
	app = 'mall'
	resource = 'order'

	@param_required(['webapp_id', 'member_id', 'count_per_page', 'cur_page'])
	def get(args):
		"""
		获取商品详情

		@param id 商品ID
		"""
		webapp_id = args['webapp_id']
		member_id = args['member_id']
		count_per_page = int(args['count_per_page'])
		cur_page = int(args['cur_page'])

		pageinfo = None

		#获取指定时间内状态更新过的订单，不获取子订单数据
		# order_ids = mall_models.OrderOperationLog.objects.filter(
		# 	created_at__range=(start_time, end_time)
		# ).exclude(order_id__contains='^').values(order_id)
		webapp_user_ids = member_models.WebAppUser.objects.filter(member_id=member_id).values('id')


		orders = mall_models.Order.objects.filter(webapp_id=webapp_id, webapp_user_id__in=webapp_user_ids).order_by('-id')
		print 'order count:', orders.count()

		pageinfo, datas = paginator.paginate(orders, cur_page, count_per_page)
		order_ids = []
		for order in datas:
			order_ids.append(order.id)

		# product_ids = []
		order_id2relations = {}
		for relation in mall_models.OrderHasProduct.objects.filter(order__id__in=order_ids):
			key = relation.order_id
			if order_id2relations.get(key):
				order_id2relations[key].append(relation)
			else:
				order_id2relations[key] = [relation]

			# if relation.product_id not in product_ids:
			# 	product_ids.append(relation.product_id)

		#商品id和商品对象字典，为了获取
		# id2product = dict([(product.id, product) for product in mall_models.Product.objects.filter(id__in=product_ids)])
		supplier_id2name = dict([(supplier.id,supplier.name) for supplier in mall_models.Supplier.objects.all()])


		items = []
		for order in datas:
			ship_info = order.ship_address
			area = get_str_value_by_string_ids_new(order.area)
			if area:
				ship_info = '%s %s' % (area, order.ship_address)

			products = []
			for relation in order_id2relations[order.id]:
				product_id = relation.product_id
				# product = id2product[product_id]
				products.append({
					'supplier_name': supplier_id2name[product.supplier],
					'product_name': relation.product.name,
					'price': relation.price,
					'number': relation.number
				})

			items.append({
				'order_id': order.order_id,
				'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
				'coupon_money': '%.2f' % order.coupon_money,
				'integral_money': '%.2f' % order.integral_money,
				'weizoom_card_money': '%.2f' % order.weizoom_card_money,
				'final_price': '%.2f' % order.final_price,
				'ship_info': ship_info,
				'products': products
			})

		return items
