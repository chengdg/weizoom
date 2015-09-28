# -*- coding: utf-8 -*-
"""@package modules.member.middleware
member的中间件

"""

from django.http import HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext, Context

from webapp.models import PageVisitLog
from account.models import UserProfile
from watchdog.utils import watchdog_fatal, watchdog_error, watchdog_info

from core.exceptionutil import unicode_full_stack
from utils import url_helper
import util as member_util
import visit_session_util

from utils.url_helper import remove_querystr_filed_from_request_url, add_query_part_to_request_url
from account.url_util import (get_webappid_from_request, is_request_for_editor,
								is_request_for_api, is_request_for_webapp, is_request_for_pcmall)
from account.social_account.models import SocialAccount, SOCIAL_PLATFORM_WEIXIN

from util import *
from models import *
import integral

from visit_session_util import record_shared_page_visit, get_request_url_digest,get_request_url

import member_settings


import middleware_util
from webapp.handlers import event_handler_util
from weixin.user.models import *


from account.url_util import get_webappid_from_request, is_request_for_api, is_request_for_webapp, is_request_for_webapp_api, is_request_for_editor, is_pay_request, is_request_for_weixin, is_paynotify_request, is_request_for_pcmall, is_js_config, is_product_stocks_request

#################
# new add by bert
#################
from member_identity_util import *
from module_api import *
from member_info_util import *
from member_relation_util import *

import module_api as member_api


class CleanUpCookieMiddleware(object):
	"""
	清除缓存的中间件
	"""
	def process_request(self, request):

		#added by duhao
		if is_product_stocks_request(request):
			return None

		#added by slzhu
		# if settings.MODE != "develop":
		# 	real_ip=request.META.get('HTTP_X_FORWARDED_FOR', None)

		# 	if real_ip is None:
		# 		real_ip = request.META.get('REMOTE_ADDR', None)

		# 	if real_ip:
		# 		ip = "request ip: %s" % real_ip
		# 		watchdog_error(ip)

		if is_pay_request(request):
			return None

		if not is_request_for_webapp(request):
			#如果是对webapp的请求，不进行任何处理
			return None

		# 不处理临时二维码请求 by liupeiyu
		if request.is_access_temporary_qrcode_image:
			return None

		#不处理非webapp和非pcmall的请求
		if (not request.is_access_webapp) and (not request.is_access_pcmall):
			return None

		if is_js_config(request):
			return None

		#不处理非微信请求
		#if not request.user.is_from_weixin:
		#	return None
		cookie_openid_webapp_id = request.COOKIES.get(member_settings.OPENID_WEBAPP_ID_KEY, None)
		if not cookie_openid_webapp_id:
			return None

		openid, webapp_id = cookie_openid_webapp_id.split('____')
		if not request.user_profile:
			return None

		url_sct = request.GET.get(member_settings.SOCIAL_ACCOUNT_TOKEN_URL_QUERY_FIELD, None)
		cookie_sct = request.COOKIES.get(member_settings.SOCIAL_ACCOUNT_TOKEN_SESSION_KEY, None)
		url_openid = request.GET.get(member_settings.URL_OPENID, None)


		is_response = False
		if webapp_id != request.user_profile.webapp_id:
			is_response = True

		if url_openid and openid and  (url_openid != openid):
			is_response = True

		if url_sct and cookie_sct and  (url_sct != cookie_sct):
			is_response = True

		if is_response:
			new_url = request.get_full_path()
			response = HttpResponseRedirect(new_url)
			response.delete_cookie(member_settings.SOCIAL_ACCOUNT_TOKEN_SESSION_KEY)
			response.delete_cookie(member_settings.OPENID_WEBAPP_ID_KEY)
			if webapp_id != request.user_profile.webapp_id:
				response.delete_cookie(member_settings.FOLLOWED_MEMBER_TOKEN_SESSION_KEY)
				response.delete_cookie(member_settings.FOLLOWED_MEMBER_SHARED_URL_SESSION_KEY)
			return response
		else:
			return None


class MemberCacheMiddleware(object):
	"""
	从缓存中获取member的middleware
	"""
	def process_request(self, request):
		#added by duhao
		if is_product_stocks_request(request):
			return None

		#added by slzhu
		request.found_member_in_cache = False
		if is_pay_request(request):
			return None

		if is_js_config(request):
			return None

		if not is_request_for_webapp(request):
			#如果是对webapp的请求，不进行任何处理
			return None

		request.webapp_user = None
		request.member = None
		request.social_account = None

		cookie_openid_webapp_id = request.COOKIES.get(member_settings.OPENID_WEBAPP_ID_KEY, None)
		if not cookie_openid_webapp_id:
			return None

		openid, webapp_id = cookie_openid_webapp_id.split('____')
		if not request.user_profile:
			return None
		#try:
		if webapp_id == request.user_profile.webapp_id:
			from cache import member_cache
			webapp_user, social_account, member = member_cache.get_accounts(openid, webapp_id)
			request.webapp_user = webapp_user
			request.social_account = social_account
			request.member = member

			request.webapp_user.member = request.member
			request.webapp_user.webapp_owner_info = request.webapp_owner_info
			request.found_member_in_cache = True
		else:
			pass
		# except:
		# 	pass


