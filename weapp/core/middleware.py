# -*- coding: utf-8 -*-
"""@package core.middleware


"""

import sys
import os
import cProfile
import time
from django.conf import settings
#from datetime import timedelta, datetime, date

from django.contrib import auth
from django.contrib.auth.models import User, AnonymousUser
#from django.contrib.sessions.models import Session
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
#from django.conf import settings

#from utils.url_helper import remove_querystr_filed_from_request_url
from account.url_util import get_webappid_from_request, is_request_for_api, is_request_for_webapp, is_request_for_webapp_api, is_request_for_editor, is_pay_request, is_request_for_weixin, is_paynotify_request, is_request_for_pcmall, is_request_for_oauth, is_request_for_temporary_qrcode_image, is_request_for_cloud_housekeeper, is_product_stocks_request
from account.models import WEBAPP_TYPE_WEIZOOM_MALL

#from core import dateutil
from core.exceptionutil import unicode_full_stack
import core.request_source_detector as request_source_detector
#from core.jsonresponse import JsonResponse, create_response

from account.models import UserProfile
#from account import cache_util as account_cache_util

#from webapp.models import WebApp, PageVisitLog, Project
from webapp.models import Project
from watchdog.utils import watchdog_alert, watchdog_emergency, watchdog_error, watchdog_info
from account import url_util

#from modules.member.util import get_social_account_token
#from modules.member.visit_session_util import get_request_url
from webapp.modules.cms.models import SpecialArticle
#from market_tools.models import MarketToolAuthority
from product import module_api as weapp_product_api

from weixin.message.material.models import News

#from webapp.handlers import event_handler_util
from cache import webapp_cache
from cache import webapp_owner_cache
import cache

from auth import models as auth_models
from auth import module_api as auth_api
from cache.service_cache import set_service_time, get_service_time, get_service_urls


__author__ = 'bert'

class ServiceMiddleware(object):
	"""
	获得页面访问计时信息
	"""
	key_prefix = 'weapp_service_cache_'
	ken_prefix_len = len(key_prefix)
	def process_request(self, request):#记录请求开始时间，方便后续使用
		request.time_start = time.time()
		return None

	def process_response(self, request, response):
		request.time_spend = time.time() - request.time_start
		time_pair = '%s:%s' % (request.time_start, request.time_spend)
		set_service_time(self.gen_urlkey(request.path_info), time_pair)
		return response

	def gen_urlkey(self, url):
		return '%s%s' % (key_prefix, url)
	
	def get_latest(self, url, index_begin = 0, index_end = 100):
		url = self.gen_urlkey(url)
		return (url, [ i.split(':',1) for i in get_service_time(url) ])

	def get_allurl(self):
		urls = get_service_urls(key_prefix + '*')
		return tuple([ i[ken_prefix_len:] for i in urls ])
	
	
class LocalCacheMiddleware(object):
	"""
	管理local cache的中间件
	"""
	def process_request(self, request):
		#记录request，方便event handler使用
		cache.request = request

	def process_response(self, request, response):
		webapp_cache.local_cache = {}
		return response


# #===============================================================================
# # WebappOwnerCacheMiddleware : 管理webapp owner相关信息的中间件
# #===============================================================================
# class WebappOwnerCacheMiddleware(object):
# 	def process_request(self, request):
# 		try:
# 			request.webapp_owner_info = webapp_owner_cache.get_webapp_owner_info(request.user_profile)
# 		except:
# 			if settings.DEBUG:
# 				raise
# 			else:
# 				request.webapp_owner_info = None
# 				request.app = None

# 	def process_response(self, request, response):
# 		webapp_owner_cache.local_cache = {}
# 		return response


class ExceptionMiddleware(object):
	"""
	将XMonitorWeb系统抛出的异常记录在watchdog的表中
	"""

	def process_exception(self, request, exception):
		# print '>>>>>>> process exception <<<<<<<'
		# exception_stack_str = unicode_full_stack()

		# alert_message = u"request url:{}\nrequest params:\n{}\n cause:\n{}"\
		# 	.format(request.get_full_path(), request.REQUEST, exception_stack_str)
		# watchdog_alert(alert_message)

		# type, value, tb = sys.exc_info()
		# output = StringIO.StringIO()
		# print >> output, type, ' : ', value.message
		# traceback.print_tb(tb, None, output)
		# watchdog('exception', output.getvalue(), severity=WATCHDOG_ERROR)
		# output.close()

		if settings.DEBUG:
			from django.views import debug
			debug_response = debug.technical_500_response(request, *sys.exc_info())
			debug_html = debug_response.content

			dst_file = open('error.html', 'wb')
			print >> dst_file, debug_html
			dst_file.close()
			return None
		else:
			from account.views import show_error_page
			return show_error_page(request)


