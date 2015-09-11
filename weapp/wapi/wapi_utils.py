#coding: utf8

from core.jsonresponse import create_response

def create_json_response(code, data):
	response = create_response(code)
	response.data = data
	return response.get_response()