class RedirectBySctMiddleware(object):
	"""
	RedirectBySctMiddleware : 处理由url中的sct引起的跳转
	"""
	def get_member_by_social_account(self, user_profile, social_account):
		member = None
		if MemberHasSocialAccount.objects.filter(account=social_account).count() > 0:
			member = MemberHasSocialAccount.objects.filter(account=social_account)[0].member

		#TODO: 什么时候有social acount无member?
		if not member:
			member = member_util.create_member_by_social_account(user_profile, social_account)

		return member

	def process_sct_in_url(self, request):
		social_account = None
		member = None
		if (member_settings.SOCIAL_ACCOUNT_TOKEN_URL_QUERY_FIELD in request.GET):
			try:
				url_sct = request.GET.get(member_settings.SOCIAL_ACCOUNT_TOKEN_URL_QUERY_FIELD, None)
				cookie_sct = request.COOKIES.get(member_settings.SOCIAL_ACCOUNT_TOKEN_SESSION_KEY, None)

				#构建跳转的url
				if request.found_member_in_cache:
					#member可能在member cache middleware中已被识别出
					fmt = request.member.token
					social_account = request.social_account
				else:
					social_account = SocialAccount.objects.get(token=url_sct)
					member = self.get_member_by_social_account(request.user_profile, social_account)
					fmt = member.token

				new_url = url_helper.remove_querystr_filed_from_request_url(request, member_settings.SOCIAL_ACCOUNT_TOKEN_URL_QUERY_FIELD)
				new_url = url_helper.add_query_part_to_request_url(new_url, member_settings.FOLLOWED_MEMBER_TOKEN_URL_QUERY_FIELD, fmt)
				response = HttpResponseRedirect(new_url)

				#设置cookie
				if not cookie_sct:
					response.set_cookie(member_settings.SOCIAL_ACCOUNT_TOKEN_SESSION_KEY, url_sct, max_age=3600*24*1000)
				else:
				 	if cookie_sct == url_sct:
						pass
					else: # cookie_sct != url_sct
						response.set_cookie(member_settings.SOCIAL_ACCOUNT_TOKEN_SESSION_KEY, url_sct, max_age=3600*24*1000)

				#向cookie中设置mt
				if social_account:
					#member_cookie = '%s_%s' % (social_account., request.user_profile.webapp_id)
					#response.set_cookie(member_settings.MEMBER_TOKEN_SESSION_KEY, member_cookie, max_age=3600*24*1000)
					response.set_cookie(member_settings.OPENID_WEBAPP_ID_KEY, "%s____%s" % (social_account.openid, social_account.webapp_id), max_age=60*60*24*365)

				return response
			except:
				notify_message = u"处理url sct失败，url_sct={}, cause:\n{}".format(url_sct, unicode_full_stack())
				watchdog_error(notify_message)
			finally:
				if not request.member:
					request.social_account = social_account
					request.member = member
		else:
			return None


	def process_sct_in_cookie(self, request):
		social_account = None
		member = None
		if (member_settings.SOCIAL_ACCOUNT_TOKEN_SESSION_KEY in request.COOKIES) and (not member_settings.FOLLOWED_MEMBER_TOKEN_URL_QUERY_FIELD in request.GET):
			cookie_sct = request.COOKIES.get(member_settings.SOCIAL_ACCOUNT_TOKEN_SESSION_KEY, None)
			try:
				if cookie_sct and len(cookie_sct.strip()):
					social_account = SocialAccount.objects.get(token=cookie_sct)
					if social_account.webapp_id == request.user_profile.webapp_id:
						member = self.get_member_by_social_account(request.user_profile, social_account)
						fmt = member.token
						new_url = url_helper.add_query_part_to_request_url(request.get_full_path(), member_settings.FOLLOWED_MEMBER_TOKEN_URL_QUERY_FIELD, fmt)
						response = HttpResponseRedirect(new_url)
						return response
					else:
						#删除cookie中的sct
						#TODO: 优化掉这一个redirect
						response = HttpResponseRedirect(request.get_full_path())
						response.delete_cookie(member_settings.SOCIAL_ACCOUNT_TOKEN_SESSION_KEY)
						return response
			except:
				notify_message = u"处理cookie sct失败，cookie_sct={}, cause:\n{}".format(cookie_sct, unicode_full_stack())
				watchdog_error(notify_message)
			finally:
				request.social_account = social_account
				request.member = member
		else:
			return None

	def modify_social_account(self, request):
		uuid = request.COOKIES.get(member_settings.UUID_SESSION_KEY, None)
		webapp_id = request.user_profile.webapp_id
		social_account_webapp_id = request.social_account.webapp_id
		if webapp_id == social_account_webapp_id:
			#当前的social account是属于webapp的social account
			if uuid != request.social_account.uuid:
				SocialAccount.objects.filter(token=request.social_account.token).update(uuid=uuid)
				request.social_account.uuid = uuid
				#TODO: 更新缓存
		else:
			#当前的social account不是属于webapp的social account，寻找合适的social account
			try:
				if WebAppUser.objects.filter(token=uuid, webapp_id=webapp_id).count() > 0:
					webapp_user= WebAppUser.objects.filter(token=uuid, webapp_id=webapp_id)[0]
					new_social_account = get_scoial_account_by_webapp_user_id(webapp_user.id)
					if new_social_account and new_social_account.webapp_id != webapp_id:
						self.remove_sct_from_request(request)
					else:
						#替换request.social_account
						request.social_account = new_social_account
				else:
					self.remove_sct_from_request(request)
			except:
				self.remove_sct_from_request(request)

	def remove_sct_from_request(self, request):
		request.META[self.NEED_REMOVE_SOCIAL_ACCOUNT_SESSION_FLAG] = True

		if request.COOKIES.has_key(member_settings.SOCIAL_ACCOUNT_TOKEN_SESSION_KEY):
			request.COOKIES.pop(member_settings.SOCIAL_ACCOUNT_TOKEN_SESSION_KEY)

	def process_request(self, request):
		#added by duhao
		if is_product_stocks_request(request):
			return None

		#added by slzhu
		if is_pay_request(request):
			return None

		if request.is_access_temporary_qrcode_image:
			return None

		# 不处理临时二维码请求 by liupeiyu
		if request.is_access_temporary_qrcode_image:
			return None

		if (not request.is_access_webapp) and (not request.is_access_pcmall):
			return None

		if request.POST:
			return None

		if request.user_profile and request.user_profile.is_oauth:
			return None

		if is_js_config(request):
			return None

		response = self.process_sct_in_url(request)
		if response:
			return response

		response = self.process_sct_in_cookie(request)
		if response:
			return response

		return None

	# def process_response(self, request, response):
	# 	if hasattr(request,'user_profile'):
	# 		if request.user_profile and request.user_profile.is_oauth is False:
	# 			response.delete_cookie(member_settings.OPENID_WEBAPP_ID_KEY)
	# 	return response


class RedirectByFmtMiddleware(object):
	"""
	RedirectByFmtMiddleware : 处理由url中的fmt引起的跳转
	"""
	def process_fmt_in_url(self, request):
		cookie_fmt = request.COOKIES.get(member_settings.FOLLOWED_MEMBER_TOKEN_SESSION_KEY, None)
		url_fmt = request.GET.get(member_settings.FOLLOWED_MEMBER_TOKEN_URL_QUERY_FIELD, None)
		# if cookie_fmt == url_fmt:
		# 	return None
		#cookie_fmt != url_fmt 或者 cookie_fmt = None
		if (member_settings.SOCIAL_ACCOUNT_TOKEN_SESSION_KEY in request.COOKIES):
			if request.member:
				new_fmt = request.member.token
				if new_fmt == url_fmt:
					#访问自己的url
					pass
				else:
					#new_url = middleware_util.replace_fmt_in_request_url(request, new_fmt)
					new_url = url_helper.remove_querystr_filed_from_request_url(request, member_settings.FOLLOWED_MEMBER_TOKEN_URL_QUERY_FIELD)
					new_url = url_helper.add_query_part_to_request_url(new_url, member_settings.FOLLOWED_MEMBER_TOKEN_URL_QUERY_FIELD, new_fmt)
					response = HttpResponseRedirect(new_url)
					response.set_cookie(member_settings.FOLLOWED_MEMBER_TOKEN_SESSION_KEY, url_fmt, max_age=60*60*24*365)
					return response
		else:
			new_url = url_helper.remove_querystr_filed_from_request_url(request, member_settings.FOLLOWED_MEMBER_TOKEN_URL_QUERY_FIELD)
			response = HttpResponseRedirect(new_url)
			response.set_cookie(member_settings.FOLLOWED_MEMBER_TOKEN_SESSION_KEY, url_fmt, max_age=60*60*24*365)
			return response

		return None


	def process_request(self, request):
		#added by duhao
		if is_product_stocks_request(request):
			return None

		#added by slzhu
		if is_pay_request(request):
			return None

		if is_js_config(request):
			return None

		# 不处理临时二维码请求 by liupeiyu
		if request.is_access_temporary_qrcode_image:
			return None
		#不处理非webapp和非pcmall的请求
		if (not request.is_access_webapp) and (not request.is_access_pcmall):
			return None
		#不处理非微信请求
		if not request.user.is_from_weixin:
			return None
		if request.user_profile and request.user_profile.is_oauth:
			return None

		#不处理url没有有效fmt的请求
		url_fmt = request.GET.get(member_settings.FOLLOWED_MEMBER_TOKEN_URL_QUERY_FIELD, None)
		if (url_fmt is None) or (len(url_fmt) == 0):
			return None
		#不处理post请求
		if request.POST:
			return None
		response = self.process_fmt_in_url(request)
		if response:
			#如果有response，意味着该shared url第一次被点击，发起event
			request.event_data = event_handler_util.extract_data(request)
			event_handler_util.handle(request, 'shared_url_page_visit')
			#将fmsurl放入cookie
			#shared_url_digest = visit_session_util.get_request_url_digest(request)
			shared_url_digest = _get_hexdigest_url(request.get_full_path())
			response.set_cookie(member_settings.FOLLOWED_MEMBER_SHARED_URL_SESSION_KEY, shared_url_digest, max_age=60*60)
			return response

		return None





