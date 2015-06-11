# -*- coding: utf-8 -*-

import random

from django.contrib.auth.decorators import login_required
from django.db.models import Q, F

from core.jsonresponse import JsonResponse, create_response
from core import paginator
from core.restful_url_route import *
from core import search_util

from modules.member.module_api import get_member_by_id_list
from modules.member.models import WebAppUser
from mall.models import Order

from models import *

#定向发放优惠券
#根据会员发放优惠券
SEND_COUPON_OF_MEMBER = 1
#根据分组发放优惠券
SEND_COUPON_OF_TAG = 2
#根据等级发放优惠券
SEND_COUPON_OF_GRADE = 3


@api(app='mall_promotion', resource='coupon', action='create')
@login_required
def create_coupon(request):
	"""
	添加库码
	"""
	rule_id = request.POST.get('rule_id', '0')
	rules = CouponRule.objects.filter(id=rule_id)
	if len(rules) != 1:
		return create_response(200, '优惠券不存在')
	count = int(request.POST.get('count', '0'))
	__create_coupons(rules[0], count)
	rules.update(
			count=(rules[0].count+count),
			remained_count=(rules[0].remained_count+count)
		)
	return create_response(200).get_response()

def __create_coupons(couponRule, count, promotion=None):
	"""
	创建未使用的优惠券
	"""
	random_args_value = ['1','2','3','4','5','6','7','8','9','0']
	i = 0
	if not promotion:
		promotion = Promotion.objects.filter(type=PROMOTION_TYPE_COUPON, detail_id=couponRule.id)[0]

	while i < count:
		try:
			coupon_id = '%03d%04d%s' % (couponRule.owner.id, couponRule.id, ''.join(random.sample(random_args_value, 6)))
			new_coupon = Coupon.objects.create(
				owner = couponRule.owner,
				coupon_id = coupon_id,
				provided_time = promotion.start_date,
				expired_time = promotion.end_date,
				money = couponRule.money,
				coupon_rule_id = couponRule.id,
				is_manual_generated = False,
				status = COUPON_STATUS_UNGOT
			)
			i += 1
		except:
			continue

@api(app='mall_promotion', resource='coupon_rules', action='create')
@login_required
def create_coupon_rule(request):
	"""
	创建，更新优惠券规则
	"""
	rule_id = request.POST.get('rule_id', '-')
	if rule_id.isdigit():
		couponRole = CouponRule.objects.filter(id=rule_id)
		couponRole.update(
			name = request.POST.get('name', ''),
			remark = request.POST.get('remark', ''),
		)
		Promotion.objects.filter(detail_id=couponRole[0].id,type=PROMOTION_TYPE_COUPON).update(
			name = request.POST.get('name', ''),
		)
		return create_response(200).get_response()
	# 优惠券限制条件
	is_valid_restrictions = request.POST.get('is_valid_restrictions', '0')
	if is_valid_restrictions=='0':
		valid_restrictions = -1
	else:
		valid_restrictions = request.POST.get('valid_restrictions', '0')
	count = int(request.POST.get('count', '1'))
	limit_product = request.POST.get('limit_product', '0')
	limit_product_id = request.POST.get('product_ids', '-1')
	if limit_product == '1' and limit_product_id.isdigit():
		limit_product_id = int(limit_product_id)
	else:
		limit_product_id = 0

	start_date = request.POST.get('start_date', None)
	if not start_date:
		start_date = '2000-01-01 00:00'

	end_date = request.POST.get('end_date', None)
	if not end_date:
		end_date = '2000-01-01 00:00'

	couponRule = CouponRule.objects.create(
		owner = request.manager,
		name = request.POST.get('name', ''),
		money = request.POST.get('money', '0.0'),
		# valid_days = request.POST.get('valid_days', '0'),
		valid_restrictions = valid_restrictions,
		limit_counts = request.POST.get('limit_counts', '1'),
		count = count,
		remained_count = count,
		remark = request.POST.get('remark', ''),
		limit_product = limit_product == '1',
		limit_product_id = limit_product_id,
		start_date = start_date,
		end_date = end_date
	)

	promotion = Promotion.objects.create(
		owner = request.manager,
		name = request.POST.get('name', ''),
		type = PROMOTION_TYPE_COUPON,
		member_grade_id = request.POST.get('member_grade', 0),
		start_date = start_date,
		end_date = end_date,
		detail_id = couponRule.id,
		status = PROMOTION_STATUS_NOT_START
	)
	__create_coupons(couponRule, count, promotion)

	if limit_product == '1':
		product_ids = request.POST.get('product_ids', '-1').split(',')
		for product_id in product_ids:
			ProductHasPromotion.objects.create(
				product_id = product_id,
				promotion = promotion
			)
	now = datetime.today()
	start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M')
	if start_date <= now:
		promotion.status = PROMOTION_STATUS_STARTED
		promotion.save()
	return create_response(200).get_response()

#筛选数据构造
COUPON_FILTERS = {
	'coupon':[
		{
			'comparator': lambda coupon, filter_value: (filter_value == coupon.coupon_id),
            'query_string_field': 'couponCode'
		},{
			'comparator': lambda coupon, filter_value: (filter_value == 'all') or (filter_value == str(coupon.status)),
            'query_string_field': 'useStatus'
		}
	],
	'member':[
		{
			'comparator': lambda member, filter_value: (filter_value in member.username_for_html),
            'query_string_field': 'memberName'
		}
	]
}

