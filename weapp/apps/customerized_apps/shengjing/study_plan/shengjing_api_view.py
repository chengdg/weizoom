# -*- coding: utf-8 -*-
__author__ = 'liupeiyu'

from watchdog.utils import watchdog_info, watchdog_error, watchdog_fatal
from core.exceptionutil import unicode_full_stack

#===============================================================================
# get_session_id : 获取session_id
#===============================================================================
from apps.customerized_apps.shengjing.api_core.shengjing_session_id import ShengjingSessionID
def get_session_id():
	session = ShengjingSessionID()
	session_id = session.get_session_id_data()
	return session_id


#===============================================================================
# get_invitation_list : 获取get_invitation_list
#===============================================================================
from apps.customerized_apps.shengjing.api_core.shengjing_get_invitation_list import ShengjingGetInvitationList
def get_invitation_list(session_id, phone):
	invitation = ShengjingGetInvitationList(session_id, phone)
	data = invitation.get_invitation_list()
	return data


#===============================================================================
# get_invitation_list : 获取get_invitation_list
#===============================================================================
from apps.customerized_apps.shengjing.api_core.shengjing_get_captcha import ShengjingGetCaptcha
def get_captcha(session_id, phone):
	capthca = ShengjingGetCaptcha(session_id, phone)
	data = capthca.get_captcha_data()
	return data


#===============================================================================
# get_invitation_list : 获取get_invitation_list
#===============================================================================
from apps.customerized_apps.shengjing.api_core.shengjing_captcha_verify import ShengjingCaptchaVerify
def get_captcha_verify(session_id, phone, capthca):
	verify = ShengjingCaptchaVerify(session_id, phone, capthca)
	data = verify.get_captcha_verify_data()
	return data


#===============================================================================
# mobile_get_invitation_list : 获取二维码列表页面
#===============================================================================
def mobile_get_invitation_list(phone):
	session_id = get_session_id()
	if session_id:
		return get_invitation_list(session_id, phone)

	return None


#===============================================================================
# mobile_get_captcha : 获取 获取验证码
#===============================================================================
def mobile_get_captcha(phone):
	session_id = get_session_id()
	if session_id:
		return get_captcha(session_id, phone)

	return None

#===============================================================================
# mobile_get_captcha_verify : 获取 检验验证码结果
#===============================================================================
def mobile_get_captcha_verify(phone, captcha):
	session_id = get_session_id()
	if session_id:
		return get_captcha_verify(session_id, phone, captcha)

	return None

