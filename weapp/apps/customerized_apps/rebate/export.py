# -*- coding: utf-8 -*-
import rebates
import models as apps_models
from mall import models as mall_models

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

def grant_weizoom_card():
	"""
	对于符合返利条件的订单，发放对应的微众卡
	@return:
	"""
	#筛选出扫码后已完成的符合要求的订单
	target_orders = get_target_orders()

def get_target_orders(record=None):
	"""
	筛选出扫码后已完成的符合要求的订单
	@param record: 活动实例
	@return: Orders
	"""
	if record:
		is_limit_cash = record.is_limit_cash #订单金额是否为现金
		rebate_order_price = record.rebate_order_price #订单返利需满多少元
		rebate_money = record.rebate_money #返利返多少元
		weizoom_card_id_from = record.weizoom_card_id_from #发放微众卡号段
		weizoom_card_id_to = record.weizoom_card_id_to

		params = {}
		if is_limit_cash:
			params["final_price__gte"] = rebate_order_price
		else:
			params["product_price__gte"] = rebate_order_price
		params["status"] = mall_models.STATUS2TEXT[mall_models.ORDER_STATUS_SUCCESSED]
		return mall_models.Order.objects.filter(**params)

	apps_models.Rebate.objects(is_deleted=False)