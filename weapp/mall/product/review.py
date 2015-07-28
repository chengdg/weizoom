# -*- coding: utf-8 -*-

from datetime import datetime

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from mall.models import ProductReview, Product, ProductReviewPicture
from mall import models as mall_models
from mall import export
from modules.member.models import Member
from core import resource
from modules.member.module_api import get_member_by_id_list
from core import paginator
from core.jsonresponse import create_response
from core import search_util

FIRST_NAV_NAME = export.PRODUCT_FIRST_NAV
COUNT_PER_PAGE = 2**32-1


REVIEW_FILTERS = {
    'review': [
        {
            'comparator': lambda review, filter_value: (filter_value == 'all') or (filter_value == review.status),
            'query_string_field': 'reviewStatus'
        }, {
            'comparator': lambda review, filter_value: (filter_value == 'all') or (
                filter_value == review.product_score),
            'query_string_field': 'productScore'
        }, {
            'comparator': lambda review, filter_value: filter_value <= review.created_at.strftime("%Y-%m-%d %H:%M"),
            'query_string_field': 'startDate'
        }, {
            'comparator': lambda review, filter_value: filter_value >= review.created_at.strftime("%Y-%m-%d %H:%M"),
            'query_string_field': 'endDate'
        }
    ],
    'product': [
        {
            'comparator': lambda product, filter_value: filter_value in product.name,
            'query_string_field': 'name'
        }
    ],
}


def _filter_reviews(request, reviews):
    # 处理商品名称、评论时间、审核状态、商品星级
    has_filter = search_util.init_filters(request, REVIEW_FILTERS)
    if not has_filter:
        # 没有filter，直接返回
        return reviews

    reviews = search_util.filter_objects(reviews, REVIEW_FILTERS['review'])
    product_id2review = dict([(review.product_id, review) for review in reviews])
    product_ids = product_id2review.keys()
    products = mall_models.Product.objects.filter(id__in=product_ids)
    products = search_util.filter_objects(products, REVIEW_FILTERS['product'])
    product_ids = [product.id for product in products]
    filter_reviews = []
    for review in reviews:
        if review.product_id in product_ids:
            filter_reviews.append(review)

    return filter_reviews


class ProductReviewInfo(resource.Resource):
    app = "mall2"
    resource = "product_review"

    """
    商品评价
    """

    @login_required
    def get(request):
        """
        商品评价详情页面
        """
        product_review_id = int(request.GET.get('id'))
        product_review = ProductReview.objects.get(id=product_review_id)
        product_review.product_name = Product.objects.get(id=product_review.product_id).name
        product_review.member_name = Member.objects.get(id=product_review.member_id).username_for_html
        product_review.pictures = [picture.att_url for picture in
                                   ProductReviewPicture.objects.filter(product_review_id=product_review.id)]
        c = RequestContext(request,
                           {
                               'first_nav_name': FIRST_NAV_NAME,
                               'second_navs': export.get_second_navs(request),
                               'second_nav_name': export.PRODUCT_REVIEW_NAV,
                               'product_review': product_review
                           })
        return render_to_response('mall/editor/product_review_update.html', c)

    @login_required
    def api_post(request):
        """
        更新评论的状态
        """
        # 单个修改
        if "product_review_id" in request.POST:

            product_review_id = request.POST.get("product_review_id", None)
            status = request.POST.get("status", None)
            from modules.member.integral import increase_member_integral
            from modules.member import models as member_models

            if product_review_id:
                review = mall_models.ProductReview.objects.filter(id=product_review_id)
                if status == '2' or status == '1':
                    if len(review) == 1 and int(review[0].status) == 0:
                        settings = member_models.IntegralStrategySttings.objects.get(
                            webapp_id=request.user_profile.webapp_id)
                        if settings.review_increase > 0:
                            member = member_models.Member.objects.get(id=review[0].member_id)
                            increase_member_integral(member, settings.review_increase, '商品评价奖励')

                if status == '2':
                    product_review = mall_models.ProductReview.objects.get(id=product_review_id)
                    top_reviews = mall_models.ProductReview.objects.filter(product_id=product_review.product_id,
                                                                           status=int(status)).order_by("top_time")
                    if top_reviews.count() >= 3:
                        ids = [review.id for review in top_reviews[:(top_reviews.count() - 2)]]
                        mall_models.ProductReview.objects.filter(id__in=ids).update(status=1,
                                                                                    top_time=mall_models.DEFAULT_DATETIME)
                        mall_models.ProductReview.objects.filter(id=product_review_id).update(status=int(status),
                                                                                              top_time=datetime.now())
                    else:
                        mall_models.ProductReview.objects.filter(id=product_review_id).update(status=int(status),
                                                                                              top_time=datetime.now())
                else:
                    review.update(status=int(status), top_time=mall_models.DEFAULT_DATETIME)
                return create_response(200).get_response()
            else:
                return create_response(500).get_response()
        # 批量修改
        else:
            ids = request.POST.get("ids", '')
            action = request.POST.get("action", '')
            ids = ids.split(',')
            from modules.member.integral import increase_member_integral
            from modules.member import models as member_models

            if action == 'pass':
                try:
                    reviews = mall_models.ProductReview.objects.filter(id__in=ids)

                    settings = member_models.IntegralStrategySttings.objects.get(
                        webapp_id=request.user_profile.webapp_id)
                    if settings.review_increase > 0:
                        # 处理增加积分
                        increase_integral_member_ids = []
                        for review in reviews:
                            if int(review.status) == 0:
                                increase_integral_member_ids.append(review.member_id)

                        if len(increase_integral_member_ids) > 0:
                            members = member_models.Member.objects.filter(id__in=increase_integral_member_ids)
                            id2member = dict((member.id, member) for member in members)
                            for review in reviews:
                                if int(review.status) == 0:
                                    increase_member_integral(id2member[review.member_id], settings.review_increase,
                                                             '商品评价奖励')
                    reviews.update(status=1, top_time=mall_models.DEFAULT_DATETIME)
                    return create_response(200).get_response()
                except:
                    return create_response(500).get_response()
            else:
                try:
                    mall_models.ProductReview.objects.filter(id__in=ids).update(status=-1)
                    return create_response(200).get_response()
                except:
                    return create_response(500).get_response()


