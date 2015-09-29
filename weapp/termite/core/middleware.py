# -*- coding: utf-8 -*-

import sys
import os
import traceback
import StringIO
import cProfile
import time
import re
import json
#from cStringIO import StringIO
from django.conf import settings
from datetime import timedelta, datetime, date

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.conf import settings
from django.db import connections

from watchdog.utils import watchdog_alert
from termite.core import dateutil
from termite.core.jsonresponse import create_response
from termite import pagestore as pagestore_manager

from workbench.models import Project, Workspace

#===============================================================================
# ExceptionMiddleware : 将XMonitorWeb系统抛出的异常记录在watchdog的表中
#===============================================================================
class ExceptionMiddleware(object):
	def process_exception(self, request, exception):
		print '>>>>>>> process exception <<<<<<<'
		type, value, tb = sys.exc_info()
		output = StringIO.StringIO()
		print >> output, type, ' : ', value.message
		traceback.print_tb(tb, None, output)
		#watchdog('exception', output.getvalue(), severity=WATCHDOG_ERROR)
		#print output.getvalue()
		output.close()
		return None


#===============================================================================
# BackupReportingMiddleware : 开启该moddleware的系统将被作为nginx的backup server
#							 一旦访问该系统，意味着nginx的upstream server都已失效
#===============================================================================
class BackupReportingMiddleware(object):
	def process_request(self, request):
		if settings.ENABLE_BACKUP_REPORT:
			watchdog_alert('nginx fcgi cluster down!!!')
		return None
		
		
#===============================================================================
# WeixinUserSessionMiddleware : 填充weixin访问session的middleware
#===============================================================================
class WeixinUserSessionMiddleware(object):
	def process_request(self, request):
		weixin_session_key = request.COOKIES.get('wxsid', None)
		if not weixin_session_key and 'sid' in request.GET:
			request.META['need_set_weixin_session'] = True
			request.weixin_session_key = None
		else:
			request.weixin_session_key = weixin_session_key

		return None

	def process_response(self, request, response):
		if 'need_set_weixin_session' in request.META:
			token = request.GET['sid']
			try:
				shop_name = WeixinUserToken.objects.get(token=token).shop
				response.set_cookie('wxsid', request.GET['sid'], max_age=3600*24*1000)
				response.set_cookie('sn', shop_name, max_age=3600*24*1000)
			except:
				pass
		else:
			pass

		return response


#===============================================================================
# PageVisitMiddleware : 记录pv
#===============================================================================
class PageVisitMiddleware(object):
	def process_request(self, request):
		path_info = request.META['PATH_INFO']
		token = request.COOKIES.get('wxsid', '')
		
		#判断是否是从手机访问
		if 'develop' == settings.MODE:
			is_from_mobile_phone = True
		else:
			is_from_mobile_phone = 'MicroMessenger' in request.META.get('HTTP_USER_AGENT', '')
		
		if is_from_mobile_phone and '/m/' in path_info:
			user_agent = request.META.get('HTTP_USER_AGENT', '')
			request.user.is_from_weixin = 'MicroMessenger' in user_agent
			request.user.is_from_android = 'Android' in user_agent
			items = path_info.split('/')
			if '/shop/' in path_info:
				shop_name = items[-2]
			else:
				shop_name = items[-3]

			PageVisitLog.objects.create(
				shop_name = shop_name, 
				weixin_user_token = token,
				url = path_info
			)
		else:
			request.user.is_from_weixin = ''

		return None


#===============================================================================
# VisitStatisticsMiddleware : 访问统计的middleware
#===============================================================================
class VisitStatisticsMiddleware(object):
	def process_request(self, request):
		recorded_visit_date = request.COOKIES.get('vd', None)
		
		#判断是否是从手机访问
		if 'develop' == settings.MODE:
			is_from_mobile_phone = True
		else:
			is_from_mobile_phone = 'MicroMessenger' in request.META.get('HTTP_USER_AGENT', '')

		if is_from_mobile_phone and not recorded_visit_date:
			request.META['need_add_visit_date'] = True

		return None

	def process_response(self, request, response):
		if 'need_add_visit_date' in request.META:
			today = dateutil.get_today()
			weixin_session_key = request.COOKIES.get('wxsid', None)
			shop_name = request.COOKIES.get('sn', None)
			if weixin_session_key and shop_name:
				try:
					visit_statistics = VisitStatistics.objects.get(token=weixin_session_key, create_date=today)
					#如果能获取今天的visit_statistics，直接设置cookie
					response.set_cookie('vd', today, max_age=24*60*60)
				except:
					VisitStatistics.objects.create(
						shop = shop_name,
						token = weixin_session_key
					)
					response.set_cookie('vd', today, max_age=24*60*60)
		else:
			pass

		return response


