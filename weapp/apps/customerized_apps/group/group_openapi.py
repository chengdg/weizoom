# -*- coding: utf-8 -*-

import json
from datetime import datetime

from core import resource
from core import paginator
from core.jsonresponse import create_response

import models as app_models
from apps import request_util
from termite import pagestore as pagestore_manager

class GroupOpenAPI(resource.Resource):
	app = 'apps/group'
	resource = 'group_buy_product'

	def api_get(request):
		"""
		获取团购商品信息
		"""
		pid = request.GET.get('pid')
		record = app_models.Group.objects(product_id=pid,status=app_models.STATUS_RUNNING)
		if record.count() > 0:
			record = record.first()
			response = create_response(200)
			response.data = {
				'pid': pid,
				# 'group_id': group_id,
				# 'url': url
			}
		else:
			response = create_response(500)
			response.errMsg = u'该商品无进行中的团购活动'
			return response.get_response()
		return response.get_response()
