# -*- coding: utf-8 -*-

from core import api_resource
from wapi.decorators import param_required
#from wapi.wapi_utils import create_json_response

#from mall import models as mall_models
from mall import module_api as mall_api
from modules.member import models as member_models

from utils import dateutil as utils_dateutil

from mall.promotion import models as promotion_models

from dummy_utils import DummyRequest, DummyUserProfile, DummyModel

class Orders(api_resource.ApiResource):
	"""
	订单列表
	"""
	app = 'mall'
	resource = 'orders'

	@staticmethod
	def to_dict(order):
		data = {
			'id': order.id,
			'buyer_name': order.buyer_name,
			'express_company_name': order.express_company_name,
			'coupon_money': order.coupon_money,
			'integral': order.integral,
			'coupon_id': order.coupon_id,
			'ship_address': order.ship_address,
			'member_grade': order.member_grade,
			'area': order.area,
			'webapp_source_id': order.webapp_source_id,
			'ship_name': order.ship_name,
			'leader_name': order.leader_name,
			'product_price': order.product_price,
			'member_grade_discount': order.member_grade_discount,
			'supplier': order.supplier,
			'member_grade_discounted_money': order.member_grade_discounted_money,
			'type': order.type,
			'integral_each_yuan': order.integral_each_yuan,
			'final_price': order.final_price,
			'status': order.status,
			'postage': order.postage,
			'weizoom_card_money': order.weizoom_card_money,
			'webapp_user_id': order.webapp_user_id,
			'order_source': order.order_source,
			'buyer_tel': order.buyer_tel,
			'pay_interface_type': order.pay_interface_type,
			'order_id': order.order_id,
			'bill_type': order.bill_type,
			'payment_time': utils_dateutil.datetime2string(order.payment_time),
			'reason': order.reason,
			'integral_money': order.integral_money,
			'ship_tel': order.ship_tel,
			'origin_order_id': order.origin_order_id,
			'customer_message': order.customer_message,
			'webapp_id': order.webapp_id,
			'remark': order.remark,
			'promotion_saved_money': order.promotion_saved_money,
			'express_number': order.express_number,
			'bill': order.bill,
			'update_at': utils_dateutil.datetime2string(order.update_at),
			'edit_money': order.edit_money,
			'created_at': utils_dateutil.datetime2string(order.created_at),
		}
		return data

	@param_required(['wuid'])
	def get(args):
		"""
		获取订单列表

		"""
		request = DummyRequest()
		request.webapp_user = DummyUserProfile()
		request.webapp_user.id = args['wuid']
		request.member = DummyModel()
		request.member.id = args['member_id']
		request.webapp_owner_info = DummyModel()

		if args.get('red_envelop_rule_id'):
			request.webapp_owner_info.red_envelope = promotion_models.RedEnvelopeRule.objects.get(id=args.get('red_envelop_rule_id') )
		else:
			request.webapp_owner_info.red_envelope = promotion_models.RedEnvelopeRule()

		#request.webapp_owner_info.red_envelope = args['red_envelop']
		request.webapp_owner_id = args['woid']
		orders = mall_api.get_orders(request)
		print("orders: {}".format(orders))
		result = []
		for order in orders:
			result.append(Orders.to_dict(order))
		return result
