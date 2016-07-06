# -*- coding: utf-8 -*-

from core import resource
from core import paginator
from core.jsonresponse import create_response

from mall.promotion.models import *
from mall.models import Order

from market_tools.tools.coupon.util import get_member_coupons, get_member_coupons_for_sign, \
	get_member_coupons_for_exsign
from modules.member.models import *

COUNT_PER_PAGE = 10


# def get_coupons_of_member(member_id, status, coupon_ids, items):
# 	if status != 0:
# 		member = Member.objects.get(id=member_id)
# 		# coupon_rec_list = Coupon.objects.filter(member_id=member_id).order_by('-provided_time', '-coupon_record_id', '-id')
# 		member_code_order_list = Order.objects.filter(webapp_user_id__in=member.get_webapp_user_ids, coupon_id__gt=0).order_by('-payment_time')
# 		for code_order in member_code_order_list:
# 			if status == -1:
# 				code_coupon = Coupon.objects.get(id=code_order.coupon_id)
# 			else:
# 				try:
# 					code_coupon = Coupon.objects.get(id=code_order.coupon_id, status=status)
# 				except:
# 					code_coupon = None
# 			if code_coupon is not None and code_coupon.member_id == 0:
# 				if code_coupon.id in coupon_ids:
# 					continue

# 				coupon_rule = code_coupon.coupon_rule
# 				item = dict()
# 				whereabouts = dict()
# 				item['provided_time'] = code_order.payment_time.strftime("%Y/%m/%d %H:%M")
# 				item['coupon_id'] = code_coupon.coupon_id
# 				item['coupon_name'] = coupon_rule.name
# 				if coupon_rule.limit_product:
# 					item['coupon_detail'] = '￥'+str(code_coupon.money)+' 单品券'
# 				else:
# 					item['coupon_detail'] = '￥'+str(code_coupon.money)+' 全店通用券'
# 				item['coupon_state'] = COUPONSTATUS[code_coupon.status]['name']

# 				if code_coupon.status == COUPON_STATUS_USED:
# 					whereabouts['type'] = COUPON_STATUS_USED  # 去处 1
# 					whereabouts['content'] = code_order.order_id
# 					whereabouts['orderid'] = code_order.id
# 				else:
# 					whereabouts['type'] = COUPON_STATUS_UNUSED  # 来源 0
# 					whereabouts['content'] = ''
# 					whereabouts['orderid'] = None

# 				item['coupon_whereabouts'] = whereabouts

# 				items.append(item)

# 		for vat in items:
# 			print('>>>>'+vat['coupon_id'])
# 		return items


class MemberCouponInfo(resource.Resource):

	app = "member"
	resource = "member_coupon"

	def api_get(request):
		member_id = request.GET.get('id')
		filter_attr = request.GET.get('filter_attr', '')
		filter_value = request.GET.get('filter_value', -1)
		filter_value = int(filter_value)
		project_id = request.GET.get('project_id', '')

		if member_id is None:
			response = create_response(500)
			response.errMsg = 'Member id is required'
			return response.get_response()

		status = -1
		if filter_attr == 'status':
			status = filter_value

		items = []
		member = Member.objects.get(id=member_id)
		if project_id:
			_, project_type, project_id = request.GET.get('project_id').split(':')
			if project_type == 'sign':
				member_coupon_list = get_member_coupons_for_sign(member, request.user, project_id, status)
			else:
				member_coupon_list = get_member_coupons_for_exsign(member, request.user, project_id, status)
		else:
			member_coupon_list = get_member_coupons(member, status)
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		current_page = int(request.GET.get('page', '1'))

		coupon_ids = []
		for coupon in member_coupon_list:
			# rule = CouponRule.objects.get(id=coupon.coupon_rule)
			coupon_rule = coupon.coupon_rule

			item = dict()
			whereabouts = dict()
			coupon_ids.append(coupon.id)
			if coupon.member_id == 0 and coupon.provided_time == DEFAULT_DATETIME:
				try:
					order = Order.objects.filter(coupon_id=coupon.id)[0]
					item['provided_time'] = order.created_at.strftime("%Y/%m/%d %H:%M")
				except:
					item['provided_time'] = coupon.provided_time.strftime("%Y/%m/%d %H:%M")
			else:
				item['provided_time'] = coupon.provided_time.strftime("%Y/%m/%d %H:%M")
			
			item['coupon_id'] = coupon.coupon_id
			item['coupon_name'] = coupon_rule.name
			if coupon_rule.limit_product:
				item['coupon_detail'] = '￥'+str(coupon.money)+' 多商品券'
			else:
				item['coupon_detail'] = '￥'+str(coupon.money)+' 通用券'
			item['coupon_state'] = COUPONSTATUS[coupon.status]['name']

			if coupon.status == COUPON_STATUS_USED:
				order = Order.objects.filter(coupon_id=coupon.id)[0]
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
			#items = get_coupons_of_member(member_id, status, coupon_ids, items)
			items.sort(lambda x,y: cmp(y['provided_time'], x['provided_time']))

		pageinfo, items = paginator.paginate(items, current_page, count_per_page,
														query_string=request.META['QUERY_STRING'])

		response = create_response(200)
		response.data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': '',
			'status': status,
			'data': {}
		}

		return response.get_response()
