# -*- coding: utf-8 -*-
import json

from core import resource
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from mall import export
from django.shortcuts import render_to_response
from core.jsonresponse import JsonResponse, create_response
from weapp import settings
import requests


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
        r = requests.get(settings.MONEY_HOST + '/weapp/api/orders_to_money/', params={"user_id": request.user.id})
        if r.status_code == 200:
            response = create_response(200)
            response.data = json.loads(r.text)
        else:
            response = create_response(500)
            response.data.erMg = u'请求失败'
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
        r = requests.get(settings.MONEY_HOST + '/weapp/cost_order_list/', params={"user_id": request.user.id})
        response = create_response(200)
        response.data = json.loads(r.text)
        return response.get_jsonp_response(request)

class ReOrderMoneyList(resource.Resource):
    """
    订单列表资源
    """
    app = "mall2"
    resource = "re_submit_list"

    @login_required
    def get(request):
        """
        显示订单列表

        """
        cost_id = request.GET.get('cost_id', '')
        c = RequestContext(request, {
            'first_nav_name': export.ORDER_FIRST_NAV,
            'second_navs': export.get_mall_order_second_navs(request),
            'second_nav_name': export.ORDER_MONEY,
            'cost_id': cost_id
        })
        return render_to_response('mall/editor/create_orders_to_money.html', c)

    @login_required
    def api_get(request):
        import requests
        cost_id = request.GET.get('cost_id', '')
        r = requests.get(settings.MONEY_HOST + '/weapp/re_submit_list/', params={"user_id": request.user.id, "cost_id": cost_id})
        response = create_response(200)
        response.data = json.loads(r.text)
        return response.get_jsonp_response(request)


class OrderMoneyViewList(resource.Resource):
    """
    订单列表资源
    """
    app = "mall2"
    resource = "cost_view_list"

    @login_required
    def get(request):
        """
        显示订单列表

        """
        cost_id = request.GET.get('cost_id', '')
        cost_status = request.GET.get('cost_status','')
        is_weapp = request.GET.get('is_weapp', '')
        c = RequestContext(request, {
            'first_nav_name': export.ORDER_FIRST_NAV,
            'second_navs': export.get_mall_order_second_navs(request),
            'second_nav_name': export.ORDER_MONEY,
            'cost_id': cost_id,
            'cost_status': cost_status,
            'is_weapp': is_weapp
        })
        return render_to_response('mall/editor/create_orders_to_money.html', c)

    @login_required
    def api_get(request):
        cost_id = request.GET.get('cost_id', '')
        cost_status = request.GET.get('cost_status', '')
        is_weapp = request.GET.get('is_weapp', '')
        r = requests.get(settings.MONEY_HOST + '/weapp/cost_view_list/', params={"user_id": request.user.id, "cost_id": cost_id, "cost_status": cost_status,"is_weapp": is_weapp})
        response = create_response(200)
        response.data = json.loads(r.text)
        return response.get_jsonp_response(request)





