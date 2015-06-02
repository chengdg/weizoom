# -*- coding: utf-8 -*-

__author__ = 'robert'

import urllib2
import json

from urllib import urlencode

from jsonresponse import create_response_from_json_str


def is_satisfy_filter(obj, one_filter):
	"""
	判断一个对象是否符合一个filter
	"""
	filter_value = one_filter['value']
	if not filter_value:
		return True

	if not one_filter['comparator'](obj, filter_value):
		return False
	else:
		pass

	return True


def filter_objects(objects, filters):
	"""
	对一组数据进行filter操作
	"""
	filtered_objs = []
	for obj in objects:
		is_satisfy = True
		#检查是否满足每一个filter
		for one_filter in filters:
			if not is_satisfy_filter(obj, one_filter):
				is_satisfy = False
				break

		#如果不满足所有的filter，直接跳过该obj
		if not is_satisfy:
			continue

		filtered_objs.append(obj)

	return filtered_objs


def init_filters(request, scope2filters):
	"""
	初始化filter
	"""
	has_filter = False
	for scope, filters in scope2filters.items():
		for one_filter in filters:
			one_filter['value'] = request.GET.get(one_filter['query_string_field'], None)
			value = one_filter['value']
			if value and value != -1 and value != '-1':
				has_filter = True

	return has_filter