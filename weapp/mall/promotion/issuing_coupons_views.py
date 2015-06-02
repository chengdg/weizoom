# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from core.restful_url_route import view

from mall import export

COUNT_PER_PAGE = 20
PROMOTION_TYPE_COUPON = 4
FIRST_NAV_NAME = export.MALL_PROMOTION_FIRST_NAV


@view(app='mall_promotion', resource='issuing_coupons_record', action='get')
@login_required
def list_issuing_coupons_record(request):
    """
    优惠券规则列表
    """
    print('-----------------------------------------')
    print(export.MALL_PROMOTION_ISSUING_COUPONS_NAV)
    c = RequestContext(request, {
        'first_nav_name': FIRST_NAV_NAME,
        'second_navs': export.get_promotion_second_navs(request),
        'second_nav_name': export.MALL_PROMOTION_ISSUING_COUPONS_NAV,
    })
    return render_to_response(
        'mall/editor/promotion/issuing_coupons_record.html',
        c)


@view(app='mall_promotion', resource='issuing_coupons_detail', action='get')
@login_required
def list_issuing_coupons_detail(request):
    """
    优惠券详情列表
    """
    record_id = request.GET.get('id', '0')

    c = RequestContext(request, {
        'first_nav_name': FIRST_NAV_NAME,
        'second_navs': export.get_promotion_second_navs(request),
        'second_nav_name': export.MALL_PROMOTION_ISSUING_COUPONS_NAV,
        'record_id': record_id,
    })
    return render_to_response(
        'mall/editor/promotion/issuing_coupons_detail.html',
        c)


@view(app='mall_promotion', resource='issuing_coupons_record', action='create')
@login_required
def create_issuing_coupons_record(request):
    """
    发放优惠券
    """
    c = RequestContext(request, {
        'first_nav_name': FIRST_NAV_NAME,
        'second_navs': export.get_promotion_second_navs(request),
        'second_nav_name': export.MALL_PROMOTION_ISSUING_COUPONS_NAV,
        'has_vip': False,
    })
    return render_to_response(
        'mall/editor/promotion/create_issuing_coupons_record.html',
        c
    )