class RequestSocialAccountMiddleware(object):
	"""
	RequestSocialAccountMiddleware : 填充当前请求使用的社交账号session的中间件

	对于微信用户和非微信用户有些区别

	微信用户

	由于微信用户访问微站不需要登录，在微信中进入微站就要做到识别当前
	所请求的微信用户，在微信中会通过两种方式进入微站：

	1. 在微站所绑定的公众号的会话环境中
	2. 其他方式

	为了实现该需求，对于第一种方式：
	在会话环境中用户所拿到的所有微站的链接都是在url增加了微信用
	户信息的，该中间件对于这样的请求，会移除url中携带的微信用户
	信息，然后设置cookie(会发生跳转)。

	对于第二种方式：
	a. 如果cookie中有当前微信用户的信息，那么需要对比当前社交账号
	信息(SocialAccount)中记录的webappid和当前所请求的webapp是否一
	致，如果是那么设置当前请求的社交账号为根据cookie信息获取到的
	社交账号；否则清除当前请求的cookie信息，同时设置当前请求社交
	账号为None

	b. 否则清除当前请求的cookie信息，同时设置当前请求社交账号为None

	非微信用户，只进行和微信用户第二种方式相同的处理

	经过该中间件处理后，view的代码中可直接通过request.social_account
	使用当前请求的社交账号信息
	"""
	NEED_REMOVE_SOCIAL_ACCOUNT_SESSION_FLAG = 'need_remove_social_account_session'
	NEED_SET_SOCIAL_ACCOUNT_SESSION_FLAG = 'need_set_social_account_session'

	def process_request(self, request):
		#added by duhao
		if is_product_stocks_request(request):
			return None

		#added by slzhu
		if is_pay_request(request):
			return None

		if is_js_config(request):
			return None

		# 不处理临时二维码请求 by liupeiyu
		if request.is_access_temporary_qrcode_image:
			return None

		#对于非webapp请求和非pc商城的请求不进行任何处理
		if (not request.is_access_webapp) and (not request.is_access_pcmall):
			request.social_account = None
			return None
		if hasattr(request, 'found_member_in_cache') and request.found_member_in_cache:
			#在cache中获得了social account
			assert hasattr(request, 'social_account')
		else:
			if not request.social_account:
				if member_settings.SOCIAL_ACCOUNT_TOKEN_SESSION_KEY in request.COOKIES:

					# sct = request.COOKIES[member_settings.SOCIAL_ACCOUNT_TOKEN_SESSION_KEY]
					# if sct:
					# 	try:
					# 		request.social_account = SocialAccount.objects.get(token=sct)
					# 	except:
					# 		notify_message = u"sct对应多于一个social account:(sct：{}), cause:\n{}".format(sct, unicode_full_stack())
					# 		watchdog_error(notify_message, user_id=request.user_profile.user_id)
					sct = request.COOKIES[member_settings.SOCIAL_ACCOUNT_TOKEN_SESSION_KEY]
					if sct:
						try:
							social_account = SocialAccount.objects.get(token=sct)
							if social_account.webapp_id != request.user_profile.webapp_id:
								uuid = request.COOKIES.get(member_settings.UUID_SESSION_KEY, None)
								webapp_id = request.user_profile.webapp_id
								if uuid and WebAppUser.objects.filter(token=uuid, webapp_id=webapp_id).count() > 0:
									webapp_user= WebAppUser.objects.filter(token=uuid, webapp_id=webapp_id)[0]
									social_account = member_api.get_scoial_account_by_webapp_user_id(webapp_user.id)
									if social_account and social_account.webapp_id == webapp_id:
										#TODO: 添加这种情况的scenario
										request.social_account = social_account
							else:
								request.social_account = social_account
						except:
							notify_message = u"sct对应多于一个social account:(sct：{}), cause:\n{}".format(sct, unicode_full_stack())
							watchdog_error(notify_message)
				else:
					#无sct，根据webapp user寻找social account
					uuid = request.COOKIES.get(member_settings.UUID_SESSION_KEY, None)
					webapp_id = request.user_profile.webapp_id
					if uuid and WebAppUser.objects.filter(token=uuid, webapp_id=webapp_id).count() > 0:
						webapp_user= WebAppUser.objects.filter(token=uuid, webapp_id=webapp_id)[0]
						social_account = member_api.get_scoial_account_by_webapp_user_id(webapp_user.id)
						if social_account and social_account.webapp_id == webapp_id:
							#TODO: 添加这种情况的scenario
							request.social_account = social_account
			else:
				#无sct，根据webapp user寻找social account
				uuid = request.COOKIES.get(member_settings.UUID_SESSION_KEY, None)
				if request.user_profile:
					webapp_id = request.user_profile.webapp_id
					if uuid and WebAppUser.objects.filter(token=uuid, webapp_id=webapp_id).count() > 0:
						webapp_user= WebAppUser.objects.filter(token=uuid, webapp_id=webapp_id)[0]
						social_account = member_api.get_scoial_account_by_webapp_user_id(webapp_user.id)
						if social_account and social_account.webapp_id == webapp_id:
							#TODO: 添加这种情况的scenario
							request.social_account = social_account
		if request.social_account:
			uuid = request.COOKIES.get(member_settings.UUID_SESSION_KEY, None)
			if uuid != request.social_account.uuid:
				#SocialAccount.objects.filter(token=request.social_account.token).update(uuid=uuid)
				if request.found_member_in_cache:
					#清除cache，更新缓存中social account的uuid，防止一直进行update操作
					#TODO: 优化这里的逻辑
					from cache import member_cache
					member_cache.delete_member_cache(request.member.token, request.user_profile.webapp_id)
				request.social_account.uuid = uuid


class MemberMiddleware(object):
	def get_member_by_social_account(self, user_profile, social_account):
		member = None
		try:
			member = MemberHasSocialAccount.objects.filter(account=social_account)[0].member
		except:
			pass
		#if MemberHasSocialAccount.objects.filter(account=social_account).count() > 0:
		#	member = MemberHasSocialAccount.objects.filter(account=social_account)[0].member

		#TODO: 什么时候有social acount无member?
		if not member:
			member = member_util.create_member_by_social_account(user_profile, social_account)

		return member

	def process_request(self, request):
		#added by duhao
		if is_product_stocks_request(request):
			return None

		#added by slzhu
		if is_pay_request(request):
			return None


		if is_js_config(request):
			return None

		# 不处理临时二维码请求 by liupeiyu
		if request.is_access_temporary_qrcode_image:
			return None

		#不处理非webapp和非pcmall的请求
		if (not request.is_access_webapp) and (not request.is_access_pcmall):
			return None

		if request.found_member_in_cache:
			assert hasattr(request, 'member')
			return None

		#不处理非微信请求
		#TODO request.user.is_from_simulator is False  not  right
		if settings.MODE not in ['develop', 'test']:
			if (not request.user.is_from_weixin) and (not request.user.is_from_simulator):
				return None
		if not request.member and request.social_account:
			request.member = self.get_member_by_social_account(request.user_profile, request.social_account)

		assert hasattr(request, 'member')
		return None



class MemberSessionMiddleware(object):
	"""
	获取当前请求的会员信息

	view中的代码可直接通过request.member获取当前请求的会员
	该中间件需要置于RequestSocialAccountSessionMiddleware之后
	该中间件需置于RequestSocialAccountSessionMiddleware之后
	"""
	NEED_SET_UUID_SESSION_FLAG = 'need_set_uuid_session'

	def process_request(self, request):
		if 'pay.weapp.com' in request.META.get('HTTP_HOST', ''):
			return None


		if is_js_config(request):
			return None

		#对于非webapp请求和非pc商城地方请求不进行处理
		if (not is_request_for_webapp(request)) and (not is_request_for_pcmall(request)):
			return None
		request.member = self.get_request_member(request)

		if request.member is None and request.uuid is None:
			#获取不到当前请求的会员信息并且uuid是none 设置uuid 信息
			uuid = get_uuid(request)
			if uuid is None:
				uuid = generate_uuid(request)
				request.META[member_settings.UUID_SESSION_KEY] = uuid
				request.META[self.NEED_SET_UUID_SESSION_FLAG] = True
			request.uuid = uuid
		else:
			#更新会员最近访问时间
			Member.update_last_visit_time(request.member)

		if request.member is not None:
			try:
				update_member_group(request.user_profile, request.member, request.social_account)
			except:
				notify_message = u"更新会员分组信息失败，会员信息:(member_id：{}), cause:\n{}".format(
						request.member.id, unicode_full_stack())
				watchdog_info(notify_message, user_id=request.user_profile.user_id)

		return None

	def get_request_member(self, request):
		member = get_member(request)
		if member is None and request.social_account:
			#还不是会员，且可以获取到当前请求的社交账号信息，则创建会员信息
			member = create_member(request)
			#首次绑定为会员，需要对积分进行计算；判断是否是新创建会员 如果是，则增加首次关注积分
			integral.increase_for_be_member_first(request.user_profile, member)

		return member

	def process_response(self, request, response):
		return response


