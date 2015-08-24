# -*- coding: utf-8 -*-
__author__ = 'liupeiyu'

from core.jsonresponse import JsonResponse, create_response
from apps.customerized_apps.shengjing.api_core import api_send_template_message as shengjing_api
from core.exceptionutil import full_stack, unicode_full_stack
from watchdog.utils import watchdog_warning, watchdog_error
from apps.customerized_apps.shengjing.api_core.api_params import ShengjingAPIParams

SHENGJING_TEMPLATE_RELEASE_TYPE="shengjing_release"
SHENGJING_TEMPLATE_CREATE_TYPE="shengjing_create"

########################################################################
#send_release_template_message: 发送释放模板消息
########################################################################
def send_release_template_message(request):
	'''
	http://mall.weapp.weizzz.com/shengjing/api/send_template_message/
	'''
	try:	
		if request.POST:		
			webapp_user_id = int(request.POST.get('webapp_user_id', 0))
			first = request.POST.get('first', None)
			remark = request.POST.get('remark', None)
			name = request.POST.get('name', None)
			date_time = request.POST.get('date_time', None)
			phone_number = request.POST.get('phone_number', None)
		else:
			webapp_user_id = int(request.GET.get('webapp_user_id', 0))
			first = request.GET.get('first', None)
			remark = request.GET.get('remark', None)
			name = request.GET.get('name', None)
			date_time = request.GET.get('date_time', None)
			phone_number = request.GET.get('phone_number', None)

		# 测试数据
		# if webapp_user_id == 4567890:
		# 	response = create_response(200)
		# 	response.data = {
		# 		'msg': '发送成功！',
		# 		# 'message_dict': json,
		# 		'result_code': True
		# 	}
		# 	return response.get_response()
		return __send_message(
			webapp_user_id,
			first,
			remark, 
			name,
			date_time, 
			phone_number,
			SHENGJING_TEMPLATE_RELEASE_TYPE
			).get_response()

	except:
		response = create_response(501)
		response.data = {
			'msg': '发送释放模板消息失败，请稍后重试！',
			# 'message_dict': json,
			'result_code': False,
			'error_msg': unicode_full_stack()
		}
		notify_message = u"shengjing发送释放模板消息异常, QUERY_STRING: {}, cause:\n{}".format(request.META.get('QUERY_STRING'), unicode_full_stack())
		# watchdog_error(notify_message, ShengjingAPIParams().WATCHDOG_TYPE_SHENGJING)

	return response.get_response()

########################################################################
#send_create_template_message: 发送创建模板消息
########################################################################
def send_create_template_message(request):
	'''
	http://mall.weapp.weizzz.com/shengjing/api/send_create_template_message/
	'''
	try:	
		if request.POST:		
			webapp_user_id = int(request.POST.get('webapp_user_id', 0))
			first = request.POST.get('first', None)
			remark = request.POST.get('remark', None)
			name = request.POST.get('name', None)
			date_time = request.POST.get('date_time', None)
			phone_number = request.POST.get('phone_number', None)
		else:
			webapp_user_id = int(request.GET.get('webapp_user_id', 0))
			first = request.GET.get('first', None)
			remark = request.GET.get('remark', None)
			name = request.GET.get('name', None)
			date_time = request.GET.get('date_time', None)
			phone_number = request.GET.get('phone_number', None)

		return __send_message(
			webapp_user_id,
			first,
			remark, 
			name,
			date_time, 
			phone_number,
			SHENGJING_TEMPLATE_CREATE_TYPE
			).get_response()

	except:
		response = create_response(501)
		response.data = {
			'msg': '发送创建模板消息失败，请稍后重试！',
			# 'message_dict': json,
			'result_code': False,
			'error_msg': unicode_full_stack()
		}
		notify_message = u"shengjing发送创建模板消息异常, QUERY_STRING: {}, cause:\n{}".format(request.META.get('QUERY_STRING'), unicode_full_stack())
		# watchdog_error(notify_message, ShengjingAPIParams().WATCHDOG_TYPE_SHENGJING)

	return response.get_response()


def __send_message(webapp_user_id,
			first,
			remark, 
			name,
			date_time, 
			phone_number,
			template_type):	
	if webapp_user_id is None or first is None or remark is None or name is None or date_time is None or phone_number is None:
		response = create_response(501)
		response.data = {
			'msg': '发送失败，请稍后重试！',
			# 'message_dict': json,
			'result_code': False,
			'error_msg': '参数不正确！'
		}
		return response

	# 获取要发送的模板数据
	template_detail = shengjing_api.TemplateDetail(first, remark, name, date_time, template_type)
	shengjing_template_api = shengjing_api.ShengjingTemplateMessage(webapp_user_id, template_detail)
	
	json = shengjing_template_api._get_message_dict()
	# print '-----------------------------------'
	# 发送模板消息
	code, data = shengjing_template_api.send_message()

	# print data

	if code:
		response = create_response(200)
		response.data = {
			'msg': '发送成功！',
			# 'message_dict': json,
			'result_code': code
		}
	else:
		response = create_response(501)
		response.data = {
			'msg': '发送失败，请稍后重试！',
			# 'message_dict': json,
			'result_code': code,
			'error_msg': data
		}
	return response

