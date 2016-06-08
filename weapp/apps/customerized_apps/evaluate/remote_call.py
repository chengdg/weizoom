# -*- coding: utf-8 -*-
from core import resource

class RemoteEvaluates(resource.Resource):
	"""
	为h5系统提供接口，获取评价数据
	"""
	app = 'apps/evaluate/remote'
	resource = 'get_evaluates'

	def get(request):
		"""
		获取单个商品的评价内容
		@return:
		"""
		pass