class BackupReportingMiddleware(object):
	"""
	开启该moddleware的系统将被作为 nginx 的 backup server。一旦访问该系统，意味着nginx的upstream server都已失效。
	"""
	def process_request(self, request):
		if settings.ENABLE_BACKUP_REPORT:
			watchdog_emergency('nginx fcgi cluster down!!!')
		return None

		
class RequestUserSourceDetectMiddleware(object):
	"""
	请求用户来源识别的中间件
	"""
	def process_request(self, request):
		#added by duhao
		if is_product_stocks_request(request):
			return None

		#added by slzhu
		if is_pay_request(request):
			return None
		
		request.user.is_from_simulator = request_source_detector.is_from_simulator(request)
		request.user.is_from_weixin = request_source_detector.is_from_weixin(request)
		request.user.is_from_android = request_source_detector.is_from_android(request)
		request.user.is_from_mobile = request_source_detector.is_from_mobile(request)
		request.user.is_from_iphone = request_source_detector.is_from_iphone(request)

		return None

from utils.user_agents import parse
class UserAgentMiddleware(object):
	"""
	UserAgentMiddleware : 对请求者的UserAgent信息进行处理的中间件

	@note 该中间件必须置于RequestUserSourceDetectMiddleware之后。该中间件处理对管理后台的请求的UserAgent进行处理，（对于api的调用不进行处理）。如果不是所指定的列表（Firefox, Chrome和Safari），则返回特殊页面禁止进行任何操作。
	"""
	def process_request(self, request):
		remote_addr = request.META['REMOTE_ADDR']
		if remote_addr == '127.0.0.1':
			#支持bdd测试
			return None
		
		# if not settings.MODE == 'deploy':
		# 	return None

		if is_request_for_weixin(request):
			return None

		if is_paynotify_request(request):
			return None

		if is_request_for_api(request):
			#对于API的访问不进行任何处理
			return None

		#如果是支付请求
		if is_pay_request(request):
			return None
		
		#非支付请求
		if is_request_for_webapp(request):
			#如果是对webapp的请求，不进行任何处理
			return None

		if is_request_for_cloud_housekeeper(request):
			# 如果是微众云商通，不进行任何处理
			return None

		user_agent_str = request.META.get('HTTP_USER_AGENT', '')
		if user_agent_str.find('Flash') >= 0:
			#对于Flash的请求不做任何处理
			return None

		if user_agent_str.find('ApacheBench') >= 0 and (
			remote_addr in ['1.202.255.198', '118.26.196.238'] or remote_addr.find('192.168.') == 0):
			# 对于公司内部ab命令不做任何处理
			return None

		user_agent = parse(user_agent_str)

		user_agent_browser_family = user_agent.browser.family
		if not ((user_agent_browser_family.find('Firefox') >= 0) or \
			(user_agent_browser_family.find('Chrome') >= 0) or \
			(user_agent_browser_family.find('Safari') >= 0)) and ('/mobile_app/' not in request.path):
			#如果请求的浏览器不是Firefox、Chrome和Safari
			#那么直接显示提示信息，不允许进行任何其他操作
			return render_to_response('account/browser_forbidden.html', Context({}))

		return None


