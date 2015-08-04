# -*- coding: utf-8 -*-

__author__ = 'liupeiyu'

from weibo_config import *
from weibo_request_params import *
import urllib

class WeiboAuthorize(object):
	'''
	https://api.weibo.com/oauth2/authorize?
		client_id=YOUR_CLIENT_ID&
		response_type=code&
		redirect_uri=YOUR_REGISTERED_REDIRECT_URI
	'''
	WEIBO_AUTHORIZE_URL_TMPL ="https://api.weibo.com/oauth2/authorize?client_id={}&response_type=code&redirect_uri={}&state={}"


	def __init__(self, request):
		self.authorize_post_request = request

		self.weibo_config = WeiboConfig(request.user_profile)
		self.weibo_params = WeiboRequestParams
		self.redirect_uri = self.weibo_config.get_login_callback_redirect_uri(request)

	def get_Http_authorize_url(self):
		state = self.weibo_config.get_state(self.authorize_post_request)
		verity_url = self.WEIBO_AUTHORIZE_URL_TMPL.format(self.weibo_config.app_id,
			urllib.quote(self.redirect_uri, ''), state)
		return verity_url