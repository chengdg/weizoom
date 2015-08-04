#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from core import resource
from mall import export
from mall.models import *


COUNT_PER_PAGE = 20
FIRST_NAV = export.ORDER_FIRST_NAV


class ExpiredTime(resource.Resource):
    """
    订单过期时间
    """
    app = "mall2"
    resource = "expired_time"

    @login_required
    def get(request):
        if MallConfig.objects.filter(owner=request.manager).count() == 0:
            MallConfig.objects.create(owner=request.use, order_expired_day=24)

        mall_config = MallConfig.objects.filter(owner=request.manager)[0]
        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV,
            'second_navs': export.get_orders_second_navs(request),
            'second_nav_name': export.ORDER_EXPIRED_TIME,
            'mall_config': mall_config,
        })
        return render_to_response('mall/editor/edit_expired_time.html', c)

    @login_required
    def post(request):
        if not request.POST.get('order_expired_day', 24):
            order_expired_day = 0
        else:
            order_expired_day = int(request.POST.get('order_expired_day', 24))
        if MallConfig.objects.filter(owner=request.manager).count() > 0:
            MallConfig.objects.filter(owner=request.manager).update(order_expired_day=order_expired_day)
        else:
            MallConfig.objects.create(owner=request.use, order_expired_day=24)

        mall_config = MallConfig.objects.filter(owner=request.manager)[0]
        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV,
            'second_navs': export.get_orders_second_navs(request),
            'second_nav_name': export.ORDER_EXPIRED_TIME,
            'mall_config': mall_config,
        })
        return render_to_response('mall/editor/edit_expired_time.html', c)
