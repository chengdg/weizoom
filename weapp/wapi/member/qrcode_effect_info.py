# -*- coding: utf-8 -*-

from core import api_resource
from core import paginator, dateutil
from wapi.decorators import param_required
from django.db.models import Q

from modules.member import models as member_models

from mall import models as mall_models
from market_tools.tools.channel_qrcode.models import ChannelQrcodeSettings,ChannelQrcodeHasMember
from mall.models import *
SKEP_ACCOUNT2WEBAPP_ID = {
	'jingxuan': '3621',
	'xuesheng': '3807',
	'mama': '3806',
	'club': '3936'
}

class QrcodeEffectInfo(api_resource.ApiResource):
	"""
	获取会员基本信息
	购买次数，付款金额，最后一次支付时间，客单价，推荐人，创建时间
	"""
	app = 'qrcode'
	resource = 'qrcode_effect_info'

	@param_required(['setting_ids'])
	def get(args):
		"""
		获取商品和供应商信息

		@param setting_id 渠道扫码二维码id

		@param is_all 是否获取全部会员，如果否，则获取
		"""
		setting_ids = args['setting_ids'].split(',')

		if setting_ids and len(setting_ids) > 0:
			relations = ChannelQrcodeHasMember.objects.filter(channel_qrcode_id__in=setting_ids)
			setting_id2member_id = {}
			setting_id2count = {}
			member_id2relation = {}
			for r in relations:

				member = member_models.Member.objects.get(id=r.member_id)
				member_id2relation[member.id]= r
				if r.channel_qrcode_id in setting_id2count:
					setting_id2count[r.channel_qrcode_id]['count'] += 1

				else:
					setting_id2count[r.channel_qrcode_id] = {}
					setting_id2count[r.channel_qrcode_id]['count'] = 1


				if r.channel_qrcode_id in setting_id2member_id:
					setting_id2member_id[r.channel_qrcode_id].append(member.id)
				else:
					setting_id2member_id[r.channel_qrcode_id] =[]
					setting_id2member_id[r.channel_qrcode_id].append(member.id)


			for sx,sy in setting_id2member_id.items():
				webapp_users = member_models.WebAppUser.objects.filter(member_id__in=sy)
				webapp_user_id2member_id = dict([(u.id, u.member_id) for u in webapp_users])
				webapp_user_ids = set(webapp_user_id2member_id.keys())

				orders = Order.by_webapp_user_id(webapp_user_ids).filter(status__in=(ORDER_STATUS_PAYED_SUCCESSED,ORDER_STATUS_PAYED_NOT_SHIP,
																					 ORDER_STATUS_PAYED_SHIPED, ORDER_STATUS_SUCCESSED))
				setting_id2count[sx]['cash'] = 0
				setting_id2count[sx]['card'] = 0

				setting_id2count[sx]['order_num'] =	0
				for order in orders:
					member_id = webapp_user_id2member_id[order.webapp_user_id]
					if member_id2relation[member_id].is_new or  member_id2relation[member_id].created_at <= order.created_at:

						setting_id2count[sx]['cash'] += order.final_price
						setting_id2count[sx]['card'] += order.weizoom_card_money
						setting_id2count[sx]['order_num'] += 1
				setting_id2count[sx]['pay_money'] = setting_id2count[sx]['card'] + setting_id2count[sx]['cash']

		items = []
		for setting_id in setting_ids:
			setting_id = int(setting_id)
			if setting_id in setting_id2count:

				items.append({
					'setting_id': setting_id,
					'pay_money': '%.2f' % setting_id2count[setting_id]['pay_money'],
					'count': setting_id2count[setting_id]['count'],
					'cash': '%.2f' % setting_id2count[setting_id]['cash'],
					'card': '%.2f' % setting_id2count[setting_id]['card'],
					'order_num': setting_id2count[setting_id]['order_num']
				})
			else:
				items.append({
					'setting_id': setting_id,
					'pay_money': '%.2f' % 0,
					'count': 0,
					'cash': '%.2f' % 0,
					'card': '%.2f' % 0,
					'order_num': 0
				})

		# if is_all == 0 :
		# pageinfo, datas = paginator.paginate(items, cur_page, count_per_page)
		return {
			'code' : 200,
			'items': items
		}

