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


class FlashSale(resource.Resource):
    app = 'mall2'
    resource = 'flash_sale'

    @login_required
    def get(request):
        """
        浏览限时抢购详情.
        """
        _type = request.GET.get('type')
        if not _type:
            promotion_id = request.GET['id']
            promotion = models.Promotion.objects.get(
                owner=request.manager,
                type=models.PROMOTION_TYPE_FLASH_SALE,
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
                "name": "product_models",
                "content": promotion.products[0].models
            }]

            c = RequestContext(request, {
                'first_nav_name': export.MALL_PROMOTION_AND_APPS_FIRST_NAV,
                'second_navs': export.get_promotion_and_apps_second_navs(request),
                'second_nav_name': export.MALL_PROMOTION_SECOND_NAV,
                'third_nav_name': export.MALL_PROMOTION_FLASH_SALE_NAV,
                'promotion': promotion,
                'jsons': jsons
            })

            return render_to_response('mall/editor/promotion/flash_sale_detail.html', c)
        elif _type == 'copy':
            """
            拷贝限时抢购

            @param id: promotion_id

            """
            promotion_id = request.GET['id']
            promotion = models.Promotion.objects.get(id=promotion_id)
            models.Promotion.fill_details(request.manager, [promotion], {
                'with_concrete_promotion': True
            })

            c = RequestContext(request, {
                'first_nav_name': export.MALL_PROMOTION_AND_APPS_FIRST_NAV,
                'second_navs': export.get_promotion_and_apps_second_navs(request),
                'second_nav_name': export.MALL_PROMOTION_SECOND_NAV,
                'third_nav_name': export.MALL_PROMOTION_FLASH_SALE_NAV,
                'promotion': promotion
            })

            return render_to_response('mall/editor/promotion/create_flash_sale.html', c)
        elif _type == 'create':
            member_grades = MemberGrade.get_all_grades_list(
                request.user_profile.webapp_id
            )

            c = RequestContext(request, {
                'member_grades': member_grades,
                'first_nav_name': export.MALL_PROMOTION_AND_APPS_FIRST_NAV,
                'second_navs': export.get_promotion_and_apps_second_navs(request),
                'second_nav_name': export.MALL_PROMOTION_SECOND_NAV,
                'third_nav_name': export.MALL_PROMOTION_FLASH_SALE_NAV
            })

            return render_to_response('mall/editor/promotion/create_flash_sale.html', c)


    @login_required
    def api_put(request):
        """
        创建限时抢购
        """

        count_per_purchase = request.POST.get('count_per_purchase', 9999999)
        if not count_per_purchase:
            count_per_purchase = 9999999
        limit_period = request.POST.get('limit_period', 0)
        if not limit_period:
            limit_period = 0
        flash_sale = models.FlashSale.objects.create(
            owner=request.manager,
            limit_period=limit_period,
            promotion_price=request.POST.get('promotion_price', 0.0),
            count_per_purchase=count_per_purchase,
            count_per_period=int(request.POST.get('count_per_period', 0))
        )
        now = datetime.today()
        start_date = datetime.strptime(
            request.POST.get('start_date', '2000-01-01 00:00'),
            '%Y-%m-%d %H:%M'
        )
        # 当前实现了Promotion.update信号捕获更新缓存，因此数据插入时状态为活动未开始
        status = models.PROMOTION_STATUS_NOT_START
        promotion = models.Promotion.objects.create(
            owner=request.manager,
            type=models.PROMOTION_TYPE_FLASH_SALE,
            name=request.POST.get('name', ''),
            promotion_title=request.POST.get('promotion_title', ''),
            status=status,
            member_grade_id=request.POST.get('member_grade', 0),
            start_date=start_date,
            end_date=request.POST.get('end_date', '2000-01-01 00:00:00'),
            detail_id=flash_sale.id
        )

        products = json.loads(request.POST['products'])
        product_ids = set([product['id'] for product in products])
        for product_id in product_ids:
            models.ProductHasPromotion.objects.create(
                product_id=product_id,
                promotion=promotion
            )

        if start_date <= now:
            promotion.status = models.PROMOTION_STATUS_STARTED
            promotion.save()
        response = create_response(200)
        return response.get_response()

    @login_required
    def put(request):
        """添加限时抢购
        """
        member_grades = MemberGrade.get_all_grades_list(
            request.user_profile.webapp_id)

        c = RequestContext(request, {
            'member_grades': member_grades,
            'first_nav_name': export.MALL_PROMOTION_AND_APPS_FIRST_NAV,
            'second_navs': export.get_promotion_and_apps_second_navs(request),
            'second_nav_name': export.MALL_PROMOTION_SECOND_NAV,
            'third_nav_name': export.MALL_PROMOTION_FLASH_SALE_NAV
        })

        return render_to_response('mall/editor/promotion/create_flash_sale.html', c)


class FlashSaleList(resource.Resource):
    app = 'mall2'
    resource = 'flash_sale_list'

    @login_required
    def get(request):
        """获得限时抢购列表.
        """
        endDate = request.GET.get('endDate', '')
        if endDate:
            endDate +=' 00:00'
        c = RequestContext(request, {
            'first_nav_name': export.MALL_PROMOTION_AND_APPS_FIRST_NAV,
            'second_navs': export.get_promotion_and_apps_second_navs(request),
            'second_nav_name': export.MALL_PROMOTION_SECOND_NAV,
            'third_nav_name': export.MALL_PROMOTION_FLASH_SALE_NAV,
            'endDate': endDate,
            'promotion_status': request.GET.get('status', '-1')
        })

        return render_to_response('mall/editor/promotion/flash_sales.html', c)
