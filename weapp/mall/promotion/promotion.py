# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.decorators import login_required

from core import resource, paginator
from core.jsonresponse import create_response
from mall import export
from mall.promotion import models  # 注意：不要覆盖此module
from mall.models import PRODUCT_SHELVE_TYPE_ON
from .utils import filter_promotions


class Promotion(resource.Resource):
    app = 'mall2'
    resource = 'promotion'

    @login_required
    def api_get(request):
        """
        获得促销活动可以选用的商品集合.

        @param type "usable_promotion_products" or "promotion_products"
        """
        promotion_product_type = request.GET.get('type', 'promotion_products')
        if promotion_product_type == 'usable_promotion_products':

            name = request.GET.get("name", "")
            barCode = request.GET.get("barCode", "")
            filter_type = request.GET.get('filter_type', "all")
            selectedProductIds = request.GET.get("selectedProductIds", "").split('_')
            products = models.Product.objects.filter(
                owner=request.manager,
                shelve_type=PRODUCT_SHELVE_TYPE_ON,
                is_deleted=False)
            if name:
                products = products.filter(name__contains=name)
            if barCode:
                products = products.filter(bar_code=barCode)
            if filter_type == 'flash_sale':
                products = products.filter(stocks__lt=2)

            # 进行分页
            count_per_page = int(request.GET.get('count_per_page', 10))
            cur_page = int(request.GET.get('page', '1'))
            pageinfo, products = paginator.paginate(
                products, cur_page, count_per_page,
                query_string=request.META['QUERY_STRING'])

            products = list(products)
            models.Product.fill_details(request.manager,
                                        products,
                                        {"with_product_model": True,
                                         "with_model_property_info": True,
                                         'with_sales': True})
            id2product = {}
            for product in products:
                data = product.format_to_dict()
                data['can_select'] = True
                id2product[product.id] = data

            #获得已经与promotion关联的product
            status_set = [
                models.PROMOTION_STATUS_NOT_START, 
                models.PROMOTION_STATUS_STARTED, 
                models.PROMOTION_STATUS_DISABLE, #手动失效的单品优惠券要等到过期后才能创建买赠或限时抢购 duhao 2015-08-18
            ]

            if filter_type == 'integral_sale':
                promotions = models.Promotion.objects.filter(
                    owner=request.manager,
                    type=models.PROMOTION_TYPE_INTEGRAL_SALE,
                    status__in=status_set)
            else:
                promotions = models.Promotion.objects.filter(
                    Q(owner=request.manager) &
                    ~Q(type=models.PROMOTION_TYPE_INTEGRAL_SALE) &
                    Q(status__in=status_set))

            id2promotion = {}
            promotion_ids = []
            for promotion in promotions:
                #手动失效的单品优惠券要等到过期后才能创建买赠或限时抢购
                if promotion.status == models.PROMOTION_STATUS_DISABLE:
                    now = datetime.now()
                    if now > promotion.end_date:
                        continue

                id2promotion[promotion.id] = promotion
                promotion_ids.append(promotion.id)

            # id2promotion = dict([(promotion.id, promotion) for promotion in promotions])
            # promotion_ids = [promotion.id for promotion in promotions]
            php = models.ProductHasPromotion.objects.filter(promotion_id__in=promotion_ids)
            for relation in php:
                product_id = relation.product_id
                product_data = id2product.get(product_id, None)
                if not product_data:
                    continue
                promotion = id2promotion.get(relation.promotion_id, None)
                if promotion:
                    product_data['promotion_name'] = promotion.name
                product_data['can_select'] = False

            # 将已选择的商品id改为 can_select 改为 False
            for product_id in selectedProductIds:
                try:
                    product_data = id2product.get(int(product_id), None)
                    if not product_data:
                        continue
                    product_data['can_select'] = False
                except:
                    pass

            items = id2product.values()
            items.sort(lambda x, y: cmp(x['id'], y['id']))

            data = {
                "items": items,
                'pageinfo': paginator.to_dict(pageinfo),
                'sortAttr': 'id',
                'data': {}
            }
        elif promotion_product_type == 'promotion_products':
            promotion_id = request.GET['id']
            promotion = models.Promotion.objects.get(id=promotion_id)
            models.Promotion.fill_details(request.manager, [promotion], {
                'with_product': True
            })

            data = []
            for product in promotion.products:
                data.append({
                    "id": product.id,
                    "name": product.name,
                    "thumbnails_url": product.thumbnails_url,
                    "bar_code": product.bar_code,
                    "stocks": product.stocks,
                    "sales": -1,
                    "display_price": product.display_price,
                    "display_price_range": product.display_price_range,
                    "is_use_custom_model": product.is_use_custom_model,
                    "current_used_model": product.current_used_model,
                    "standard_model": product.standard_model,
                    "models": product.models[1:]
                })
        else:
            return create_response(500)
        response = create_response(200)
        response.data = data
        return response.get_response()

    @login_required
    def api_post(request):
        """
        结束促销活动

        @todo 其实应该用DELETE之类的method。
        """
        promotion_type = models.PROMOTIONSTR2TYPE[request.POST['type']]

        ids = request.POST.getlist('ids[]')
        start = request.POST.get('start', '')
        status = None
        if start == 'true':
            status = models.PROMOTION_STATUS_STARTED
        elif promotion_type == models.PROMOTION_TYPE_COUPON:
            status = models.PROMOTION_STATUS_DISABLE
        else:
            status = models.PROMOTION_STATUS_FINISHED
        # TODO 确认 结束促销的逻辑是在task里运行的，此处是否可以移动到 start == 'true' 的判断分支下
        models.Promotion.objects.filter(
            owner=request.manager,
            id__in=ids
        ).update(status=status)
        if promotion_type == models.PROMOTION_TYPE_COUPON:
            # 处理优惠券相关状态 
            ruleIds = [i.detail_id for i in models.Promotion.objects.filter(
                owner=request.manager,
                id__in=ids)
            ]
            models.CouponRule.objects.filter(
                owner=request.manager,
                id__in=ruleIds
            ).update(is_active=False, remained_count=0)

            models.Coupon.objects.filter(
                owner=request.manager,
                coupon_rule_id__in=ruleIds,
                status=models.COUPON_STATUS_UNGOT
            ).update(status=models.COUPON_STATUS_Expired)

        if start == 'true':
            pass
        else:
            #发送finish_promotion event
            from webapp.handlers import event_handler_util
            event_data = {
               "id": ','.join(ids),
               "type": promotion_type
            }
            event_handler_util.handle(event_data, 'finish_promotion')

        response = create_response(200)
        return response.get_response()

    @login_required
    def api_delete(request):
        """删除促销活动.

        """
        promotion_type = models.PROMOTIONSTR2TYPE[request.POST['type']]
        ids = request.POST.getlist('ids[]')
        if promotion_type == models.PROMOTION_TYPE_ALL:
            models.Promotion.objects.filter(
                owner=request.manager, id__in=ids
            ).update(status=models.PROMOTION_STATUS_DELETED)
        else:
            models.Promotion.objects.filter(
                owner=request.manager, type=promotion_type, id__in=ids
            ).update(status=models.PROMOTION_STATUS_DELETED)

        response = create_response(200)
        return response.get_response()


