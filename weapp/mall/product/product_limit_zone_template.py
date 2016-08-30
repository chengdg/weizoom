# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from core import resource

from .. import export

class ProductLimitZoneTemplate(resource.Resource):
    app = 'mall2'
    resource = 'product_limit_zone_template'

    @login_required
    def get(request):
        """
        商品限购区域列表
        @return:
        """
        c = RequestContext(request, {
            'first_nav_name': export.PRODUCT_FIRST_NAV,
            'second_navs': export.get_mall_product_second_navs(request),
            'second_nav_name': export.PRODUCT_LIMIT_ZONE,
        })

        return render_to_response('mall/editor/product_limit_zone_template.html', c)

    @login_required
    def api_get(request):
        pass