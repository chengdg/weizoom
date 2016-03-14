# -*- coding: utf-8 -*-
import json

from core import resource
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from mall import export
from django.shortcuts import render_to_response
from core.jsonresponse import JsonResponse, create_response


class OrderList(resource.Resource):
    """
    订单列表资源
    """
    app = "mall2"
    resource = "orders_to_money"

    @login_required
    def get(request):
        """
        显示订单列表

        """
        c = RequestContext(request, {
            'first_nav_name': export.ORDER_FIRST_NAV,
            'second_navs': export.get_mall_order_second_navs(request),
            'second_nav_name': export.ORDER_MONEY,
        })
        return render_to_response('mall/editor/orders_to_money.html', c)

    @login_required
    def api_get(request):
        import requests
        r = requests.get('http://dev.money.com/weapp/api/orders_to_money/', data={"user_id": request.user.id})
        response = create_response(200)
        response.data = json.loads(r.text)
        return response.get_jsonp_response(request)

class OrderMoneyList(resource.Resource):
    """
    订单列表资源
    """
    app = "mall2"
    resource = "cost_order_list"

    @login_required
    def get(request):
        """
        显示订单列表

        """
        c = RequestContext(request, {
            'first_nav_name': export.ORDER_FIRST_NAV,
            'second_navs': export.get_mall_order_second_navs(request),
            'second_nav_name': export.ORDER_MONEY,
        })
        return render_to_response('mall/editor/create_orders_to_money.html', c)

    @login_required
    def api_get(request):
        import requests
        r = requests.get('http://dev.money.com/weapp/cost_order_list/', data={"user_id": request.user.id})
        response = create_response(200)
        response.data = json.loads(r.text)
        return response.get_jsonp_response(request)