def _is_need_process_for_shared_url_request(request):
	if not is_request_for_webapp(request):
		#对于非webapp的请求不进行任何处理
		return False

	followed_member_token = get_followed_member_token_from_url_querystr(request)
	if followed_member_token is None or len(followed_member_token) == 0:
		#对于url中没有分享者token信息的不进行处理
		#因为不是分享链接
		return False

	return True


class RemoveSharedInfoMiddleware(object):
	SHOULD_REMOVE_SHARED_URL_SESSION_FLAG = 'should_remove_shared_url_session'

	def process_response(self, request, response):
		if self.SHOULD_REMOVE_SHARED_URL_SESSION_FLAG in request.META:
			response.delete_cookie(member_settings.FOLLOWED_MEMBER_TOKEN_SESSION_KEY)
			response.delete_cookie(member_settings.FOLLOWED_MEMBER_SHARED_URL_SESSION_KEY)

		return response

#===============================================================================
# SharedPageVisitSessionMiddleWare : 对分享页的访问信息进行记录的MiddleWare
#===============================================================================
# class SharedPageVisitSessionMiddleWare(object):
# 	#TODO: [CACHE] 将该逻辑移动到service中
# 	def process_request(self, request):
# 		if not _is_need_process_for_shared_url_request(request):
# 			return None

# 		#记录分享链接的访问记录
# 		try:
# 			record_shared_page_visit(request)
# 		except:
# 			notify_message = u"进行页面访问记录失败，path={}, cause:\n{}".format(request.get_full_path(), unicode_full_stack())
# 			watchdog_error(notify_message)

# 		return None


class MemberRelationMiddleware(object):
	"""
	MemberRelationMiddleware : 会员关系中间件
	"""
	#TODO: [CACHE] 将该逻辑移动到service中
	SHOULD_REMOVE_FOLLOWED_MEMBER_SESSION_FLAG = 'should_remove_followed_member_session'

	def process_request(self, request):
		#对于管理后台的请求不进行任何处理
		if is_request_for_editor(request):
			return None

		#TODO 是否需要考虑避免每次都尝试建立关系
		build_member_follow_relation(request)
		return None

	def process_response(self, request, response):
		if self.SHOULD_REMOVE_FOLLOWED_MEMBER_SESSION_FLAG in request.META:
			response.delete_cookie(member_settings.FOLLOWED_MEMBER_TOKEN_SESSION_KEY)
			response.delete_cookie(member_settings.FOLLOWED_MEMBER_SHARED_URL_SESSION_KEY)

		return response


class WebAppUserMiddleware(object):
	"""
	WebAppUserMiddleware : WebApp用户的中间件

	该中间件在处理过程中会统一同一用户在成为会员前和成为会员后对应的WebAppUser
	"""
	def process_request(self, request):
		#added by duhao
		if is_product_stocks_request(request):
			return None

		#added by slzhu
		if is_pay_request(request):
			return None

		if is_js_config(request):
			return None

		# 不处理临时二维码请求 by liupeiyu
		if request.is_access_temporary_qrcode_image:
			return None

		if not request.is_access_webapp and not is_paynotify_request(request):
			return None

		if request.is_access_mock_pay:
			return None

		if request.is_access_pay and not request.is_access_mock_pay:
			webapp_user = get_request_webapp_user_by_member(request)
			if webapp_user:
				request.webapp_user = webapp_user
				request.webapp_user.member = request.member
				request.webapp_user.webapp_owner_info = request.webapp_owner_info
			return None

		#如果当前请求的cookie中携带了uuid信息，该uuid有对应的webappuser
		#并且和当前请求的会员对应的webappuser不同，那么把当前请求的会员
		#对应的webappuser对应到uuid对应的webappuser，这样当一个用户在成
		#为会员后能够关联成为会员前所进行的所有操作
		webapp_user = None

		uuid = request.COOKIES.get(member_settings.UUID_SESSION_KEY, None)

		if (uuid is not None) and (request.member is not None):
			uuid_related_webapp_user = get_request_webapp_user_by_uuid(uuid, request.user_profile.webapp_id)
			if uuid_related_webapp_user is not None:
				if request.found_member_in_cache:
					member_related_webapp_user = request.webapp_user
				else:
					member_related_webapp_user = get_request_webapp_user_by_member(request, False)
				if member_related_webapp_user is not None:
					webapp_user = member_related_webapp_user
					request.webapp_user = webapp_user
					if (member_related_webapp_user.id != uuid_related_webapp_user.id):# and (uuid_related_webapp_user.member_id != member_related_webapp_user.member_id):
						#uuid_related_webapp_user.token = member_related_webapp_user.token
						uuid_related_webapp_user.member_id = member_related_webapp_user.member_id
						uuid_related_webapp_user.father_id = member_related_webapp_user.id
						uuid_related_webapp_user.save()
						update_models_use_webapp_user(member_related_webapp_user, uuid_related_webapp_user)

		if not request.found_member_in_cache:
			if webapp_user is None:
				webapp_user = get_request_webapp_user_by_member(request)
				request.webapp_user = webapp_user
				request.webapp_user.member = request.member
				request.webapp_user.webapp_owner_info = request.webapp_owner_info
		try:
			if request.webapp_user:
				request.webapp_user.member = request.member
				request.webapp_user.webapp_owner_info = request.webapp_owner_info
				assert hasattr(request, 'webapp_user')
				assert hasattr(request.webapp_user, 'member')
				assert hasattr(request.webapp_user, 'webapp_owner_info')
		except:
			notify_message = u"WebAppUserMiddleware error, cause:\n{}".format(unicode_full_stack())
			watchdog_error(notify_message)


class MemberSouceMiddleware(object):
	"""
	目前针对非扫会员二维码成为会员的会员进行判断是否曾点击过其他会员分享的链接。
	"""
	def process_request(self, request):
		#对于非webapp请求和非pc商城的请求不进行任何处理
		try:
			if (not is_request_for_webapp(request)) and (not is_request_for_pcmall(request)):
				return None


			if is_js_config(request):
				return None


			if request.app is None:
				return None

			member = get_request_member(request)
			if member is None:
				return None
			if member.source == -1:
				followed_member_token = get_followed_member_token(request)
				if followed_member_token:
					followed_member = get_member_by_member_token(followed_member_token)
					if followed_member and member and member.id != followed_member.id and followed_member.webapp_id == request.app.appid:
						Member.objects.filter(id=member.id).update(source=SOURCE_BY_URL)
						try:
							shared_url_digest = request.COOKIES.get(member_settings.FOLLOWED_MEMBER_SHARED_URL_SESSION_KEY, None)
							if shared_url_digest:
								integral.increase_shared_url_followers(followed_member,shared_url_digest)
						except :
							notify_message = u"MemberSouceMiddleware error, cause:\n{}".format(unicode_full_stack())
							watchdog_error(notify_message)
					else:
						Member.objects.filter(id=member.id).update(source=SOURCE_SELF_SUB)
				else:
					Member.objects.filter(id=member.id).update(source=SOURCE_SELF_SUB)
			return None
		except:
			notify_message = u"MemberSouceMiddleware error, cause:\n{}".format(unicode_full_stack())
			watchdog_error(notify_message)



