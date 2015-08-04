# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.shortcuts import render_to_response

from apps.customerized_apps.shengjing.crm_api import api_views as crm_apis
from apps.customerized_apps.shengjing.user_center.util import get_binding_info_by_member
from apps.customerized_apps.shengjing.models import LEADER

from watchdog.utils import watchdog_alert, watchdog_fatal

from modules.member import module_api as member_module_api
from apps.customerized_apps.shengjing.study_plan.mobile_views import _get_template_name_and_response_data

from apps.register import mobile_view_func

################################################
# 获取账单明细
################################################
@mobile_view_func(resource='bills', action='get')
def get_order(request):
	response_data, template_name = _get_template_name_and_response_data(request)
	if template_name:
		c = RequestContext(request, response_data)
		return render_to_response(template_name, c)
	else:
		#得到会员信息
		member = None
		if hasattr(request, 'member'):
			member = request.member
		else:
			member_id = request.GET.get('member_id', '')
			try:
				member = member_module_api.get_member_by_id(int(member_id))
			except:
				fatal_message = u'账单(获取时间卡、人次卡信息), 未获取到 member_id:{};'.format(member_id)
				watchdog_fatal(fatal_message, user_id=211)

				c = RequestContext(request, {
					'page_title': u'查看账单',
					'error_info': u'获取会员信息失败',
					'is_hide_weixin_option_menu': True
				})
			return render_to_response('webapp/order_error.html', c)
		binding_member, member_info = get_binding_info_by_member(member)
	
		# #不是决策人
		# if not is_leader(member_info):
		#  	c = RequestContext(request, {
		#  		'page_title': u'查看账单',
		#  		'error_info': u'您尚未购买盛景课程或者您不是企业决策人，所以您无法看到此信息！',
		#  		'is_hide_weixin_option_menu': True
		#  	})
		#  	return render_to_response('webapp/order_error.html', c)
	
		#获取公司信息
		company_objects = member_info.companys
		companys = []
		for company_obj in company_objects:
			companys.append(company_obj.name)
	
		company = request.GET.get('company', '')
		if company == '':
			try:
				company = companys[0]
			except:
				fatal_message = u'账单(获取时间卡、人次卡信息), 查看账单, 您尚未购买盛景课程, 公司 company:{}; member_id:{}'.format(company, member_id)
				watchdog_fatal(fatal_message, user_id=211)
				c = RequestContext(request, {
					'page_title': u'查看账单',
					'error_info': u'您尚未购买盛景课程!',
					'is_hide_weixin_option_menu': True
				})
				return render_to_response('webapp/order_error.html', c)
	
		c = RequestContext(request, {
				'page_title': u'账单明细',
				'companys': companys,
				'member': member,
				'is_hide_weixin_option_menu': True
			})
		return render_to_response('webapp/order.html', c)


################################################
# 判断member是否为决策人
################################################
def is_leader(member_info):
	if member_info and member_info.status==LEADER:
		return True
	return False