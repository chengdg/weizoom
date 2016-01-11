# -*- coding: utf-8 -*-
"""@package core.debug_middleware
各种DEBUG用的中间件

"""

#import sys
import os
import cProfile
import time
import json
#from datetime import timedelta, datetime, date

#from django.contrib.auth.models import User
from django.shortcuts import render_to_response
#from django.contrib.sessions.models import Session
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.conf import settings
from django.db import connections
from django.db.models import Model

from account.social_account.models import SocialAccount
from weixin.user.models import WeixinUser
from modules.member.models import Member, WebAppUser, MemberHasSocialAccount, MemberInfo
from account.models import UserProfile
from webapp.models import Project

from core.jsonresponse import create_response

__author__ = 'chuter'


ALLSQL_JS = '''
<script type="text/javascript">
	if (!window.__W_DBG_table2sqls) {
		window.__W_DBG_table2sqls = {};
	}

	if (!window.__W_DBG_source2sqls) {
		window.__W_DBG_source2sqls = {};
	}

	var SOURCE = 0;
	var TABLE = 1;

	window.__W_DBG_tableType = SOURCE;
	window.__W_DBG_totalSqlCount = 0;

	function __W_DBG_extraceTable(sql) {
		var beg = sql.indexOf('`');
		var end = sql.indexOf('`', beg+1);
		if (beg === -1 || end === -1) {
			alert('解析sql失败: ' + sql);
			return;
		}

		return sql.substring(beg+1, end);
	}

	function __W_DBG_parseSqls(sqlsJson, source) {
		window.__W_DBG_totalSqlCount += sqlsJson.length;
		for (var i = 0; i < sqlsJson.length; ++i) {
			var sqlJson = sqlsJson[i];
			sqlJson.source = source;
			var table = __W_DBG_extraceTable(sqlJson.sql);

			var sqls = __W_DBG_table2sqls[table];
			if (!sqls) {
				__W_DBG_table2sqls[table] = [];
				sqls = __W_DBG_table2sqls[table];
			}
			sqls.push(sqlJson);
			
			var sqls = __W_DBG_source2sqls[source];
			if (!sqls) {
				__W_DBG_source2sqls[source] = [];
				sqls = __W_DBG_source2sqls[source];
			}
			sqls.push(sqlJson);
		}

		__W_DBG_refreshSqlTable();
	}

	function __W_DBG_createSqlPanel() {
		$('body').append(
			'<div id="w-dbg-sqlPanel" style="position:fixed; bottom:0px; left:0px; background-color:rgba(0, 0, 0, 0.6); height:100%%; z-index:1040; width:100%%; overflow: auto;">' +
				'<div style="text-align:right;">' +
					'<a id="w-dbg-expandBtn" class="btn btn-primary" href="javascript:void(0);" style="display: none;"><i class="icon-chevron-up icon-white"></i></a>' +
					'<a id="w-dbg-collapseBtn" class="btn btn-primary" href="javascript:void(0);"><i class="icon-chevron-down icon-white"></i></a>' +
					'<a id="w-dbg-closeBtn" class="btn btn-danger" href="javascript:void(0);"><i class="icon-remove icon-white"></i></a>' +
				'</div>' +
				'<div style="width: 90%%; margin: 0px auto; color: white;" class="clearfix">' +
					'<div style="float: left; line-height: 30px;">总数:<span id="x-dbg-totalSqlCount"></span>，&nbsp;&nbsp;排序:</div>' +
					'<div class="btn-group" data-toggle="buttons-radio" style="float: left; margin-left: 10px;">' +
						'<button id="w-dbg-sortBySource-btn" type="button" class="btn btn-warning active">来源</button>' +
						'<button id="w-dbg-sortByTable-btn" type="button" class="btn btn-warning">表</button>' +
					'</div>' +
				'</div>' +
				'<div id="w-dbg-sqlTable" style="width: 90%%; margin: 5px auto;">' + 
				'</div>' +
			'</div>'
		);
		
		$('#w-dbg-sortBySource-btn').click(function() {
			window.__W_DBG_tableType = SOURCE;
			__W_DBG_refreshSqlTable();
		});

		$('#w-dbg-sortByTable-btn').click(function() {
			window.__W_DBG_tableType = TABLE;
			__W_DBG_refreshSqlTable();
		});	
		
		$('#w-dbg-expandBtn').click(function() {
			$(this).hide();
			$('#w-dbg-collapseBtn').show();
			$('#w-dbg-sqlPanel').height('100%%');
		});

		$('#w-dbg-collapseBtn').click(function() {
			$(this).hide();
			$('#w-dbg-expandBtn').show();
			$('#w-dbg-sqlPanel').height('300px');
		});

		$('#w-dbg-closeBtn').click(function() {
			$('#w-dbg-sqlPanel').remove();
			var url = window.location.href;
			url = url.replace('d-allsql', 'd-close-allsql')
			window.location.href = url;
		})
	}

	function __W_DBG_refreshSqlTable() {
		var $table = $('#w-dbg-sqlTable');
		if ($table.length == 0) {
			return;
		}

		$('#x-dbg-totalSqlCount').text(__W_DBG_totalSqlCount);

		$table.empty();

		var items = [];
		items.push('<table class="table table-hover table-bordered table-condensed">')
		if (__W_DBG_tableType === SOURCE) {
			_.each(__W_DBG_source2sqls, function(sqls, source) {
				items.push("<tr><th style='width: 80px;'>Source</th><th>SQL</th><th style='width: 50px;'>Time</th></tr>");
				for (var i = 0; i < sqls.length; ++i) {
					var sql = sqls[i];
					items.push(
						"<tr class='info'>" +
							"<td>" +
								source +
							"</td>" +
							"<td>" +
								sql.sql.substring(0, 500) +
								"<div style='background-color: #FFF; padding: 5px; margin: 10px;'>" +
								sql.stack +
								"</div>" +
							"</td>" +
							"<td>" +
								sql.time +
							"</td>" +
						"</tr>"
					)
				}
			});
		} else {
			_.each(__W_DBG_table2sqls, function(sqls, table) {
				items.push("<tr><th>Table</th><th style='width: 60px;'>Source</th><th>SQL</th><th style='width: 50px;'>Time</th></tr>");
				for (var i = 0; i < sqls.length; ++i) {
					var sql = sqls[i];
					items.push(
						"<tr class='info'>" +
							"<td>" +
								table +
							"</td>" +
							"<td>" +
								sql.source +
							"</td>" +
							"<td>" +
								sql.sql.substring(0, 500) +
								"<div style='background-color: #FFF; padding: 5px; margin: 10px;'>" +
								sql.stack +
								"</div>" +
							"</td>" +
							"<td>" +
								sql.time +
							"</td>" +
						"</tr>"
					)
				}
			});
		}
		items.push('</table>');

		$table.html(items.join(''));
	}

	__W_DBG_createSqlPanel();
	__W_DBG_parseSqls($.parseJSON('%s'), 'page');
</script>
'''


