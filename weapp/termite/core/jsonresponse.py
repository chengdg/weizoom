import json
import	copy
from datetime import date

from django.http import HttpResponse


class JsonResponse(dict):
	# Redefine to allow for nested attributes.
	# E.g. when calling the leaf attribute, text, in chart.title.text
	#      without previously defining the branch attribute, title.
	def __getattribute__(self, key):
		try:
			return dict.__getattribute__(self, key)
		except AttributeError:
			self.__dict__[key] = JsonResponse()
			return dict.__getattribute__(self, key)

	# This copy function is called when we want to get all the attributes of the 
	# chart instance so we can pass it off to cjson to create the JSON string.
	# Recursive trick to get leaf attributes.  Have to be careful of list types.
	# Also, replace certain underscored keys.
	# E.g. getting the leaf attribute, text, from the parent Chart instance where a  
	#      previous assignment was to chart.title.text
	def __copy__(self):
		attributes = dict()
		for key, value in self.__dict__.items():
			if isinstance(value, list):
				attributes[key] = [copy.copy(item) for item in value]
			else:
				attributes[key] = copy.copy(value)
		return attributes
	
	#copy all attributes in src into dst
	def copy(self, src, dst):
		if not dst in self.__dict__:
			self.__dict__[dst] = JsonResponse()
			
		dst = getattr(self, dst)
		for key, value in src.__dict__.items():
			if isinstance(value, date):
				value = str(value)
			setattr(dst, key, value)

	# Encode the chart attributes as JSON
	def get_response(self, attribute=None):
		attributes = copy.copy(self)
		if attribute:
			attributes = attributes[attribute]
		return HttpResponse(json.dumps(attributes), 'application/json; charset=utf-8')

	# Encode the chart attributes as JSON
	def get_jsonp_response(self, request, attribute=None):
		attributes = copy.copy(self)
		if attribute:
			attributes = attributes[attribute]

		callback = request.GET.get('callback', None)
		if callback:
			content = "%s(%s)" % (callback, json.dumps(attributes))
			return HttpResponse(content, 'application/json; charset=utf-8')
		else:
			return HttpResponse(json.dumps(attributes), 'application/json; charset=utf-8')

	# get raw JSON str
	def get_json(self, attribute=None):
		attributes = copy.copy(self)
		if attribute:
			attributes = attributes[attribute]
		return json.dumps(attributes)


def decode_json_str(str):
	return json.loads(str)


def create_response(code):
	response = JsonResponse()
	response.code = code
	response.errMsg = ""
	response.innerErrMsg = ""
	if code == 200:
		response.success = True
	response.data = JsonResponse()
	return response