class ProductReviewList(resource.Resource):
    app = "mall2"
    resource = "product_review_list"
    """
    商品评价列表
    """

    @login_required
    def get(request):
        """
        商品评价列表页面
        """
        c = RequestContext(request,
                           {
                               'first_nav_name': FIRST_NAV_NAME,
                               'second_navs': export.get_second_navs(request),
                               'second_nav_name': export.PRODUCT_REVIEW_NAV,
                           })

        return render_to_response('mall/editor/product_review_list.html', c)

    @login_required
    def api_get(request):
        """
        得到属于当前用户的所有评论过的商品的列表
        返回包含产品信息和产品评价的json
        advanced table
        """
        name = request.GET.get('name', '')
        user_code = request.GET.get('userCode', '')
        review_status = request.GET.get('reviewStatus', 'all')
        start_date = request.GET.get('startDate', '')
        end_date = request.GET.get('endDate', '')
        product_score = request.GET.get('productScore', '-1')

        is_fetch_all_reviews = (not name) and (not user_code) and (not start_date) and (not end_date) and (
            review_status == 'all') and (product_score == 'all')

        # 当前用户
        owner = request.manager
        all_reviews = mall_models.ProductReview.objects.filter(owner_id=owner.id).order_by("-created_at")

        if is_fetch_all_reviews:
            # 分页
            count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
            current_page = int(request.GET.get('page', '1'))
            pageinfo, product_reviews = paginator.paginate(all_reviews, current_page, count_per_page,
                                                           query_string=request.META['QUERY_STRING'])
        else:
            all_reviews = _filter_reviews(request, all_reviews)

            # 处理商品编码
            product_reviews = []
            if user_code:
                for review in all_reviews:
                    from cache import webapp_cache

                    review_product = mall_models.OrderHasProduct.objects.get(id=review.order_has_product_id)
                    product = webapp_cache.get_webapp_product_detail(request.webapp_owner_id, review.product_id)
                    product.fill_specific_model(review_product.product_model_name, product.models)
                    if product.model['user_code'] == user_code:
                        review.product_user_code = user_code
                        product_reviews.append(review)
            else:
                product_reviews = all_reviews

            count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
            current_page = int(request.GET.get('page', '1'))
            pageinfo, product_reviews = paginator.paginate(product_reviews, current_page, count_per_page,
                                                           query_string=request.META['QUERY_STRING'])


        # 处理商品
        product_ids = [review.product_id for review in product_reviews]
        id2product = dict([(product.id, product) for product in mall_models.Product.objects.filter(id__in=product_ids)])
        # 处理会员
        member_ids = [review.member_id for review in product_reviews]
        members = get_member_by_id_list(member_ids)
        member_id2member_name = dict([(m.id, m.username_for_html) for m in members])

        items = []
        from cache import webapp_cache

        reviewids = [r.order_has_product_id for r in product_reviews]
        orderhasproducts = mall_models.OrderHasProduct.objects.filter(id__in=reviewids)
        review2orderhasproductsmap = dict([(i.id, i) for i in orderhasproducts])

        for review in product_reviews:
            if not hasattr(review, 'product_user_code'):
                review_product = review2orderhasproductsmap[review.order_has_product_id]
                review.product_name = review_product.product_name
                review.product_model_name = review_product.product_model_name
                product = webapp_cache.get_webapp_product_detail(request.webapp_owner_id, review.product_id)
                product.fill_specific_model(review.product_model_name, product.models)
                review.product_user_code = product.model.get('user_code', '')
            items.append({
                'id': review.id,
                'product_user_code': review.product_user_code,
                'product_name': id2product[review.product_id].name,
                'user_name': member_id2member_name[review.member_id],
                'created_at': review.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'content': review.review_detail,
                'product_id': review.product_id,
                'member_id': review.member_id,
                'product_score': review.product_score,
                'status': {
                    'name': mall_models.PRODUCT_REVIEW_STATUS[int(review.status) + 1][1],  # 返回产品状态
                    'value': review.status,
                }
            })

        response = create_response(200)
        response.data = {
            'items': items,
            'pageinfo': paginator.to_dict(pageinfo),
            'sortAttr': '',
            'data': {},
        }
        return response.get_response()
