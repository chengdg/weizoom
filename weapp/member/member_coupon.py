# -*- coding: utf-8 -*-

from core import resource
from core import paginator
from core.jsonresponse import create_response

from mall.promotion.models import *
from mall.models import Order

COUNT_PER_PAGE = 10


class MemberCouponInfo(resource.Resource):

	app = "member"
	resource = "member_coupon"

	def api_get(request):
		status = -1
		member_id = request.GET.get('id')

		if member_id is None:
			response = create_response(500)
			response.errMsg = 'Member id is required'
			return response.get_response()

		items = []
		member_coupon_list = Coupon.objects.filter(member_id=member_id)
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		current_page = int(request.GET.get('page', '1'))
		pageinfo, member_coupon_list = paginator.paginate(member_coupon_list, current_page, count_per_page,
														query_string=request.META['QUERY_STRING'])

		for coupon in member_coupon_list:
			# rule = CouponRule.objects.get(id=coupon.coupon_rule)
			coupon_rule = coupon.coupon_rule

			item = dict()
			item['provided_time'] = coupon.provided_time.strftime("%Y/%m/%d %H:%M")
			item['coupon_name'] = coupon_rule.name
			if coupon_rule.limit_product:
				item['coupon_detail'] = '￥'+str(coupon.money)+' 单品券'
			else:
				item['coupon_detail'] = '￥'+str(coupon.money)+' 全店通用券'
			item['coupon_state'] = COUPONSTATUS[coupon.status]['name']

			if coupon.status == COUPON_STATUS_USED:
				order = Order.objects.get(coupon_id=coupon.id)
				item['coupon_whereabouts'] = str(order.order_id)
			else:
				item['coupon_whereabouts'] = ''

			items.append(item)

		response = create_response(200)
		response.data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': '',
			'status': status,
			'data': {}
		}

		return response.get_response()