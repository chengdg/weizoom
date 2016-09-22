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
WESHOP_DING_GROUP_ID = '80035247'  #发消息测试群

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
	anonymous_member_list = []
	anonymous_order_list = []
	anonymous_order_money = 0
	
	for order in orderList:
		# 获取会员信息
		member = member_models.WebAppUser.get_member_by_webapp_user_id(order.webapp_user_id)
		# 判断是否存在这样的会员
		if member:
			# print "member",member.id,member.webapp_id,order.order_id
			# 判断订单的weapp_id 与 会员的weapp_id 是否相同
			if member.webapp_id == order.webapp_id:
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
								message = u'分组失败'
								logging.info(message)
								logging.info(e)
				# 匿名用户
				else:
					# print "---",member.id
					if member.id not in anonymous_member_list:
						anonymous_member_list.append(member.id)
					anonymous_order_list.append(order.final_price)
			else:
				message = u"信息不匹配"
				logging.info(message)
		else:
			message = u"会员信息获取失败"
			logging.info(message)

	# 统计匿名购买者的总订单数与总金额
	for order_list in anonymous_order_list:
		anonymous_order_money += order_list

	print "count(kangou order money):",len(anonymous_member_list),len(anonymous_order_list),anonymous_order_money
	message = u'未关注的看购会员数: %d\n订单总数: %d\n订单总金额: %.2f' % (len(anonymous_member_list), len(anonymous_order_list), anonymous_order_money)
	logging.info(message)
	# ding_util.send_to_ding(message, WESHOP_DING_GROUP_ID)

	return 'OK {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))