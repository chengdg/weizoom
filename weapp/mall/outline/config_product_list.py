#-*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from core import resource
from mall import export
from mall.models import MallConfig

class ConfigProductList(resource.Resource):
    app = 'mall2'
    resource = 'config_product_list'

    @login_required
    def get(request):
        try:
            mall_config = MallConfig.objects.get(owner=request.user)
        except:
            mall_config = MallConfig.objects.create(owner=request.user, order_expired_day=24)
        c = RequestContext(request, {
            'first_nav_name': export.MALL_HOME_FIRST_NAV,
            'second_navs': export.get_mall_home_second_navs(request),
            'second_nav_name': export.MALL_HOME_CONFIG_PRODUCT_LIST_NAV,
            'mall_config': mall_config
        })
        return render_to_response('mall/editor/config_product_list.html', c)

    @login_required
    def post(request):
        product_sales = int(request.POST.get('product_sales', '0'))
        product_sort = int(request.POST.get('product_sort', '0'))
        product_search = int(request.POST.get('product_search', '0'))
        shopping_cart = int(request.POST.get('shopping_cart', '0'))

        MallConfig.objects.filter(owner=request.user).update(
                show_product_sales=product_sales,
                show_product_sort=product_sort,
                show_product_search=product_search,
                show_shopping_cart=shopping_cart
            )
        mall_config = MallConfig.objects.get(owner=request.user)
        c = RequestContext(request, {
            'first_nav_name': export.MALL_HOME_FIRST_NAV,
            'second_navs': export.get_mall_home_second_navs(request),
            'second_nav_name': export.MALL_HOME_CONFIG_PRODUCT_LIST_NAV,
            'mall_config': mall_config
        })
        return render_to_response('mall/editor/config_product_list.html', c)