# -*- coding: utf-8 -*-

__author__ = 'bert'

from shengjing.models import *
from shengjing.crm_api import api_views as crm_api
from shengjing.crm_api import crm_settings

from core.send_phone_msg import send_phone_captcha
from core.exceptionutil import full_stack, unicode_full_stack

from modules.member.models import MemberTag,MemberHasTag

from watchdog.utils import watchdog_fatal, watchdog_error, watchdog_warning, watchdog_debug

MSG_CONTENT = u"您的验证码为[%s]，请不要泄露给任何人【盛景网联】"

########################################################################
# get_binding_info_by_member: 根据member获取bingding信息
########################################################################
def get_binding_info_by_member(member, is_need_to_add_integral_for_father=False):
	binding_member = _get_binding_member_by_member_id(member.id)

	if binding_member is not None:
		#更新胜景数据库个人信息
		update_member_info_from_shengjing(binding_member, member.webapp_id, is_need_to_add_integral_for_father)

		member_info = _get_binding_member_info_by_binding_member_id(binding_member.id)
		if member_info:
			member_info.companys = _get_companys_by_binding_member_id(binding_member.id)
			member_info.phone_number = binding_member.phone_number

		return binding_member, member_info

	return None, None

########################################################################
# _get_binding_member_phone_by_member_id: 根据member_id获取bingding信息
########################################################################
def _get_binding_member_by_member_id(member_id):
	try:
		binding_members = ShengjingBindingMember.objects.filter(member_id=member_id)
		if binding_members.count() > 0:
			return binding_members[0]
		else:
			notify_message = u"根据member_id没有到一条获取盛景BindingMember会员,member_id={}".format(member_id)
			watchdog_warning(notify_message)
			return None
	except:
		notify_message = u"根据member_id获取盛景BindingMember会员信息失败,member_id={}, cause:\n{}".format(member_id, unicode_full_stack())
		watchdog_warning(notify_message)
		return None

########################################################################
# _get_binding_member_info_by_binding_member_id: 根据member获取bingding信息
########################################################################
def _get_binding_member_info_by_binding_member_id(binding_member_id):
	try:
		member_infos = ShengjingBindingMemberInfo.objects.filter(binding_id=binding_member_id)
		if member_infos.count() > 0:
			return member_infos[0]
		else:
			notify_message = u"根据binding_member_id没有获取盛景BindingMemberInfo会员信息,ShengjingBindingMemberId = {}".format(binding_member_id)
			watchdog_warning(notify_message)
			return None
	except:
		notify_message = u"根据binding_member_id获取盛景BindingMemberInfo会员信息,ShengjingBindingMemberId = {}, cause:\n{}".format(binding_member_id, unicode_full_stack())
		watchdog_warning(notify_message)
		return None

########################################################################
# _get_companys_by_binding_member_id: 根据binding_member_id获取公司信息
########################################################################
def _get_companys_by_binding_member_id(binding_member_id):	
	return list(ShengjingBindingMemberHasCompanys.objects.filter(binding_id=binding_member_id).order_by('-id'))

########################################################################
# update_member_info_from_shengjing: 获取胜景信息
########################################################################
def update_member_info_from_shengjing(binding_member, webapp_id, is_need_to_add_integral_for_father=False):
	try:
		binding_member_tag, binding_created =MemberTag.objects.get_or_create(webapp_id=webapp_id, name=u'注册绑定CRM')
		not_binding_member_tag, not_binding_created =MemberTag.objects.get_or_create(webapp_id=webapp_id, name=u'注册未绑定CRM')
		crm_data = crm_api.get_userinfo_by_phone_number(binding_member.phone_number)
		if crm_data:
			status = crm_data[crm_settings.IDENTIFY] if crm_data.has_key(crm_settings.IDENTIFY) else OUTSIDER
			
			name = crm_data[crm_settings.CONTACT_NAME] if crm_data.has_key(crm_settings.CONTACT_NAME) else u'未知'

			shengjing_member_info, created = ShengjingBindingMemberInfo.objects.get_or_create(binding=binding_member)

			is_increase_integral = _is_increase_integral_for_becomed_shengjing_member(status, binding_member)

			shengjing_member_info.name = name
			shengjing_member_info.position = ''
			shengjing_member_info.status = status	
			shengjing_member_info.save()
			
			if crm_data.has_key(crm_settings.COMPANYS):
				# 清空之前的公司信息
				if len(crm_data[crm_settings.COMPANYS]) > 0:
					ShengjingBindingMemberHasCompanys.objects.filter(binding=binding_member).delete()
				
				for company in crm_data[crm_settings.COMPANYS]:
					ShengjingBindingMemberHasCompanys.objects.create(name=company, binding=binding_member)
			
			# 是否需要加become_member_of_shengjing_for_father积分
			if is_increase_integral:
				ShengjingIntegralStrategySttings.increase_integral_become_member_of_shengjing_for_father(binding_member.id, webapp_id)

			# 是否需要加binding_for_father积分
			if is_need_to_add_integral_for_father:
				ShengjingIntegralStrategySttings.increase_integral_for_father_by_binding_id(binding_member.id, webapp_id)
			
			current_member_tag = binding_member_tag
		else:
			current_member_tag = not_binding_member_tag

		# 盛景会员分组
		try:
			shengjing_member_tag_ids = [mt.id for mt in MemberTag.objects.filter(webapp_id=webapp_id)]
			MemberHasTag.objects.filter(member_id=binding_member.member_id, member_tag_id__in=shengjing_member_tag_ids).delete()
		except:
			pass
		MemberHasTag.objects.create(member_id=binding_member.member_id, member_tag=current_member_tag)

	except:
		notify_message = u"更新胜景信息异常 SengjingBindingId = {}, cause:\n{}".format(binding_member.id, unicode_full_stack())
		watchdog_warning(notify_message, user_id=211)
		crm_data = None

def _is_increase_integral_for_becomed_shengjing_member(status, binding_member):	
	shengjing_binding_member_infos = ShengjingBindingMemberInfo.objects.filter(binding=binding_member)
	if shengjing_binding_member_infos.count() > 0:
		shengjing_member_info = shengjing_binding_member_infos[0]
		if status > OUTSIDER and shengjing_member_info.status == OUTSIDER:
		# if status > OUTSIDER
			return True
		else:
			return False
	else:
		return False

########################################################################
# send_phone_msg: 发送手机验证码
########################################################################
def send_phone_msg(phone_number):
	captcha = __get_random_captcha(phone_number)
	content = MSG_CONTENT % captcha
	result = send_phone_captcha(phone_number, content)
	return result,captcha

def __get_random_captcha(phone_number):
	import random
	import string
	sample_list = ['0','1','2','3','4','5','6','7','8','9'] 
		
	captcha = ''.join(random.sample(sample_list, 6))
	return captcha 