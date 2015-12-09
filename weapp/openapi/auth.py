# -*- coding: utf-8 -*-
__author__ = 'Administrator'
from core import resource
import wapi as api_resource
from core.jsonresponse import create_response

class Auth(resource.Resource):
    """
    订单列表资源
    """
    app = "openapi"
    resource = "auth"


    def post(request):

		response = create_response(200)
		response.data = []
		username = request.POST.get('username','')
		password = request.POST.get('password','')
		auth = api_resource.post('open', 'auth_token', {'username':username,'password':password})
		response.data = auth
		return response.get_response()


