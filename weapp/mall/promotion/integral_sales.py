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
from modules.member.models import MemberGrade, IntegralStrategySttings


class IntegralSales(resource.Resource):
    app = 'mall2'
    resource = 'integral_sale'
    
    @login_required
    def get(request):
        promotion_id = request.GET.get('id', None)
        if promotion_id:
            promotion = promotion_models.Promotion.objects.get(owner=request.manager, type=promotion_models.PROMOTION_TYPE_INTEGRAL_SALE, id=promotion_id)
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
                    promotion.member_grade_name = MemberGrade.get_default_grade(request.manager_profile.webapp_id).name


            jsons = [{
                "name": "product_models",
                "content": promotion.products[0].models
            }]

            for rule in promotion.detail['rules']:
                if rule['member_grade_id'] > 0:
                    rule['member_grade_name'] = MemberGrade.objects.get(id=rule['member_grade_id']).name
                else:
                    rule['member_grade_name'] = '全部等级'

            c = RequestContext(request, {
                'first_nav_name': export.MALL_PROMOTION_FIRST_NAV,
                'second_navs': export.get_promotion_second_navs(request),
                'second_nav_name': export.MALL_PROMOTION_INTEGRAL_SALE_NAV,
                'promotion': promotion,
                'jsons': jsons
            })

            return render_to_response('mall/editor/promotion/integral_sale_detail.html', c)
        else:
            member_grades = MemberGrade.get_all_grades_list(request.user_profile.webapp_id)
            c = RequestContext(request, {
                'member_grades': member_grades,
                'first_nav_name': export.MALL_PROMOTION_FIRST_NAV,
                'second_navs': export.get_promotion_second_navs(request),
                'second_nav_name': export.MALL_PROMOTION_INTEGRAL_SALE_NAV,
            })

            return render_to_response('mall/editor/promotion/create_integral_sale.html', c)

    @login_required
    def api_put(request):
        integral_sale_type = promotion_models.INTEGRAL_SALE_TYPE_PARTIAL
        if integral_sale_type == promotion_models.INTEGRAL_SALE_TYPE_PARTIAL:
            discount = request.POST.get('discount', 100)
            discount_money = request.POST.get('discount_money', 0.0)
            integral_price = 0.0
        else:
            discount = 100
            discount_money = 0.0
            integral_price = request.POST.get('integral_price', 0.0)

        integral_sale = promotion_models.IntegralSale.objects.create(
            owner = request.manager,
            type = integral_sale_type,
            discount = 0,
            discount_money = 0.0,
            integral_price = 0,
            is_permanant_active = (request.POST.get('is_permanant_active', 'false') == 'true')
        )

        #创建integral rule
        rules = json.loads(request.POST.get('rules'))
        for rule in rules:
            promotion_models.IntegralSaleRule.objects.create(
                owner = request.manager,
                integral_sale = integral_sale,
                member_grade_id = rule['member_grade_id'],
                discount = rule['discount'],
                discount_money = rule['discount_money']
            )

        #创建promotion
        now = datetime.today()
        start_date = datetime.strptime(request.POST.get('start_date', '2000-01-01 00:00'), '%Y-%m-%d %H:%M')
        end_date = datetime.strptime(request.POST.get('end_date', '2000-01-01 00:00'), '%Y-%m-%d %H:%M')
        # 当前实现了Promotion.update信号捕获更新缓存，因此数据插入时状态为活动未开始
        status = promotion_models.PROMOTION_STATUS_NOT_START
        promotion = promotion_models.Promotion.objects.create(
            owner = request.manager,
            type = promotion_models.PROMOTION_TYPE_INTEGRAL_SALE,
            name = request.POST.get('name', ''),
            status = status,
            promotion_title = request.POST.get('promotion_title', ''),
            member_grade_id = 0,
            start_date = datetime.strptime('1900-01-01', '%Y-%m-%d') if integral_sale.is_permanant_active else start_date,
            end_date = datetime.strptime('2999-01-01', '%Y-%m-%d') if integral_sale.is_permanant_active else end_date,
            detail_id = integral_sale.id
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



class IntegralSaleList(resource.Resource):
    app = 'mall2'
    resource = 'integral_sales_list'

    @login_required
    def get(request):
        """获得限时抢购列表.
        """
        integral_strategy = IntegralStrategySttings.objects.get(webapp_id=request.user_profile.webapp_id)
        c = RequestContext(request, {
            'first_nav_name': export.MALL_PROMOTION_FIRST_NAV,
            'second_navs': export.get_promotion_second_navs(request),
            'second_nav_name': export.MALL_PROMOTION_INTEGRAL_SALE_NAV,
            'is_order_integral_open': integral_strategy.use_ceiling > 0
        })

        return render_to_response('mall/editor/promotion/integral_sales.html', c)