class AddUuidSessionMiddleware(object):
	"""
	AddUuidSessionMiddleware : uuid 在系统中唯一标识
	流程经过AddUuidSessionMiddleware后，request中一定有request.uuid
	"""
	def process_request(self, request):
		#added by slzhu
		if is_pay_request(request):
			return None

		#对于支付请求，不处理
		if request.is_access_pay or request.is_access_paynotify_callback:
			return None

		# 不处理临时二维码请求 by liupeiyu
		if request.is_access_temporary_qrcode_image:
			return None

		#对于非webapp请求和非pc商城地方请求不进行处理
		if (not request.is_access_webapp) and (not request.is_access_pcmall):
			return None

		#设置request.uuid
		uuid = request.COOKIES.get(member_settings.UUID_SESSION_KEY, None)
		if uuid is None:
			uuid = member_identity_util.generate_uuid(request)
			request.META[member_settings.UUID_SESSION_KEY] = uuid

		request.uuid = uuid
		return None

	def process_response(self, request, response):
		""" TODO : (not request.is_access_webapp) and (not request.is_access_pcmall) """
		if (not is_request_for_webapp(request)) and (not is_request_for_pcmall(request)):
			return response

		if member_settings.UUID_SESSION_KEY in request.META:
			uuid = request.META[member_settings.UUID_SESSION_KEY]
			try:
				response.set_cookie(member_settings.UUID_SESSION_KEY, uuid, max_age=60*60*24*365)
			except:
				try:
					response.set_cookie(member_settings.UUID_SESSION_KEY, uuid, max_age=60*60*24*365)
				except:
					pass

		return response

from modules.member.integral_new import increase_for_click_shared_url
import urllib2
import urllib
import json
import hashlib
from BeautifulSoup import BeautifulSoup
from weixin.user.models import get_token_for

