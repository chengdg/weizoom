# -*- coding: utf-8 -*-
from core import api_resource, dateutil
from wapi.decorators import param_required
from wapi.wapi_utils import get_webapp_id_via_username
from datetime import timedelta, datetime
import json

from mall.models import *
from account.models import *
from modules.member.models import *
from mall.promotion.models import *
from eaglet.utils.resource_client import Resource
from django.conf import settings

class CostAnalysis(api_resource.ApiResource):
	"""
	卡券分统计接口
	"""
	app = 'stats'
	resource = 'cost_analysis'

	@param_required(['start_date', 'end_date'])
	def get(args):
		"""
		获取自营平台的卡券分使用情况

		"""
		start_time = time.time()
		start_date = args['start_date']
		end_date = args['end_date']

		userprofiles = UserProfile.objects.filter(webapp_type=1, is_active=True).exclude(store_name="")
		webapp_id2userprofile = {userp.webapp_id: userp for userp in userprofiles}
		webapp_ids = webapp_id2userprofile.keys()

		#获取自营平台的订单
		logging.info('start get orders')
		orders = Order.objects.filter(
			webapp_id__in=webapp_ids,
			status__in=[ORDER_STATUS_PAYED_NOT_SHIP, ORDER_STATUS_PAYED_SHIPED, ORDER_STATUS_SUCCESSED],
			origin_order_id__lte=0,
			created_at__gte=start_date,created_at__lte=end_date)
		logging.info('orders count: %d' % orders.count())

		webapp_id2order_numbers = {}
		order_numbers =[]
		webapp_id2cost = {}
		for order in orders:
			weapp_id = order.webapp_id
			if order.weizoom_card_money:
				order_numbers.append(order.order_id)
				if not webapp_id2order_numbers.has_key(weapp_id):
					webapp_id2order_numbers[weapp_id] = [order.order_id]
				else:
					webapp_id2order_numbers[weapp_id].append(order.order_id)
			coupon_count = 1 if order.coupon_id else 0
			sale_money = order.weizoom_card_money + order.final_price + order.coupon_money + order.integral_money  #销售额
			loss_money = sale_money - order.total_purchase_price
			kangou_money = order.final_price if order.pay_interface_type == PAY_INTERFACE_KANGOU else 0
			best_money = order.final_price if order.pay_interface_type == PAY_INTERFACE_BEST_PAY else 0
			ali_money = order.final_price if order.pay_interface_type == PAY_INTERFACE_ALIPAY else 0
			weixin_money = order.final_price if order.pay_interface_type == PAY_INTERFACE_WEIXIN_PAY else 0


			if not webapp_id2cost.has_key(weapp_id):
				webapp_id2cost[order.webapp_id] = {
					"order_count": 1,
					"coupon_money": order.coupon_money,
					"coupon_count": coupon_count,
					"integral_money": order.integral_money,
					"integral": order.integral,
					"weizoom_card_money": order.weizoom_card_money,
					"final_price": order.final_price,
					"total_purchase_price": order.total_purchase_price,
					"loss_money": loss_money,
					"sale_money": sale_money,
					"kangou_money": kangou_money,
					"best_money": best_money,
					"ali_money": ali_money,
					"weixin_money": weixin_money
				}
			else:
				cur_cost = webapp_id2cost[order.webapp_id]
				cur_cost["order_count"] += 1
				cur_cost["coupon_money"] += order.coupon_money
				cur_cost["coupon_count"] += coupon_count
				cur_cost["integral_money"] += order.integral_money
				cur_cost["integral"] += order.integral
				cur_cost["weizoom_card_money"] += order.weizoom_card_money
				cur_cost["final_price"] += order.final_price
				cur_cost["total_purchase_price"] += order.total_purchase_price
				cur_cost["loss_money"] += loss_money
				cur_cost["sale_money"] += sale_money
				cur_cost["kangou_money"] += kangou_money
				cur_cost["best_money"] += best_money
				cur_cost["ali_money"] += ali_money
				cur_cost["weixin_money"] += weixin_money


		webapp_id2order_card_info = {}
		for weapp_id,order_numbers in webapp_id2order_numbers.items():
			#使用微众卡的接口
			resp = Resource.use('card_apiserver').post({
				'resource': 'card.order_use_card_type',
				'data': {"order_ids": ','.join(order_numbers)}
			})
			order_cards = []
			if resp:
				order_cards = resp['data']
				for order_card in order_cards:
					if order_card["order_id"] in order_numbers:
						if not webapp_id2order_card_info.has_key(weapp_id):
							webapp_id2order_card_info[weapp_id] = {
								"sale": order_card["sale"],
								"internal": order_card["internal"],
								"rebate": order_card["rebate"],
								"unknown": order_card["unknown"]
							}
						else:
							order_card_info = webapp_id2order_card_info[weapp_id]
							order_card_info["sale"] += order_card["sale"]
							order_card_info["internal"] += order_card["internal"]
							order_card_info["rebate"] += order_card["rebate"]
							order_card_info["unknown"] += order_card["unknown"]

		owner_ids = []
		for w_id in webapp_ids:
			owner_ids.append(webapp_id2userprofile[w_id].user_id)

		#获取自营平台的优惠券规则
		coupon_rules = CouponRule.objects.filter(owner_id__in=owner_ids,created_at__gte=start_date,created_at__lte=end_date)
		logging.info('coupon_rules count: %d', coupon_rules.count())
		owner_id2coupon_info ={}
		for cr in coupon_rules:
			if not owner_id2coupon_info.has_key(cr.owner_id):
				owner_id2coupon_info[cr.owner_id] = {
					"count": cr.count,
					"money": cr.count*cr.money,
					"get_count": cr.get_count,
					"get_money": cr.get_count*cr.money
				}
			else:
				coupon_info = owner_id2coupon_info[cr.owner_id]
				coupon_info["count"] += cr.count
				coupon_info["money"] += cr.count*cr.money
				coupon_info["get_count"] += cr.get_count
				coupon_info["get_money"] += cr.get_count*cr.money

		logging.info('start get member_integral_logs')
		member_integral_logs = MemberIntegralLog.objects.filter(
			created_at__range=(start_date, end_date),
			integral_count__gt=0).exclude(event_type__in=[RETURN_BY_SYSTEM,RETURN_BY_CANCEl_ORDER,MANAGER_MODIFY,MANAGER_MODIFY_ADD,MANAGER_MODIFY_REDUCT])

		# 每个会员新增的积分数
		member_set = set()
		member_id2integral = {}
		for log in  member_integral_logs:
			member_set.add(log.member_id)
			if not member_id2integral.has_key(log.member_id):
				member_id2integral[log.member_id] = log.integral_count
			else:
				member_id2integral[log.member_id] += log.integral_count

		#每个自营平台的新增积分数
		webapp_id2integral = {}
		members = Member.objects.filter(id__in=member_set, webapp_id__in=webapp_ids)
		for member in members:
			if not webapp_id2integral.has_key(member.webapp_id):
				webapp_id2integral[member.webapp_id] = 0
			webapp_id2integral[member.webapp_id] += member_id2integral.get(member.id,0)

		logging.info('get member_integral_logs end')

		cost_list = []
		for webapp_id in webapp_ids:
			cost = webapp_id2cost.get(webapp_id,None)
			userprofile = webapp_id2userprofile[webapp_id]
			user_id = userprofile.user_id

			coupon = owner_id2coupon_info.get(user_id,None)
			order_card_info = webapp_id2order_card_info.get(webapp_id,None)
			cost_list.append({
				"store_name": userprofile.store_name,
				"order_count": cost["order_count"] if cost else 0,
				"coupon_money": u"%.2f" % (cost["coupon_money"] if cost else 0),
				"coupon_count": cost["coupon_count"] if cost else 0,
				"integral_money": u"%.2f" % (cost["integral_money"] if cost else 0),
				"integral": cost["integral"] if cost else 0,
				"weizoom_card_money": u"%.2f" % (cost["weizoom_card_money"] if cost else 0),
				"sale": u"%.2f" % (order_card_info["sale"] if order_card_info else 0),
				"internal": u"%.2f" % (order_card_info["internal"] if order_card_info else 0),
				"rebate": u"%.2f" % (order_card_info["rebate"] if order_card_info else 0),
				"unknown": u"%.2f" % (order_card_info["unknown"] if order_card_info else 0),
				"final_price": u"%.2f" % (cost["final_price"] if cost else 0),
				"total_purchase_price": u"%.2f" % (cost["total_purchase_price"] if cost else 0),
				"loss_money": u"%.2f" % (cost["loss_money"] if cost else 0),
				"sale_money": u"%.2f" % (cost["sale_money"] if cost else 0),
				"publish_count": coupon["count"] if coupon else 0,
				"publish_money": u"%.2f" % (coupon["money"] if coupon else 0),
				"get_count": coupon["get_count"] if coupon else 0,
				"get_money": u"%.2f" % (coupon["get_money"] if coupon else 0),
				"increase_integral": webapp_id2integral.get(webapp_id, 0),
				"kangou_money": u"%.2f" % (cost["kangou_money"] if cost else 0),
				"best_money": u"%.2f" % (cost["best_money"] if cost else 0),
				"ali_money": u"%.2f" % (cost["ali_money"] if cost else 0),
				"weixin_money": u"%.2f" % (cost["weixin_money"] if cost else 0)
			})
		end_time = time.time()
		print end_time - start_time, "pppppppppp"

		return cost_list
