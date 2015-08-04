# -*- coding: utf-8 -*-

__author__ = 'liupeiyu'

import sys
import unittest

if __name__ == '__main__':
	sys.path.insert(0, '../../')
	sys.path.insert(0, '../')

from test import test_env_with_db as test_env
from apps.customerized_apps.shengjing.api_core.shengjing_session_id import ShengjingSessionID
from apps.customerized_apps.shengjing.api_core.shengjing_get_invitation_list import ShengjingGetInvitationList
from apps.customerized_apps.shengjing.api_core.shengjing_submit_booking import ShengjingSubmitBooking
from apps.customerized_apps.shengjing.api_core.shengjing_captcha_verify import ShengjingCaptchaVerify
from apps.customerized_apps.shengjing.api_core.shengjing_get_captcha import ShengjingGetCaptcha

class ShengjingAPIUtilTest(unittest.TestCase):
	def setUp(self):
		pass

	def get_session_id(self):
		print '************************'
		session = ShengjingSessionID()
		self.session_id = session.get_session_id_data()
		print 'test_get_session_id_data'
		print self.session_id
		return self.session_id

	def get_invitation_list(self):
		invitation_list = ShengjingGetInvitationList(self.session_id, '15528161888')
		data = invitation_list.get_invitation_list()
		print 'test_get_invitation_list'
		print data

	def mobile_get_invitation_list(phone):
		session_id = self.get_session_id()
		if session_id:
			return self.get_invitation_list(self.session_id, phone)

		return None


	def test_submit_booking(self):
		session_id = self.get_session_id()
		submit_booking = ShengjingSubmitBooking(self.session_id, Course())
		data = submit_booking.set_submit_booking()
		print 'test_submit_booking'
		print data


	def test_get_captcha(self):
		session_id = self.get_session_id()
		get_captcha = ShengjingGetCaptcha(self.session_id, '15811324269')
		data = get_captcha.get_captcha_data()
		print 'test_get_captcha'
		print data


	def test_captcha_verify(self):
		session_id = self.get_session_id()
		captcha_verify = ShengjingCaptchaVerify(self.session_id, '15811324269', '2323')
		data = captcha_verify.get_captcha_verify_data()
		print 'test_captcha_verify'
		print data


class Course():
	def __init__(self):
		self.name = u'测试团队合作课程'
		self.member_name = u'王芳芳'
		self.member_phone = u'139888888888'
		self.member_company = u'北京科技股份公司'
		self.number = 1
		self.date_time = u'2015-01-20 08:51'

# if __name__ == '__main__':
	# shengjing = ShengjingAPIUtilTest()
	# shengjing.test_get_session_id_data()
	# shengjing.test_get_invitation_list()
	# shengjing.test_submit_booking()

if __name__ == '__main__':
	test_env.start_test_withdb()