class OAUTHMiddleware(object):
	"""
	授权的中间件
	"""
	def _get_webapp_user(self, member):
		try:
			webapp_user = WebAppUser.objects.filter(member_id=member.id, webapp_id=member.webapp_id, father_id=0)[0]
		except:
			webapp_user = WebAppUser.objects.create(member_id=member.id, webapp_id=member.webapp_id)

		return webapp_user

	def process_request(self, request):
		#added by duhao
		if is_product_stocks_request(request):
			return None

		#added by slzhu
		if is_pay_request(request):
			return None

		if is_js_config(request):
			return None

		#对于支付请求，不处理
		if request.is_access_pay or request.is_access_paynotify_callback:
			return None
		if request.user.is_from_simulator:
			return None

		#不处理非微信请求
		if not request.user.is_from_weixin:
			return None

		# 不处理临时二维码请求 by liupeiyu
		if request.is_access_temporary_qrcode_image:
			return None

		#对于非webapp请求和非pc商城地方请求不进行处理
		if (not request.is_access_webapp) and (not request.is_access_pcmall):
			return None

		if 'model=address' in request.get_full_path():
			return None
		# if is_request_for_api(request):
		#  	return None
		if request.webapp_owner_info and \
			request.webapp_owner_info.mpuser and \
			request.webapp_owner_info.mpuser.is_certified and \
			request.webapp_owner_info.mpuser.is_service and \
			request.webapp_owner_info.mpuser.is_active and request.user_profile and request.user_profile.is_oauth:
			is_oauth = False
			#cookie_openid_webapp_id  ==  'openid____webappid'
			cookie_openid_webapp_id = request.COOKIES.get(member_settings.OPENID_WEBAPP_ID_KEY, None)
			request_fmt = request.GET.get(member_settings.FOLLOWED_MEMBER_TOKEN_SESSION_KEY, None)
			if is_request_for_api(request) or 'pay' in request.get_full_path():
				request_fmt = True
			#cookie_webapp_id = request.COOKIES.get('webapp_id', None)
			#1 如果cookie中没有 cookie_open_id or cookie_opeqqqn_id 则进行授权
			#print '================middleware cookie :', request.COOKIES.get(member_settings.FOLLOWED_MEMBER_TOKEN_SESSION_KEY, None)
			if (cookie_openid_webapp_id is None) or (not request_fmt):
				is_oauth = True
			else:
				split_list = cookie_openid_webapp_id.split('____')
				if len(split_list) != 2:
					is_oauth =True
				else:
					webapp_id = split_list[1]
					openid = split_list[0]
					if webapp_id != request.user_profile.webapp_id or (not openid):
						is_oauth =True
					else:
						try:
							#通过openid_webapp_id获取用户信息
							is_new_created_member = False
							if request.found_member_in_cache is False:
								social_accounts = SocialAccount.objects.filter(openid=openid, webapp_id=request.user_profile.webapp_id)
								if social_accounts.count() > 0:
									social_account = social_accounts[0]
									member, response = get_member_by(request, social_account)
								else:
									token = get_token_for(request.user_profile.webapp_id, openid)
									social_account = member_util.create_social_account(request.user_profile.webapp_id, openid, token, SOCIAL_PLATFORM_WEIXIN)
									member = self.get_member_by(request, social_account)
								# if response:
								# 	return response
								if member and hasattr(member, 'is_new_created_member'):
									is_new_created_member = member.is_new_created_member

								request.member = member
								request.social_account = social_account
								request.webapp_user = self._get_webapp_user(request.member)
							#处理sct

							response = self.process_sct_in_url(request)
							if response:
								return response
							#处理fmt
							response = self.process_fmt_in_url(request, is_new_created_member)
							if response:
								return response

							if ('share_red_envelope' in request.get_full_path() or 'refueling' in request.get_full_path()) and (not request.member.user_icon):
								# 分享红包没有用户头像时跳转授权接口
								is_oauth = True
							else:
								return None
						except:
							notify_message = u"OAUTHMiddleware error 获取socialaccount, cause:\n{}".format(unicode_full_stack())
							watchdog_error(notify_message)
							is_oauth = True
							request.social_account = None
							request.member = None
							request.webapp_user = None

			if is_oauth:
				response_data, response =  get_oauthinfo_by(request)
				if response:
					return response

				if response_data.has_key('openid'):
					weixin_user_name = response_data['openid']
					access_token = response_data['access_token']
					social_accounts = SocialAccount.objects.filter(openid=weixin_user_name, webapp_id=request.user_profile.webapp_id)
					if social_accounts.count() > 0:
						social_account = social_accounts[0]
					else:
						token = get_token_for(request.user_profile.webapp_id, weixin_user_name)
						social_account = member_util.create_social_account(request.user_profile.webapp_id, weixin_user_name, token, SOCIAL_PLATFORM_WEIXIN)

					member = self.get_member_by(request, social_account)

					if not member:
						watchdog_error(u'授权时创建会员信息失败1 %s' % weixin_user_name)
						member = self.get_member_by(request, social_account)
						watchdog_error(u'授权时创建会员信息失败2 %s' % weixin_user_name)

					if ('share_red_envelope' in request.get_full_path() or 'refueling' in request.get_full_path())and member:
						if (not member.user_icon) or (not member.user_icon.startswith('http')):
							get_user_info(weixin_user_name, access_token, member)

					request.social_account = social_account
					request.member = member
					#处理分享链接
					self.process_shared_url(request, member.is_new_created_member)

					response = self.process_current_url(request)
					return response
		return None


	def get_member_by(self, request, social_account):
		member = member_util.get_member_by_binded_social_account(social_account)
		if member is None:
			#创建会员信息
			try:
				member = member_util.create_member_by_social_account(request.user_profile, social_account, True)
				member_util.member_basic_info_updater(request.user_profile, member, True)
				#member = Member.objects.get(id=member.id)
				#之后创建对应的webappuser
				_create_webapp_user(member)
				member.is_new_created_member = True
				"""
					不增加积分，关注时候增加积分
				"""
				# try:
				# 	integral.increase_for_be_member_first(request.user_profile, member)
				# except:
				# 	notify_message = u"get_member_by中创建会员后增加积分失败，会员id:{}, cause:\n{}".format(
				# 			member.id, unicode_full_stack())
				# 	watchdog_error(notify_message)
				try:
					name = url_helper.get_market_tool_name_from(request.get_full_path())
					#if name:
					if not name:
						name = ''
					if request:
						MemberMarketUrl.objects.create(
							member = member,
							market_tool_name = name,
							url = request.get_full_path(),
							)
				except:
					notify_message = u"get_member_by中MemberMarketUrl失败，会员id:{}, cause:\n{}".format(member.id, unicode_full_stack())
					watchdog_error(notify_message)
				return member
			except:
				notify_message = u"MemberHandler中创建会员信息失败，社交账户信息:('openid':{}), cause:\n{}".format(
					social_account.openid, unicode_full_stack())
				watchdog_fatal(notify_message)
				try:
					member = member_util.create_member_by_social_account(request.user_profile, social_account, True)
					#之后创建对应的webappuser
					_create_webapp_user(member)
					member.is_new_created_member = True
					member_util.member_basic_info_updater(request.user_profile, member, True)
					# try:
					# 	integral.increase_for_be_member_first(request.user_profile, member)
					# except:
					# 	notify_message = u"get_member_by中创建会员后增加积分失败，会员id:{}, cause:\n{}".format(
					# 			member.id, unicode_full_stack())
					# 	watchdog_error(notify_message)
					return member
				except:
					#response = process_to_oauth(request,weixin_mp_user_access_token)
					#if response:
					#	return None,response
					return None

		else:
			member.is_new_created_member = False
			return member

	# 授权并且创建结束后进行跳转并且设置cookie 信息
	# 删除 当前url中的fmt
	def process_current_url(self, request):
		member = request.member
		social_account = request.social_account
		fmt = request.GET.get(member_settings.FOLLOWED_MEMBER_TOKEN_URL_QUERY_FIELD, None)
		new_url = request.get_full_path()
		if fmt != member.token:
			new_url = url_helper.remove_querystr_filed_from_request_path(new_url, member_settings.FOLLOWED_MEMBER_TOKEN_URL_QUERY_FIELD)

		if 'code' in request.GET:
			new_url = url_helper.remove_querystr_filed_from_request_path(new_url, 'code')

		if 'appid' in request.GET:
			new_url = url_helper.remove_querystr_filed_from_request_path(new_url, 'appid')

		if member_settings.SOCIAL_ACCOUNT_TOKEN_SESSION_KEY in request.GET:
			new_url = url_helper.remove_querystr_filed_from_request_path(new_url, member_settings.SOCIAL_ACCOUNT_TOKEN_SESSION_KEY)

		if member_settings.URL_OPENID in request.GET:
			new_url = url_helper.remove_querystr_filed_from_request_url(new_url, member_settings.URL_OPENID)

		new_url = url_helper.add_query_part_to_request_url(new_url, member_settings.FOLLOWED_MEMBER_TOKEN_URL_QUERY_FIELD, member.token)
		response = HttpResponseRedirect(new_url)
		response.set_cookie(member_settings.OPENID_WEBAPP_ID_KEY, "%s____%s" % (social_account.openid, request.user_profile.webapp_id), max_age=60*60*24*365)
		response.set_cookie(member_settings.SOCIAL_ACCOUNT_TOKEN_SESSION_KEY, social_account.token, max_age=60*60*24*365)
		if fmt != member.token:
			response.set_cookie(member_settings.FOLLOWED_MEMBER_TOKEN_SESSION_KEY, fmt, max_age=60*60*24*365)
			shared_url_digest = _get_hexdigest_url(request.get_full_path())
			response.set_cookie(member_settings.FOLLOWED_MEMBER_SHARED_URL_SESSION_KEY, shared_url_digest, max_age=60*60)
		return response

	def process_fmt_in_url(self, request, is_new_created_member=False):
		cookie_fmt = request.COOKIES.get(member_settings.FOLLOWED_MEMBER_TOKEN_SESSION_KEY, None)
		url_fmt = request.GET.get(member_settings.FOLLOWED_MEMBER_TOKEN_URL_QUERY_FIELD, None)
		self.process_shared_url(request,is_new_created_member)
		# if cookie_fmt == url_fmt:
		# 	return None
		#cookie_fmt != url_fmt 或者 cookie_fmt = None
		print '===========',request.member.token, url_fmt, cookie_fmt
		if request.member and url_fmt:
			new_fmt = request.member.token
			if new_fmt == url_fmt:
				return None
			else:
				new_url = url_helper.remove_querystr_filed_from_request_url(request, member_settings.FOLLOWED_MEMBER_TOKEN_URL_QUERY_FIELD)

				if member_settings.URL_OPENID in request.GET:
					new_url = url_helper.remove_querystr_filed_from_request_url(new_url, member_settings.URL_OPENID)

				new_url = url_helper.add_query_part_to_request_url(new_url, member_settings.FOLLOWED_MEMBER_TOKEN_URL_QUERY_FIELD, new_fmt)
				response = HttpResponseRedirect(new_url)

				response.set_cookie(member_settings.FOLLOWED_MEMBER_TOKEN_SESSION_KEY, url_fmt, max_age=60*60*24*365)

				shared_url_digest = _get_hexdigest_url(request.get_full_path())

				response.set_cookie(member_settings.FOLLOWED_MEMBER_SHARED_URL_SESSION_KEY, shared_url_digest, max_age=60*60)
				return response
		return None


	def process_sct_in_url(self, request):
		if (member_settings.SOCIAL_ACCOUNT_TOKEN_URL_QUERY_FIELD in request.GET):
			try:
				#构建跳转的url
				social_account =  request.social_account
				if hasattr(request, 'member')  and request.member:
					member = request.member
				else:
					member, _ = get_member_by(request, social_account)
				fmt = member.token

				new_url = url_helper.remove_querystr_filed_from_request_url(request, member_settings.SOCIAL_ACCOUNT_TOKEN_URL_QUERY_FIELD)
				new_url = url_helper.add_query_part_to_request_url(new_url, member_settings.FOLLOWED_MEMBER_TOKEN_URL_QUERY_FIELD, fmt)

				if member_settings.URL_OPENID not in request.GET:
					new_url = url_helper.add_query_part_to_request_url(new_url, member_settings.FOLLOWED_MEMBER_TOKEN_URL_QUERY_FIELD, fmt)

				response = HttpResponseRedirect(new_url)
				response.delete_cookie(member_settings.FOLLOWED_MEMBER_TOKEN_SESSION_KEY)
				response.delete_cookie(member_settings.FOLLOWED_MEMBER_SHARED_URL_SESSION_KEY)
				return response
			except:
				notify_message = u"处理url sct失败 cause:\n{}".format(unicode_full_stack())
				watchdog_error(notify_message)
				return None
		else:
			return None

	def process_shared_url(self, request, is_new_created_member=False):
		request.event_data = event_handler_util.extract_data(request)
		request.event_data['is_new_created_member'] = is_new_created_member
		event_handler_util.handle(request, 'oauth_shared_url')
		# fmt = request.GET.get(member_settings.FOLLOWED_MEMBER_TOKEN_URL_QUERY_FIELD, None)
		# member = request.member
		# if member:
		# 	from modules.member.tasks import process_oauth_member_relation_and_source
		# 	process_oauth_member_relation_and_source.delay(fmt, member.id, is_new_created_member)

def _create_webapp_user(member):
	try:
		if WebAppUser.objects.filter(token = member.token, webapp_id = member.webapp_id, member_id = member.id).count() == 0:
			WebAppUser.objects.create(
				token = member.token,
				webapp_id = member.webapp_id,
				member_id = member.id
				)
	except:
		pass

