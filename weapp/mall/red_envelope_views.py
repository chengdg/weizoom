# -*- coding: utf-8 -*-
import json
from datetime import datetime

from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from core.restful_url_route import view

from promotion import models as promotion_models

import export

COUNT_PER_PAGE = 20
PROMOTION_TYPE_COUPON = 4
FIRST_NAV_NAME = export.ORDER_FIRST_NAV

@view(app="mall", resource="red_envelope_rule", action="get")
@login_required
def get_red_envelope_rule(request):
    """
    红包规则列表
    """
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

    c = RequestContext(request, {
        'first_nav_name': FIRST_NAV_NAME,
        'second_navs': export.get_promotion_second_navs(request),
        'second_nav_name': export.ORDER_RED_ENVELOPE,
        "coupon_rule_info": json.dumps(coupon_rule_info)
    })
    return render_to_response('mall/editor/red_envelope_rules.html',c)

@view(app="mall", resource="red_envelope_rule", action="create")
@login_required
def create_red_envelope_rule(request):
    """
    新建分享红包规则
    """
    coupon_rules = promotion_models.CouponRule.objects.filter(owner=request.manager, is_active=True, end_date__gt=datetime.now(), limit_counts=-1)
    c = RequestContext(request, {
        'first_nav_name': FIRST_NAV_NAME,
        'second_navs': export.get_orders_second_navs(request),
        'second_nav_name': export.ORDER_RED_ENVELOPE,
        'coupon_rules': coupon_rules
    })
    return render_to_response('mall/editor/create_red_envelope_rule.html',c)

@view(app="mall", resource="red_envelope_rule", action="select")
@login_required
def select_red_envelope_rule(request):
    """
    查看分享红包规则
    """
    id = request.GET.get('id', None)
    if id:
        red_envelope_rule = promotion_models.RedEnvelopeRule.objects.get(id=id)
        coupon_rule = promotion_models.CouponRule.objects.get(id=red_envelope_rule.coupon_rule_id)
        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV_NAME,
            'second_navs': export.get_orders_second_navs(request),
            'second_nav_name': export.ORDER_RED_ENVELOPE,
            'coupon_rule': coupon_rule,
            'red_envelope_rule': red_envelope_rule,
        })
        return render_to_response('mall/editor/create_red_envelope_rule.html',c)