class SqlMonitorMiddleware(object):
	"""
	监控查询中的sql执行情况
	"""
	def process_request(self, request):
		#清空上一次的cache queries
		from utils import cache_util
		cache_util.CACHE_QUERIES= []

		if not 'HTTP_USER_AGENT' in request.META:
			return None

		if 'flash' in request.META['HTTP_USER_AGENT'].lower():
			return None

		if 'd-sql' in request.GET or 'd-allsql' in request.GET:
			settings.DEBUG = True
			request.enable_sql_monitor = True
		else:
			request.enable_sql_monitor = False
		return None

	def process_response(self, request, response):
		if request.GET.get('wztest'):
			response.set_cookie('wztest', '1', max_age=3600*1000)
		if request.GET.get('un_wztest'):
			response.delete_cookie('wztest')
		if not 'HTTP_USER_AGENT' in request.META:
			return response

		if 'flash' in request.META['HTTP_USER_AGENT'].lower():
			return response

		if ('d-sql' in request.GET) or ('d-allsql' in request.GET) or hasattr(request, 'enable_json2html'):
			settings.DEBUG = True
			request.enable_sql_monitor = True
		else:
			request.enable_sql_monitor = False
			
		if not request.enable_sql_monitor:
			return response

		#a = dir(response)
		#b = response.items()
		#d = response.serialize_headers()
		#1/0

		is_sql = ('d-sql' in request.GET)
		is_close_allsql = ('d-close-allsql' in request.GET)
		is_allsql = ('d-allsql' in request.GET)
		if not is_allsql:
			is_allsql = ('w-dbg-allsql' in request.COOKIES)

		# if is_allsql:
		# 	print request.POST
		# 	for k, v in request.META.items():
		# 		print k, ' ', v
		# 	print request.META['HTTP_USER_AGENT']

		if is_close_allsql:
			if 'w-dbg-allsql' in request.COOKIES:
				response.delete_cookie('w-dbg-allsql')

			return response


		if is_sql or is_allsql:
			sqls = []
			for query in connections['default'].queries:
				if 'watchdog_message' in query['sql']:
					continue
				sqls.append({'time':query['time'], 'sql':query['sql'], 'stack':query.get('stack', 'set settings.DJANGO_HACK_PARAMS[`enable_record_sql_stacktrace`]=True to enable sql stack trace')})

			from utils import cache_util
			for query in cache_util.CACHE_QUERIES:
				sqls.insert(0, {'time':query['time'], 'sql':query['sql'], 'stack':query.get('stack', 'set settings.DJANGO_HACK_PARAMS[`enable_record_sql_stacktrace`]=True to enable sql stack trace')})

			if is_sql:
				response = create_response(200)
				response.data = {'count':len(connections['default'].queries), 'sqls':sqls}
				response = response.get_response()
			else:
				#添加cookie
				if not 'w-dbg-allsql' in request.COOKIES:
					response.set_cookie('w-dbg-allsql', '1', max_age=3600*24*1000)

				#对api调用，添加sqls
				if ('/api/' in request.path) and (not hasattr(request, 'enable_json2html')):
					data = json.loads(response.content)['data']
					response = create_response(200)
					response.data = data
					response.apiSource = request.path
					response.sqls = sqls
					response = response.get_response()
				#对普通页面，添加sqls 
				else:
					response.write(ALLSQL_JS % json.dumps(sqls).replace("'", '`'))

			if settings.MODE == 'deploy':
				settings.DEBUG = False

			return response
		else:
			return response