class UserProfileMiddleware(object):
	"""
	获得userprofile
	"""
	def process_request(self, request):
		#added by duhao
		if is_product_stocks_request(request):
			return None

		#added by slzhu
		if is_pay_request(request):
			return None
		
		#根据module判断访问的页面类型
		module = request.GET.get('module', None)
		if not module:
			request.page_type = 'home_page'
		else:
			if 'market_tool:' in module:
				request.page_type = 'market_tool'
			elif 'apps' in module:
				request.page_type = 'apps'
			else:
				request.page_type = 'webapp'
		#支付宝在同步和异步回调属于webapp     add by bert
		if request.get_full_path().find('mall/pay_notify_result/get') != -1 or request.get_full_path().find('mall/pay_result/get') != -1:
			request.page_type = 'webapp'
	
		#处理user profile
		webapp_owner_id = -1
		request.user_profile = None
		if request.user.is_authenticated() and not request.user.is_superuser and not request.is_access_webapp and not request.is_access_webapp_api:

			if hasattr(request, 'manager'):
				request.user_profile = request.manager.get_profile()
			# else:
			# 	# request.user_profile = request.user.get_profile()
			# 	request.user_profile = request.webapp_owner_info.user_profile
				webapp_owner_id = request.user_profile.user_id
		else:
			webapp_owner_id = request.REQUEST.get('woid', -1)
			if webapp_owner_id == -1:
				webapp_owner_id = request.REQUEST.get('webapp_owner_id', -1)
			if webapp_owner_id == -1:
				#TODO: 消除project_id
				project_id = request.REQUEST.get('project_id', None)
				if project_id:
					if 'market_tool:' in project_id:
						_, market_tool, webapp_owner_id = project_id.split(':')
					elif 'apps' in project_id:
						_, app, webapp_owner_id = project_id.split(':')
					else:
						project = Project.objects.get(id=project_id)
						webapp_owner_id = project.owner_id

		if (webapp_owner_id == -1) and request.get_full_path().find('message/material/news_detail/mshow/') > -1:
			try:
				query_list = request.get_full_path().split('/')
				user = News.objects.get(id=query_list[query_list.index('mshow')+1]).material.owner
				webapp_owner_id = user.id
			except:
				pass

		if (webapp_owner_id == -1) and request.get_full_path().find('mall/pay_notify_result/get') != -1 or request.get_full_path().find('mall/pay_result/get') != -1:
			try:
				request_url_split_list = request.get_full_path().split('/')
				webapp_owner_id = int(request_url_split_list[request_url_split_list.index('get')+1])
			except:
				error_msg = u"UserProfileMiddleware: get webapp_owner_id from pay url failed. {}: cause:\n{}"\
					.format(int(request_url_split_list[request_url_split_list.index('get')+1]),unicode_full_stack())
				watchdog_info(error_msg)
				
		#记录webapp_owner_id
		request.webapp_owner_id = webapp_owner_id
		if request.webapp_owner_id:
			request.webapp_owner_id = int(request.webapp_owner_id)

		#根据webapp_owner_id获取user_profile以及webapp_owner_info
		if request.webapp_owner_id != -1:
			if request.is_access_webapp or request.is_access_pay or request.is_access_paynotify_callback:
				try:
					request.webapp_owner_info = webapp_owner_cache.get_webapp_owner_info(webapp_owner_id)
					request.mall_data = webapp_cache.get_webapp_mall_data(webapp_owner_id)
					request.webapp_owner_info.mall_data = request.mall_data
					if not request.user_profile:
						request.user_profile = request.webapp_owner_info.user_profile
				except:
					if settings.DEBUG:
						raise
					else:
						alert_message = u"获取缓存信息失败, cause:\n{}".format(unicode_full_stack())
						watchdog_alert(alert_message, type='WEB')
						request.webapp_owner_info = None
						request.mall_data = None
						request.user_profile = UserProfile.objects.get(user_id=webapp_owner_id)
			else:
				request.user_profile = UserProfile.objects.get(user_id=webapp_owner_id)
				request.webapp_owner_info = None
		else:
			print "------------log-----------------" * 10
			request.webapp_owner_info = None
			request.user_profile = None

		print "webapp_owner_id", request.webapp_owner_id
		#add by duhao 20150519
		from account.account_util import get_token_for_logined_user
		request.user_token = get_token_for_logined_user(request.user)
		assert hasattr(request, 'user_token')


		assert hasattr(request, 'webapp_owner_id')
		assert hasattr(request, 'user_profile')
		assert hasattr(request, 'webapp_owner_info')
		return None



class ForceLogoutMiddleware(object):
	"""
	ForceLogoutMiddleware : 根据同一账号用户的强制退出状态强制处于已登录状态的用户退出登录
	
	如果用户session中记录的登录的时间<最后退出时间则强制退出。

	@note 该中间件必须置于UserProfileMiddleware之后。
	"""
	def process_request(self, request):
		#added by duhao
		if is_product_stocks_request(request):
			return None

		#added by slzhu
		if is_pay_request(request):
			return None
		
		if not request.user.is_authenticated() or request.user_profile is None:
			return None

		if request.user_profile.force_logout_date > 0 and\
          ('LAST_LOGIN_DATE' not in request.session or \
          	request.session['LAST_LOGIN_DATE'] < request.user_profile.force_logout_date):
			auth.logout(request)

		return None


