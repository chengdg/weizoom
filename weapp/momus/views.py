# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response

from core.jsonresponse import JsonResponse, create_response


def handle_request(request, get_commands, post_commands, default_context):
	exec_context = {}
	if request.method == 'GET':
		#处理GET
		result = None
		for command in get_commands:
			print command
			result = command(request, default_context, result, exec_context)
		return result
	else:
		#处理POST
		result = None
		for command in post_commands:
			result = command(request, default_context, result, exec_context)
		return result