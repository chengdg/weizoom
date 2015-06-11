# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.shortcuts import render_to_response
from models import *
from modules.member import util as member_util
from modules.member import models as member_model
from core.jsonresponse import JsonResponse, create_response, decode_json_str
from django.contrib.auth.decorators import login_required, permission_required
from core.exceptionutil import full_stack, unicode_full_stack
from django.db.models import Q

from core import paginator
from core import apiview_util
from core.wxapi import get_weixin_api
from account.util import get_binding_weixin_mpuser, get_mpuser_accesstoken
from watchdog.utils import watchdog_warning, watchdog_error

from mall import models as mall_model

def __build_member_basic_json(member):
	return {
		'id': member.id,
		'username': member.username_for_html,
		'user_icon': member.user_icon,
		'integral': member.integral,
		'grade_name': member.grade.name
	}

########################################################################
# get_channel_qrcode_settings: 获取渠道扫码配置列表
########################################################################
@login_required
def get_channel_qrcode_settings(request):
	#处理搜索
	query = request.GET.get('query', '').strip()
	if query:
		settings = ChannelQrcodeSettings.objects.filter(owner=request.user, name__contains=query)
	else:
		settings = ChannelQrcodeSettings.objects.filter(owner=request.user)
	
	setting_ids = [s.id for s in settings]
	relations = ChannelQrcodeHasMember.objects.filter(channel_qrcode_id__in=setting_ids)
	setting_id2count = {}
	member_id2setting_id = {} 
	member_ids = []
	for r in relations:
		member_ids.append(r.member_id)
		member_id2setting_id[r.member_id] = r.channel_qrcode_id
		if r.channel_qrcode_id in setting_id2count:
			setting_id2count[r.channel_qrcode_id] += 1
		else:
			setting_id2count[r.channel_qrcode_id] = 1
	
	webapp_users = member_model.WebAppUser.objects.filter(member_id__in=member_ids)
	webapp_user_id2member_id = dict([(u.id, u.member_id) for u in webapp_users])
	webapp_user_ids = set(webapp_user_id2member_id.keys())
	orders = mall_model.Order.objects.filter(webapp_user_id__in=webapp_user_ids, status=mall_model.ORDER_STATUS_SUCCESSED)
	member_id2total_final_price = {}
	for order in orders:
		member_id = webapp_user_id2member_id[order.webapp_user_id]
		if member_id in member_id2total_final_price:
			member_id2total_final_price[member_id] += order.final_price
		else:
			member_id2total_final_price[member_id] = order.final_price
	
	setting_id2total_final_price = {}
	for member_id in member_id2total_final_price.keys():
		final_price = member_id2total_final_price[member_id]
		setting_id = member_id2setting_id[member_id]
		if setting_id in setting_id2total_final_price:
			setting_id2total_final_price[setting_id] += final_price
		else:
			setting_id2total_final_price[setting_id] = final_price
	
	
	response = create_response(200)
	response.data.items = []
	items = []

	mp_user = get_binding_weixin_mpuser(request.user)
	mpuser_access_token = get_mpuser_accesstoken(mp_user)

	for setting in settings:
		cur_setting = JsonResponse()
		prize_info = decode_json_str(setting.award_prize_info)
		if prize_info['name'] == '_score-prize_':
			setting.cur_prize = '[%s]%d' % (prize_info['type'], prize_info['id'])
		elif prize_info['name'] == 'non-prize':
			setting.cur_prize = prize_info['type']
		else:
			setting.cur_prize = '[%s]%s' % (prize_info['type'], prize_info['name'])
		
		if setting.id in setting_id2count:
			setting.count = setting_id2count[setting.id]
		else:
			setting.count = 0
		if setting.id in setting_id2total_final_price:
			setting.total_final_price = setting_id2total_final_price[setting.id]
		else:
			setting.total_final_price = 0
		
		#如果没有ticket信息则获取ticket信息
		if not setting.ticket:
			try:
				if mp_user.is_certified and mp_user.is_service and mpuser_access_token.is_active:
					weixin_api = get_weixin_api(mpuser_access_token)
					qrcode_ticket = weixin_api.create_qrcode_ticket(int(setting.id), QrcodeTicket.PERMANENT)
			
					try:
						ticket = qrcode_ticket.ticket
					except:
						ticket = ''
					setting.ticket = ticket
					setting.save()
			except:
				pass
		cur_setting.id = setting.id
		cur_setting.name = setting.name
		cur_setting.count = setting.count
		cur_setting.total_final_price = round(setting.total_final_price,2)
		cur_setting.cur_prize = setting.cur_prize
		cur_setting.ticket = setting.ticket
		cur_setting.remark = setting.remark
		items.append(cur_setting)

	#进行分页
	response.data.sortAttr = request.GET.get('sort_attr', 'count')
	
	if '-' in response.data.sortAttr:
		sorter = response.data.sortAttr[1:]
		is_reverse = True
	else:
		sorter = response.data.sortAttr
		is_reverse = False
	items = sorted(items, reverse=is_reverse, key=lambda b : getattr(b, sorter))
	count_per_page = int(request.GET.get('count_per_page', 15))
	cur_page = int(request.GET.get('page', '1'))
	pageinfo, items = paginator.paginate(items, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
	
	
	# 
	response.data.items = items
	response.data.pageinfo = paginator.to_dict(pageinfo)
	
	return response.get_response()


@login_required
def get_channel_members(request):
	try:
		setting_id = int(request.GET['setting_id'])

		member_ids = [relation.member_id for relation in \
			ChannelQrcodeHasMember.objects.filter(channel_qrcode=setting_id)]
		
		channel_members = Member.objects.filter(id__in=member_ids)
		return_channel_members_json_array = []
		for channel_member in channel_members:
			return_channel_members_json_array.append(__build_member_basic_json(channel_member))

		response = create_response(200)
		response.data.items = return_channel_members_json_array
	except:
		response = create_response(500)
		response.innerErrMsg = unicode_full_stack()
	
	return response.get_response()


def call_api(request):
	api_function = apiview_util.get_api_function(request, globals())
	return api_function(request)