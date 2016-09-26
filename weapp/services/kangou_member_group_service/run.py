# -*- coding: utf-8 -*-

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weapp.settings")

from django.core.management import execute_from_command_line
execute_from_command_line(sys.argv)

from mall import models as mall_models
from modules.member import models as member_models
import logging

ORDER_STATUS_PAYED_NOT_SHIP = 3  # 待发货：已付款，未发货
ORDER_STATUS_PAYED_SHIPED = 4  # 已发货：已付款，已发货
ORDER_STATUS_SUCCESSED = 5  # 已完成：自下单10日后自动置为已完成状态
ORDER_STATUS_TYPE = [ORDER_STATUS_PAYED_NOT_SHIP,ORDER_STATUS_PAYED_SHIPED,ORDER_STATUS_SUCCESSED]

KANGOU_TAG_ID = 3400  #看购会员分组id

def group_kangou_member():
	member_has_tag_list = member_models.MemberHasTag.objects.filter(member_tag_id=KANGOU_TAG_ID)
	kangou_members = [member_has_tag.member_id for member_has_tag in member_has_tag_list]
	logging.info(u"当前看购分组内会员个数：%d" % len(kangou_members))
	added_number = 0

	# 获取所有待发货、已发货、已完成订单
	orderList = mall_models.Order.objects.filter(
			status__in=ORDER_STATUS_TYPE,
			pay_interface_type=12,
			origin_order_id__lt=0
		)
	cancel_subscribed_members = []
	cancel_subscribed_orders = 0
	cancel_subscribed_price = 0
	not_subscribed_members = []
	not_subscribed_orders = 0
	not_subscribed_price = 0
	
	for order in orderList:
		# 获取会员信息
		member = member_models.WebAppUser.get_member_by_webapp_user_id(order.webapp_user_id)
		# 判断是否存在这样的会员
		if member:
			# 判断是否关注
			if member.is_subscribed == True and member.id not in kangou_members:
				try:
					# 添加看购分组记录
					member_models.MemberHasTag.objects.create(member_id=member.id, member_tag_id=KANGOU_TAG_ID)
					kangou_members.append(member.id)
					added_number += 1
				except Exception, e:
					message = u'加入看购分组失败，会员id: %d分组id: %d' % (member.id, KANGOU_TAG_ID)
					logging.error(message)
					logging.error(e)
			# 匿名用户
			else:
				# 关注后取消了的用户
				if member.status == 1:
					# 统计未关注的会员数
					if member.id not in cancel_subscribed_members:
						cancel_subscribed_members.append(member.id)
					# 统计订单总数
					cancel_subscribed_orders += 1
					# 统计订单总金额
					cancel_subscribed_price += order.final_price
				# 从未关注的用户
				else:
					# 统计未关注的会员数
					if member.id not in not_subscribed_members:
						not_subscribed_members.append(member.id)
					# 统计订单总数
					not_subscribed_orders += 1
					# 统计订单总金额
					not_subscribed_price += order.final_price
		else:
			message = u"会员信息获取失败,订单id: %d" % (order.order_id)
			logging.info(message)

	message_cancel = u'已取消关注的看购会员数: %d，订单总数: %d，订单总金额: %.2f' % (len(cancel_subscribed_members), cancel_subscribed_orders, cancel_subscribed_price)
	message_not = u'从未关注的看购会员数: %d，订单总数: %d，订单总金额: %.2f' % (len(not_subscribed_members), not_subscribed_orders, not_subscribed_price)
	logging.info(message_cancel)
	logging.info(message_not)
	logging.info(u"看购分组新增会员个数：%d" % added_number)


group_kangou_member()