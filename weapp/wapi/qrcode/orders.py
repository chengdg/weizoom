# -*- coding: utf-8 -*-
import json
import time

from core import api_resource, paginator
from market_tools.tools.channel_qrcode.models import ChannelQrcodeSettings, ChannelQrcodeHasMember
from wapi.decorators import param_required
from modules.member.models import *
from mall.models import Order, STATUS2TEXT, OrderHasProduct, Product, ProductModel,OrderOperationLog


class QrcodeOrder(api_resource.ApiResource):
	"""
	二维码
	"""
	app = 'qrcode'
	resource = 'orders'

	@param_required(['channel_qrcode_ids'])
	def get(args):
		"""
		获取订单
		"""
		channel_qrcode_ids = json.loads(args.get('channel_qrcode_ids'), '[]')
		channel_qrcodes = ChannelQrcodeSettings.objects.filter(id__in=channel_qrcode_ids)

		member_name = args.get('member_name', None)
		channel_filter_data_args = {
			"channel_qrcode_id__in": channel_qrcode_ids
		}
		member_ids = []
		if member_name:
			members = Member.objects.filter(username_hexstr__contains=byte_to_hex(member_name))
			for member in members:
				member_ids.append(member.id)
			channel_filter_data_args["member_id__in"] = member_ids

		channel_members = ChannelQrcodeHasMember.objects.filter(**channel_filter_data_args)

		channel_qrcode_id2member_id = {}
		member_ids = []
		for member_log in channel_members:
			member_ids.append(member_log.member_id)
			if not channel_qrcode_id2member_id.has_key(member_log.channel_qrcode_id):
				channel_qrcode_id2member_id[member_log.channel_qrcode_id] = [member_log.member_id]
			else:
				channel_qrcode_id2member_id[member_log.channel_qrcode_id].append(member_log.member_id)

		member_id2created_at = {}
		for cq in channel_qrcodes:
			if cq.is_bing_member:
				member_ids.append(cq.bing_member_id)
				if not channel_qrcode_id2member_id.has_key(cq.id):
					channel_qrcode_id2member_id[cq.id] = [cq.bing_member_id]
				else:
					channel_qrcode_id2member_id[cq.id].append(cq.bing_member_id)
				member_id2created_at[cq.bing_member_id] = cq.created_at.strftime('%Y-%m-%d %H:%M:%S')



		webapp_user_ids = [webappuser.id for webappuser in WebAppUser.objects.filter(member_id__in=member_ids)]

		filter_data_args = {
			"webapp_user_id__in": webapp_user_ids,
			"origin_order_id__lte": 0
		}
		status = args.get('status', '-1')
		# #下单时间
		start_date = args.get('start_date', None)
		end_date = args.get('end_date', None)
		is_first_order = int(args.get('is_first_order', '0'))
		order_number = args.get('order_number', None)
		if status != '-1':
			filter_data_args["status"] = status
		if start_date and end_date:
			start_time = start_date + ' 00:00:00'
			end_time = end_date + ' 23:59:59'
			filter_data_args["created_at__gte"] = start_time if min(member_id2created_at.values()) <= start_time else min(member_id2created_at.values())
			filter_data_args["created_at__lte"] = end_time
		if is_first_order:
			filter_data_args["is_first_order"] = True
		if order_number:
			filter_data_args["order_id"] = order_number

		channel_orders = Order.objects.filter(**filter_data_args).order_by('-created_at')

		is_export = int(args.get('is_export', 0))
		if not is_export:
			#处理分页
			count_per_page = int(args.get('count_per_page', '20'))
			cur_page = int(args.get('cur_page', '1'))
			pageinfo, channel_orders = paginator.paginate(channel_orders, cur_page, count_per_page)


		channel_webapp_user_ids = []
		order_ids = []
		for channel in channel_orders:
			channel_webapp_user_ids.append(channel.webapp_user_id)
			order_ids.append(channel.id)



		#子单的信息
		origin_orders = Order.objects.filter(origin_order_id__in=order_ids)
		origin_order_ids = []
		order_id2origin_order_id = {}  #订单的id对应的子单id
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

		#获取订单对应的商品
		relations = OrderHasProduct.objects.filter(order_id__in=order_ids)
		order_id2product_info = {}  #订单的id对应的商品的商品的id、规格名、个数
		product_ids = []

		for r in relations:
			product_ids.append(r.product_id)
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

		id2product = {product.id: product for product in Product.objects.filter(id__in=product_ids)}
		product_id2product_model = {}  #商品的id对应商品规格
		for pm in ProductModel.objects.filter(product_id__in=id2product.keys()):
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
				"sale_price": u'%.2f' % sale_price,  #销售额
				"sale_money": sale_price,  # 销售额
				"price": final_price,  # 支付金额
				"status_text": STATUS2TEXT[channel_order.status],
				"created_at": channel_order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
				"update_at": channel_order.update_at.strftime('%Y-%m-%d %H:%M:%S'),
				"final_price": u'%.2f' % final_price
			})
		if not is_export:
			return {
				'items': orders,
				'pageinfo': paginator.to_dict(pageinfo) if pageinfo else ''
			}
		else:
			return {
				'items': orders
			}