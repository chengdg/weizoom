# -*- coding: utf-8 -*-
# import json
# from datetime import datetime

# from django.contrib.auth.decorators import login_required

# from core.jsonresponse import JsonResponse, create_response
# from core import paginator
# from models import (CouponRule, Coupon, CouponRecord, COUPON_STATUS_USED,
#                     COUPONSTATUS, COUPON_STATUS_EXPIRED)
# from . import models as promotion_models
# from mall import models as mall_models
# from modules.member.module_api import get_member_by_id_list
# from modules.member.models import (MemberGrade, MemberTag, WebAppUser)
# from core.restful_url_route import api
# from core import search_util
# from market_tools.tools.coupon.api_views import send_coupons

# COUNT_PER_PAGE = 10

# RECORD_FILTERS = {
#     'record': [
#             {
#             'comparator': lambda record, filter_value: filter_value <= record.send_time.strftime("%Y-%m-%d %H:%M"),
#             'query_string_field': 'startDate'
#         }, {
#             'comparator': lambda record, filter_value: filter_value >= record.send_time.strftime("%Y-%m-%d %H:%M"),
#             'query_string_field': 'endDate'
#         }
#     ],
#     'coupon': [
#         {
#             'comparator': lambda coupon, filter_value: filter_value in coupon.name,
#             'query_string_field': 'name'
#         }
#     ]
# }
#
#
# def __filter_records(request, records):
#     has_filter = search_util.init_filters(request, RECORD_FILTERS)
#     if not has_filter:
#         #没有filter，直接返回
#         return records
#
#     records = search_util.filter_objects(records, RECORD_FILTERS['record'])
#
#     return records

# @api(app='mall_promotion', resource='issuing_coupons_record', action='get')
# @login_required
# def get_issuing_coupons_record(request):
    # """
    # 获取发优惠券记录的集合
    # """
    # name = request.GET.get('name', '')
    # type_str = request.GET.get('couponType', '-1')
    # start_date = request.GET.get('startDate', '')
    # end_date = request.GET.get('endDate', '')
    #
    # is_fetch_all_promotions = (not name) and (not (type_str != '-1')) and (not start_date) and (not end_date)
    # records = [record for record in list(CouponRecord.objects.filter(owner=request.manager).order_by('-id'))]
    # if not is_fetch_all_promotions:
    #     #按时间筛选
    #     records = __filter_records(request, records)
    #     #按优惠券条件筛选
    #     filter_records = []
    #     coupon_rule_id2record = dict([(record.coupon_rule_id, record) for record in records])
    #     coupon_rule_ids = coupon_rule_id2record.keys()
    #     coupon_rules = CouponRule.objects.filter(id__in=coupon_rule_ids)
    #     coupon_rules = search_util.filter_objects(coupon_rules, RECORD_FILTERS['coupon'])
    #
    #
    #     coupon_type = request.GET.get('couponType', None)
    #     if coupon_type != '-1':
    #         if coupon_type == '2':
    #             coupon_rules = [rule for rule in coupon_rules if rule.limit_product == 1]
    #         else:
    #             coupon_rules = [rule for rule in coupon_rules if rule.limit_product == 0]
    #
    #     coupon_rule_ids = [rule.id for rule in coupon_rules]
    #     for record in records:
    #         if record.coupon_rule_id in coupon_rule_ids:
    #             filter_records.append(record)
    #
    #     records = filter_records
    #
    # count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
    # cur_page = int(request.GET.get('page', '1'))
    # pageinfo, records = paginator.paginate(records, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
    #
    # items = []
    # coupon_rule_ids = []
    # record_ids = []
    # record_id2coupon_used_count = dict()
    # for record in records:
    #     record_ids.append(record.id)
    #     coupon_rule_ids.append(record.coupon_rule_id)
    # id2coupon_rule = dict([(rule.id, rule)for rule in CouponRule.objects.filter(id__in=coupon_rule_ids)])
    # coupons = Coupon.objects.filter(coupon_record_id__in=record_ids)
    #
    # #计算每个规则有多少已经使用了的
    # for coupon in coupons:
    #     if coupon.status == COUPON_STATUS_USED:
    #         if record_id2coupon_used_count.has_key(coupon.coupon_record_id):
    #             record_id2coupon_used_count[coupon.coupon_record_id] += 1
    #         else:
    #             record_id2coupon_used_count[coupon.coupon_record_id] = 1
    #
    # for record in records:
    #     coupon_rule_id = record.coupon_rule_id
    #     coupon_rule = id2coupon_rule[coupon_rule_id]
    #     data = {
    #         "id": record.id,
    #         "coupon_name": coupon_rule.name,
    #         "limit_product": coupon_rule.limit_product,
    #         "money": str(coupon_rule.money),
    #         "coupon_count": record.coupon_count,
    #         "send_time": record.send_time.strftime("%Y-%m-%d %H:%M:%S"),
    #         "person_count": record.person_count,
    #         "used_count": record_id2coupon_used_count[record.id] if record_id2coupon_used_count.has_key(record.id) else 0
    #     }
    #     items.append(data)
    #
    # data = {
    #     "items": items,
    #     'pageinfo': paginator.to_dict(pageinfo),
    #     'sortAttr': 'id',
    #     'data': {}
    # }
    #
    # response = create_response(200)
    # response.data = data
    # return response.get_response()

