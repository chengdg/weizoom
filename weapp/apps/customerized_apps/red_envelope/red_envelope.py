# -*- coding: utf-8 -*-

from datetime import datetime

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from core import resource
from mall.promotion import models as promotion_models
from mall import export
from core.jsonresponse import create_response


COUNT_PER_PAGE = 20

FIRST_NAV_NAME  = export.MALL_PROMOTION_AND_APPS_FIRST_NAV


class RedEnvelopeRule(resource.Resource):
    app = "apps/red_envelope"
    resource = "red_envelope_rule"

    @login_required
    def get(request):
        """
        红包规则创建、查看页面
        """

        rule_id = request.GET.get('id', None)
        if rule_id:
            red_envelope_rule = promotion_models.RedEnvelopeRule.objects.get(id=rule_id)
            coupon_rule = promotion_models.CouponRule.objects.get(id=red_envelope_rule.coupon_rule_id)
            c = RequestContext(request, {
                'first_nav_name': FIRST_NAV_NAME,
                'second_navs': export.get_promotion_and_apps_second_navs(request),
                'second_nav_name': export.MALL_APPS_SECOND_NAV,
                'third_nav_name': export.MALL_APPS_RED_ENVELOPE_NAV,
                'coupon_rule': coupon_rule,
                'red_envelope_rule': red_envelope_rule,
            })
            return render_to_response('red_envelope/templates/editor/create_red_envelope_rule.html', c)
        else:
            coupon_rules = promotion_models.CouponRule.objects.filter(owner=request.manager, is_active=True,
                                                                      end_date__gt=datetime.now(), limit_counts=-1)
            c = RequestContext(request, {
                'first_nav_name': FIRST_NAV_NAME,
                'second_navs': export.get_promotion_and_apps_second_navs(request),
                'second_nav_name': export.MALL_APPS_SECOND_NAV,
                'third_nav_name': export.MALL_APPS_RED_ENVELOPE_NAV,
                'coupon_rules': coupon_rules
            })
            return render_to_response('red_envelope/templates/editor/create_red_envelope_rule.html', c)

    @login_required
    def api_post(request):
        """
        开启、关闭、删除红包规则
        """
        id = request.POST.get('id', 0)
        status = request.POST.get('status', None)
        # try:
        if status == 'over':
            promotion_models.RedEnvelopeRule.objects.filter(id=id).update(status=False)
        elif status == 'start':
            #除去图文领取的
            start_rule = promotion_models.RedEnvelopeRule.objects.filter(owner=request.manager, status=True, receive_method=False)
            if start_rule.count() > 0:
                response = create_response(500)
                response.errMsg = "请先关闭其他分享红包活动！"
                return response.get_response()
            promotion_models.RedEnvelopeRule.objects.filter(id=id).update(status=True)
        elif status == 'delete':
            promotion_models.RedEnvelopeRule.objects.filter(id=id).update(status=False, is_delete=True)
        # except:
        #     return create_response(500).get_response()
        return create_response(200).get_response()

    @login_required
    def api_put(request):
        limit_money = request.POST.get('limit_money', 0)
        status = False
        if not limit_money:
            limit_money = 0.0
        if request.POST.get('receive-method-order'):
            receive_method = False #下单领取
        else:
            receive_method = True
            status = True #图文领取-状态默认开启
        if request.POST.get('start_date', None) and request.POST.get('end_date', None):
            promotion_models.RedEnvelopeRule.objects.create(
                owner=request.user,
                name=request.POST.get('name', ''),
                coupon_rule_id=request.POST.get('coupon_rule', 0),
                start_time=request.POST.get('start_date'),
                end_time=request.POST.get('end_date'),
                receive_method = receive_method,
                status = status,
                limit_order_money=limit_money,
                use_info=request.POST.get('detail', ''),
                share_pic=request.POST.get('share_pic', ''),
                share_title=request.POST.get('remark', '')
            )
        else:
            promotion_models.RedEnvelopeRule.objects.create(
                owner=request.user,
                name=request.POST.get('name', ''),
                coupon_rule_id=request.POST.get('coupon_rule', 0),
                limit_time=True,
                receive_method = receive_method,
                status = status,
                limit_order_money=limit_money,
                use_info=request.POST.get('detail', ''),
                share_pic=request.POST.get('share_pic', ''),
                share_title=request.POST.get('remark', '')
            )

        return create_response(200).get_response()
