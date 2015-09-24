# coding: utf8

import wapi

from core.jsonresponse import create_response
from core.exceptionutil import unicode_full_stack

def api_wrapper(request, app, resource):
	"""
	try:
		result = wapi.get(app, resource, request.REQUEST)
		response = create_response(200)
		response.data = result
		#except Exception,e:
	except:
		response = create_response(400)
		response.errMsg = u"出现错误"
		response.innerErrMsg = unicode_full_stack()
	"""
	result = wapi.get(app, resource, request.REQUEST)
	print("WAPI RESULT: {}".format(result))
	response = create_response(200)
	response.data = result
	return response.get_response()
