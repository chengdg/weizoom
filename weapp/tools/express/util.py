# -*- coding: utf-8 -*-

import os
import json
from models import ExpressDetail

########################################################################
# get_express_company_json: 获得快递公司信息, 读取json文件
########################################################################
def get_express_company_json():
	file = open("tools/express/express_company.json", 'rb')
	data_json = json.load(file)
	return data_json



########################################################################
# get_name_by_id: 根据快递公司id，获取快递公司名称
########################################################################
def get_name_by_id(value):
	if not value:
		return ''
		
	data_json = get_express_company_json()
	for item in data_json:
		if item['id'] == value:
			return item['name']

	return ''


########################################################################
# get_name_by_value: 根据快递公司value，获取快递公司名称
########################################################################
def get_name_by_value(value):
	if not value:
		return ''
		
	data_json = get_express_company_json()
	for item in data_json:
		if item['value'] == value:
			return item['name']

	return value


########################################################################
# get_value_by_name: 根据快递公司名称，获取快递公司value
########################################################################
def get_value_by_name(name):
	if not name:
		return ''

	data_json = get_express_company_json()
	for item in data_json:
		if item['name'] == name:
			return item['value']

	return name


def get_express_details_by_order(order_id):
	"""
	根据 order_id 获取 快递明细信息
	"""
	return list(ExpressDetail.objects.filter(order_id=order_id).order_by('-display_index'))