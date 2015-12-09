# -*- coding: utf-8 -*-
__author__ = 'Administrator'
from core import resource
import wapi as api_resource
from core.jsonresponse import create_response

class OrderList(resource.Resource):
    """
    订单列表资源
    """
    app = "openapi"
    resource = "order_list"

    def post(request):

        response = create_response(200)
        response.data = {}
        access_token = request.POST.get('access_token','')
        found_begin_time = request.POST.get('found_begin_time','')
        found_end_time = request.POST.get('found_end_time','')
        pay_begin_time = request.POST.get('pay_begin_time','')
        pay_end_time = request.POST.get('pay_end_time','')
        orders = api_resource.get('open', 'orders', {'access_token':access_token,
													 'found_begin_time':found_begin_time,
													 'found_end_time':found_end_time,
													 'pay_begin_time':pay_begin_time,
													 'pay_end_time':pay_end_time})
        response.data = orders
        return response.get_response()


