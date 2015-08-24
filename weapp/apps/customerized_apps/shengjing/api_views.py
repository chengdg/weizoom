# -*- coding: utf-8 -*-
__author__ = 'liupeiyu'

from core.jsonresponse import JsonResponse, create_response
from apps.customerized_apps.shengjing.api_core import api_send_template_message as shengjing_api
from core.exceptionutil import full_stack, unicode_full_stack
from watchdog.utils import watchdog_warning, watchdog_error
from apps.customerized_apps.shengjing.api_core.api_params import ShengjingAPIParams
import models as shengjing_models
from modules.member import models as member_models

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
		# 验证参数
		is_success, data = __validate_parameter(request, SHENGJING_TEMPLATE_RELEASE_TYPE)
		if not is_success:
			return data.get_response()

		return __send_message(data).get_response()
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
		# 验证参数
		is_success, data = __validate_parameter(request, SHENGJING_TEMPLATE_CREATE_TYPE)
		if not is_success:
			return data.get_response()

		# 该手机号是否绑定
		phone_number = data.get('phone_number')
		webapp_user_id = __member_webapp_user(phone_number)
		if webapp_user_id is None:			
			response = create_response(502)
			response.data = {
				'msg': '发送创建模板消息失败，未找到与该手机号对应的会员！',
				'result_code': False,
				'phone_number': phone_number
			}
			return response.get_response()

		return __send_message(data).get_response()

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


def __member_webapp_user(phone_number):
	shengjing_members = shengjing_models.ShengjingBindingMember.objects.filter(phone_number=phone_number)
	member_ids = [s.member_id for s in shengjing_members]
	webapp_users = member_models.WebAppUser.objects.filter(member_id__in=member_ids)
	if webapp_users.count() == 0:
		return None
	else:
		webapp_user_ids = [w.id for w in webapp_users]
		return webapp_user_ids[0]


def __validate_parameter(request, template_type):	
	if request.POST:		
		webapp_user_id = request.POST.get('webapp_user_id', '0')
		webapp_user_id = int(webapp_user_id) if webapp_user_id.isdigit() else 0
		first = request.POST.get('first', '').strip()
		remark = request.POST.get('remark', '').strip()
		name = request.POST.get('name', '').strip()
		date_time = request.POST.get('date_time', '').strip()
		phone_number = request.POST.get('phone_number', '').strip()
	else:
		webapp_user_id = request.GET.get('webapp_user_id', '0')
		webapp_user_id = int(webapp_user_id) if webapp_user_id.isdigit() else 0
		first = request.GET.get('first', '').strip()
		remark = request.GET.get('remark', '').strip()
		name = request.GET.get('name', '').strip()
		date_time = request.GET.get('date_time', '').strip()
		phone_number = request.GET.get('phone_number', '').strip()

	response = create_response(501)
	response.data = {
		'msg': '发送失败，请稍后重试！',
		# 'message_dict': json,
		'result_code': False,
		'error_msg': '参数不正确！'
	}
	if template_type == SHENGJING_TEMPLATE_RELEASE_TYPE:
		if webapp_user_id == 0 or first == '' or remark == '' or name == '' or date_time == '' or phone_number == '':
			return False, response
	elif template_type == SHENGJING_TEMPLATE_CREATE_TYPE:
		if first == '' or remark == '' or name == '' or date_time == '' or phone_number == '':
			return False, response

	data = {
		'webapp_user_id': webapp_user_id,
		'first': first,
		'remark': remark,
		'name': name,
		'date_time': date_time,
		'phone_number': phone_number,
		'template_type': template_type
	}
	return True, data


def __send_message(data):
	# 获取要发送的模板数据
	template_detail = shengjing_api.TemplateDetail(
		data.get('first'), 
		data.get('remark'),
		data.get('name'),
		data.get('date_time'),
		data.get('template_type')
	)
	shengjing_template_api = shengjing_api.ShengjingTemplateMessage(data.get('webapp_user_id'), template_detail)
	
	json = shengjing_template_api._get_message_dict()

	# 发送模板消息
	code, data = shengjing_template_api.send_message()

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

