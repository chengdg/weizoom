# # -*- coding: utf-8 -*-

# from django.template import RequestContext
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render_to_response
# from core.restful_url_route import view

# from mall import export
# from .models import RedEnvelop
# COUNT_PER_PAGE = 20
# PROMOTION_TYPE_COUPON = 4
# FIRST_NAV_NAME = export.MALL_PROMOTION_FIRST_NAV


# @view(app='mall_promotion', resource='red_enevlop_record', action='get')
# @login_required
# def list_red_enevlop_record(request):
#     """
#     优惠券规则列表
#     """
#     c = RequestContext(request, {
#         'first_nav_name': FIRST_NAV_NAME,
#         'second_navs': export.get_promotion_second_navs(request),
#         'second_nav_name': export.MALL_PROMOTION_RED_ENVELOP_NAV,
#     })
#     return render_to_response('mall/editor/promotion/red_enevlop_record.html', c)


# @view(app='mall_promotion', resource='create_red_enevlop_record', action='get')
# @login_required
# def create_red_enevlop_record(request):
#     c = RequestContext(request, {
#         'first_nav_name': FIRST_NAV_NAME,
#         'second_navs': export.get_promotion_second_navs(request),
#         'second_nav_name': export.MALL_PROMOTION_RED_ENVELOP_NAV,
#     })
#     return render_to_response(
#         'mall/editor/promotion/create_red_enevlop_record.html',
#         c
#     )