def __filter_reviews(request, coupons):
	has_filter = search_util.init_filters(request, COUPON_FILTERS)
	if not has_filter:
		#没有filter，直接返回
		return coupons

	coupons = search_util.filter_objects(coupons, COUPON_FILTERS['coupon'])

	#处理领取人
	member_name = request.GET.get('memberName', '')
	filter_coupons = coupons
	if member_name:
		member_ids = [c.member_id for c in coupons]
		members = get_member_by_id_list(member_ids)
		members = search_util.filter_objects(members, COUPON_FILTERS['member'])
		member_ids = [member.id for member in members]
		filter_coupons = []
		for coupon in coupons:
			if coupon.member_id in member_ids:
				filter_coupons.append(coupon)
	return filter_coupons

@api(app='mall_promotion', resource='coupons', action='get')
@login_required
def get_records(request):
	"""
	获取优惠券
	"""
	coupon_code = request.GET.get('couponCode', '')
	use_status = request.GET.get('useStatus', '')
	member_name = request.GET.get('memberName', '')


	is_fetch_all_coupon = (not coupon_code) and (use_status == 'all') and (not member_name)
	#处理排序
	sort_attr = request.GET.get('sort_attr', '-id')
	coupons = Coupon.objects.filter(owner=request.manager, coupon_rule_id=request.GET.get('id')).order_by(sort_attr)

	#获取coupon所属的rule的name
	id2rule = dict([(rule.id, rule) for rule in CouponRule.objects.filter(owner=request.manager)])

	if is_fetch_all_coupon:
		#进行分页
		count_per_page = int(request.GET.get('count_per_page', 15))
		cur_page = int(request.GET.get('page', '1'))
		pageinfo, coupons = paginator.paginate(coupons, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
	else:
		coupons = __filter_reviews(request, coupons)
		count_per_page = int(request.GET.get('count_per_page', 15))
		cur_page = int(request.GET.get('page', '1'))
		pageinfo, coupons = paginator.paginate(coupons, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])


	#避免便利整个优惠券列表
	member_ids = [c.member_id for c in coupons]
	members = get_member_by_id_list(member_ids)
	member_id2member = dict([(m.id, m) for m in members])

	#获取被使用的优惠券使用者信息
	coupon_ids = [c.id for c in coupons if c.status==COUPON_STATUS_USED]
	orders = Order.get_orders_by_coupon_ids(coupon_ids)
	if orders:
		coupon_id2webapp_user_id = dict([(o.coupon_id, \
			{'id': o.id, 'user':o.webapp_user_id, 'order_id':o.order_id, 'created_at': o.created_at})\
			for o in orders])
	else:
		coupon_id2webapp_user_id = {}

	response = create_response(200)
	response.data.items = []
	#统计是否有active的coupon
	# has_active_coupon = False
	now = datetime.today()
	for coupon in coupons:
		cur_coupon = JsonResponse()
		cur_coupon.id = coupon.id
		cur_coupon.coupon_id = coupon.coupon_id
		cur_coupon.provided_time = coupon.provided_time.strftime("%Y-%m-%d %H:%M")
		cur_coupon.created_at = coupon.created_at.strftime("%Y-%m-%d %H:%M")
		cur_coupon.money = str(coupon.money)
		cur_coupon.is_manual_generated = coupon.is_manual_generated
		cur_member = JsonResponse()
		member_id = int(coupon.member_id)
		# if coupon.status == COUPON_STATUS_UNUSED:
			# has_active_coupon = True
		if member_id in member_id2member:
			member = member_id2member[member_id]
			cur_member.username_for_html = member.username_for_html
		else:
			member = ''
			cur_member.username_for_html = ''
		cur_member.id = member_id

		consumer = JsonResponse()
		consumer.username_for_html = ''
		if coupon.status == COUPON_STATUS_USED:
			if coupon.id in coupon_id2webapp_user_id:
				order = coupon_id2webapp_user_id[coupon.id]
				cur_coupon.order_id = order['id']
				cur_coupon.order_fullid = order['order_id']
				cur_coupon.use_time = order['created_at'].strftime("%Y-%m-%d %H:%M")
				webapp_user_id = order['user']
				member = WebAppUser.get_member_by_webapp_user_id(webapp_user_id)
				if member:
					consumer.username_for_html = member.username_for_html
					consumer.id = member.id
				else:
					consumer.username_for_html = '未知'
			else:
				consumer.username_for_html = '未知'
			cur_coupon.status = COUPONSTATUS.get(coupon.status)['name']
		elif coupon.expired_time <= now:
			cur_coupon.status = COUPONSTATUS.get(COUPON_STATUS_EXPIRED)['name']
		else:
			cur_coupon.status = COUPONSTATUS.get(coupon.status)['name']

		cur_coupon.member = cur_member
		cur_coupon.consumer = consumer
		cur_coupon.rule_name = id2rule[coupon.coupon_rule_id].name
		response.data.items.append(cur_coupon)

	response.data.sortAttr = request.GET.get('sort_attr', '-created_at')
	response.data.pageinfo = paginator.to_dict(pageinfo)
	return response.get_response()

@api(app='mall_promotion', resource='coupons', action='delete')
@login_required
def delete_coupons(request):
    """
    删除优惠券
    """
    ids = request.POST.getlist('ids[]')
    Coupon.objects.filter(owner=request.manager, id__in=ids).delete()

    response = create_response(200)
    return response.get_response()