# -*- coding: utf-8 -*-
import json
import time

from core import api_resource, paginator
from market_tools.tools.channel_qrcode.models import ChannelQrcodeSettings, ChannelQrcodeHasMember
from wapi.decorators import param_required
from modules.member.models import *
from mall.models import Order, ORDER_STATUS_SUCCESSED, ORDER_STATUS_REFUNDED, STATUS2TEXT, OrderHasProduct, Product, ProductModel,OrderOperationLog, \
	ProductCategory, CategoryHasProduct
from core import dateutil

class QrcodeBalance(api_resource.ApiResource):
	"""
	二维码
	"""
	app = 'qrcode'
	resource = 'balance_member'

	@param_required(['channel_qrcode_ids'])
	def get(args):
		"""
		获取结算的数据
		现金总收入：订单提成+首单提成
		订单提成：（店铺总销售额-店铺退款金额）*？%
		首单提成：已完成的首次下单个数*？
		店铺总销售额：已完成订单的总额
		店铺退款金额：该订单上次已结算过，但本期次订单发生了退款，这类的退款订单金额
		"""

		channel_qrcode_ids = json.loads(args.get('channel_qrcode_ids'), '[]')
		channel_qrcodes = ChannelQrcodeSettings.objects.filter(id__in=channel_qrcode_ids).order_by('created_at')
		if channel_qrcodes.count() > 0:
			created_at = channel_qrcodes.first().created_at.strftime("%Y-%m-%d %H:%M:%S")
		else:
			created_at = dateutil.get_today()

		member_logs = ChannelQrcodeHasMember.objects.filter(channel_qrcode_id__in=channel_qrcode_ids)
		member_ids = [member_log.member_id for member_log in member_logs]
		webappusers = WebAppUser.objects.filter(member_id__in=member_ids)
		webapp_user_ids = [webappuser.id for webappuser in webappusers]

		filter_data_args = {
			"webapp_user_id__in": webapp_user_ids,
			"origin_order_id__lte": 0,
			"created_at__gte": created_at
		}
		channel_filter_data_args = {
			"channel_qrcode_id__in": channel_qrcode_ids
		}

		channel_members = ChannelQrcodeHasMember.objects.filter(**channel_filter_data_args)

		channel_qrcode_id2member_id = {}
		member_ids = []
		for member_log in channel_members:
			member_ids.append(member_log.member_id)
			if not channel_qrcode_id2member_id.has_key(member_log.channel_qrcode_id):
				channel_qrcode_id2member_id[member_log.channel_qrcode_id] = [member_log.member_id]
			else:
				channel_qrcode_id2member_id[member_log.channel_qrcode_id].append(member_log.member_id)

		webapp_user_ids = [webappuser.id for webappuser in WebAppUser.objects.filter(member_id__in=member_ids)]

		# 某个固定的商品分组
		product_category = ProductCategory.objects.filter(id=5)
		product_ids = []
		if product_category.count() > 0:
			category_products = CategoryHasProduct.objects.filter(category_id=product_category[0].id)
			product_ids = [chp.product_id for chp in category_products]

		# 获取商品对应的订单
		relations = OrderHasProduct.objects.filter(product_id__in=product_ids)

		order_id2product_info = {}

		order_ids = []
		for r in relations:
			order_ids.append(r.order_id)
			if not order_id2product_info.has_key(r.order_id):
				order_id2product_info[r.order_id] = [{
					"product_id": r.product_id,  #商品的id
					"product_model_name": r.product_model_name,  #商品规格名
					"number": r.number  #商品的个数
				}]
			else:
				order_id2product_info[r.order_id].append({
					"product_id": r.product_id,
					"product_model_name": r.product_model_name,
					"number": r.number
				})

		products = Product.objects.filter(id__in=product_ids)
		id2product = {product.id: product for product in products}
		product_id2product_model = {}  # 商品的id对应商品规格
		product_models = ProductModel.objects.filter(product_id__in=id2product.keys())
		for pm in product_models:
			product_id_model_name = u'%s_%s' % (pm.product_id, pm.name)
			product_id2product_model[product_id_model_name] = pm

		order_id2products = {}
		for order_id, product_infos in order_id2product_info.items():
			products = []
			for product_info in product_infos:
				product_id_model_name = u'%s_%s' % (product_info["product_id"], product_info["product_model_name"])
				product_model = product_id2product_model.get(product_id_model_name)
				product = id2product.get(product_info["product_id"])
				products.append({
					"thumbnails_url": product.thumbnails_url if product else u'',
					"name": product.name if product else u'',
					"price": u'%.2f' % product_model.price if product_model else 0,
					"number": product_info["number"]
				})
			order_id2products[order_id] = products

		channel_orders = Order.objects.filter(webapp_user_id__in=webapp_user_ids,id__in=order_ids, origin_order_id__lte=0,created_at__gte=created_at)
		channel_webapp_user_ids = []
		for channel in channel_orders:
			channel_webapp_user_ids.append(channel.webapp_user_id)


		# 子单的信息
		origin_orders = Order.objects.filter(origin_order_id__in=order_ids)
		origin_order_ids = []
		order_id2origin_order_id = {}  # 订单的id对应的子单id
		for origin_order in origin_orders:
			origin_order_ids.append(origin_order.id)
			if not order_id2origin_order_id.has_key(origin_order.origin_order_id):
				order_id2origin_order_id[origin_order.origin_order_id] = [origin_order.id]
			else:
				order_id2origin_order_id[origin_order.origin_order_id].append(origin_order.id)

		weapp_user_id2member_id = {wu.id: wu.member_id for wu in WebAppUser.objects.filter(id__in=channel_webapp_user_ids)}
		member_id2relations = {m.id: m for m in Member.objects.filter(id__in=weapp_user_id2member_id.values())}

		order_ids = set(origin_order_ids) | set(order_ids)

		for or_id in order_ids:
			if not order_id2origin_order_id.has_key(or_id):
				order_id2origin_order_id[or_id] = [or_id]


		orders = []
		for channel_order in channel_orders:
			member_id = weapp_user_id2member_id.get(channel_order.webapp_user_id)
			member = None
			if member_id:
				member = member_id2relations.get(member_id)
			order_ids = order_id2origin_order_id.get(channel_order.id, [])
			products = []
			for o_id in order_ids:
				order_products = order_id2products.get(o_id, [])
				for order_product in order_products:
					products.append(order_product)
			sale_price = channel_order.final_price + channel_order.coupon_money + channel_order.integral_money + channel_order.weizoom_card_money + channel_order.promotion_saved_money + channel_order.edit_money
			final_price = channel_order.final_price
			if member:
				try:
					name = member.username.decode('utf8')
				except:
					name = member.username_hexstr
			else:
				name = u'未知'
			channel_qrcode_id = 0
			for qrcode_id, member_ids in channel_qrcode_id2member_id.items():
				if member_id in member_ids:
					channel_qrcode_id = qrcode_id
			orders.append({
				"channel_qrcode_id": channel_qrcode_id,
				"order_id": channel_order.id,
				"order_number": channel_order.order_id,
				"is_first_order": channel_order.is_first_order,
				"member_name": member.username_for_html if member else u'未知',
				"member_name_for_export": name,
				"products": products,
				"sale_price": u'%.2f' % sale_price,  # 销售额
				"sale_money": sale_price,  # 销售额
				"price": final_price,  # 支付金额
				"balance_money": 50,
				"balance_price": u'￥%.2f' % 50,
				"status_text": STATUS2TEXT[channel_order.status],
				"created_at": channel_order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
				"update_at": channel_order.update_at.strftime('%Y-%m-%d %H:%M:%S'),
				"final_price": u'%.2f' % final_price
			})




		start = time.time()
		# channel_qrcode_ids = json.loads(args.get('channel_qrcode_ids'))
		# balance_time_from = args.get('balance_time_from','2016-06-24 00:00:00')
		# channel_qrcodes = ChannelQrcodeSettings.objects.filter(id__in=channel_qrcode_ids).order_by('created_at')
		# if channel_qrcodes.count() > 0:
		# 	created_at = channel_qrcodes.first().created_at.strftime("%Y-%m-%d %H:%M:%S")
		# else:
		# 	created_at = dateutil.get_today()
		#
		# member_ids = [member_log.member_id for member_log in ChannelQrcodeHasMember.objects.filter(channel_qrcode_id__in=channel_qrcode_ids)]
		# webapp_user_ids = [webappuser.id for webappuser in WebAppUser.objects.filter(member_id__in=member_ids)]
		#
		# filter_data_args = {
		# 	"webapp_user_id__in": webapp_user_ids,
		# 	"origin_order_id__lte": 0,
		# 	"created_at__gte": created_at
		# }
		#
		# cur_start_date = args.get('start_date', None)
		# cur_end_date = args.get('end_date', None)
		# filter_data_args["status__in"] = [ORDER_STATUS_SUCCESSED, ORDER_STATUS_REFUNDED]
		# channel_orders = Order.objects.filter(**filter_data_args).order_by('-created_at')
		# order_numbers = [co.order_id for co in channel_orders]
		# order_log_numbers = []
		# order_number2finished_at = {}
		# #处理筛选
		# if cur_start_date and cur_end_date:
		# 	if cur_start_date < created_at:
		# 		cur_start_date = created_at
		# 	orderoperationlogs = OrderOperationLog.objects.filter(
		# 		order_id__in=order_numbers,
		# 		action__in=[u'完成', u'退款完成'],
		# 		created_at__gte=cur_start_date,
		# 		created_at__lte=cur_end_date
		# 	)
		#
		# 	for op in orderoperationlogs:
		# 		if op.created_at.strftime("%Y-%m-%d %H:%M:%S") >= cur_start_date and op.created_at.strftime("%Y-%m-%d %H:%M:%S") <= cur_end_date:
		# 			order_log_numbers.append(op.order_id)
		# 		order_number2finished_at[op.order_id] = op.created_at
		#
		# orders = []
		# for channel_order in channel_orders:
		# 	if channel_order.order_id in order_log_numbers:
		# 		sale_price = channel_order.final_price + channel_order.coupon_money + channel_order.integral_money + channel_order.weizoom_card_money + channel_order.promotion_saved_money + channel_order.edit_money
		# 		final_price = channel_order.final_price
		# 		orders.append({
		# 			"order_id": channel_order.id,
		# 			"order_number": channel_order.order_id,
		# 			"is_first_order": channel_order.is_first_order,
		# 			"status_text": STATUS2TEXT[channel_order.status],
		# 			"sale_price": sale_price,  #销售额
		# 			"finished_at": order_number2finished_at.get(channel_order.order_id, channel_order.update_at).strftime('%Y-%m-%d %H:%M:%S'),
		# 			"final_price": final_price,
		# 			"created_at": channel_order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
		# 		})
		end = time.time()
		print end - start, "pppppppppp"

		return {
			'items': orders
		}
