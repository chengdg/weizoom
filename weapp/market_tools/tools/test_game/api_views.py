# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.shortcuts import render_to_response
from models import *
from modules.member import util as member_util
from core.jsonresponse import JsonResponse, create_response
from django.contrib.auth.decorators import login_required, permission_required
from core.exceptionutil import full_stack
from core import paginator
from django.db.models import Q
import mobile_views
from account.views import save_base64_img_file_local_for_webapp

from core import apiview_util
from core.exceptionutil import full_stack, unicode_full_stack


def __build_member_basic_json(member):
	return {
		'id': member.id,
		'username': member.username_for_html,
		'user_icon': member.user_icon,
		'integral': member.integral,
		'grade_name': member.grade.name
	}


@login_required
def get_join_users(request):
	try:
		game_id = int(request.GET['game_id'])
		
		game = TestGame.objects.get(id=game_id)

		join_users = game.joined_users
		member_ids = [webapp_user.member_id for webapp_user in join_users]
		
		jion_members = Member.objects.filter(id__in=member_ids)
		return_jion_users_json_array = []
		for jion_member in jion_members:
			return_jion_users_json_array.append(__build_member_basic_json(jion_member))

		response = create_response(200)
		response.data.items = return_jion_users_json_array
	except:
		response = create_response(500)
		response.innerErrMsg = unicode_full_stack()
	
	return response.get_response()


def call_api(request):
	api_function = apiview_util.get_api_function(request, globals())
	return api_function(request)