# -*- coding: utf-8 -*-
import json

from core import api_resource, paginator
from mall.models import Order, ORDER_STATUS_CANCEL, ORDER_STATUS_REFUNDING, \
	ORDER_STATUS_REFUNDED, ORDER_STATUS_GROUP_REFUNDING, ORDER_STATUS_GROUP_REFUNDED
from mall.promotion.models import CouponRule, Coupon, COUPON_STATUS_USED
from market_tools.tools.channel_qrcode.models import ChannelQrcodeSettings, ChannelQrcodeHasMember
from wapi.decorators import param_required
from modules.member.models import *
from utils.string_util import hex_to_byte, byte_to_hex

class CouponOrder(api_resource.ApiResource):
	"""
	优惠券统计
	"""
	app = 'qrcode'
	resource = 'coupon_order'

	@param_required(['coupon_rule_ids'])
	def get(args):
		"""
		优惠券统计
		"""
		coupon_rule_ids = json.loads(args.get('coupon_rule_ids'))
		# coupon_rule_ids = [int(coupon_rule_id) for coupon_rule_id in coupon_rule_ids]
		coupon_rules = CouponRule.objects.filter(id__in=coupon_rule_ids)

		# 处理分页
		count_per_page = int(args.get('count_per_page', '20'))
		cur_page = int(args.get('cur_page', '1'))
		pageinfo, coupon_rules = paginator.paginate(coupon_rules, cur_page, count_per_page)

		coupon_rule_ids = [coupon_rule.id for coupon_rule in coupon_rules]
		coupon_rule_id2coupon_ids = {}
		coupon_ids = []
		for c in Coupon.objects.filter(coupon_rule_id__in=coupon_rule_ids, status=COUPON_STATUS_USED):
			coupon_ids.append(c.id)
			if not coupon_rule_id2coupon_ids.has_key(c.coupon_rule_id):
				coupon_rule_id2coupon_ids[c.coupon_rule_id] = [c.id]
			else:
				coupon_rule_id2coupon_ids[c.coupon_rule_id].append(c.id)


		coupon_id2order = {order.coupon_id: order for order in Order.objects.filter(coupon_id__in=coupon_ids,origin_order_id__lte=0)}

		coupon_infos = []
		for coupon_rule in coupon_rules:
			order_count = 0
			price = 0
			first_order_count = 0
			coupon_ids = coupon_rule_id2coupon_ids.get(coupon_rule.id)
			for coupon_id in coupon_ids:
				order = coupon_id2order[coupon_id]
				order_count += 1
				if order.status not in [ORDER_STATUS_CANCEL, ORDER_STATUS_REFUNDING, ORDER_STATUS_REFUNDED, ORDER_STATUS_GROUP_REFUNDING, ORDER_STATUS_GROUP_REFUNDED]:
					price += order.final_price
				if order.is_first_order:
					first_order_count += 1

			coupon_infos.append({
				"id": coupon_rule.id,
				"get_person_count": coupon_rule.get_person_count,
				"order_count": order_count,
				"first_order_count": first_order_count,
				"price": u'%.2f' % price
			})



		return {
			'items': coupon_infos,
			'pageinfo': paginator.to_dict(pageinfo) if pageinfo else ''
		}
