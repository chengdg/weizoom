# -*- coding: utf-8 -*-

from core import api_resource
from core import paginator, dateutil
from wapi.decorators import param_required
from django.db.models import Q

from modules.member import models as member_models
from mall import models as mall_models

SKEP_ACCOUNT2WEBAPP_ID = {
	'jingxuan': '3621',
	'xuesheng': '3807',
	'mama': '3806',
	'club': '3936'
}

class MemberBaseBuyInfo(api_resource.ApiResource):
	"""
	获取会员基本信息
	购买次数，付款金额，最后一次支付时间，客单价，推荐人，创建时间
	"""
	app = 'member'
	resource = 'member_base_buy_info'

	@param_required(['account', 'count_per_page', 'cur_page', 'is_all'])
	def get(args):
		"""
		获取商品和供应商信息

		@param account skep账号
		@param count_per_page 每页个数
		@param cur_page 第几页
		@param is_all 是否获取全部会员，如果否，则获取
		"""
		account = args['account']
		count_per_page = int(args['count_per_page'])
		cur_page = int(args['cur_page'])
		webapp_id = SKEP_ACCOUNT2WEBAPP_ID[account]
		is_all = args['is_all']
		print 'account:', account
		print 'count_per_page:', count_per_page
		print 'cur_page:', cur_page
		print 'webapp_id:', webapp_id
		print 'is_all:', is_all

		pageinfo = None
		datas = []
		members = []

		if is_all == "1":
			#获取全部会员信息
			members = member_models.Member.objects.filter(webapp_id=webapp_id, pay_times__gt=0, status__in=(0, 1)).order_by('id')
			print 'members count:', members.count()
		elif is_all == "0":
			#从mall_order_operation_log中获取支付和完成的订单id列表，然后根据订单id获取会员信息
			yesterday = dateutil.get_yesterday_str('today')
			start_time = yesterday + ' 00:00:00'
			end_time = yesterday + ' 23:59:59'

			order_ids = mall_models.OrderOperationLog.objects.filter(
				Q(action=u'支付') | Q(action__startswith="完成"), 
				created_at__range=(start_time, end_time)
			).values('order_id')
			webapp_user_ids = mall_models.Order.objects.filter(webapp_id=webapp_id, order_id__in=order_ids).values('webapp_user_id')
			if webapp_user_ids:
				#这部分数据来自字典，所以取出来的数据需要排序一下
				members = sorted(member_models.Member.members_from_webapp_user_ids(webapp_user_ids).values())

			print 'members count:', len(members)

		pageinfo, datas = paginator.paginate(members, cur_page, count_per_page)

		member_ids = []
		for member in datas:
			member_ids.append(member.id)

		member_id2referee_member_id = {}
		relations = member_models.MemberFollowRelation.objects.filter(follower_member_id__in=member_ids, is_fans=True)
		for relation in relations:
			member_id2referee_member_id[relation.follower_member_id] = relation.member_id


		items = []
		for member in datas:
			nickname = None
			try:
				#解决用户名本身就是字节码串导致不能正常转换得问题，例如ae
				nickname = member.username.decode('utf8')
			except:
				nickname = member.username

			print '---',member.id,type(member.username),member.username
			items.append({
				'id': member.id,
				'pay_money': '%.2f' % member.pay_money,
				'pay_times': member.pay_times,
				'last_pay_time': member.last_pay_time.strftime('%Y-%m-%d %H:%M:%S') if member.last_pay_time else '',
				'unit_price': '%.2f' % member.unit_price,
				'referee_member_id': member_id2referee_member_id.get(member.id, ""),
				'created_at': member.created_at.strftime('%Y-%m-%d %H:%M:%S'),
				'nickname': nickname
			})

		return {
			'items': items,
			'page_count': pageinfo.max_page
		}
