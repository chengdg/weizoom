# -*- coding: utf-8 -*-
__author__ = 'Administrator'
from core import resource
from core import paginator
import wapi as api_resource
from core.jsonresponse import create_response

import datetime as dt
# from wapi.models import SupplierOAuthToken
from eaglet.utils.resource_client import Resource
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
        order_status = request.POST.get('order_status','')
        order_id = request.POST.get('order_id','')
        cur_page = request.POST.get('cur_page',1)
        supplier_id = request.POST.get('supplier_id',0)
        if supplier_id:
            now = dt.datetime.now()
            tokens = api_resource.models.SupplierOAuthToken.objects.filter(supplier_id=supplier_id, access_token=access_token, expire_time__gt=now)
            data = {
                'supplier_ids': supplier_id,
                'page': cur_page,
                'count_per_page': 10, #暂定每页10条
                'order_id': order_id,
                'start_time': found_begin_time,
                'end_time': found_end_time,
                'status': order_status,
                }
            if tokens.count() > 0:
                resp = Resource.use('zeus').get({
                    'resource':'panda.order_list_by_supplier',
                    'data': data
                    })
                if resp and resp['code'] == 200:
                    data = resp['data']
                    response.data['pageinfo'] = data['pageinfo']
                    response.data['items'] = data['orders']
                    return response.get_response()

            #     else:
            #         return {'message': 'system error, please connect administrator'}
            # else:
            #     return {'message': 'access_token error'}


        orders,pageinfo,count = api_resource.get('open', 'orders', {'access_token':access_token,
													 'found_begin_time':found_begin_time,
													 'found_end_time':found_end_time,
													 'pay_begin_time':pay_begin_time,
													 'pay_end_time':pay_end_time,
                                                     'order_status':order_status,
                                                     'order_id':order_id,
                                                     'cur_page':cur_page
                                                      })
        response.data = {}
        response.data['pageinfo'] = paginator.to_dict(pageinfo)
        response.data['count'] = count
        response.data['items'] = orders
        return response.get_response()


