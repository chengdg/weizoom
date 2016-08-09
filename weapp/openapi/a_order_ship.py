# -*- coding: utf-8 -*-
__author__ = 'Administrator'
from core import resource
import wapi as api_resource
from core.jsonresponse import create_response

class OrderShip(resource.Resource):
    """
    订单列表资源
    """
    app = "openapi"
    resource = "order_ship"

    def post(request):

		response = create_response(200)
		response.data = {}
		access_token = request.POST.get('access_token','')
		
		logistics_name = request.POST.get('logistics_name','')
		logistics_number = request.POST.get('logistics_number','')
		result = api_resource.post('open', 'order_ship', {'order_id':order_id,'logistics_number':logistics_number,
						'logistics_name':logistics_name,'access_token':access_token})
		print "reseult-------------------",result
		response.errMsg = result['err_msg']
		response.is_success = result['is_success']
		return response.get_response()