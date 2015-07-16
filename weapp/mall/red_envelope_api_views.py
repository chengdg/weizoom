#-*- coding: utf-8 -*-
import json
from datetime import datetime

from django.contrib.auth.decorators import login_required

from core.jsonresponse import JsonResponse, create_response
from core import paginator
from core.restful_url_route import api
from core import search_util

from promotion import models as promotion_models

COUNT_PER_PAGE = 10

RULE_FILTERS = {
    'rule': [
        {
            'comparator': lambda rule, filter_value: filter_value in rule.name,
            'query_string_field': 'name'
        }, {
            'comparator': lambda rule, filter_value: int(filter_value) == rule.coupon_rule_id,
            'query_string_field': 'couponRule'
        }, {
            'comparator': lambda rule, filter_value: filter_value <= rule.start_time.strftime("%Y-%m-%d %H:%M"),
            'query_string_field': 'startDate'
        }, {
            'comparator': lambda rule, filter_value: filter_value >= rule.end_time.strftime("%Y-%m-%d %H:%M"),
            'query_string_field': 'endDate'
        }
    ]
}

def __filter_rules(request, rules):
    has_filter = search_util.init_filters(request, RULE_FILTERS)
    if not has_filter:
        #没有filter，直接返回
        return rules

    rules = search_util.filter_objects(rules, RULE_FILTERS['rule'])

    return rules

@api(app='mall', resource='red_envelope_rule', action='create')
@login_required
def create_red_envelope_rule(request):
    limit_money = request.POST.get('limit_money', 0)
    if not limit_money:
        limit_money = 0.0
    if request.POST.get('start_date', None) and request.POST.get('end_date', None):
        promotion_models.RedEnvelopeRule.objects.create(
            owner = request.user,
            name = request.POST.get('name', ''),
            coupon_rule_id = request.POST.get('coupon_rule', 0),
            start_time = request.POST.get('start_date'),
            end_time = request.POST.get('end_date'),
            limit_order_money = limit_money,
            use_info = request.POST.get('detail', ''),
            share_pic = request.POST.get('share_pic', ''),
            share_title = request.POST.get('remark', '')
        )
    else:
        promotion_models.RedEnvelopeRule.objects.create(
            owner = request.user,
            name = request.POST.get('name', ''),
            coupon_rule_id = request.POST.get('coupon_rule', 0),
            limit_time = True,
            limit_order_money = limit_money,
            use_info = request.POST.get('detail', ''),
            share_pic = request.POST.get('share_pic', ''),
            share_title = request.POST.get('remark', '')
        )
    return create_response(200).get_response()

@api(app="mall", resource="red_envelope_rules", action="get")
@login_required
def get_red_envelope_rules(request):
    """
    获取红包规则列表
    """
    name = request.GET.get('name', '')
    coupon_rule_id = int(request.GET.get('couponRule', 0))
    start_date = request.GET.get('startDate', '')
    end_date = request.GET.get('endDate', '')


    is_fetch_all_rules = (not name) and (not coupon_rule_id) and (not start_date) and (not end_date)
    rules = promotion_models.RedEnvelopeRule.objects.filter(owner=request.manager,is_delete=False).order_by('-id')

    if not is_fetch_all_rules:
        rules = __filter_rules(request, rules)

    count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
    cur_page = int(request.GET.get('page', '1'))
    pageinfo, rules = paginator.paginate(rules, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

    items = []
    coupon_rule_ids = []
    rule_ids = []

    for rule in rules:
        rule_ids.append(rule.id)
        coupon_rule_ids.append(rule.coupon_rule_id)

    id2coupon_rule = dict([(coupon_rule.id, coupon_rule)for coupon_rule in promotion_models.CouponRule.objects.filter(id__in=coupon_rule_ids)])
    records = promotion_models.GetRedEnvelopeRecord.objects.filter(owner=request.manager)
    rule_id2count = {}
    for record in records:
        if rule_id2count.has_key(record.red_envelope_rule_id):
            rule_id2count[record.red_envelope_rule_id] += 1
        else:
            rule_id2count[record.red_envelope_rule_id] = 1

    for rule in rules:
        data = {
            "id": rule.id,
            "rule_name": rule.name,
            "limit_time": rule.limit_time,
            "start_time": rule.start_time.strftime("%Y/%m/%d %H:%M:%S"),
            "end_time": rule.end_time.strftime("%Y/%m/%d %H:%M:%S"),
            "coupon_rule_name": id2coupon_rule[rule.coupon_rule_id].name,
            "status": rule.status,
            "get_count": rule_id2count[rule.id] if rule_id2count.has_key(rule.id) else 0,
            "remained_count": id2coupon_rule[rule.coupon_rule_id].remained_count,
            "is_timeout": False if rule.end_time > datetime.now() else True
        }
        items.append(data)

    data = {
        "items": items,
        'pageinfo': paginator.to_dict(pageinfo),
        'sortAttr': 'id',
        'data': {}
    }

    response = create_response(200)
    response.data = data
    return response.get_response()

@api(app="mall", resource="red_envelope_rule", action="update")
@login_required
def update_red_envelope_rule(request):
    """
    更改红包规则的状态
    """
    id = request.POST.get('id', 0)
    status = request.POST.get('status', None)
    try:
        if status == 'over':
            promotion_models.RedEnvelopeRule.objects.filter(id=id).update(status=False)
        elif status == 'start':
            start_rule = promotion_models.RedEnvelopeRule.objects.filter(owner=request.manager, status=True)
            if start_rule.count() > 0:
                response = create_response(500)
                response.errMsg = "请先关闭其他分享红包活动！"
                return response.get_response()
            promotion_models.RedEnvelopeRule.objects.filter(id=id).update(status=True)
        elif status == 'delete':
            promotion_models.RedEnvelopeRule.objects.filter(id=id).update(status=False, is_delete=True)
    except:
        return create_response(500).get_response()
    return create_response(200).get_response()