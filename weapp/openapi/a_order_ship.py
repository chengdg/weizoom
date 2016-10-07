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
		order_id = request.POST.get('order_id','')
		logistics_name = request.POST.get('logistics_name','')
		logistics_number = request.POST.get('logistics_number','')
		supplier_id = request.POST.get('supplier_id',0)
		if supplier_id:
			now = dt.datetime.now()
			tokens = SupplierOAuthToken.objects.filter(supplier_id=supplier_id, access_token=access_token, expire_time__gt=now)
			data = {
				 'express_company_name': logistics_name,
				 'express_number': logistics_number,
				 'order_id': order_id
				 }
			if tokens.count() > 0:
				resp = Resource.use('zeus').get({
					'resource':'mall.delivery',
					'data': data
					 })
				if resp and resp['code'] == 200:
					 
					is_success = resp['data']['result']
					msg = resp['data']['msg']
				else:
					is_success = False
					msg = 'system error, please connect administrator'
			else:
				is_success = False
				msg = 'access_token error'
			response.errMsg = msg
			response.is_success = is_success
			return response.get_response()
		result = api_resource.post('open', 'order_ship', {'order_id':order_id,'logistics_number':logistics_number,
						'logistics_name':logistics_name,'access_token':access_token})
		print "reseult-------------------",result
		response.errMsg = result['err_msg']
		response.is_success = result['is_success']
		return response.get_response()