class RequestWebAppMiddleware(object):
	"""
	获得当前请求的WebApp
	"""
	def process_request(self, request):
		#added by duhao
		if is_product_stocks_request(request):
			return None

		#added by slzhu
		if is_pay_request(request):
			return None
		
		if request.user.is_superuser:
			request.app = None
			return None

		# app_id = get_webappid_from_request(request)
		# if app_id:
		# 	try:
		# 		from webapp import cache_util as webapp_cache_util
		# 		app = webapp_cache_util.get_webapp_by_appid(app_id) #WebApp.objects.get(appid=app_id)
		# 	except:
		# 		watchdog_error(u"根据url信息获取app失败，url:{}, appid:{}, 原因:\n{}".format(
		# 				request.get_full_path(), app_id, unicode_full_stack()))

		# if app is None:
		# 	#如果从url中没有获取到appid信息，那么尝试从登陆信息中获取
		# 	if request.user.is_authenticated():
		# 		try:
		# 			app = WebApp.objects.get(owner=request.user)
		# 		except:
		# 			watchdog_error(u"根据用户获取app失败，username:{}, appid:{}, 原因:\n{}".format(
		# 				request.user.username, app_id, unicode_full_stack()))

		if request.webapp_owner_info:
			request.app = request.webapp_owner_info.app
		else:
			request.app = None
		return None	



class ProfilerMiddleware(object):
	"""
	获得系统运行的profile信息
	"""
	def process_view(self, request, callback, callback_args, callback_kwargs):
		hobbit_setting = HobbitSetting.objects.all()[0]
		request.is_profiling_enabled = False
		if hobbit_setting and hobbit_setting.enable_profiling:
			request.is_profiling_enabled = True
			self.profiler = cProfile.Profile()
			args = (request,) + callback_args
			return self.profiler.runcall(callback, *args, **callback_kwargs)

	def process_response(self, request, response):
		if hasattr(request, 'is_profiling_enabled') and request.is_profiling_enabled:
			pid = str(os.getpid())
			dir = os.path.join(settings.PROFILE_DUMP_DIR, pid)
			if not os.path.exists(dir):
				os.makedirs(dir)
			url = request.path.replace('/', '_')
			file = os.path.join(dir, '%s_%f.prof' % (url, time.time()))
			self.profiler.dump_stats(file)

		return response


class WebAppPageVisitMiddleware(object):
	"""
	记录webapp中页面的pv, 必须在 RequestUserSourceDetectMiddleware 和 RequestWebAppMiddleware 之后。
	"""
	def process_request(self, request):
		#added by slzhu
		if is_pay_request(request):
			return None
		
		if (not request.is_access_webapp):
			#对于非webapp的请求不进行记录
			return None

		if request.is_access_webapp_api:
			#不处理对api的访问
			return None

		if request.app is None:
			return None

		
		if request.user.is_from_simulator:
			#不处理来自模拟器中的点击
			return None

		from webapp.handlers import event_handler_util
		request.event_data = event_handler_util.extract_data(request)
		event_handler_util.handle(request, 'page_visit')
		return None
		
	def process_response(self, request, response):
		if is_pay_request(request):
			return response
			
		if 'api' in request.get_full_path() or 'resource_js' in request.get_full_path():
			#不处理对api的访问
			return response
		try:
			if hasattr(request,'member') and request.member:
				page_title = ''
				if hasattr(request, 'context_dict'):
					page_title = request.context_dict.get('page_title', '')
				from modules.member.tasks import record_member_pv
				record_member_pv.delay(request.member.id, request.get_full_path(), page_title)
		except:
			pass
		
		return response


class ModuleNameMiddleware(object):
	"""
	获取module对应的中文名，用于支持pv与uv的统计
	"""
	def process_request(self, request):
		#added by slzhu
		if is_pay_request(request):
			return None
		
		request.module_name = None
		module = request.GET.get('module', None)
		if module:
			if module == 'cms':
				request.module_name = u'文章管理'
			elif module == 'mall':
				request.module_name = u'微商城'
			elif module == 'user_center':
				request.module_name = u'用户中心'
			else:
				pass

		return None


