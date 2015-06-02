# -*- coding: utf-8 -*-

__author__ = 'chuter'

import os
import shutil
from svn_repository import SvnRepository

from utils import os_util

#from core.tasks.task import Task
#from core.tasks.task_executors import executors

if os_util.is_windows():
	WORD_DIR = 'c:/.weapp_work/'
else:
	WORD_DIR = '/tmp/.weapp_work/'

def __get_app_svn_repository(app):
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

def __get_app_deployed_dir(app):
	return os.path.join()

def init_workdir():
	if os.path.exists(WORD_DIR):
		shutil.rmtree(WORD_DIR, ignore_errors=True)
	else:
		os.makedirs(WORD_DIR)



"""
从定制化APP的产品库check out一份最新代码，部署
到weapp环境中：即从svn库export出代码至工作区，
然后拷贝到部署目录
"""
def deploy_app(app, deploy_target_path):
	return executors.append_task(
			Task(deploy_app_runner, app, deploy_target_path)
		)


from watchdog.utils import watchdog_warning
from core.exceptionutil import unicode_full_stack

def deploy_app_runner(app, deploy_target_path):
	work_path = os.path.join(WORD_DIR, app.name)
	if os.path.exists(work_path):
		shutil.rmtree(work_path, ignore_errors=True)

	svn_rep = __get_app_svn_repository(app)
	if svn_rep is None:
		return
	
	svn_rep.export_to(WORD_DIR)
	shutil.copytree(work_path, deploy_target_path)

"""
先删除再部署
"""
def remove_and_deploy_app(app, deploy_target_path):
	return executors.append_task(
			Task(__remove_and_deploy_app_runner, app, deploy_target_path)
		)

def __remove_and_deploy_app_runner(app, deploy_target_path):
	__remove_deploied_app_from_fs_runner(deploy_target_path)
	deploy_app_runner(app, deploy_target_path)

"""
移除已经安装的APP
该操作只删除文件系统中的相关文件
"""
def remove_deploied_app_from_fs(deploy_target_path):
	return executors.append_task(
			Task(__remove_deploied_app_from_fs_runner, deploy_target_path)
		)
	

def __remove_deploied_app_from_fs_runner(deploy_target_path):
	if deploy_target_path is not None and os.path.exists(deploy_target_path):
		shutil.rmtree(deploy_target_path, ignore_errors=True)