class ProfilerMiddleware(object):
	"""
	获得系统运行的profile信息

	@TODO 将core.profiling_middleware.ProfileMiddleware合并
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
#			self.profiler.create_stats()
#			out = StringIO()
#			old_stdout, sys.stdout = sys.stdout, out
#			self.profiler.print_stats(1)
#			sys.stdout = old_stdout
#			response.content = '<pre>%s</pre>' % out.getvalue()
			pid = str(os.getpid())
			dir = os.path.join(settings.PROFILE_DUMP_DIR, pid)
			if not os.path.exists(dir):
				os.makedirs(dir)
			url = request.path.replace('/', '_')
			file = os.path.join(dir, '%s_%f.prof' % (url, time.time()))
			self.profiler.dump_stats(file)

		return response


class DisplayImportantObjectMiddleware(object):
	"""
	显示重要对象信息的中间件
	"""
	def dump_models(self, model_class, models, name=None):
		TargetModel = model_class
		model_name = name if name else TargetModel._meta.db_table
		is_request_data = True if name else False #是否是request中的数据
		columns = [field.get_attname() for field in TargetModel._meta.fields]

		if len(models) == 0:
			return {
				'name':model_name, 
				'columns': columns, 
				'rows': [], 
				'is_request_data': is_request_data
			}

		rows = []
		for model in models:
			values = []
			for field in TargetModel._meta.fields:
				values.append(field.value_to_string(model))
			rows.append(values)

		return {
			'name':model_name, 
			'columns': columns, 
			'rows': rows, 
			'is_request_data': is_request_data
		}


	def process_view(self, request, callback, callback_args, callback_kwargs):
		if not 'wx-dump-model' in request.GET:
			return None

		if 'wx-ca' in request.GET:
			if settings.MODE == 'develop':
				MemberHasSocialAccount.objects.all().delete()
				SocialAccount.objects.all().delete()
				MemberInfo.objects.all().delete()
				Member.objects.all().delete()
				WebAppUser.objects.all().delete()
				WeixinUser.objects.all().delete()
				return HttpResponseRedirect('./?wx-dump-model=1')

		request_webapp_users = []
		if hasattr(request, 'webapp_user') and request.webapp_user:
			request_webapp_users.append(request.webapp_user)

		request_projects = []
		if hasattr(request, 'project') and request.project:
			request_projects.append(request.project)

		request_user_profiles = []
		if hasattr(request, 'user_profile') and request.user_profile:
			request_user_profiles.append(request.user_profile)

		request_members = []
		if hasattr(request, 'member') and request.member:
			request_members.append(request.member)

		c = RequestContext(request, {
			'dumped_models': [
				self.dump_models(Project, request_projects, 'request.project'),
				self.dump_models(UserProfile, request_user_profiles, 'request.user_profile'),

				self.dump_models(WebAppUser, request_webapp_users, 'request.webapp_user'),	
				self.dump_models(WebAppUser, WebAppUser.objects.all()),

				self.dump_models(SocialAccount, SocialAccount.objects.all()),
				self.dump_models(Member, request_members, 'request.member'),				
				self.dump_models(Member, Member.objects.all()),
				self.dump_models(MemberHasSocialAccount, MemberHasSocialAccount.objects.all()),
				self.dump_models(MemberInfo, MemberInfo.objects.all()),
				
				self.dump_models(WeixinUser, WeixinUser.objects.all()),
			],
			'enable_clear_accounts': (settings.MODE == 'develop'),
		})
		return render_to_response('dump_model.html', c)



class SimulateWeixinMiddleware(object):
	"""
	模拟微信的中间件
	"""

	def process_request(self, request):
		if request.COOKIES.get('wx-simulate-weixin', 'false') == 'true':
			agent = request.META.get('HTTP_USER_AGENT', '')
			request.META['HTTP_USER_AGENT'] = agent + ' simulateWeixin:MicroMessenger'

		if request.COOKIES.get('wx-simulator', 'false') == 'true':
			agent = request.META.get('HTTP_USER_AGENT', '')
			request.META['HTTP_USER_AGENT'] = agent + ' simulator'			

		return None	



class DumpContextMiddleware(object):
	"""
	输出context内容的中间件
	"""
	def process_request(self, request):
		pass

	def process_response(self, request, response):
		if not 'wx-dump-context' in request.GET:
			return response
			
		if hasattr(response, '_debug_context'):
			datas = []
			filters = set([
				'termite_dialogs', 
				'weapp_dialogs', 
				'weapp_views', 
				'weapp_models', 
				'request', 
				'False', 
				'None', 
				'True',
				'messages',
				'perms',
				'csrf_token',
			])
			for data in response._debug_context:
				buf = []
				for key, value in data.items():
					if key in filters:
						continue
					else:
						if isinstance(value, Model):
							type_value = str(type(value)).replace('<', '[').replace('>', ']')
							value = '%s<br/><br/>%s' % (type_value, value.to_dict())

						value = unicode(value).replace('<', '&lt;').replace('>', '&gt;')
						buf.append((key, value))

				if len(buf) > 0:
					buf.sort(lambda x,y: cmp(x[0], y[0]))
					datas.append(buf)

			return render_to_response('request_context.html', {
				'datas': datas,
			})

		return response



class DumpCookieMiddleware(object):
	"""
	输出cookie信息的middleware
	"""
	def process_request(self, request):
		print '>>> start REQUEST INFOS FOR %s' % request.META['PATH_INFO']
		print 'GET: ', request.GET
		print 'POST: ', request.POST
		print 'COOKIES: ', request.COOKIES 			
		print '>>> finish REQUEST INFOS'

		return None


class JsonToHtmlMiddleware(object):
	"""
	将json转化为html，主要是为了获取api调用时的SQL查询信息时使用
	"""
	def process_request(self, request):
		if ('/api/' in request.path) and ('POST' == request.method):
			request.enable_json2html = True

	def process_response(self, request, response):
		if hasattr(request, 'enable_json2html'):
			if 'application/json' in response['Content-Type']:
				#change json response to html response
				response = render_to_response('api_sqls.html', {'json_data':response.content})

		return response