class PromotionList(resource.Resource):
    app = 'mall2'
    resource = 'promotion_list'

    @login_required
    def get(request):
        c = RequestContext(request, {
            'first_nav_name': export.MALL_PROMOTION_FIRST_NAV,
            'second_navs': export.get_promotion_second_navs(request),
            'second_nav_name': export.MALL_PROMOTION_PROMOTIONS_NAV
        })

        return render_to_response('mall/editor/promotion/promotions.html', c)

    @login_required
    def api_get(request):
        COUNT_PER_PAGE = 10
        """获得促销活动集合.
        """
        name = request.GET.get('name', '')
        bar_code = request.GET.get('barCode', '')
        promotion_status = int(request.GET.get('promotionStatus', -1))
        start_date = request.GET.get('startDate', '')
        end_date = request.GET.get('endDate', '')
        type_str = request.GET.get('type', 'all')
        coupon_id = request.GET.get('couponId', '')
        promotion_type = models.PROMOTIONSTR2TYPE[type_str]

        is_fetch_all_promotions = ((not name) and
                                   (not bar_code) and
                                   (not start_date) and
                                   (not end_date) and
                                   (not coupon_id) and
                                   (promotion_status == -1) and
                                   (promotion_type == 'all'))
        if is_fetch_all_promotions:
            #获取promotion列表
            if promotion_type == models.PROMOTION_TYPE_ALL:
                # 全部类型不查询优惠券数据
                promotions = models.Promotion.objects.filter(
                    Q(owner=request.manager) &
                    ~Q(status=models.PROMOTION_STATUS_DELETED) &
                    Q(type=models.PROMOTION_TYPE_COUPON)
                ).order_by('-id')
            else:
                promotions = models.Promotion.objects.filter(
                    Q(owner=request.manager) &
                    Q(type=promotion_type) &
                    ~Q(status=models.PROMOTION_STATUS_DELETED)
                ).order_by('-id')

            #进行分页
            count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
            cur_page = int(request.GET.get('page', '1'))
            pageinfo, promotions = paginator.paginate(
                promotions, cur_page,
                count_per_page, query_string=request.META['QUERY_STRING'])
            models.Promotion.fill_details(request.manager,
                                          promotions,
                                          {'with_product': True,
                                           'with_concrete_promotion': True})
        else:
            #获得promotion集合并过滤
            if promotion_type == models.PROMOTION_TYPE_ALL:
                # 全部类型不查询优惠券数据
                promotions = models.Promotion.objects.filter(
                    Q(owner=request.manager) &
                    ~Q(status=models.PROMOTION_STATUS_DELETED) &
                    ~Q(type=models.PROMOTION_TYPE_COUPON)
                ).order_by('-id')
            else:
                promotions = models.Promotion.objects.filter(
                    Q(owner=request.manager, type=promotion_type) &
                    ~Q(status=models.PROMOTION_STATUS_DELETED)
                ).order_by('-id')

            promotions = filter_promotions(request, promotions)

            #
            if coupon_id:
                coupon_rule_id2promotion = dict([(promotion.detail_id, promotion) for promotion in promotions])
                coupon = models.Coupon.objects.filter(coupon_id=coupon_id)
                if coupon.count() > 0:
                    try:
                        promotions = [
                            coupon_rule_id2promotion[coupon[0].coupon_rule_id]
                        ]
                    except KeyError:
                        promotions = []
                else:
                    promotions = []

            # 进行分页
            count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
            cur_page = int(request.GET.get('page', '1'))
            pageinfo, promotions = paginator.paginate(
                promotions, cur_page, count_per_page,
                query_string=request.META['QUERY_STRING'])
            models.Promotion.fill_details(request.manager, promotions, {
                'with_product': True,
                'with_concrete_promotion': True
            })

        #获取返回数据
        items = []
        for promotion in promotions:
            if promotion.detail.get('money'):
                promotion.detail['money'] = str(promotion.detail['money'])
            data = {
                "id": promotion.id,
                "status": promotion.status_name,
                "name": promotion.name,
                "promotionTitle": promotion.promotion_title,
                "type": models.PROMOTION2TYPE[promotion.type],
                "start_date": promotion.start_date,
                "end_date": promotion.end_date,
                "created_at": promotion.created_at,
                "detail": promotion.detail,
                "products": []
            }
            if hasattr(promotion, 'products'):
                for product in promotion.products:
                    data["products"].append({
                        'id': product.id,
                        'name': product.name,
                        'thumbnails_url': product.thumbnails_url,
                        'display_price': product.display_price,
                        'display_price_range': product.display_price_range,
                        'bar_code': product.bar_code,
                        'stocks': product.stocks,
                        'sales': product.sales,
                        'is_use_custom_model': product.is_use_custom_model,
                        'models': product.models[1:],
                        'standard_model': product.standard_model,
                        'current_used_model': product.current_used_model,
                        'created_at': datetime.strftime(product.created_at, '%Y-%m-%d %H:%M'),
                        "detail_link": '/mall2/product/?id=%d&source=onshelf' % product.id
                    })

                if len(data['products']) == 1:
                    data['product'] = data['products'][0]
                else:
                    data['product'] = []
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