class BrowserSourceDetectMiddleware(object):
	"""
	检测处理不同浏览器来源的中间件
	"""
	def process_request(self, request):
		#added by duhao
		if is_product_stocks_request(request):
			return None

		#added by slzhu
		if is_pay_request(request):
			return None
		
		if not url_util.is_request_for_webapp(request):
			return None

		if request.user.is_from_weixin:
			return None

		if request.user.is_authenticated():
			return None

		if is_request_for_api(request):
			return None


		if settings.MODE == 'develop':
			return None
		else:
			if request.user.is_from_simulator:
				#不处理来自模拟器中的点击
				return None
			if 'webapp_page' in request.get_full_path():
				return None
			webapp_owner_id = int(request.GET.get('webapp_owner_id', '0'))
			if webapp_owner_id == 0:
				webapp_owner_id = int(request.GET.get('woid', '0'))
			if webapp_owner_id > 0:
				not_from_weixin_article = SpecialArticle.objects.get(owner_id=webapp_owner_id, name='not_from_weixin')
				c = Context({
					'qrcode_image': not_from_weixin_article.content
				})
			else:
				c = Context({
				})
			return render_to_response('webapp/qrcode.html', c)
			

class PageIdMiddleware(object):
	"""
	为Page产生唯一识别id的中间件，用于支持help system
	"""
	def process_view(self, request, callback, callback_args, callback_kwargs):
		if is_request_for_editor(request):
			page_id = '%s.%s' % (callback.__module__, callback.func_name)
			request.page_id = page_id
		else:
			request.page_id = None
			
		return None


class ManagerDetectMiddleware(object):
	"""
	检测是否是manager的中间件
	"""
	def process_request(self, request):
		#added by duhao
		if is_product_stocks_request(request):
			return None

		#added by slzhu
		if is_pay_request(request):
			return None
		
		username = request.user.username
		if username == 'manager' or username == 'product_support':
			request.user.is_manager = True
		else:
			request.user.is_manager = False

		return None


class UserManagerMiddleware(object):
	"""
	确定user的manager
	"""
	def process_request(self, request):
		user = request.user
		manager = user
		if is_pay_request(request) or request.is_access_webapp or request.is_access_webapp_api:
			return None
		if isinstance(request.user, User):
			departmentUser = auth_models.DepartmentHasUser.objects.filter(user=request.user)
			if len(departmentUser) == 1:
				manager = User.objects.get(id=departmentUser[0].owner_id)
			request.manager = manager
		return None


class DisablePostInPcBrowserUnderDeployMiddleware(object):
	"""
	DisablePostInPcBrowserUnderDeployMiddleware : 在deploy模式下禁止浏览器预览webapp时的post操作
	"""
	def process_request(self, request):
		if not settings.MODE == 'deploy':
			return None
		
		# 泰兴大厦可以用浏览器访问
		remote_addr = request.META.get('REMOTE_ADDR', '')
		if remote_addr == '111.202.10.158' or remote_addr == '1.202.255.198':
			return 

		
		#added by duhao
		if is_product_stocks_request(request):
			return None

		#added by slzhu
		if is_pay_request(request):
			return None

		if not is_request_for_webapp(request):
			return None

		if request.user.is_from_weixin:
			return None

		if request.method == 'POST':
			if is_pay_request(request):
				return None
			else:
				from core.jsonresponse import create_response
				response = create_response(600)
				response.errMsg = 'post in pc browser is not allowed under "deploy" MODE'
				return response.get_response()
		else:
			return None


class MarketToolsMiddleware(object):
	"""
	检查模块权限
	"""
	def process_request(self, request):
		#added by slzhu
		if is_pay_request(request):
			return None
		
		if self.__is_request_for_webapp_market_tools_page(request):
			request.should_hide_footer = True

		if (not request.is_access_webapp) and request.user.is_authenticated():
			request.user.market_tool_modules = weapp_product_api.get_market_tool_modules_for_user(request.user)
			request.user.has_market_tool_modules = (len(request.user.market_tool_modules) > 0)
			if not weapp_product_api.has_permission_to_access(request.user, request.path):
				#无访问权限，调回market_tools首页
				return HttpResponseRedirect('/market_tools/')

		return None

	def __is_request_for_webapp_market_tools_page(self, request):
		if request is None:
			return False

		return request.GET.get('module', '').find('market_tool') >= 0

	def __is_request_for_market_tool_editor_page(self, request):
		if request and '/market_tools/' in request.path:
			return True

		return False



from account.account_util import get_logined_user_from_token
class AuthorizedUserMiddleware(object):
	"""
	根据请求进行自动登录处理的中间件

	@author chuter
	"""
	def process_request(self, request):
		#added by slzhu
		if is_pay_request(request):
			return None
		
		token = request.REQUEST.get('token', None)
		if token is None:
			return None

		request_host = request.get_host()
		authorized_user = get_logined_user_from_token(token, request_host=request_host)
		if authorized_user is None:
			return None

		auth.login(request, authorized_user)
		if request.path_info.endswith('GET'):
			path_info = request.path_info[:request.path_info.find('GET')]
		else:
			path_info = request.path_info

		return HttpResponseRedirect(path_info)


