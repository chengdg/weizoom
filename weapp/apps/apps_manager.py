# -*- coding: utf-8 -*-

__author__ = 'chuter'

import os
import sys
import shutil
import time

from django.conf import settings
from django.shortcuts import render_to_response

from models import CustomizedApp, AppOps, CustomizedAppOpLog, CustomizedappStatus

from core.jsonresponse import create_response
from core.exceptionutil import full_stack, unicode_full_stack
from watchdog.utils import watchdog_fatal, watchdog_alert, watchdog_warning

from utils.classes_util import singleton, import_module

import app_tasks
from svn_repository import SvnRepository

from core.tasks.defer import passthru

"""
定制化APP的管理

包括的操作：
reload_app(str)    -- 重新load整个app，在整个系统不重启的基础上
                      ，保证使用最新的app代码
update(app)        -- 更新app，会自动进行判断，如果只是资源文件
                      做了更新，不会进行reload，否则需要进行reload
install_all_apps() -- 安装所有的定制化app

所有的定制化app都是一个独立的package，也可是一个django的app
定制化app有如下约定：
1. 每个app的package下必须有settings.py,对app进行一些配置，
具体配置信息参见settings.py(创建定制化app时会自动生成)
中的说明
2. 每个app中使用的资源(js、css和img等)全部放置于该app下的static目录
   引用资源路径的url地址为：
   /customerized_apps_static/${app_name}/static/${dir_name}/${filename}
   例如：
   /customerized_apps_static/app1/static/css/style.css
3. weapp系统的所有基础资源文件(js,css和img)都可以直接使用
4. weapp系统中的基础库(utils,core)和其它的api都可以直接使用
5. 不可引用其它定制化app的代码

所有的定制化app都放置于customerized_apps下
"""

class APPModule(object):
	def __init__(self, module_obj, module_name):
		self.module_obj = module_obj
		self.module_name = module_name

		self.load_all_views_module()

	@property
	def template_dir(self):
		return "{}/templates".format(self.package.replace('.', '/'))

	def load_all_views_module(self):
		app_settings = self.settings
		app_export = self.export
		for installed_view in app_settings.INSTALLED_VIEWS:
			self.__load_sub_module(installed_view)

	@property
	def settings(self):
		if hasattr(self, 'settings_module'):
			return self.settings_module
		else:
			self.settings_module = self.__load_settings_module()
			return self.settings_module
	
	@property
	def export(self):
		if hasattr(self, 'export_module'):
			return self.export_module
		else:
			self.export_module = self.__load_export_module()
			return self.export_module

	@property
	def package(self):
		return self.module_obj.__name__

	def __load_settings_module(self):
		return self.__load_sub_module('settings')

	def __load_export_module(self):
		return self.__load_sub_module('export')

	def __load_sub_module(self, module_name):
		try:
			return import_module("{}.{}".format(self.package, module_name))
		except:
			raise ImportError(u"load定制APP({})的{}失败, cause:\n{}".format(
				self.package, module_name, unicode_full_stack()))


class AppOpResult(object):
	def __init__(self, app, op, msg):
		self.app = app
		self.op = op
		self.msg = msg
		self._is_failed = False
		self._is_succeed = False

	def is_failed(self):
		return self._is_failed


class AppSucceedOpResult(AppOpResult):
	def __init__(self, app, op, msg):
		super(AppSucceedOpResult, self).__init__(app, op, msg)
		self._is_succeed = True

	@property
	def op_result(self):
		return self.msg

	def unicode(self):
		return u"app:{}, op:{}, result:{}".format(
				self.app.__str__(),
				self.op,
				self.msg
			)

	def __str__(self):
		return self.unicode().encode('utf-8')


class AppFailedOpResult(AppOpResult):
	def __init__(self, app, op, msg):
		super(AppFailedOpResult, self).__init__(app, op, msg)
		self._is_failed = True

	@property
	def cause(self):
		return self.msg

	def unicode(self):
		return "app:{}, op:{}, cause:{}".format(
				self.app.__str__(),
				self.op,
				self.msg
			)

	def __str__(self):
		return self.unicode().encode('utf-8')


