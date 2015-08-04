# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response
from django.conf import settings

from watchdog.utils import *
from core.jsonresponse import JsonResponse, create_response

MESSAGE_COUNT_PER_PAGE = 50

#===============================================================================
# list : 显示watch dog message的列表
#===============================================================================
@login_required
def list(request, cur_page=1):
	if not 'severity' in request.GET:
		cur_severity_id = 0
	else:
		cur_severity_id = int(request.GET['severity'])	
	cur_severity = severities[cur_severity_id]
	
	if cur_severity_id == 0:
		total_messages = Message.objects.all()
	else:
		total_messages = Message.objects.filter(severity=cur_severity_id)
	
	messages = total_messages
	
	c = RequestContext(request, {
								'watchdog_messages' : messages,
								'severities': severities,
								'cur_severity': cur_severity,
								})
	return render_to_response('watchdog/list.html', c)


#===============================================================================
# create_watchdog : 创建watchdog
#===============================================================================
def create_watchdog(request):
	message = request.POST.get('message', '***empty message***')
	type = request.POST.get('type', 'SERVICE')
	watchdog(type, message)

	return create_response(200).get_response()


@login_required
def delete(request, message_id):
	Message.objects.filter(id=message_id).delete()
	return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def delete_all(request, severity):
	if 0 == int(severity):
		Message.objects.all().delete()
	else:
		Message.objects.filter(severity=severity).delete()
	return HttpResponseRedirect(request.META['HTTP_REFERER'])


def get_newest_error(request):
	secrect = request.GET.get('secrect', '')
	if secrect == 'ilovetiger':
		message = Message.objects.filter(severity=WATCHDOG_ERROR)[0]
		return HttpResponse('{"code":200, "id":%d}' % message.id, 'application/json')
	else:
		return HttpResponse('{"code":200, "result":"success"}', 'application/json')


def get_newest_fatal(request):
	secrect = request.GET.get('secrect', '')
	if secrect == 'ilovetiger':
		try:
			message = Message.objects.filter(severity=WATCHDOG_FATAL)[0]
			return HttpResponse('{"code":200, "id":%d}' % message.id, 'application/json')
		except:
			return HttpResponse('{"code":200, "result":"success"}', 'application/json')
	else:
		return HttpResponse('{"code":200, "result":"success"}', 'application/json')


def get_operation_infos(request):
	secrect = request.GET.get('secrect', '')
	from_id = int(request.GET.get('from', 0))
	if secrect == 'i@love*tiger(':
		result = JsonResponse()
		result.code = 200
		result.operations = []
		for message in Message.objects.filter(severity=WATCHDOG_OPERATION, id__gt=from_id):
			operation = JsonResponse()
			operation.id = message.id
			operation.message = message.message
			operation.create_time = message.create_time.strftime('%H:%M')
			result.operations.append(operation)

		return result.get_response()
	else:
		return HttpResponse('{"code":200, "result":"success"}', 'application/json')


def write_api_infos(request):
	message = request.POST.get('message', None)
	
	if message:
		report_api_fatal(message)
	
	return HttpResponse('{"code":200, "result":"success"}', 'application/json')