#===============================================================================
# ExpirationMiddleware : 判断过期
#===============================================================================
class ExpirationMiddleware(object):
	def process_request(self, request):
		if not request.user.is_anonymous():
			try:
				user_profile = request.user.get_profile()
			except:
				return None
			today = date.today()
			if user_profile.expire_date <= today:
				user_profile.is_expired = True
				user_profile.save()

			if user_profile.is_expired or user_profile.is_frozen or user_profile.is_deleted:
				request.user.is_active = False
			else:
				if not request.user.is_active:
					request.user.is_active = True
			request.user.save()

		if not request.user.is_anonymous():
			if request.user.is_active:
				return None
			else:
				session_key = request.COOKIES.get('sessionid', None)
				if session_key:
					Session.objects.filter(session_key=session_key).delete()
				return HttpResponseRedirect('/')

#===============================================================================
# UserProfile : 获得userprofile
#===============================================================================
class UserProfileMiddleware(object):
	def process_request(self, request):
		if request.user.is_authenticated():
			try:
				request.user_profile = request.user.get_profile()
			except:
				request.user_profile = ''
			
		else:
			url = request.get_full_path()
			#得到请求手机端或者直接访问模拟器请求的webapp_id,eg:url:/mall/3013/xx/x/x/ 取3013
			first_digit = re.findall(r'[a-zA-X]/(\d)',url)
			if first_digit != []:
				webapp_id_str = url[url.find(first_digit[0]):]
				webapp_id = webapp_id_str[:webapp_id_str.find('/')]
				profile = UserProfile.objects.get(shop_name=webapp_id)

				request.user_profile = profile
			else:
				request.user_profile = ''
		return None



#==================================================================================================
# ChangeUnderPreviewedMiddleware : 修改预览状态  所有显示管理模块的预览请求的url必须要使用/preview/ 
#==================================================================================================
class ChangeUnderPreviewedMiddleware(object):
		def process_request(self, request):
			if  request.user.is_from_weixin:
				pass
			else:
				url = request.get_full_path()
				if  url.find('m/')>0 or url.find('/preview/')>0 or url == '/loading/':
					pass
				else:
					if request.user.is_authenticated() and request.user_profile != '':
						user_profile = request.user_profile
						user_profile.is_under_previewed = 0
						user_profile.save()

			

#==================================================================================================
# BuilderDetectorMiddleware : 检测builder类型
#==================================================================================================
from utils.request_helper import get_request_host
class BuilderDetectorMiddleware(object):
	def process_request(self, request):
		if 'viper' in get_request_host(request):
			request.builder_type = 'viper'
		elif 'jqm' in get_request_host(request):
			request.builder_type = 'jqm'
		else:
			request.builder_type = 'unknown'


#==================================================================================================
# DesignModeDetectorMiddleware : 检测是否位于design mode下
#==================================================================================================
class DesignModeDetectorMiddleware(object):
	def process_request(self, request):
		request.in_design_mode = ('design_mode' in request.GET or 'design_mode' in request.POST)
		request.in_preview_mode = ('preview_mode' in request.GET or 'preview_mode' in request.POST)
		request.in_production_mode = not(request.in_design_mode or request.in_preview_mode)


