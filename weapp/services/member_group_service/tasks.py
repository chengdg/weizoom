#coding:utf8
"""
@package services.virtual_product_service.tasks
virtual_product_service 的Celery task实现

"""
from __future__ import absolute_import
from datetime import datetime

from celery import task

from mall.promotion import models as promotion_models
from mall import models as mall_models
from modules.member import models as member_models
from utils import ding_util
from mall import module_api
import logging

ORDER_STATUS_PAYED_NOT_SHIP = 3  # 待发货：已付款，未发货
ORDER_STATUS_PAYED_SHIPED = 4  # 已发货：已付款，已发货
ORDER_STATUS_SUCCESSED = 5  # 已完成：自下单10日后自动置为已完成状态

ORDER_STATUS_TYPE = [ORDER_STATUS_PAYED_NOT_SHIP,ORDER_STATUS_PAYED_SHIPED,ORDER_STATUS_SUCCESSED]

# WESHOP_DING_GROUP_ID = '105507196'  #微众商城FT团队钉钉id
# WESHOP_DING_GROUP_ID = '80035247'  #发消息测试群

@task
def deliver_member_group(request, args):
	"""
	每隔一天自动执行一次

	@param request 无用，为了兼容
	@param args dict类型
	"""
	logging.info('start service member_group {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

	# 获取所有待发货、已发货、已完成订单
	orderList = mall_models.Order.objects.filter(
			status__in=ORDER_STATUS_TYPE,
			pay_interface_type=12,
			origin_order_id__lt=0
		)
	# print "orderList",len(orderList)
	cancel_subscribed_members = []
	cancel_subscribed_orders = 0
	cancel_subscribed_price = 0
	not_subscribed_members = []
	not_subscribed_orders = 0
	not_subscribed_price = 0
	
	for order in orderList:
		# 获取会员信息
		member = member_models.WebAppUser.get_member_by_webapp_user_id(order.webapp_user_id)
		# print "member",member.id,member.webapp_id,order.order_id
		# 判断是否存在这样的会员
		if member:
			# print "member",member.id,member.webapp_id,order.order_id
			# 判断是否关注
			if member.is_subscribed == True:
				# 获取分组是 看购会员分组 的id,返回list 
				member_tag_id = member_models.MemberTag.objects.filter(webapp_id=member.webapp_id, name="看购会员分组")
				# 遍历list
				for member_tag in member_tag_id:
					# 查询是否已经加入看购分组
					kangou_records = member_models.MemberHasTag.objects.filter(member_id=member.id, member_tag_id=member_tag.id)
					if kangou_records.count() == 0:
						try:
							# 添加看购分组记录
							member_models.MemberHasTag.objects.create(member_id=member.id, member_tag_id=member_tag.id)
						except Exception, e:
							message = u'加入看购分组失败，会员id: %d分组id: %d' % (member.id, member_tag.id)
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
			message = u"会员信息获取失败,订单id: %d\n" % (order.order_id)
			logging.info(message)

	# print "count cancel_subscribed (kangou order money):",len(cancel_subscribed_members), cancel_subscribed_orders, cancel_subscribed_price
	# print "count not_subscribed (kangou order money):",len(not_subscribed_members), not_subscribed_orders, not_subscribed_price
	message_cancel = u'已取消关注的看购会员数: %d\n订单总数: %d\n订单总金额: %.2f' % (len(cancel_subscribed_members), cancel_subscribed_orders, cancel_subscribed_price)
	message_not = u'从未关注的看购会员数: %d\n订单总数: %d\n订单总金额: %.2f' % (len(not_subscribed_members), not_subscribed_orders, not_subscribed_price)
	logging.info(message_cancel)
	logging.info(message_not)
	# ding_util.send_to_ding(message, WESHOP_DING_GROUP_ID)

	return 'OK {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))