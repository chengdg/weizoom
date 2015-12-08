# -*- coding: utf-8 -*-

from core import api_resource
#from core.jsonresponse import create_response
from wapi.decorators import param_required
from wapi.decorators import auth_required

class Sample(api_resource.ApiResource):
	"""
	演示API
	"""
	app = 'open'
	resource = 'sample'

	@auth_required
	#@param_required([])
	def get(args):
		"""
		输入用户名、授权密码获取授权token
		"""
		user = args['user']

		data = {
			'username': user.username,
			'is_active': user.is_active,
		}
		return data
