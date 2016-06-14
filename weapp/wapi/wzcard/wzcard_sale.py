# -*- coding: utf-8 -*-

from core import api_resource, paginator
from wapi.decorators import param_required

from mall import module_api as mall_api
from mall import models as mall_models
from mall.promotion import models as promotion_models
from modules.member import models as member_models

class WzcardSale(api_resource.ApiResource):
	"""
	订单
	"""
	app = 'wzcard'
	resource = 'wzcard_sale'

	@param_required([])
	def get(args):
		"""
		获取商品详情

		@param id 商品ID
		"""
		start_date = args.get('start_date', None)
		end_date = args.get('end_date', None)
		count_per_page = int(args.get('count_per_page', '0'))
		cur_page = int(args.get('cur_page', '0'))
		is_all = int(args.get('is_all', '0'))

		pageinfo = None
		wzcards = promotion_models.VirtualProductHasCode.objects.filter(virtual_product__product__type='wzcard')
		if start_date and end_date:
			start_time = start_date + ' 00:00:00'
			end_time = end_date + ' 23:59:59'
			wzcards = wzcards.filter(get_time__range=(start_time, end_time))
		if is_all != 1:
			pageinfo, wzcards = paginator.paginate(wzcards, cur_page, count_per_page)

		member_ids = [w.member_id for w in wzcards]
		members = member_models.Member.objects.filter(id__in=member_ids)
		member_id2name = {}
		for member in members:
			member_id2name[str(member.id)] = member.username_for_html

		items = []
		for wzcard in wzcards:
			items.append({
				'order_id': wzcard.order_id,
				'get_time': wzcard.get_time.strftime('%Y-%m-%d %H:%M:%S'),
				'code': wzcard.code,
				'member_id': wzcard.member_id,
				'member_name': member_id2name[wzcard.member_id] if member_id2name.get(wzcard.member_id, None) else wzcard.member_id,
				'activity_name': wzcard.virtual_product.name
			})

		return {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo) if pageinfo else ''
		}