# @api(app='mall_promotion', resource='issuing_coupons_detail', action='get')
# @login_required
# def get_issuing_coupons_detail(request):
    # """
    # 获取发优惠券详情
    # """
    # #处理排序
    # sort_attr = request.GET.get('sort_attr', '-id')
    # coupons = Coupon.objects.filter(owner=request.manager, coupon_record_id=request.GET.get('id')).order_by(sort_attr)
    # if coupons:
    #     coupon_rule = CouponRule.objects.get(id=coupons[0].coupon_rule_id)
    #
    # #获取coupon所属的rule的name
    # id2rule = dict([(rule.id, rule) for rule in CouponRule.objects.filter(owner=request.manager)])
    #
    # #进行分页
    # count_per_page = int(request.GET.get('count_per_page', 15))
    # cur_page = int(request.GET.get('page', '1'))
    # pageinfo, coupons = paginator.paginate(coupons, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
    # #避免便利整个优惠券列表
    # member_ids = [c.member_id for c in coupons]
    # members = get_member_by_id_list(member_ids)
    # member_id2member = dict([(m.id, m) for m in members])
    #
    # #获取被使用的优惠券使用者信息
    # coupon_ids = [c.id for c in coupons if c.status==COUPON_STATUS_USED]
    # orders = mall_models.Order.get_orders_by_coupon_ids(coupon_ids)
    # if orders:
    #     coupon_id2webapp_user_id = dict([(o.coupon_id, \
    #         {'id': o.id, 'user':o.webapp_user_id, 'order_id':o.order_id, 'created_at': o.created_at})\
    #         for o in orders])
    # else:
    #     coupon_id2webapp_user_id = {}
    #
    # response = create_response(200)
    # response.data.items = []
    # #统计是否有active的coupon
    # # has_active_coupon = False
    # now = datetime.today()
    # for coupon in coupons:
    #     cur_coupon = JsonResponse()
    #     cur_coupon.id = coupon.id
    #     cur_coupon.coupon_id = coupon.coupon_id
    #     cur_coupon.provided_time = coupon.provided_time.strftime("%Y-%m-%d %H:%M:%S")
    #     cur_coupon.start_time = coupon_rule.start_date.strftime("%Y-%m-%d %H:%M:%S")
    #     cur_coupon.end_time = coupon_rule.end_date.strftime("%Y-%m-%d %H:%M:%S")
    #     cur_coupon.created_at = coupon.created_at.strftime("%Y-%m-%d %H:%M")
    #     cur_coupon.money = str(coupon.money)
    #     cur_coupon.is_manual_generated = coupon.is_manual_generated
    #     cur_member = JsonResponse()
    #     member_id = int(coupon.member_id)
    #     # if coupon.status == COUPON_STATUS_UNUSED:
    #         # has_active_coupon = True
    #     if member_id in member_id2member:
    #         member = member_id2member[member_id]
    #         cur_member.username_for_html = member.username_for_html
    #     else:
    #         member = ''
    #         cur_member.username_for_html = ''
    #     cur_member.id = member_id
    #
    #     consumer = JsonResponse()
    #     consumer.username_for_html = ''
    #     if coupon.status == COUPON_STATUS_USED:
    #         if coupon.id in coupon_id2webapp_user_id:
    #             order = coupon_id2webapp_user_id[coupon.id]
    #             cur_coupon.order_id = order['id']
    #             cur_coupon.order_fullid = order['order_id']
    #             cur_coupon.use_time = order['created_at'].strftime("%Y-%m-%d %H:%M")
    #             webapp_user_id = order['user']
    #             member = WebAppUser.get_member_by_webapp_user_id(webapp_user_id)
    #             if member:
    #                 consumer.username_for_html = member.username_for_html
    #                 consumer.id = member.id
    #             else:
    #                 consumer.username_for_html = '未知'
    #         else:
    #             consumer.username_for_html = '未知'
    #         cur_coupon.status = COUPONSTATUS.get(coupon.status)['name']
    #     elif coupon.expired_time <= now:
    #         cur_coupon.status = COUPONSTATUS.get(COUPON_STATUS_EXPIRED)['name']
    #     else:
    #         cur_coupon.status = COUPONSTATUS.get(coupon.status)['name']
    #
    #     cur_coupon.member = cur_member
    #     cur_coupon.consumer = consumer
    #     cur_coupon.rule_name = id2rule[coupon.coupon_rule_id].name
    #     response.data.items.append(cur_coupon)
    #
    # response.data.sortAttr = request.GET.get('sort_attr', '-created_at')
    # response.data.pageinfo = paginator.to_dict(pageinfo)
    # return response.get_response()