def get_member_by(request, social_account):
	member = member_util.get_member_by_binded_social_account(social_account)
	if member is None:
		#创建会员信息
		try:
			member = member_util.create_member_by_social_account(request.user_profile, social_account)
			member_util.member_basic_info_updater(request.user_profile, member)
			member = Member.objects.get(id=member.id)
			#之后创建对应的webappuser
			_create_webapp_user(member)
			member.is_new_created_member = True
			try:
				integral.increase_for_be_member_first(request.user_profile, member)
			except:
				notify_message = u"get_member_by中创建会员后增加积分失败，会员id:{}, cause:\n{}".format(
						member.id, unicode_full_stack())
				watchdog_error(notify_message)
			try:
				name = url_helper.get_market_tool_name_from(request.get_full_path())
				#if name:
				if not name:
					name = ''
				if request:
					MemberMarketUrl.objects.create(
						member = member,
						market_tool_name = name,
						url = request.get_full_path(),
						)
			except:
				notify_message = u"get_member_by中MemberMarketUrl失败，会员id:{}, cause:\n{}".format(member.id, unicode_full_stack())
				watchdog_error(notify_message)

			return member,None
		except:
			notify_message = u"MemberHandler中创建会员信息失败，社交账户信息:('openid':{}), cause:\n{}".format(
				social_account.openid, unicode_full_stack())
			watchdog_fatal(notify_message)
			try:
				member = member_util.create_member_by_social_account(request.user_profile, social_account)
				#之后创建对应的webappuser
				_create_webapp_user(member)
				member.is_new_created_member = True
				try:
					integral.increase_for_be_member_first(request.user_profile, member)
				except:
					notify_message = u"get_member_by中创建会员后增加积分失败，会员id:{}, cause:\n{}".format(
							member.id, unicode_full_stack())
					watchdog_error(notify_message)
				return member,None
			except:
				#response = process_to_oauth(request,weixin_mp_user_access_token)
				#if response:
				#	return None,response
				return None, None

	else:
		member.is_new_created_member = False
		return member, None

def get_oauthinfo_by(request):
	code = request.GET.get('code', None)
	appid = request.GET.get('appid', None)
	mpuser = request.webapp_owner_info.mpuser
	weixin_mp_user_access_token = WeixinMpUserAccessToken.objects.get(mpuser=mpuser)
	response = process_to_oauth(request, weixin_mp_user_access_token, code, appid)
	if response:
		return None, response

	# data = {
	# 	'appid': weixin_mp_user_access_token.app_id,
	# 	'secret': weixin_mp_user_access_token.app_secret,
	# 	'code': code,
	# 	'grant_type': 'authorization_code'
	# }

	# url = 'https://api.weixin.qq.com/sns/oauth2/access_token?'
	component_authed_appid = ComponentAuthedAppid.objects.filter(authorizer_appid=appid, user_id=request.user_profile.user_id)[0]
	component_info = component_authed_appid.component_info
	component_access_token = component_info.component_access_token
	data = {
		'appid': appid,
		#'secret': weixin_mp_user_access_token.app_secret,
		'code': code,
		'grant_type': 'authorization_code',
		'component_appid': component_info.app_id,
		'component_access_token': component_access_token
	}
	url = 'https://api.weixin.qq.com/sns/oauth2/component/access_token'

	try:
		req = urllib2.urlopen(url, urllib.urlencode(data))
		response_data = eval(req.read())
		return response_data, None
	except:
		try:
			req = urllib2.urlopen(url, urllib.urlencode(data))
			response_data = eval(req.read())
			return response_data, None
		except :
			try:
				req = urllib2.urlopen(url, urllib.urlencode(data))
				response_data = eval(req.read())
				return response_data, None
			except :
				notify_message = u"oauth2 access_token: cause:\n{}".format(unicode_full_stack())
				watchdog_fatal(notify_message)
				response = process_to_oauth(request,weixin_mp_user_access_token)
				if response:
					return None, response

def get_user_info(openid, access_token, member):
	url = 'https://api.weixin.qq.com/sns/userinfo'
	data = {
		'access_token': access_token,
		'openid': openid,
		'lang': 'zh_CN'
	}
	response_data = {}
	try:
		req = urllib2.urlopen(url, urllib.urlencode(data))
		response_data = eval(req.read())
	except:
		try:
			req = urllib2.urlopen(url, urllib.urlencode(data))
			response_data = eval(req.read())
		except :
			notify_message = u"userinfo: cause:\n{}".format(unicode_full_stack())
			watchdog_fatal(notify_message)

	if response_data.has_key('openid'):
		nickname = response_data['nickname']
		if isinstance(nickname, unicode):
			member_nickname_str = nickname.encode('utf-8')
		else:
			member_nickname_str = nickname
		username_hexstr = byte_to_hex(member_nickname_str)
		user_icon = ''
		if '\/' in response_data['headimgurl']:
			user_icon = response_data['headimgurl'].replace('\/', '/')
		Member.objects.filter(id=member.id).update(
					username_hexstr=username_hexstr,
					user_icon=user_icon,
					sex=response_data['sex'],
					province=response_data['province'],
					city=response_data['city'],
					country=response_data['country']
			)

def process_to_oauth(request, weixin_mp_user_access_token, code=None, appid=None):
	if not code or not appid:# 没有code需要跳转至微信授权页面
		redirect_url = request.get_full_path()
		if 'code' in request.GET:
			redirect_url = url_helper.remove_querystr_filed_from_request_url(request, 'code')

		if 'appid' in request.GET:
			redirect_url = url_helper.remove_querystr_filed_from_request_path(redirect_url, 'appid')

		if 'scope' in request.GET:
			redirect_url = url_helper.remove_querystr_filed_from_request_path(redirect_url, 'scope')

		if 'state' in request.GET:
			redirect_url = url_helper.remove_querystr_filed_from_request_path(redirect_url, 'state')

		if 'component_appid' in request.GET:
			redirect_url = url_helper.remove_querystr_filed_from_request_path(redirect_url, 'component_appid')

		if not redirect_url.startswith('http'):
			redirect_url = "http://%s%s" % (request.META['HTTP_HOST'], redirect_url)

		if "share_red_envelope" in request.get_full_path() or "refueling_page" in request.get_full_path():
			api_style = "snsapi_userinfo"
		else:
			api_style = "snsapi_base"

		component_info = ComponentAuthedAppid.objects.filter(authorizer_appid=weixin_mp_user_access_token.app_id)[0].component_info
		weixin_auth_url = 'https://open.weixin.qq.com/connect/oauth2/authorize' \
			+ '?appid=%s&redirect_uri=%s&response_type=code&scope=%s&state=123&component_appid=%s#wechat_redirect' \
			% (weixin_mp_user_access_token.app_id, urllib.quote(redirect_url).replace('/','%2F'), api_style, component_info.app_id)
		return HttpResponseRedirect(weixin_auth_url)
	else:
		return None