#==================================================================================================
# ProjectMiddleware : 获得project
#==================================================================================================
class ProjectMiddleware(object):
	def process_request(self, request):
		#保留逻辑，兼容升级到只是用webapp_owner_id的机制之前的url
		project_id = None
		request.project = None
		if (('/termite2/webapp_page/' in request.path) or ('/jqm/preview/' in request.path)) and ('workspace_id' in request.GET) and (not 'project_id' in request.GET) and (not 'webapp_owner_id' in request.GET) and (not 'woid' in request.GET):
			import urllib
			workspace = Workspace.objects.get(id=request.GET['workspace_id'])
			#project_id = workspace.template_project_id
			query_strings = {'project_id': workspace.template_project_id}
			for key, value in request.GET.items():
				if 'workspace_id' == key:
					continue
				query_strings[key] = value

			return HttpResponseRedirect('./?%s' % urllib.urlencode(query_strings))
			
		if not project_id:
			project_id = request.GET.get('project_id', None)
		if not project_id:
			project_id = request.POST.get('project_id', None)

		if project_id == None:
			request.project = None
		else:
			try:
				project_id = int(project_id)
			except:
				#project_id是'market_tool:xyz'字符串
				pass

			if project_id == 0:
				#未指定project_id，使用workspace的template project
				workspace_id = request.GET.get('workspace_id', '')
				if 'market_tool' in workspace_id:
					webapp_owner_id = request.GET['webapp_owner_id']
					owner = User.objects.get(id=webapp_owner_id)
					request.project = Project.get_market_tool_project(owner, workspace_id)
				elif 'apps:' in workspace_id:
					webapp_owner_id = request.GET['webapp_owner_id']
					owner = User.objects.get(id=webapp_owner_id)
					request.project = Project.get_app_project(owner, workspace_id)
				else:
					pass
					#webapp_owner_id机制已经上线很久了
					#可以尝试注掉下面的逻辑，观察是否会出问题
					#try:
					#	workspace_id = int(workspace_id)
					#	workspace = Workspace.objects.get(id=workspace_id)
					#except:
					#	webapp_owner_id = request.GET['webapp_owner_id']
					#	workspace = Workspace.objects.get(owner_id=webapp_owner_id, inner_name=workspace_id)

					#request.webapp_owner_id_from_project_middleware = workspace.owner_id
			elif project_id:
				#处理market_tool的参数
				project_id = str(project_id)
				if 'market_tool:' in project_id:
					_, market_tool, webapp_owner_id = project_id.split(':')

					request.webapp_owner_id_from_project_middleware = webapp_owner_id
					request.market_tool_name = market_tool
					request.project = None
				elif 'apps:' in project_id:
					_, app, webapp_owner_id = project_id.split(':')

					request.webapp_owner_id_from_project_middleware = webapp_owner_id
					request.app_name = app
					request.project = None
				elif 'fake:' in project_id:
					_, project_type, webapp_owner_id, page_id, mongodb_id = project_id.split(':')

					request.webapp_owner_id_from_project_middleware = webapp_owner_id
					request.app_name = '%s:%s' % (project_type, page_id)
					project = Project()
					project.name = 'fake:%s:%s' % (project_type, page_id)
					project.type = project_type
					project.id = project_id
				elif 'new_app:' in project_id:
					#_, app_project_id = project_id.split(':')
					#request.webapp_owner_id_from_project_middleware = webapp_owner_id
					request.project = None
				else:
					# request.project = Project.objects.get(id=project_id)
					
					projects = Project.objects.filter(id=project_id)
					if projects.count() > 0:
						request.project = projects[0]
			else:
				workspace_id = request.GET.get('workspace_id', '')
				if 'market_tool' in workspace_id:
					webapp_owner_id = request.GET['webapp_owner_id']
					owner = User.objects.get(id=webapp_owner_id)
					request.project = Project.get_market_tool_project(owner, workspace_id)

		if request.project:
			#升级到只是用webapp_owner_id的机制
			request.webapp_owner_id_from_project_middleware = request.project.owner_id


#==================================================================================================
# ModifyStaticMiddleware : 修改static的middleware
#==================================================================================================
class ModifyStaticMiddleware(object):
	def process_response(self, request, response):
		if '/termite/' in request.path or '/termite2/' in request.path:
			if '/termite/workbench/viper/' in request.path:
				pass
			else:
				print 'modify static to /termite_static/'
				content = response.content.replace('/static/', '/termite_static/')
				response.content = content
		return response