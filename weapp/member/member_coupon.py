# -*- coding: utf-8 -*-

from core import resource
from core import paginator
from core.jsonresponse import create_response

from mall.promotion.models import *
from mall.models import Order

COUNT_PER_PAGE = 10


def get_coupons_of_member(member_id, status):
		items = []
		if status != 0:
			member = Member.objects.get(id=member_id)
			# coupon_rec_list = Coupon.objects.filter(member_id=member_id).order_by('-provided_time', '-coupon_record_id', '-id')
			member_code_order_list = Order.objects.filter(webapp_user_id__in=member.get_webapp_user_ids, coupon_id__gt=0).order_by('-payment_time')
			for code_order in member_code_order_list:
				if status == -1:
					code_coupon = Coupon.objects.get(id=code_order.coupon_id)
				else:
					code_coupon = Coupon.objects.get(id=code_order.coupon_id).filter(status=status)
				if code_coupon.member_id == 0:
					coupon_rule = code_coupon.coupon_rule
					item = dict()
					whereabouts = dict()
					item['provided_time'] = code_order.payment_time.strftime("%Y/%m/%d %H:%M")
					item['coupon_id'] = code_coupon.coupon_id
					item['coupon_name'] = coupon_rule.name
					if coupon_rule.limit_product:
						item['coupon_detail'] = '￥'+str(code_coupon.money)+' 单品券'
					else:
						item['coupon_detail'] = '￥'+str(code_coupon.money)+' 全店通用券'
					item['coupon_state'] = COUPONSTATUS[code_coupon.status]['name']

					if code_coupon.status == COUPON_STATUS_USED:
						whereabouts['type'] = COUPON_STATUS_USED  # 去处 1
						whereabouts['content'] = code_order.order_id
						whereabouts['orderid'] = code_order.id
					else:
						whereabouts['type'] = COUPON_STATUS_UNUSED  # 来源 0
						whereabouts['content'] = ''
						whereabouts['orderid'] = None

					item['coupon_whereabouts'] = whereabouts

					items.append(item)

			return items


class MemberCouponInfo(resource.Resource):

	app = "member"
	resource = "member_coupon"

	def api_get(request):
		member_id = request.GET.get('id')
		filter_attr = request.GET.get('filter_attr', '')
		filter_value = request.GET.get('filter_value', -1)
		filter_value = int(filter_value)

		if member_id is None:
			response = create_response(500)
			response.errMsg = 'Member id is required'
			return response.get_response()

		status = -1
		if filter_attr == 'status':
			status = filter_value

		items = []
		if status == -1:
			member_coupon_list = Coupon.objects.filter(member_id=member_id).order_by('-provided_time', '-coupon_record_id', '-id')
		else:
			member_coupon_list = Coupon.objects.filter(member_id=member_id).filter(status=status).order_by('-provided_time', '-coupon_record_id', '-id')
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		current_page = int(request.GET.get('page', '1'))
		pageinfo, member_coupon_list = paginator.paginate(member_coupon_list, current_page, count_per_page,
														query_string=request.META['QUERY_STRING'])

		for coupon in member_coupon_list:
			# rule = CouponRule.objects.get(id=coupon.coupon_rule)
			coupon_rule = coupon.coupon_rule

			item = dict()
			whereabouts = dict()

			item['provided_time'] = coupon.provided_time.strftime("%Y/%m/%d %H:%M")
			item['coupon_id'] = coupon.coupon_id
			item['coupon_name'] = coupon_rule.name
			if coupon_rule.limit_product:
				item['coupon_detail'] = '￥'+str(coupon.money)+' 单品券'
			else:
				item['coupon_detail'] = '￥'+str(coupon.money)+' 全店通用券'
			item['coupon_state'] = COUPONSTATUS[coupon.status]['name']

			if coupon.status == COUPON_STATUS_USED:
				order = Order.objects.get(coupon_id=coupon.id)
				whereabouts['type'] = COUPON_STATUS_USED  # 去处 1
				whereabouts['content'] = order.order_id
				whereabouts['orderid'] = order.id
			else:
				whereabouts['type'] = COUPON_STATUS_UNUSED  # 来源 0
				whereabouts['content'] = ''
				whereabouts['orderid'] = None

			item['coupon_whereabouts'] = whereabouts

			items.append(item)

		if status != 0:
			items.extend(get_coupons_of_member(member_id, status))
			items.sort(lambda x,y: cmp(y['provided_time'], x['provided_time']))

		response = create_response(200)
		response.data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': '',
			'status': status,
			'data': {}
		}

		return response.get_response()
