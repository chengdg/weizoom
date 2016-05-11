# -*- coding: utf-8 -*-
import rebates
import models as apps_models
from account.models import UserProfile
from mall import models as mall_models
from mall.promotion import models as promotion_models
from modules.member import models as member_models

NAV = {
	'section': u'',
	'navs': [
		{
			'name': "rebates",
			'title': "返利活动",
			'url': '/apps/rebate/rebates/',
			'need_permissions': []
		},
	]
}


########################################################################
# get_second_navs: 获得二级导航
########################################################################
def get_second_navs(request):
	if request.manager.username == 'manager':
		second_navs = [NAV]
	else:
		# webapp_module_views.get_modules_page_second_navs(request)
		second_navs = [NAV]
	
	return second_navs


def get_link_targets(request):
	pageinfo, datas = rebates.Rebates.get_datas(request)
	link_targets = []
	for data in datas:
		link_targets.append({
			"id": str(data.id),
			"name": data.name,
			"link": '/m/apps/rebate/m_rebate/?webapp_owner_id=%d&id=%s' % (request.manager.id, data.id),
			"isChecked": False,
			"created_at": data.created_at.strftime("%Y-%m-%d %H:%M:%S")
		})
	return pageinfo, link_targets

def handle_rebate_core():
	"""
	对于符合返利条件的订单，发放对应的微众卡
	@return:
	"""
	all_records = apps_models.Rebate.objects(is_deleted=False,status__ne=apps_models.STATUS_NOT_START)

	#筛选出扫码后已完成的符合要求的订单
	webapp_user_id_belong_to_member_id, id2record, member_id2records, member_id2order_ids, all_orders = get_target_orders(all_records)
	order_id2order = {o.order_id: o for o in all_orders}

	#判定每个订单属于哪个活动
	#首先找到这个会员都参与过哪些活动，然后拿这些活动的生效日期范围与下单时间一一比较
	# for order in all_orders:
	# 	created_at = order.created_at
	# 	webapp_user_id = order.webapp_user_id
	# 	belong_to_member_id = webapp_user_id_belong_to_member_id[webapp_user_id]
	# 	records = member_id2records[belong_to_member_id]
	# 	for record in records:
	# 		is_limit_first_buy = record.is_limit_first_buy
	owner_id2webapp_id = {u.manager_id: u.webapp_id for u in UserProfile.objects.filter(is_mp_registered=True, is_active=True)}
	member_id2member = {m.id: m for m in member_models.Member.objects.filter(id__in=member_id2records.keys())}
	need_grant_info = []
	for member_id, records in member_id2records.items():
		target_order_ids = member_id2order_ids[member_id]
		for record in records:
			is_limit_first_buy = record.is_limit_first_buy
			is_limit_cash = record.is_limit_cash
			rebate_order_price = record.rebate_order_price
			start_time = record.start_time
			end_time = record.end_time
			for order_id in target_order_ids:
				target_order = order_id2order[order_id]
				order_created_time = target_order.created_at
				if is_limit_first_buy and order_created_time < start_time:
					continue	#返利活动限制首单且该订单在该活动之前就产生了，不算
				if order_created_time < start_time or order_created_time > end_time:
					continue	#不在该返利活动的有效期内，不算
				if is_limit_cash and target_order.final_price < rebate_order_price:
					continue	#返利活动限制现金且该订单没有达到现金值，不算
				if not is_limit_cash and target_order.product_price < rebate_order_price:
					continue	#返利活动不限制现金但该订单的商品价格没有达到要求值，不算
				need_grant_info.append({
					"webapp_id": owner_id2webapp_id[record.owner_id],
					"weizoom_card_id_from": record.weizoom_card_id_from,
					"weizoom_card_id_to": record.weizoom_card_id_to,
					"target_member_info": member_id2member[member_id],
				})




	#根据每个活动的配置，发放对应的微众卡

def grant_card():
	pass
	# promotion_models.CardHasExchanged.objects.create(
	# 				webapp_id = webapp_id,
	# 				card_id = sorted(card_ids_list)[0],
	# 				owner_id = member_id,
	# 				owner_name = owner_name
	# 			)

def get_target_orders(records=None):
	"""
	筛选出扫码后已完成的符合要求的订单
	@param record: 活动实例
	@return: {member_id: [order1, order2,...]}
	"""

	if not records:
		records = apps_models.Rebate.objects(is_deleted=False,status__ne=apps_models.STATUS_NOT_START)

	id2record = {r.id: r for r in records}
	record_ids = id2record.keys()
	all_partis = apps_models.RebateParticipance.objects(belong_to__in=record_ids).order_by('-created_at')
	record_id2partis = {} #各活动的参与人member_id集合
	member_id2records = {} #每个会员参与的所有活动
	all_member_ids = set() #所有member_id
	for part in all_partis:
		record_id = part.belong_to
		member_id = part.member_id
		if not record_id2partis.has_key(record_id):
			record_id2partis[record_id] = [member_id]
		else:
			record_id2partis[record_id].append(member_id)
		all_member_ids.add(member_id)
		if not member_id2records.has_key(member_id):
			member_id2records[member_id] = [record_id]
		else:
			member_id2records[member_id].append(record_id)

	webapp_user_id_belong_to_member_id = {} #webapp_user_id相关联的member_id
	all_webapp_user_ids = [] #所有的webapp_user_id
	for w in member_models.WebAppUser.objects.filter(member_id__in=all_member_ids):
		member_id = w.member_id
		webapp_user_id = w.id
		webapp_user_id_belong_to_member_id[webapp_user_id] = member_id
		all_webapp_user_ids.append(webapp_user_id)

	all_orders = mall_models.Order.objects.filter(webapp_user_id__in=all_webapp_user_ids)

	member_id2order_ids = {} #会员所下的订单
	for order in all_orders:
		webapp_user_id = order.webapp_user_id
		member_id = webapp_user_id_belong_to_member_id[webapp_user_id]
		if not member_id2order_ids.has_key(member_id):
			member_id2order_ids[member_id] = [order.order_id]
		else:
			member_id2order_ids[member_id].append(order.order_id)

	return webapp_user_id_belong_to_member_id, id2record, member_id2records, member_id2order_ids, all_orders