# -*- coding: utf-8 -*-
import json
from datetime import datetime
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from core import resource
from core.jsonresponse import create_response
from mall import export
from mall.promotion import models as promotion_models  # 注意：不要覆盖此module
from modules.member.models import MemberGrade


class PriceCut(resource.Resource):
    app = 'mall2'
    resource = 'price_cut'
    
    @login_required
    def get(request):
        promotion_id = request.GET.get('id', None)
        if promotion_id:
            promotion = promotion_models.Promotion.objects.get(owner=request.manager, type=promotion_models.PROMOTION_TYPE_PRICE_CUT, id=promotion_id)
            promotion_models.Promotion.fill_details(request.manager, [promotion], {
                'with_product': True,
                'with_concrete_promotion': True
            })

            for product in promotion.products:
                product.models = product.models[1:]

            if promotion.member_grade_id:
                try:
                    promotion.member_grade_name = MemberGrade.objects.get(id=promotion.member_grade_id).name
                except:
                    promotion.member_grade_name = MemberGrade.get_default_grade(request.user_profile.webapp_id).name


            jsons = [{
                "name": "product_models",
                "content": promotion.products[0].models
            }]

            c = RequestContext(request, {
                'first_nav_name': export.MALL_PROMOTION_FIRST_NAV,
                'second_navs': export.get_promotion_second_navs(request),
                'second_nav_name': export.MALL_PROMOTION_PRICE_CUT_NAV,
                'promotion': promotion,
                'jsons': jsons
            })

            return render_to_response('mall/editor/promotion/price_cut_detail.html', c)
        else:
            member_grades = MemberGrade.get_all_grades_list(request.user_profile.webapp_id)

            c = RequestContext(request, {
                'member_grades': member_grades,
                'first_nav_name': export.MALL_PROMOTION_FIRST_NAV,
                'second_navs': export.get_promotion_second_navs(request),
                'second_nav_name': export.MALL_PROMOTION_PRICE_CUT_NAV
            })

            return render_to_response('mall/editor/promotion/create_price_cut.html', c)

    @login_required
    def api_put(request):
        price_cut = promotion_models.PriceCut.objects.create(
            owner = request.manager,
            price_threshold = request.POST.get('price_threshold', 0),
            cut_money = request.POST.get('cut_money', 0),
            is_enable_cycle_mode = (request.POST.get('is_enable_cycle_mode', 'false') == 'true')
        )

        now = datetime.today()
        start_date = datetime.strptime(request.POST.get('start_date', '2000-01-01 00:00'), '%Y-%m-%d %H:%M')
        # 当前实现了Promotion.update信号捕获更新缓存，因此数据插入时状态为活动未开始
        status = promotion_models.PROMOTION_STATUS_NOT_START
        promotion = promotion_models.Promotion.objects.create(
            owner = request.manager,
            type = promotion_models.PROMOTION_TYPE_PRICE_CUT,
            name = request.POST.get('name', ''),
            status = status,
            promotion_title = request.POST.get('promotion_title', ''),
            member_grade_id = request.POST.get('member_grade', 0),
            start_date = start_date,
            end_date = request.POST.get('end_date', '2000-01-01 00:00:00'),
            detail_id = price_cut.id
        )

        products = json.loads(request.POST.get('products', '[]'))
        product_ids = set([product['id'] for product in products])
        for product_id in product_ids:
            promotion_models.ProductHasPromotion.objects.create(
                product_id = product_id,
                promotion = promotion
            )

        if start_date <= now:
            promotion.status = promotion_models.PROMOTION_STATUS_STARTED
            promotion.save()
        response = create_response(200)
        return response.get_response()


class PriceCutList(resource.Resource):
    app = 'mall2'
    resource = 'price_cut_list'

    @login_required
    def get(request):
        c = RequestContext(request, {
            'first_nav_name': export.MALL_PROMOTION_FIRST_NAV,
            'second_navs': export.get_promotion_second_navs(request),
            'second_nav_name': export.MALL_PROMOTION_PRICE_CUT_NAV
        })

        return render_to_response('mall/editor/promotion/price_cuts.html', c)