# @api(app='mall_promotion', resource='issuing_coupons_record', action='create')
# @login_required
# def create_red_enevlop(request):
    # '''
    # 需要提供如下字段：
    #
    # 需要非空
    #
    #     member_id: '',
    #     coupon_rule_id,
    #     pre_person_count,
    #     send_time
    #
    # '''
    # from market_tools.tools.coupon.util import consume_coupon
    # response = create_response(200)
    #
    # member_ids = request.POST.get('member_id', None)  # 获取会员id 组
    # member_ids = json.loads(member_ids)
    # coupon_rule_id = int(request.POST.get('coupon_rule_id'))  # 优惠券规则
    # pre_person_count = int(request.POST.get('pre_person_count'))  # 每人几张
    # person_count = len(member_ids)  # 发放的人数
    # send_count = pre_person_count * person_count  # 发放的张数
    #
    # # 对应优惠券的库存
    # coupon_count = promotion_models.CouponRule.objects.get(id=coupon_rule_id).remained_count
    # if coupon_count < send_count:
    #     response = create_response(500)
    #     response.errMsg = u"发放数量大于优惠券库存,请先增加库存"
    #     return response.get_response()
    #
    # # 创建优惠券记录
    # coupon_record = promotion_models.CouponRecord.objects.create(
    #     owner=request.manager,
    #     coupon_rule_id=coupon_rule_id,
    #     pre_person_count=pre_person_count,
    #     person_count=person_count,
    #     coupon_count=send_count)
    # coupon_record.save()
    # if member_ids:  # 会员列表
    #     # 对每个会员创建优惠券
    #     real_person_count = 0
    #     real_coupon_count = 0
    #     for member_id in member_ids:
    #         c_index = 0
    #         c_real_count = 0
    #         while c_index < pre_person_count:
    #             coupon, msg = consume_coupon(request.manager.id, coupon_rule_id, member_id, coupon_record_id=coupon_record.id)
    #             if coupon:
    #                 c_real_count += 1
    #             c_index += 1
    #         if c_real_count:
    #             real_person_count += 1
    #             real_coupon_count += c_real_count
    #
    #     if real_coupon_count < coupon_count:
    #         # 修正优惠券实际发放数量
    #         promotion_models.CouponRecord.objects.filter(id=coupon_record.id).update(
    #             person_count=real_person_count,
    #             coupon_count=real_coupon_count)
    #
    #     return response.get_response()
    # else:
    #     print("create_red_enevlop error")
    #     return response.get_response(403)


# @api(app='mall_promotion', resource='all_coupon_rules', action='get')
# @login_required
# def get_all_coupon_rules(request):
#     """
#     获取所有可选的优惠券规则
#     """
#     response = create_response(200)
#     response.data.items = []
#
#     rules = CouponRule.objects.filter(owner=request.manager, is_active=True, end_date__gte=datetime.now()).order_by('-id')
#
#     # 进行分页
#     count_per_page = int(request.GET.get('count_per_page', 15))
#     cur_page = int(request.GET.get('page', '1'))
#     pageinfo, rules = paginator.paginate(rules, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
#
#     for rule in rules:
#         cur_coupon_rule = JsonResponse()
#         cur_coupon_rule.id = rule.id
#         cur_coupon_rule.name = rule.name
#         cur_coupon_rule.limit_product = rule.limit_product
#         cur_coupon_rule.start_time = rule.start_date.strftime("%Y-%m-%d %H:%M")
#         cur_coupon_rule.end_time = rule.end_date.strftime("%Y-%m-%d %H:%M")
#         cur_coupon_rule.money = str(rule.money)
#         cur_coupon_rule.remained_count = rule.remained_count
#         cur_coupon_rule.count = rule.remained_count
#         cur_coupon_rule.limit_counts = rule.limit_counts
#         response.data.items.append(cur_coupon_rule)
#
#     response.data.sortAttr = request.GET.get('sort_attr', '-created_at')
#     response.data.pageinfo = paginator.to_dict(pageinfo)
#     return response.get_response()


# @api(app="mall_promotion", resource='all_vip_search_info', action='get')
# @login_required
# def get_vip_search_info(request):
#     response = create_response(200)
#     data = {}  # context
#     data['member_grade'] = json.dumps([
#         {'id': m.id, 'name': m.name} for m in MemberGrade.get_all_grades_list(request.GET.get('webapp_id'))
#     ])
#     data['member_tags'] = json.dumps([
#         {'id': m.id, 'name': m.name} for m in MemberTag.get_member_tags(request.GET.get('webapp_id'))
#     ])
#     response.data = data
#     return response.get_response()