class ProcessOpenidMiddleware(object):
	"""替换url中的opid to sct = xx"""

	def process_request(self, request):
		#对于非webapp请求和非pc商城的请求不进行任何处理
		openid = request.GET.get('opid', '')
		member = None
		social_account = None
		if openid and request.user_profile:
			if SocialAccount.objects.filter(openid=openid, webapp_id=request.user_profile.webapp_id).count() > 0:
				social_account = SocialAccount.objects.get(openid=openid, webapp_id=request.user_profile.webapp_id)
				member, _ = get_member_by(request, social_account)
			else:
				try:
					if request.user_profile.is_oauth is False:
						member, social_account = _process_error_openid(openid, request.user_profile, request)
				except:
					notify_message = u"ProcessOpenidMiddleware error, cause:\n{}".format(unicode_full_stack())
					watchdog_error(notify_message)
			if member and social_account:
				new_url = url_helper.remove_querystr_filed_from_request_url(request, member_settings.SOCIAL_ACCOUNT_TOKEN_URL_QUERY_FIELD)
				fmt = member.token

				if member_settings.URL_OPENID in request.GET:
					new_url = url_helper.remove_querystr_filed_from_request_url(new_url, member_settings.URL_OPENID)

				new_url = url_helper.add_query_part_to_request_url(new_url, member_settings.FOLLOWED_MEMBER_TOKEN_URL_QUERY_FIELD, fmt)

				response = HttpResponseRedirect(new_url)
				response.set_cookie(member_settings.OPENID_WEBAPP_ID_KEY, social_account.openid+"____"+social_account.webapp_id, max_age=60*60*24*365)
				response.set_cookie(member_settings.SOCIAL_ACCOUNT_TOKEN_SESSION_KEY, social_account.token, max_age=60*60*24*365)
				response.set_cookie(member_settings.FOLLOWED_MEMBER_TOKEN_SESSION_KEY, fmt, max_age=60*60*24*365)
				return response
			else:
				new_url = str(request.get_full_path())
				if member_settings.URL_OPENID in request.GET:
					new_url = url_helper.remove_querystr_filed_from_request_url(new_url, member_settings.URL_OPENID)
				response = HttpResponseRedirect(new_url)
				response.delete_cookie(member_settings.FOLLOWED_MEMBER_TOKEN_SESSION_KEY)
				response.delete_cookie(member_settings.FOLLOWED_MEMBER_SHARED_URL_SESSION_KEY)
				response.delete_cookie(member_settings.SOCIAL_ACCOUNT_TOKEN_SESSION_KEY)
				response.delete_cookie(member_settings.OPENID_WEBAPP_ID_KEY)
				return response
		return None

from weixin.user.models import WeixinUser, get_token_for
def _process_error_openid(openid, user_profile, request=None):  #response_rule, from_weixin_user, is_from_simulator):
	member = None
	social_account = None

	if user_profile:
		webapp_id = user_profile.webapp_id
		if WeixinUser.objects.filter(username=openid).count() > 0:
			if SocialAccount.objects.filter(openid=openid, webapp_id=webapp_id).count() > 0:
				social_account = SocialAccount.objects.filter(openid=openid, webapp_id=webapp_id)[0]
				if MemberHasSocialAccount.objects.filter(account=social_account, webapp_id=webapp_id).count() == 0:
					member = member_util.create_member_by_social_account(user_profile, social_account)
			else:
				token = get_token_for(webapp_id, openid)
				social_account = member_util.create_social_account(webapp_id, openid, token, 0)
				member = member_util.create_member_by_social_account(user_profile, social_account)

		else:
			if settings.MODE == 'develop':
				is_access_openid = True
			else:
				from account.social_account.account_info import check_openid_by_api
				is_access_openid = check_openid_by_api(user_profile, openid)
			if is_access_openid:
				weixin_user = WeixinUser.objects.create(
						username =openid,
						webapp_id = webapp_id,
						nick_name = '',
						weixin_user_icon = '',
						is_subscribed = True
						)
				token = get_token_for(webapp_id, openid)
				social_account = member_util.create_social_account(webapp_id, openid, token, 0)
				member = member_util.create_member_by_social_account(user_profile, social_account)
				try:
					member_util.member_basic_info_updater(user_profile, member)
					member = Member.objects.get(id=member.id)
				except:
					notify_message = u"_process_error_openid update_member_basic_info cause:\n{}".format(unicode_full_stack())
					watchdog_error(notify_message)

				try:
					integral.increase_for_be_member_first(user_profile, member)
				except:
					notify_message = u"_process_error_openid cause:\n{}".format(unicode_full_stack())
					watchdog_error(notify_message)
				#print 1/0
				name = url_helper.get_market_tool_name_from(request.get_full_path())
				#if name:
				if not name:
					name = ''
				if request:
					MemberMarketUrl.objects.create(
						member = member,
						market_tool_name = name,
						url = request.get_full_path(),
						)
	return member, social_account

class RefuelingMiddleware(object):
	"""
	加油活动中间件
	"""
	def process_request(self, request):
		#added by duhao
		if is_product_stocks_request(request):
			return None

		#added by slzhu
		if is_pay_request(request):
			return None

		#对于支付请求，不处理
		if request.is_access_pay or request.is_access_paynotify_callback:
			return None

		# 不处理临时二维码请求 by liupeiyu
		if request.is_access_temporary_qrcode_image:
			return None

		#对于非webapp请求和非pc商城地方请求不进行处理
		if (not request.is_access_webapp) and (not request.is_access_pcmall):
			return None

		if '/weixin/js/config' in request.get_full_path():
			return None

		#设置request.uuid

		if request.member:
			if 'refueling_page' in request.get_full_path():
				url_fid = request.GET.get(member_settings.REFUELING_FID, None)
				cookie_fid = request.COOKIES.get(member_settings.REFUELING_FID, None)
				crmid = request.GET.get('crmid', None)
				if not url_fid:
					new_url = url_helper.add_query_part_to_request_url(request.get_full_path(), member_settings.REFUELING_FID, request.member.id)
					new_url = url_helper.remove_querystr_filed_from_request_url(new_url, 'crmid')
					response = HttpResponseRedirect(new_url)
					response.set_cookie(member_settings.REFUELING_FID, request.member.id, max_age=60*60*24*365)
					return response
				else:

					if url_fid != str(request.member.id):
						new_url = url_helper.remove_querystr_filed_from_request_url(request, 'crmid')
						new_url = url_helper.remove_querystr_filed_from_request_url(new_url, member_settings.REFUELING_FID)
						new_url = url_helper.add_query_part_to_request_url(new_url, member_settings.REFUELING_FID, request.member.id)
						response = HttpResponseRedirect(new_url)
						response.set_cookie(member_settings.REFUELING_FID, url_fid, max_age=60*60*24*365)
						return response
					elif crmid and crmid == str(request.member.id):
						print '==================>>>crmid:', crmid,  crmid == str(request.member.id), request.member.id
						new_url = url_helper.remove_querystr_filed_from_request_url(request, 'crmid')
						new_url = url_helper.add_query_part_to_request_url(new_url, member_settings.REFUELING_FID, request.member.id)
						response = HttpResponseRedirect(new_url)
						response.set_cookie(member_settings.REFUELING_FID, request.member.id, max_age=60*60*24*365)
						return response

			if 'mileke_page' in  request.get_full_path() and request.member.is_subscribed:
				url_fid = request.GET.get(member_settings.REFUELING_FID, None)
				cookie_fid = request.COOKIES.get(member_settings.REFUELING_FID, None)
				crmid = request.GET.get('crmid', None)
				
				
				if not url_fid:
					new_url = url_helper.add_query_part_to_request_url(request.get_full_path(), member_settings.REFUELING_FID, request.member.id)
					new_url = url_helper.remove_querystr_filed_from_request_url(new_url, 'crmid')
					response = HttpResponseRedirect(new_url)
					response.set_cookie(member_settings.REFUELING_FID, request.member.id, max_age=60*60*24*365)
					return response

		return None

def _get_hexdigest_url(shared_url):
	shared_url = remove_querystr_filed_from_request_url(shared_url, 'from')
	shared_url = remove_querystr_filed_from_request_url(shared_url, 'isappinstalled')
	shared_url = remove_querystr_filed_from_request_url(shared_url, 'code')
	shared_url = remove_querystr_filed_from_request_url(shared_url, 'state')
	shared_url = remove_querystr_filed_from_request_url(shared_url, 'appid')
	shared_url = remove_querystr_filed_from_request_url(shared_url, 'workspace_id')
	shared_url = remove_querystr_filed_from_request_url(shared_url, 'workspace_id')
	shared_url_digest = hashlib.md5(shared_url).hexdigest()
	return shared_url_digest