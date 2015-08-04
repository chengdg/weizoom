# -*- coding: utf-8 -*-

__author__ = 'chuter'


from django.contrib.auth.decorators import login_required

from core.jsonresponse import create_response
from core.exceptionutil import unicode_full_stack

from modules.member.models import IntegralStrategySttings

from models import OperationSettings

@login_required
def update_settings(request):
	try:
		IntegralStrategySttings.objects.filter(webapp_id=request.user_profile.webapp_id).update(
			integral_each_yuan = int(request.POST['integral_each_yuan']),
			be_member_increase_count = int(request.POST['be_member_increase_count']),
			click_shared_url_increase_count_after_buy = int(request.POST['click_shared_url_increase_count_after_buy']),
			click_shared_url_increase_count_before_buy = int(request.POST['click_shared_url_increase_count_before_buy']),
			buy_via_shared_url_increase_count_for_author = int(request.POST['buy_via_shared_url_increase_count_for_author']),
			usable_integral_or_conpon = int(request.POST.get('usable_integral_or_conpon')),
			buy_increase_count_for_father = int(request.POST.get('buy_increase_count_for_father'))
			)
		response = create_response(200)
	except:
		response = create_response(500)
		response.errMsg = u'保存积分策略配置失败'
		response.innerErrMsg = unicode_full_stack()

	return response.get_response()

@login_required
def update_operation_settings(request):
	try:
		OperationSettings.objects.filter(owner=request.user).update(
			non_member_followurl = request.POST.get('non_member_followurl', ''),
			weshop_followurl = request.POST.get('weshop_followurl', '')
			)
		response = create_response(200)
	except:
		response = create_response(500)
		response.errMsg = u'运营策略配置失败'
		response.innerErrMsg = unicode_full_stack()

	return response.get_response()