# -*- coding: utf-8 -*-
__author__ = 'Administrator'
from core import resource
import wapi as api_resource
from core.jsonresponse import create_response

class OrderInfo(resource.Resource):
    """
    订单列表资源
    """
    app = "openapi"
    resource = "order_info"

    def post(request):

        response = create_response(200)
        response.data = {}
        access_token = request.POST.get('access_token','')
        order_id = request.POST.get('order_id','')
        order = api_resource.get('open', 'order', {'order_id':order_id,'access_token':access_token})
        response.data = order
        return response.get_response()


