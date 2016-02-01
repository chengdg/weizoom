# -*- coding: utf-8 -*-

from django.contrib.auth.models import User

import module_api
from core.jsonresponse import JsonResponse, create_response
from tools.express import util as express_util
from mall import models as mall_models

def get_user_by_username(username):
	try:
		return User.objects.get(username=username)
	except:
		return None


#decorator
def session_required(func):
	def inner_func(request):
		#检查用户是否已授权
		username = request.REQUEST.get('token', '').strip()
		if not module_api.is_auth_user(username):
			response = create_response(500)
			response.errMsg = u'未授权用户'
			return response.get_response()

		#检查用户是否存在
		user = get_user_by_username(username)
		if user is None:
			response = create_response(502)
			response.errMsg = u'用户不存在'
			return response.get_response()

		request.user = user
		return func(request)

	return inner_func


#decorator
def arguments_required(*args):
	def inner_arguments_required(func):
		def inner_func(request):
			for arg in args:
				value = request.REQUEST.get(arg, None)
				if not value:
					response = create_response(503)
					response.errMsg = u'参数不完整，需要以下参数: %s' % ', '.join(args)
					return response.get_response()

			return func(request)

		return inner_func
	return inner_arguments_required


#validator
def check_invalid_order(user, order_id):
	is_check_success = True
	try:
		order = mall_models.Order.objects.get(order_id=order_id)
		if order.webapp_id != user.get_profile().webapp_id:
			is_check_success = False
	except:
		is_check_success = False

	if not is_check_success:
		response = create_response(510)
		response.errMsg = u'无效订单号'
		return response.get_response()

	return None


#validator
def check_invalid_product(user, product_id):
	is_check_success = True
	try:
		if mall_models.Product.objects.filter(owner=user, id=product_id).count() == 0:
			is_check_success = False
	except:
		is_check_success = False

	if not is_check_success:
		response = create_response(550)
		response.errMsg = u'无效商品'
		return response.get_response()

	return None


#validator
def check_invalid_product_model(user, product_id, product_model_id):
	is_check_success = True

	try:
		if mall_models.ProductModel.objects.filter(owner=user, product_id=product_id, id=product_model_id).count() == 0:
			is_check_success = False
	except:
		is_check_success = False

	if not is_check_success:
		response = create_response(551)
		response.errMsg = u'无效商品规格'
		return response.get_response()

	return None


#
def get_express_company_name(express_company_id):
	name = express_util.get_name_by_id(express_company_id)
	return name


#validator
def check_invalid_serach_type(serach_type):
	is_check_success = True
	try:
		serach_type = int(serach_type)
		if serach_type != 0 and serach_type != 1:
			is_check_success = False
	except:
		is_check_success = False

	if not is_check_success:
		response = create_response(510)
		response.errMsg = u'serach_type参数错误'
		return response.get_response()

	return None