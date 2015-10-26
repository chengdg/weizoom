# -*- coding: utf-8 -*-
from core import api_resource, dateutil
from wapi.decorators import param_required
from wapi.wapi_utils import get_webapp_id_via_username

import stats.util as stats_util
import modules.member.models as member_models

class Fans(api_resource.ApiResource):
	"""
	获取购买趋势的接口
	"""
	app = 'stats'
	resource = 'fans'

	@param_required(['un'])
	def get(args):
		"""
		为大数据系统提供粉丝相关数据

		@param un username
		@param sd 起始日期(可选参数)
		@param ed 结束日期(可选参数)
		"""
		username = args.get('un')
		start_date = args.get('sd', None)
		end_date = args.get('ed', None)

		webapp_id = get_webapp_id_via_username(username)

		today = '%s 23:59:59' % dateutil.get_yesterday_str('today')
		yesterday = '%s 00:00:00' % dateutil.get_yesterday_str('today')

		#会员总数
		total_member_count = stats_util.get_total_member_count(webapp_id)
		
		new_member_count = member_models.Member.objects.filter(
			webapp_id=webapp_id, 
			created_at__range=(yesterday, today), 
			status=member_models.SUBSCRIBED, 
			is_for_test=False
		).count()

		#关注会员
		subscribed_member_count = stats_util.get_subscribed_member_count(webapp_id)
		#直接关注会员
		self_follow_member_count = stats_util.get_self_follow_member_count(webapp_id, '2014-01-01 00:00:00', today)
		#推荐关注
		recommend_member_count = subscribed_member_count - self_follow_member_count

		#发起扫码会员和扫码新增会员
		ori_qrcode_member_count, member_from_qrcode_count = stats_util.get_ori_qrcode_member_count(webapp_id, '2014-01-01 00:00:00', today)
		#发起链接会员
		share_url_member_count = stats_util.get_share_url_member_count(webapp_id, '2014-01-01 00:00:00', today)
		#发起传播
		spread_member_count = ori_qrcode_member_count + share_url_member_count
		
		return {
			'total_member_count': total_member_count,
			'new_member_count': new_member_count,
			'recommend_member_count': recommend_member_count,
			'spread_member_count': spread_member_count
		}
