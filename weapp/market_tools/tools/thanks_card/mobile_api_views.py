# # -*- coding: utf-8 -*-
#
# __author__ = 'sunny'
#
# from django.http import HttpResponseRedirect, HttpResponse, Http404
# from django.template import Context, RequestContext
# from django.shortcuts import render_to_response
#
# from core.jsonresponse import JsonResponse, create_response, decode_json_str
# from models import *
# from modules.member import util as member_util
# from mall.models import ThanksCardOrder
# from account.views import save_base64_img_file_local_for_webapp
#
# ########################################################
# # check_thanks_card_secret: 校验感恩贺卡是否存在
# ########################################################
# def get_thanks_card(request):
# 	secret = request.GET['secret']
# 	response = None
# 	if ThanksCardOrder.objects.filter(thanks_secret=secret, is_used=True).count() > 0:
# 		response = create_response(200)
# 		response.data.secret = secret
# 		response.data.code = 200
# 	else:
# 		response = create_response(500)
# 		response.errMsg = u'该感恩贺卡不存在'
# 	return response.get_response()
#