#TODO 1. 考虑安全性，操作中间步骤失败后如何保证后续的操作
#TODO 2. 考虑操作便利性，例如提供“使用上一个版本”操作
#TODO 3. 允许defer的callback仍为deffer，进行结果的传递
#        可把一个任务再进行切分进行异步执行
@singleton
class AppManager(object):
	APPS_ROOT = os.path.dirname(os.path.abspath(__file__))
	CUSTOMERIZED_APPS_ROOT = os.path.join(APPS_ROOT, "customerized_apps")
	
	CUSTOMERIZED_APP_PACKAGE_PREFIX = "apps.customerized_apps"

	APPNAMES_2_MODULES = {}
	RESOURCE_ACTION_2_VIEW_FUNC = {}
	RESOURCE_ACTION_2_API_FUNC = {}

	has_installed = False

	def __init__(self):
		sys.path.insert(0, self.CUSTOMERIZED_APPS_ROOT)		
		app_tasks.init_workdir()

	def all_app_modules(self):
		return self.APPNAMES_2_MODULES.values()

	def get_app_module(self, app):
		if app is None:
			return None

		if self.APPNAMES_2_MODULES.has_key(app.name):
			return self.APPNAMES_2_MODULES[app.name]
		else:
			#如果本地有该app，且该app状态为运行中, 则直接进行load操作
			if not app.is_running:
				return None

			app_full_path = self.__get_app_full_path(app)
			if os.path.exists(app_full_path):
				return self.__load_app_module(app)
			else:
				return None

	def install_all_apps(self):
		if self.has_installed:
			return

		all_apps = CustomizedApp.all_running_apps_list()
		failed_ops = self.__install_all_apps(all_apps)
		if len(failed_ops) > 0:
			notify_msges = [failed_op.unicode() for failed_op in failed_ops]
			watchdog_alert(u'\n\n'.join(notify_msges))

		self.has_installed = True

	def stop_app(self, app):
		app.update_status(CustomizedappStatus.STOPPING)
		self.__remove_app_modules(app)
		app.update_status(CustomizedappStatus.STOPEED)

	def start_app(self, app):
		app.update_status(CustomizedappStatus.STARTING)
		self.__load_app_module(app)

	def __add_task_defer_err_callback(self, app, op, task_defer):
		def app_op_err_callback(task, result, *args, **kw):
			if result.is_failed():
				app_op_result = AppFailedOpResult(app, op, result.result)
			else:
				app_op_result = AppSucceedOpResult(app, op, result.result)

			CustomizedAppOpLog.objects.create(
					owner = app.owner,
					customized_app = app,
					op = op,
					op_result_msg = '' if result.is_failed() else result.result,
					failed_cause_stack = result.result if result.is_failed else ''
				)

			watchdog_fatal(app_op_result.unicode(), app.owner.id)

		task_defer.add_callbacks(
				passthru,
				errback=app_op_err_callback
			)

	def uninstall_app_asyc(self, app):
		def set_appstatus_to_uninstalled(task, result, *args, **kw):
			app.update_status(CustomizedappStatus.UNINSTALLED)

		self.__remove_app_modules(app)
		app_full_path = self.__get_app_full_path(app)

		remove_task_defer = app_tasks.remove_deploied_app_from_fs(app_full_path)

		remove_task_defer.add_callbacks(set_appstatus_to_uninstalled)

		self.__add_task_defer_err_callback(
				app,
				AppOps.UNINSTALL,
				remove_task_defer				
			)
		return remove_task_defer

	def install_app_asyc(self, app):
		def install_app_after_deploy(task, result, *args, **kw):
			self.__load_app_module(app)
			app.update_status(CustomizedappStatus.RUNNING)

		app_full_path = self.__get_app_full_path(app)
		install_task_defer = app_tasks.deploy_app(app, app_full_path)

		install_task_defer.add_callbacks(install_app_after_deploy)

		self.__add_task_defer_err_callback(
				app,
				AppOps.UNINSTALL,
				install_task_defer				
			)
		return install_task_defer

	def update_app_asyc(self, app):
		#先对比版本号看是否需要进行实际的更新操作
		if not self.__app_has_new_version(app):
			#如果距离上次代码没有更新，那么不进行任何操作
			warning_msg = u"app:{}没有最新版本".format(app.__unicode__())
			watchdog_warning(warning_msg, app.owner.id)
			return
		
		app.update_status(CustomizedappStatus.UPDATING)
		#否则，需要先进行uninstall操作, 然后进行部署操作
		#最后进行load操作
		self.stop_app(app)

		app_full_path = self.__get_app_full_path(app)
		update_task_defer = app_tasks.remove_and_deploy_app(app, app_full_path)

		update_task_defer.add_callbacks(
			self.__update_callback,
			callback_args=(app, self.__get_latest_release_version(app))
		)
		self.__add_task_defer_err_callback(
			app,
			AppOps.UPDATE,
			update_task_defer
		)

		return update_task_defer

	def register_view_func(self, func_module_full_name, view_func, resource, action='GET'):
		self.__register_resource_process_func(
				func_module_full_name,
				view_func,
				resource,
				action,
				self.RESOURCE_ACTION_2_VIEW_FUNC
			)

	def register_api_func(self, func_module_full_name, api_func, resource, action='GET'):
		self.__register_resource_process_func(
				func_module_full_name,
				api_func,
				resource,
				action,
				self.RESOURCE_ACTION_2_API_FUNC
			)

	def __register_resource_process_func(
			self,
			func_module_full_name,
			process_func,
			resource,
			action,
			key_2_func
			):
		if (func_module_full_name is None) or (process_func is None) \
			or (resource is None) or (action is None):
			return

		app_module_full_name = '.'.join(func_module_full_name.split('.')[:-1])
		key = self.__generate_resource_action_2_func_key(app_module_full_name, resource, action)
		if key is None:
			return

		key_2_func[key] = process_func

	def get_api_func(self, app, module_name, resource, action):
		if app is None:
			return None
		self.__load_app_module(app)
		time.sleep(1)
		try:
			app_module_full_name = self.__get_app_module_full_name(app, module_name)
		except:
			self.__load_app_module(app)
			time.sleep(1)
			app_module_full_name = self.__get_app_module_full_name(app, module_name)

		# app_module_full_name = self.__get_app_module_full_name(app, module_name)
		key = self.__generate_resource_action_2_func_key(app_module_full_name, resource, action)
		
		if key is None:
			return None
		else:
			return self.RESOURCE_ACTION_2_API_FUNC.get(
					key, 
					self.__not_registered_resource_api_process(app, resource, action)
				)

	def get_view_func(self, app, module_name, resource, action):
		if app is None:
			return None
		self.__load_app_module(app)
		time.sleep(1)
		try:
			app_module_full_name = self.__get_app_module_full_name(app, module_name)
		except:
			self.__load_app_module(app)
			time.sleep(1)
			app_module_full_name = self.__get_app_module_full_name(app, module_name)
		
		key = self.__generate_resource_action_2_func_key(app_module_full_name, resource, action)
		b = self.RESOURCE_ACTION_2_VIEW_FUNC
		if key is None:
			return None
		else:
			return self.RESOURCE_ACTION_2_VIEW_FUNC.get(
					key, 
					self.__not_registered_resource_view_process(app, resource, action)
				)

	def __get_app_module_full_name(self, app, module_name):
		app_module = self.APPNAMES_2_MODULES.get(app.name, None)
		return "{}.{}".format(app_module.package, module_name)

	def __get_app_package_name(self, app):
		return "{}.{}".format()

	def __not_registered_resource_view_process(self, app, resource, action):
		def process(*args, **kwargs):
			return render_to_response('apps/404.html', {})

		return process

	def __not_registered_resource_api_process(self, app, resource, action):
		def process(*args, **kwargs):
			return create_response(404).get_response()

		return process

	def __generate_resource_action_2_func_key(self, module_name, resource, action):
		if (module_name is None) or (resource is None) or (action is None):
			return None
		else:
			return "{}@{}_{}".format(module_name, action, resource)

	def __remove_app_modules(self, app):
		for loaded_module_name in sys.modules.keys():
			if '.{}.'.format(app.name) in loaded_module_name:
				#属于该app的module
				del sys.modules[loaded_module_name]

		
		if self.APPNAMES_2_MODULES.has_key(app.name):
			target_app_module = self.APPNAMES_2_MODULES[app.name]
			settings.TEMPLATE_DIRS.remove(target_app_module.template_dir)
			del self.APPNAMES_2_MODULES[app.name]

	def __get_latest_release_version(self, app):
		app_svn_rep = self.__get_app_svn_repository(app)
		if app_svn_rep is None:
			return -1
		else:
			return app_svn_rep.version

	def __app_has_new_version(self, app):
		return self.__get_latest_release_version(app) > app.last_version

	def __get_app_svn_repository(self, app):
		if app.appinfo.repository_path is None or \
			len(app.appinfo.repository_path.strip()) == 0 or \
			app.appinfo.repository_username is None or \
			app.appinfo.repository_passwd is None:
			return None

		return SvnRepository(
				app.appinfo.repository_path,
				app.appinfo.repository_username,
				app.appinfo.repository_passwd
			)

	def __install_app_sync(self, app):
		if not self.__has_installed_app(app):
			app_full_path = self.__get_app_full_path(app)
			app_tasks.deploy_app_runner(app, app_full_path)

		return self.__load_app_module(app)

	def __install_all_apps(self, apps_list):
		failed_ops = []
		if apps_list is None:
			return failed_ops

		for app in apps_list:
			if app is None:
				continue

			# 此过程只进行本地安装，
			try:
				#进行本地安装
				self.__install_app_sync(app)
			except:
				info = unicode_full_stack()
				print info
				failed_op = AppFailedOpResult(app, AppOps.INSTALL, info)
				failed_ops.append(failed_op)

		return failed_ops

	def __has_installed_app(self, app):
		return os.path.exists(self.__get_app_full_path(app))	

	def __get_app_full_path(self, app):
		if app is None:
			return None

		return os.path.join(self.CUSTOMERIZED_APPS_ROOT, app.name)

	def __load_app_module_callback(self, task, result, *args, **kw):
		target_app = args[0][0]
		return self.__load_app_module(target_app)

	def __update_callback(self, task, result, *args, **kw):
		target_app = args[0][0]
		latest_release_version = args[0][1]

		self.__load_app_module(target_app)
		#更新版本号
		target_app.update_version(latest_release_version)

	#
	#load营销的module，如果load失败会抛ImportError异常，
	#否则返回ToolModule实例
	#
	def __load_app_module(self, app):
		# app_root_dir, app_name = os.path.split(full_path_to_app)

		if (self.APPNAMES_2_MODULES is not None) and (self.APPNAMES_2_MODULES.has_key(app.name)):
			print '__load_app_module: 1', 
			return self.APPNAMES_2_MODULES[app.name]
		app_module_obj = import_module(".{}".format(app.name), package=self.CUSTOMERIZED_APP_PACKAGE_PREFIX)
		app_module = APPModule(app_module_obj, app.name)
		self.APPNAMES_2_MODULES[app.name] = app_module
		
		settings.TEMPLATE_DIRS.append(app_module.template_dir)

		#TODO 完成TODO3之后会移除
		app.update_status(CustomizedappStatus.RUNNING)

		return app_module

manager = AppManager()
