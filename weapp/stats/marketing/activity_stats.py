# -*- coding: utf-8 -*-

import json
#from datetime import datetime
#from django.http import HttpResponseRedirect
#from django.template import RequestContext
from django.contrib.auth.decorators import login_required
#from django.shortcuts import render_to_response
#from django.db.models import F

from core import resource
#from core import paginator
from core.jsonresponse import create_response
#from weixin.mp_decorators import mp_required
from market_tools.tools.channel_qrcode.models import ChannelQrcodeSettings, ChannelQrcodeHasMember
from market_tools.tools.lottery.models import Lottery, LotteryRecord
import utils.dateutil as dateutil
from market_tools.tools.lottery.models import STATUS2TEXT as LOTTERY_STATUS2TEXT
from core.exceptionutil import unicode_full_stack
from mall.models import Order, QUALIFIED_ORDER_STATUS
from modules.member.models import MemberMarketUrl


DEFAULT_COUNT_PER_PAGE = 20

def __is_new_member(relation, existed_member_map):
	return (relation.member_id not in existed_member_map) or (relation.created_at <= existed_member_map[relation.member_id])


def get_lottery_stats(lottery_id):
	"""
	获取微信抽奖的统计数据
	"""
	#获取活动的开始时间，认为活动开始时间后来的用户为新用户
	lottery = Lottery.objects.get(id=lottery_id)
	created_at = lottery.start_at

	relations = LotteryRecord.objects.filter(lottery_id=lottery_id).order_by('created_at')

	# 获得member_id和最早created_at
	member_ids = {relation.member_id:relation.created_at for relation in relations} # id=>created_at
	#统计人数
	all_member_count = len(member_ids)
	new_added = 0

	if len(relations) > 0:
		owner_id = relations[0].owner_id
		#为了计算新增用户计算商户下的用户第一次消费记录,结果按create_at倒叙排列
		relations_member = LotteryRecord.objects.filter(owner_id=owner_id).order_by('-created_at')
		#由上一条结果，选出一个用户最早参加的活动
		relations_member_map = {relation.member_id:relation.lottery_id for relation in relations_member}

		#过滤出新用户记录的时间
		existed_member_map = {record.member_id: record.created_at for record in MemberMarketUrl.objects.filter(market_tool_name='lottery')}
		# 记录的时间小于member活动记录的时间
		new_added = len(filter(lambda x: ( relations_member_map[x] == int(lottery_id) and x in existed_member_map and created_at < existed_member_map[x]), relations_member_map.keys()))
	

	stats = [
		{
			"name": "参与会员数",
			"value": all_member_count
		}, {
			"name": "新会员数",
			"value": new_added
		}, {
			"name": "老会员数",
			"value": all_member_count-new_added
		}
	]
	return stats


def get_channel_qrcode_stats(setting_id):
	"""
	渠道扫码的分析结果
	"""
	relations = ChannelQrcodeHasMember.objects.filter(channel_qrcode=setting_id, is_new=True)
	member_num = relations.count()
	member_with_order_num = 0
	order_num = 0
	order_amount = 0.0
	repurchase_member_num = 0
	repurchase_order_num = 0
	repurchase_order_amount = 0.0
	
	for relation in relations:
		orders = Order.by_webapp_user_id(relation.member.get_webapp_user_ids).filter(status__in=QUALIFIED_ORDER_STATUS).order_by('created_at')
		order_count = orders.count()
		if order_count > 0:
			total_paid_amount = 0.0
			first_paid_amount = None
			for order in orders:
				current_paid_amount = float(order.final_price) + float(order.weizoom_card_money)
				total_paid_amount += current_paid_amount
				if first_paid_amount == None:
					first_paid_amount = current_paid_amount
					
			order_amount += total_paid_amount
			member_with_order_num += 1
			order_num += order_count
			if order_count >= 2:
				repurchase_member_num += 1
				# 复购订单统计不计第一张订单
				repurchase_order_num += order_count - 1
				repurchase_order_amount += total_paid_amount - first_paid_amount
	
	if member_num > 0:
		transform_ratio = "%.2f%%" % float(float(member_with_order_num) / float(member_num) * 100)
	else:
		transform_ratio = '0.00%'
	# 被推荐用户数
	stats = [
		{
			"name": "被推荐用户数",
			"value": member_num
		}, {
			"name": "被推荐用户下单人数",
			"value": member_with_order_num
		}, {
			"name": "被推荐用户下单单数",
			"value": order_num
		}, {
			"name": "被推荐用户下单金额",
			"value": '%.2f' % order_amount
		}, {
			"name": "推荐扫码下单转换率",
			"value": transform_ratio
		}, {
			"name": "复购用户数",
			"value": repurchase_member_num
		}, {
			"name": "复购订单数",
			"value": repurchase_order_num
		}, {
			"name": "复购总金额",
			"value": '%.2f' % repurchase_order_amount
		}
	]
	return stats


class ActivityStats(resource.Resource):
	"""
	营销活动结果分析
	"""
	app = 'stats'
	resource = 'activity_stats'

	@login_required
	def api_get(request):
		"""
		营销活动结果分析

		@param id 活动ID
		@param type 活动类型(lottery, qrcode)

		@see  channel_qrcode/api_view.py

		"""
		# 分析活动的类型: qrcode, lottery
		activity_id = request.GET.get('id')
		activity_type = request.GET.get('type', 'qrcode')

		#try:
		if activity_type == 'qrcode':
			# 处理渠道扫码的数据
			stats = get_channel_qrcode_stats(activity_id)
		elif activity_type == 'lottery':
			# 处理微信抽奖的数据
			stats = get_lottery_stats(activity_id)

		response = create_response(200)
		response.data = {
			'stats': stats,
			'type': activity_type
		}
		#except:
		#	response = create_response(500)
		#	response.errMsg = u"出现异常"
		#	response.innerErrMsg = unicode_full_stack()
		return response.get_response()
