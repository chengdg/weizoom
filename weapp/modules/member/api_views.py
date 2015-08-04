# -*- coding: utf-8 -*-

__author__ = 'chuter'

import json

from django.conf import settings
from core.jsonresponse import create_response
from django.contrib.auth.decorators import login_required
from core.exceptionutil import unicode_full_stack

from models import *
from integral import increase_member_integral
from account.social_account.models import SocialAccount
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, Http404

from excel_response import ExcelResponse

@login_required
def update_member_remarks_name(request):
	member_id = request.POST.get('id', None)
	new_remarks_name = request.POST.get('remarks_name', None)

	if member_id is None or new_remarks_name is None:
		response = create_response(500)
		response.errMsg = u'参数错误'
	else:
		try:
			Member.objects.filter(id=int(member_id)).update(remarks_name=new_remarks_name)
			response = create_response(200)			
		except:
			response = create_response(500)
			response.errMsg = u'更新错误'
			response.innerErrMsg = unicode_full_stack()

	return response.get_response()	


def get_presented_award(request, webapp_id):
	medal_value = request.GET.get('medal_type', None)
	member_id = request.GET.get('mid', None)

	response = create_response(200)
	integral_increase_count = 0
	if medal_value and member_id:
		try:
			member = Member.objects.get(id = int(member_id))
			integral_strategy_settings = IntegralStrategySttings.objects.get(webapp_id=webapp_id)

			if GOLD_MEDAL_VALUE == medal_value:
				integral_increase_count = integral_strategy_settings.reward_integral_count_for_gold_medal
			elif SILVER_MEDAL_VALUE == medal_value:
				integral_increase_count = integral_strategy_settings.reward_integral_count_for_silver_medal
			elif BRONZE_MEDAL_VALUE == medal_value:
				integral_increase_count = integral_strategy_settings.reward_integral_count_for_bronze_medal			
			else:
				pass

			if integral_increase_count > 0:
				increase_member_integral(member, integral_increase_count, AWARD)
		except:
			response = create_response(200)
			response.innerErrMsg = unicode_full_stack()

	response.data.integral_increase_count = integral_increase_count
	return response.get_response()


def get_browse_record(request):
	member_id = request.GET.get('member_id', None)
	sct = request.GET.get('sct', None)
	uuid = request.GET.get('uuid', None)
	items = []
	if member_id is None and sct is None and uuid is None:
		raise Http404('invalid member_id or sct can not none')
	if member_id:
		for member_record in MemberBrowseRecord.objects.filter(member_id=member_id):
		 	items.append({
		 		'member_id': member_id,
				'title': member_record.title,
				'url': member_record.url,
			})
	elif sct:
		try:
			sociall_account = SocialAccount.objects.get(token=sct)
			for member_has_sociall_account in MemberHasSocialAccount.objects.filter(account=sociall_account):
				for member_record in MemberBrowseRecord.objects.filter(member_id=member_has_sociall_account.member.id):
				 	items.append({
				 		'member_id': member_id,
						'title': member_record.title,
						'url': member_record.url,
					})	
		except:
			raise Http404('invalid sct ')
	elif uuid:
		for webapp_user in WebAppUser.objects.filter(token=uuid, member_id__gt=0):
			for member_record in MemberBrowseRecord.objects.filter(member_id=webapp_user.member_id):
			 	items.append({
			 		'member_id': member_id,
					'title': member_record.title,
					'url': member_record.url,
				})	
	else:
		raise Http404('invalid member_id and sct')
		
	return HttpResponse(json.dumps(items), content_type='application/json')


@login_required
def get_member_share(request):
	share_url = request.GET.get('share_url', '')

	if share_url == '':
		return HttpResponse(u"请输入share_url")

	member_share_list = [
		[u'会员id',u'会员昵称',u'pv',u'引导人数']
	]
	member_share_urls = MemberSharedUrlInfo.objects.filter(shared_url__icontains=share_url)
	for member_share in member_share_urls:
		member = Member.objects.get(id=member_share.member_id)
		nike_name = member.username
		try:
			nike_name = nike_name.decode('utf8')
		except:
			nike_name = member.username_hexstr
		member_share_list.append([
			member_share.member_id,
			nike_name,
			member_share.pv,
			member_share.followers
		])
	
	return ExcelResponse(member_share_list,output_name=u'链接分享信息'.encode('utf8'),force_csv=False)
	


