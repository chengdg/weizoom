# -*- coding: utf-8 -*-
__author__ = 'cl'

import json
from datetime import datetime

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from core import resource
from mall.promotion import models as promotion_models
from mall import export
from core.jsonresponse import create_response
from core import paginator

COUNT_PER_PAGE = 20

FIRST_NAV_NAME  = export.MALL_PROMOTION_AND_APPS_FIRST_NAV
class RedEnvelopeRuleList(resource.Resource):
    app = "apps/red_envelope"
    resource = "red_envelope_rule_list"

    @login_required
    def get(request):
        """
        红包规则列表页面
        """
        is_create = int(request.GET.get('is_create', 0))
        rules = promotion_models.RedEnvelopeRule.objects.filter(owner=request.manager).order_by('-id')
        coupon_rule_ids = [rule.coupon_rule_id for rule in rules]
        coupon_rules = promotion_models.CouponRule.objects.filter(id__in=coupon_rule_ids)
        coupon_rule_info = []
        for coupon_rule in coupon_rules:
            info = {
                "id": coupon_rule.id,
                "name": coupon_rule.name
            }
            coupon_rule_info.append(info)

        items = []
        if not is_create:
            rules = promotion_models.RedEnvelopeRule.objects.filter(owner=request.manager, is_delete=False).order_by('-id')
            coupon_rule_ids = []
            rule_ids = []

            for rule in rules:
                rule_ids.append(rule.id)
                coupon_rule_ids.append(rule.coupon_rule_id)

            id2coupon_rule = dict([(coupon_rule.id, coupon_rule) for coupon_rule in
                                   promotion_models.CouponRule.objects.filter(id__in=coupon_rule_ids)])

            #库存不足20时获取规则数据
            flag = True
            is_warring = False
            for rule in rules:
                if id2coupon_rule[rule.coupon_rule_id].remained_count <= 20:
                    if rule.status:
                        data ={}
                        if rule.limit_time:
                            if flag:
                                flag = False
                                is_warring = True
                            else:
                                is_warring = False
                            data = {
                                "id": rule.id,
                                "rule_name": rule.name,
                                "receive_method": rule.receive_method,
                                "is_warring": is_warring
                            }
                            items.append(data)
                        else:
                            is_timeout = False if rule.end_time > datetime.now() else True
                            print is_timeout,"is_timeout"
                            if not is_timeout:
                                if flag:
                                    flag = False
                                    is_warring = True
                                else:
                                    is_warring = False
                                data = {
                                    "id": rule.id,
                                    "rule_name": rule.name,
                                    "receive_method": rule.receive_method,
                                    "is_warring": is_warring
                                }
                                items.append(data)
        endDate = request.GET.get('endDate','')
        status = request.GET.get('status','')
        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV_NAME,
            'second_navs': export.get_promotion_and_apps_second_navs(request),
            'second_nav_name': export.MALL_APPS_SECOND_NAV,
            'third_nav_name': export.MALL_APPS_RED_ENVELOPE_NAV,
            "coupon_rule_info": json.dumps(coupon_rule_info),
            "items": items,
            "is_create": is_create,
            "endDate": endDate,
            "status": status
        })
        return render_to_response('red_envelope/templates/editor/red_envelope_rules.html', c)


    @login_required
    def api_get(request):
        """
        获取红包规则列表advanced table
        """
        name = request.GET.get('name', '')
        coupon_rule_id = int(request.GET.get('couponRule', 0))
        start_date = request.GET.get('startDate', '')
        end_date = request.GET.get('endDate', '')
        status = request.GET.get('status', '')

        rules = promotion_models.RedEnvelopeRule.objects.filter(owner=request.manager, is_delete=False).order_by('-id')

        #处理筛选
        if name:
            rules = rules.filter(name__contains=name)
        if coupon_rule_id:
            rules = rules.filter(coupon_rule_id=coupon_rule_id)
        if start_date:
             rules = rules.filter(start_time__gte=start_date)
        if end_date:
            rules = rules.filter(end_time__lte=end_date)
        if status:
            rules = rules.filter(limit_time=False,status=status)
        #处理过期排序
        for rule in rules:
            is_timeout = False if rule.end_time > datetime.now() else True
            if is_timeout and not rule.limit_time:
                if rule.receive_method:
                    rule.order_index = -1
                else:
                    if not rule.status:
                        rule.order_index = -1
                rule.save()
        rules = rules.order_by("-order_index", "-id")
        cur_rules = []
        if status:
            for rule in rules:
                is_timeout = False if rule.end_time > datetime.now() else True
                if not is_timeout:
                    cur_rules.append(rule)

        count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
        cur_page = int(request.GET.get('page', '1'))
        #从首页的即将到期的
        if status:
            pageinfo, rules = paginator.paginate(cur_rules, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
        else:
            pageinfo, rules = paginator.paginate(rules, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

        items = []
        coupon_rule_ids = []
        rule_ids = []

        for rule in rules:
            rule_ids.append(rule.id)
            coupon_rule_ids.append(rule.coupon_rule_id)

        id2coupon_rule = dict([(coupon_rule.id, coupon_rule) for coupon_rule in
                               promotion_models.CouponRule.objects.filter(id__in=coupon_rule_ids)])
        records = promotion_models.GetRedEnvelopeRecord.objects.filter(owner=request.manager)
        rule_id2count = {}
        for record in records:
            if rule_id2count.has_key(record.red_envelope_rule_id):
                rule_id2count[record.red_envelope_rule_id] += 1
            else:
                rule_id2count[record.red_envelope_rule_id] = 1

        for rule in rules:
            remained_count = id2coupon_rule[rule.coupon_rule_id].remained_count
            is_timeout = False if rule.end_time > datetime.now() else True
            is_warring = False
            if remained_count <= 20:
                if rule.receive_method:
                    if rule.limit_time:
                        is_warring = True
                    else:
                        if not is_timeout:
                            is_warring = True
                else:
                    if rule.status:
                        if rule.limit_time:
                            is_warring = True
                        else:
                            if not is_timeout:
                                is_warring = True
            data = {
                "id": rule.id,
                "rule_name": rule.name,
                "limit_time": rule.limit_time,
                "start_time": rule.start_time.strftime("%Y/%m/%d %H:%M:%S"),
                "end_time": rule.end_time.strftime("%Y/%m/%d %H:%M:%S"),
                "coupon_rule_name": id2coupon_rule[rule.coupon_rule_id].name,
                "status": rule.status,
                "get_count": rule_id2count[rule.id] if rule_id2count.has_key(rule.id) else 0,
                "remained_count": remained_count,
                "is_timeout": is_timeout,
                "receive_method": rule.receive_method,
                "is_warring": is_warring
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