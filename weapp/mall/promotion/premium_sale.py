# -*- coding: utf-8 -*-
import json
from datetime import datetime
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from core import resource
from core.jsonresponse import create_response
from mall import export
from mall.promotion import models  # 注意：不要覆盖此module
from modules.member.models import MemberGrade


class PremiumSaleList(resource.Resource):
    app = 'mall2'
    resource = 'premium_sale_list'

    @login_required
    def get(request):
        """获得买赠列表.
        """
        endDate = request.GET.get('endDate', '')
        if endDate:
            endDate +=' 00:00'
        c = RequestContext(request, {
            'first_nav_name': export.MALL_PROMOTION_AND_APPS_FIRST_NAV,
            'second_navs': export.get_promotion_and_apps_second_navs(request),
            'second_nav_name': export.MALL_PROMOTION_SECOND_NAV,
            'third_nav_name': export.MALL_PROMOTION_PREMIUM_SALE_NAV,
            'endDate': endDate,
            'promotion_status': request.GET.get('status', '-1')
        })

        return render_to_response('mall/editor/promotion/premium_sales.html', c)


class PremiumSale(resource.Resource):
    app = 'mall2'
    resource = 'premium_sale'

    @login_required
    def get(request):
        """添加买赠
        """
        _type = request.GET.get('type')
        if not _type:
            promotion_id = request.GET['id']
            promotion = models.Promotion.objects.get(
                owner=request.manager,
                type=models.PROMOTION_TYPE_PREMIUM_SALE,
                id=promotion_id)
            models.Promotion.fill_details(request.manager, [promotion], {
                'with_product': True,
                'with_concrete_promotion': True
            })

            for product in promotion.products:
                product.models = product.models[1:]

            if promotion.member_grade_id:
                try:
                    promotion.member_grade_name = MemberGrade.objects.get(
                        id=promotion.member_grade_id).name
                except:
                    promotion.member_grade_name = MemberGrade.get_default_grade(
                        request.user_profile.webapp_id).name

            jsons = [{
                "name": "primary_product_models",
                "content": promotion.products[0].models
            }, {
                "name": "premium_products",
                "content": promotion.detail['premium_products']
            }]

            c = RequestContext(request, {
                'first_nav_name': export.MALL_PROMOTION_AND_APPS_FIRST_NAV,
                'second_navs': export.get_promotion_and_apps_second_navs(request),
                'second_nav_name': export.MALL_PROMOTION_SECOND_NAV,
                'third_nav_name': export.MALL_PROMOTION_PREMIUM_SALE_NAV,
                'promotion': promotion,
                'jsons': jsons
            })

            return render_to_response('mall/editor/promotion/premium_sale_detail.html', c)

        elif _type == 'create':
            member_grades = MemberGrade.get_all_grades_list(
                request.user_profile.webapp_id)

            c = RequestContext(request, {
                'member_grades': member_grades,
                'first_nav_name': export.MALL_PROMOTION_AND_APPS_FIRST_NAV,
                'second_navs': export.get_promotion_and_apps_second_navs(request),
                'second_nav_name': export.MALL_PROMOTION_SECOND_NAV,
                'third_nav_name': export.MALL_PROMOTION_PREMIUM_SALE_NAV
            })

            return render_to_response('mall/editor/promotion/create_premium_sale.html', c)
        # elif _type == 'copy':
        #     promotion_id = request.GET['id']
        #     promotion = models.Promotion.objects.get(id=promotion_id)
        #     models.Promotion.fill_details(request.manager, [promotion], {
        #         'with_concrete_promotion': True,
        #         'with_product': True
        #     })

        #     products_json = []
        #     for product in promotion.products:
        #         products_json.append(product.format_to_dict())

        #     premium_products_json = []
        #     for product in promotion.detail['premium_products']:
        #         premium_products_json.append(product)

        #     jsons = [{
        #         "name": 'products',
        #         "content": products_json
        #     }, {
        #         "name": 'premium_products',
        #         "content": premium_products_json
        #     }]

        #     c = RequestContext(request, {
        #         'first_nav_name': export.MALL_PROMOTION_AND_APPS_FIRST_NAV,
        #         'second_navs': export.get_promotion_and_apps_second_navs(request),
        #         'second_nav_name': export.MALL_PROMOTION_PREMIUM_SALE_NAV,
        #         'promotion': promotion,
        #         'jsons': jsons
        #     })

        # return
        # render_to_response('mall/editor/promotion/create_premium_sale.html',
        # c)

    @login_required
    def api_put(request):
        """创建买赠活动
        """
        premium_sale = models.PremiumSale.objects.create(
            owner=request.manager,
            count=request.POST.get('count', 1) or 1,
            is_enable_cycle_mode=(
                request.POST.get('is_enable_cycle_mode', 'false') == 'true')
        )

        now = datetime.today()
        start_date = datetime.strptime(
            request.POST.get('start_date', '2000-01-01 00:00'),
            '%Y-%m-%d %H:%M')
        # 当前实现了Promotion.update信号捕获更新缓存，因此数据插入时状态为活动未开始
        status = models.PROMOTION_STATUS_NOT_START
        promotion = models.Promotion.objects.create(
            owner=request.manager,
            type=models.PROMOTION_TYPE_PREMIUM_SALE,
            name=request.POST.get('name', ''),
            status=status,
            promotion_title=request.POST.get('promotion_title', ''),
            member_grade_id=request.POST.get('member_grade', 0),
            start_date=start_date,
            end_date=request.POST.get('end_date', '2000-01-01 00:00:00'),
            detail_id=premium_sale.id
        )

        # 处理主商品
        products = json.loads(request.POST.get('products', '[]'))
        product_ids = set([product['id'] for product in products])
        for product_id in product_ids:
            models.ProductHasPromotion.objects.create(
                product_id=product_id,
                promotion=promotion
            )

        # 处理赠品
        premium_products = json.loads(
            request.POST.get('premium_products', '[]'))
        for product in premium_products:
            models.PremiumSaleProduct.objects.create(
                owner=request.manager,
                premium_sale=premium_sale,
                product_id=product['id'],
                count=product['count'],
                unit=product['unit'],
            )

        if start_date <= now:
            promotion.status = models.PROMOTION_STATUS_STARTED
            promotion.save()
        response = create_response(200)
        return response.get_response()