from utils.uuid import uniqueid
import core_setting
class WeizoomCardUseAuthKeyMiddleware(object):
	"""
	增加微众卡支付时的安全key

	@author bert

	@TODO 会员重构完成后统一曾成uuid
	"""
	def process_response(self, request, response):
		weizoom_card_auth_key = request.COOKIES.get(core_setting.WEIZOOM_CARD_AUTH_KEY, None)
		if weizoom_card_auth_key is None:
			response.set_cookie(core_setting.WEIZOOM_CARD_AUTH_KEY, uniqueid(), max_age=60*60*24*365)

		return response


from mall.models import WeizoomMall
class WeizoomMallMiddleware(object):
	"""
	微众商城中间件
	"""

	def process_request(self, request):
		#added by duhao
		if is_product_stocks_request(request):
			return None

		#added by slzhu
		if is_pay_request(request):
			return None
		
		if request.user_profile:
			request.user.is_weizoom_mall = request.user_profile.webapp_type == WEBAPP_TYPE_WEIZOOM_MALL#WeizoomMall.is_weizoom_mall(request.user_profile.webapp_id)
			if hasattr(request, 'manager'):
				request.manager.is_weizoom_mall = request.user.is_weizoom_mall
			request.is_access_weizoom_mall = request.user.is_weizoom_mall
		else:
			request.user.is_weizoom_mall = False
			request.is_access_weizoom_mall = False
		return None



class GetRequestInfoMiddleware(object):
	"""
	获取request各项信息的中间件
	"""
	def process_request(self, request):
		#added by slzhu
		if is_pay_request(request):
			return None
			
		#获取访问目标
		is_access_pay_domain = ('pay.weapp.com' in request.META.get('HTTP_HOST', ''))
		request.is_access_webapp = is_request_for_webapp(request)
		request.is_access_webapp_api = is_request_for_webapp_api(request)
		request.is_access_pcmall = is_request_for_pcmall(request)
		request.is_access_pay = is_pay_request(request) or is_access_pay_domain
		request.is_access_mock_pay = is_access_pay_domain
		request.is_access_paynotify_callback = is_paynotify_request(request) or is_access_pay_domain
		request.is_access_temporary_qrcode_image = is_request_for_temporary_qrcode_image(request)

		#检查用户来源
		is_from_simulator = request_source_detector.is_from_simulator(request)
		if is_request_for_webapp or is_request_for_webapp_api or request.user.is_authenticated():
			return None
			
		if request.is_access_webapp and not is_from_simulator:
			#阻止auth从数据库获取request.user
			request._cached_user = AnonymousUser()
		return None



from account import module_api as account_module_api
class SubUserMiddleware(object):
	"""
	SubUser middleware

	"""
	def process_request(self, request):
		#added by slzhu
		if is_pay_request(request):
			return None
		
		if request.is_access_webapp:
			return None

		if  hasattr(request, 'sub_user') and request.sub_user and User.objects.filter(id=id).count() == 0: 
			auth.logout(request)
			return HttpResponseRedirect('/login/')

		try:
			id = request.session['sub_user_id']
			if id:
				try:
					request.sub_user = User.objects.get(id=request.session['sub_user_id'])
				except:
					request.sub_user = None
					auth.logout(request)
					return HttpResponseRedirect('/login/')
			else:
				request.sub_user = None
		except:
			request.sub_user = None
			
		return None


class PermissionMiddleware(object):
	"""
	填充request.user的权限数据，用于支持request.user.has_perm操作
	"""
	def process_request(self, request):
		if is_request_for_webapp(request) or is_request_for_webapp_api(request):
			return None
		if not request.user.is_authenticated():
			return None
			
		group_ids = [relation.group_id for relation in auth_models.UserHasGroup.objects.filter(user=request.user)]
		permission_ids = [relation.permission_id for relation in auth_models.GroupHasPermission.objects.filter(group_id__in=group_ids)]
		user_permission_ids = [relation.permission_id for relation in auth_models.UserHasPermission.objects.filter(user=request.user)]

		permission_ids.extend(user_permission_ids)
		permission_ids = set(permission_ids)
		auth_api.fill_parent_permissions(permission_ids)

		permission_set = set([permission.code_name for permission in auth_models.Permission.objects.filter(id__in=permission_ids)])

		request.user.permission_set = permission_set
