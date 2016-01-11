# -*- coding: utf-8 -*-
import time

from django.dispatch.dispatcher import Signal

from core.jsonresponse import create_response

########################################################
# Object: 通用对象
########################################################
class Object(object):
	def __init__(self, name="unknown"):
		self.name = name


##################################################################################
# check_failed_signal_response: 如果存在fail的signal response，则返回500 response
##################################################################################
def check_failed_signal_response(signal_responses):
	failed_signal_responses = [signal_response[1] for signal_response in signal_responses if not signal_response[1]['success']]
	if failed_signal_responses:
		failed_signal_response = failed_signal_responses[0]
		data_detail = []
		real_data_detail = []
		for data in failed_signal_responses:
			if data['data'].has_key('detail'):
				for detail in data['data']['detail']:
					data_detail.append(detail)

		products_ids = [detail['id'] for detail in data_detail]
		products_ids = list(set(products_ids))
		print "products_ids----------------",products_ids
		print "data_detail----------------",data_detail
		for id in products_ids:
			flag,index = _check_pro_id_in_detail_list(data_detail,id)
			if flag:
				real_data_detail.append(data_detail[index])
				continue
			else:
				for detail in data_detail:
					print "id----------------",detail['id'],id
					print "detail----------------",detail
					if detail['id'] == id:
						real_data_detail.append(detail)
		print real_data_detail
		failed_signal_response['data']['detail'] = real_data_detail
		response = create_response(500)
		response.data = failed_signal_response['data']
		return response.get_response()
	return None

def _check_pro_id_in_detail_list(datadetail,pro_id):
	from mall.signal_handler import UnSalesInfo
	flag,index = False,0
	for index,data in enumerate (datadetail):
		if data['id'] == pro_id and data['short_msg'] == '已删除':
			flag,index = True,index # 存在，以及索引
			break
		elif data['id'] == pro_id and data['short_msg'] == UnSalesInfo:
		    flag,index = True,index # 存在，以及索引
		else:
			flag,index = False,index # 存在，以及索引
	return flag,index

##################################################################################
# register_signal_handlers: 注册signal handler
##################################################################################
def register_signal_handlers(signals, signal_handlers):
	#记录(signal object, signal name)的映射关系
	signal2name = {}
	for name, obj in signals.__dict__.items():
		if isinstance(obj, Signal):
			signal2name[obj] = name

	#注册signal handler
	for signal, package_names in signal_handlers.items():
		signal_name = signal2name[signal]
		for package_name in package_names:
			signal_handler_module_name = '%s.signal_handler' % package_name
			module = __import__(signal_handler_module_name, {}, {}, ['*',])
			handler_function_name = '%s_handler' % signal_name
			handler_function = getattr(module, handler_function_name)
			signal.connect(handler_function, sender=signals, dispatch_uid="%s:%s" % (signal_handler_module_name, handler_function_name))
		#mall_signals.check_order_related_resource.connect(check_order_related_resource_handler, sender=mall_signals, dispatch_uid = "xyz")


##################################################################################
# ignore_exception: 用于signal handler的descriptor，忽略handler中抛出的异常
##################################################################################
def ignore_exception(func):
	def inner_func(*args, **kwargs):
		try:
			return func(*args, **kwargs)
		except:
			#TODO: 记录exception信息
			return {'success':True}
	return inner_func
