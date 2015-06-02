# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required

from core.restful_url_route import view
from django.template import RequestContext
from django.shortcuts import render_to_response
from .models import ProductReview, Product, ProductReviewPicture
from . import export
from modules.member.models import Member

FIRST_NAV_NAME = export.PRODUCT_FIRST_NAV


@view(app='mall', resource='product_review', action='get')
@login_required
def get_list(request):
    '''

    商品评价列表
    '''
    c = RequestContext(request,
                       {
                           'first_nav_name': FIRST_NAV_NAME,
                           'second_navs': export.get_second_navs(request),
                           'second_nav_name': export.PRODUCT_REVIEW_NAV,
                       })
    return render_to_response(
        'mall/editor/product_review_list.html',
        c)


@view(app="mall", resource="product_review", action="update")
@login_required
def update_product_review(request):
    '''

    更新产品评价
    Precondition: product_review_id

    '''
    product_review_id = int(request.GET.get('id'))
    product_review = ProductReview.objects.get(id=product_review_id)
    product_review.product_name = Product.objects.get(id=product_review.product_id).name
    product_review.member_name = Member.objects.get(id=product_review.member_id).username_for_html
    product_review.pictures = [picture.att_url for picture in ProductReviewPicture.objects.filter(product_review_id=product_review.id)]
    c = RequestContext(request,
                       {
                           'first_nav_name': FIRST_NAV_NAME,
                           'second_navs': export.get_second_navs(request),
                           'second_nav_name': export.PRODUCT_REVIEW_NAV,
                           'product_review': product_review
                       })
    return render_to_response('mall/editor/product_review_update.html',c)