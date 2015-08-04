# -*- coding: utf-8 -*-

__author__ = 'liupeiyu'

from qq_config import *
from qq_request_params import *
import urllib

class QQAuthorize(object):
	'''
	https://graph.qq.com/oauth2.0/authorize?response_type=code&
		client_id=[YOUR_APPID]&
		redirect_uri=[YOUR_REDIRECT_URI]&
		scope=[THE_SCOPE]
	'''
	QQ_AUTHORIZE_URL_TMPL ="https://graph.qq.com/oauth2.0/authorize?response_type=code&client_id={}&redirect_uri={}&state={}"


	def __init__(self, request):
		self.authorize_post_request = request

		self.qq_config = QQConfig(request.user_profile)
		self.qq_params = QQRequestParams
		self.redirect_uri = self.qq_config.get_login_callback_redirect_uri(request)

	def get_Http_authorize_url(self):
		state = self.qq_config.get_state(self.authorize_post_request)
		verity_url = self.QQ_AUTHORIZE_URL_TMPL.format(
			self.qq_config.app_id,
			urllib.quote(self.redirect_uri, ''),
			state)
		return verity_url