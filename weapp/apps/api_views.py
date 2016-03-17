# -*- coding: utf-8 -*-
from account.util import get_binding_weixin_mpuser, get_mpuser_accesstoken
from apps.customerized_apps.red_packet.models import RedPacketCertSettings

__author__ = 'liupeiyu, chuter'
import json
import os

from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import User

from models import *
from core.jsonresponse import create_response, JsonResponse
from core.exceptionutil import unicode_full_stack
from core.wxapi import get_weixin_api

from watchdog.utils import watchdog_alert, watchdog_warning

from apps_manager import manager
import termite.pagestore as pagestore_manager

@login_required
def create_installed_app(request):
	appid = request.POST.get('id')

	try:
		app = CustomizedApp.objects.get(id=appid)
	except:
		response = create_response(500)
		response.errMsg = u'获取app失败，请稍后重试'
		response.innerErrMsg = unicode_full_stack()
		return response.get_response()


	#暂时关闭gevent的异步操作，直接修改数据库状态
	#TODO 进行操作记录记录？
	# if app.status in [CustomizedappStatus.INACTIVE, CustomizedappStatus.UNINSTALLED]:
	# 	try:
	# 		manager.install_app_asyc(app)
	# 	except:
	# 		alert_msg = u"安装app:{}失败，cause:\n{}".format(
	# 				app.__unicode__(),
	# 				unicode_full_stack()
	# 			)
	# 		watchdog_alert(alert_msg, app.owner.id)
	if app.status in [CustomizedappStatus.INACTIVE, CustomizedappStatus.UNINSTALLED]:
		try:
			manager.start_app(app)
		except:
			alert_msg = u"安装(直接启动)app:{}失败，cause:\n{}".format(
					app.__unicode__(),
					unicode_full_stack()
				)
			watchdog_alert(alert_msg, app.owner.id)

	response = create_response(200)
	response.data.status = app.status
	return response.get_response()

@login_required
def create_uninstalled_app(request):
	appid = request.POST.get('id')

	try:
		app = CustomizedApp.objects.get(id=appid)
	except:
		response = create_response(500)
		response.errMsg = u'获取app失败，请稍后重试'
		response.innerErrMsg = unicode_full_stack()
		return response.get_response()

	#TODO 进行操作记录记录？
	if app.status in [CustomizedappStatus.STOPEED]:
		try:
			manager.uninstall_app_asyc(app)
		except:
			alert_msg = u"卸载app:{}失败，cause:\n{}".format(
					app.__unicode__(),
					unicode_full_stack()
				)
			watchdog_alert(alert_msg, app.owner.id)

	response = create_response(200)
	response.data.status = app.status
	return response.get_response()

@login_required
def create_stopped_app(request):
	appid = request.POST.get('id')

	try:
		app = CustomizedApp.objects.get(id=appid)
	except:
		response = create_response(500)
		response.errMsg = u'获取app失败，请稍后重试'
		response.innerErrMsg = unicode_full_stack()
		return response.get_response()

	#TODO 进行操作记录记录？
	if app.status in [CustomizedappStatus.RUNNING, CustomizedappStatus.WITHERROR]:
		try:
			manager.stop_app(app)
		except:
			alert_msg = u"停止app:{}失败，cause:\n{}".format(
					app.__unicode__(),
					unicode_full_stack()
				)
			watchdog_alert(alert_msg, app.owner.id)

	response = create_response(200)
	response.data.status = app.status
	return response.get_response()

@login_required
def create_started_app(request):
	appid = request.POST.get('id')

	try:
		app = CustomizedApp.objects.get(id=appid)
	except:
		response = create_response(500)
		response.errMsg = u'获取app失败，请稍后重试'
		response.innerErrMsg = unicode_full_stack()
		return response.get_response()

	#TODO: 进行操作记录记录？
	if CustomizedappStatus.STOPEED == app.status:
		try:
			manager.start_app(app)
		except:
			alert_msg = u"启动app:{}失败，cause:\n{}".format(
					app.__unicode__(),
					unicode_full_stack()
				)
			watchdog_alert(alert_msg, app.owner.id)

	response = create_response(200)
	response.data.status = app.status
	return response.get_response()

@login_required
def create_updated_app(request):
	appid = request.POST.get('id')

	try:
		app = CustomizedApp.objects.get(id=appid)
	except:
		response = create_response(500)
		response.errMsg = u'获取app失败，请稍后重试'
		response.innerErrMsg = unicode_full_stack()
		return response.get_response()

	#TODO 进行操作记录记录？
	if CustomizedappStatus.RUNNING == app.status:
		try:
			manager.update_app_asyc(app)
		except:
			alert_msg = u"更新app:{}失败，cause:\n{}".format(
					app.__unicode__(),
					unicode_full_stack()
				)
			watchdog_alert(alert_msg, app.owner.id)

	response = create_response(200)
	response.data.status = app.status
	return response.get_response()

@login_required
def delete_app(request):
	appid = request.POST.get('id')

	try:
		app = CustomizedApp.objects.get(id=appid)
	except:
		response = create_response(500)
		response.errMsg = u'获取app失败，请稍后重试'
		response.innerErrMsg = unicode_full_stack()
		return response.get_response()

	#TODO 进行操作记录记录？
	try:
		app.delete()
	except:
		alert_msg = u"删除app:{}失败，cause:\n{}".format(
			app.__unicode__(),
			unicode_full_stack()
		)
		watchdog_alert(alert_msg, app.owner.id)

	response = create_response(200)
	return response.get_response()

@login_required
def get_app_status(request):
	appid = request.POST.get('id')
	try:
		app = CustomizedApp.objects.get(id=appid)
	except:
		response = create_response(500)
		response.errMsg = u'获取app失败，请稍后重试'
		response.innerErrMsg = unicode_full_stack()
		return response.get_response()

	response = create_response(200)
	response.data.status = app.status
	return response.get_response()

def __app_status_list_to_json(apps):
	if apps is None or len(apps) == 0:
		return {}

	apps_status_json = {}
	for app in apps:
		apps_status_json[app.id] = app.status

	return apps_status_json

@login_required
def get_all_app_status(request):
	all_user_apps = list(CustomizedApp.objects.all())

	response = create_response(200)
	response.data.status_list = __app_status_list_to_json(all_user_apps)
	return response.get_response()

from core import apiview_util

def call_api(request):
	api_function = apiview_util.get_api_function(request, globals())
	return api_function(request)

@login_required
def select_app_status(request):
	id = request.POST.get('id')
	response = create_response(200)
	is_refresh = False
	try:
		infos = CustomizedAppInfo.objects.filter(id=id)
		if infos.count() > 0:
			customized_app = infos[0].customized_app
			if customized_app.status == CustomizedappStatus.RUNNING:
				is_refresh = True
	except:
		response = create_response(500)
		response.errMsg = u'系统繁忙，请稍后重试'
		response.innerErrMsg = unicode_full_stack()

	response.data.is_refresh = is_refresh
	return response.get_response()


@login_required
def get_dynamic_pages(request):
	pagestore = pagestore_manager.get_pagestore('mongo')

	project_id = request.GET['project_id']
	_, app_name, real_project_id = project_id.split(':')
	if real_project_id == '0':
		#新建app的project
		app_settings_module_path = 'apps.customerized_apps.%s.settings' % app_name
		app_settings_module = __import__(app_settings_module_path, {}, {}, ['*',])
		pages = [json.loads(app_settings_module.NEW_PAGE_JSON)['component']]
	else:
		pages = pagestore.get_page_components(real_project_id)
			
	response = create_response(200)
	response.data = pages
	return response.get_response()

@login_required
def get_upload_file(request):
	"""
	处理上传文件
	@param request:
	@return:
	"""
	upload_file = request.FILES.get('Filedata', None)
	owner_id = request.POST.get('owner_id', None)
	file_cat = request.POST.get('cat', None)
	response = create_response(500)
	if upload_file:
		try:
			file_path = __save_cert_file('red_packet', upload_file, owner_id)
		except:
			response.errMsg = u'保存文件出错'
			return response.get_response()
		cert_setting = RedPacketCertSettings.objects(owner_id=owner_id)
		if cert_setting.count() > 0:
			cert_setting = cert_setting.first()
			if 'cert_file' == file_cat:
				cert_setting.update(set__cert_path=file_path)
			elif 'key_file' == file_cat:
				cert_setting.update(set__key_path=file_path)
		else:
			cert_setting = RedPacketCertSettings(
				owner_id = owner_id
			)
			if 'cert_file' == file_cat:
				cert_setting.cert_path = file_path
			elif 'key_file' == file_cat:
				cert_setting.key_path = file_path
			cert_setting.save()
		response = create_response(200)
		response.data = file_path
	else:
		response.errMsg = u'文件错误'
	return response.get_response()


def __save_cert_file(res, file, owner_id):
	"""
	将上传的文件保存在每个resource的upload目录下
	@param res: 资源名
	@param file: 文件
	@param owner_id: webapp_owner_id
	@return: 文件保存路径
	"""
	content = []
	curr_dir = os.path.dirname(os.path.abspath(__file__))
	if file:
		for chunk in file.chunks():
			content.append(chunk)

	dir_path = os.path.join(curr_dir, 'customerized_apps', res, 'upload', 'owner_id'+owner_id)
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)
	file_path = os.path.join(dir_path, file.name)

	dst_file = open(file_path, 'wb')
	print >> dst_file, ''.join(content)
	dst_file.close()
	return file_path

@login_required
def get_template_message_list(request):
	"""
	获取商家的模板消息
	@param request:
	@return:
	"""
	print 'in get_template_message_list-----------------------'
	action = request.GET.get('action', None) #全量更新
	apps_type = request.GET.get('apps_type', "") #全量更新
	#首先从数据库中获取
	template_ids = [t.template_id for t in UserHasTemplateMessages.objects(owner_id=request.manager.id)]
	if action or len(template_ids) <= 0:
		#发起api请求，从微信获取
		get_templates(request.manager)
		template_ids = [t.template_id for t in UserHasTemplateMessages.objects(owner_id=request.manager.id)]

	items = TemplateMessageDetails.objects(template_id__in=template_ids)
	#获取历史数据
	um = UserappHasTemplateMessages.objects(owner_id=request.manager.id, apps_type=apps_type)
	control_data = 0
	if um.count() > 0:
		um = um.first()
		control_data = um.data_control
	templates = []
	for t in items:
		templates.append({
			"template_id": t.template_id,
			"template_title": t.title
		})

	response = create_response(200)
	response.data = {"hasData": 0 if len(templates) <= 0 else 1, "templates": templates, "control_data": control_data}
	return response.get_response()

@login_required
def save_apps_use_template(request):
	"""
	各百宝箱活动所使用的模板消息
	@param request:
	@return:
	"""
	response = create_response(500)
	try:
		fields = request.POST

		template_settings = json.loads(fields.get('template_settings', "{}"))
		apps_type = fields.get('apps_type', "")
		selected_template_ids = fields.get('template_ids','')
		UserappHasTemplateMessages.objects(owner_id=request.manager.id, apps_type=apps_type).delete()
		UserappHasTemplateMessages(owner_id=request.manager.id, apps_type=apps_type, data_control=template_settings).save()
		response = create_response(200)
	except Exception, e:
		print e
		response.errMsg =  u"配置模板出错"
	return response.get_response()

def get_templates(user):
	"""
	从微信获取商家在公众号中配置的所有模板消息
	@param owner_id:
	@return:
	"""
	mpuser_access_token = _get_mpuser_access_token(user)
	if mpuser_access_token:
		weixin_api = get_weixin_api(mpuser_access_token)
		try:
			print '22123123'
			result = weixin_api.get_all_template_messages(True)
			template_list = result['template_list']
			need_save_list = []
			user_update_list = []
			for t in template_list:
				if TemplateMessageDetails.objects(template_id=t['template_id']).count()<=0:
					need_save_list.append(TemplateMessageDetails(
						template_id = t['template_id'],
						title = t['title'],
						primary_industry = t['primary_industry'],
						deputy_industry = t['deputy_industry'],
						content = t['content']
					))
				user_update_list.append(UserHasTemplateMessages(
					owner_id = user.id,
					template_id = t['template_id']
				))
			UserHasTemplateMessages.objects(owner_id=user.id).delete()
			UserHasTemplateMessages.objects.insert(user_update_list)
			TemplateMessageDetails.objects.insert(need_save_list)
			print result,'asdfsgsf'
		except Exception, e:
			print e
			notify_message = u"获取模板列表异常, cause:\n{}".format(unicode_full_stack())
			watchdog_warning(notify_message)
	print 'get_all_template_messages api return =================='

def get_single_template_info(template_id):
	"""
	获取制定模板的详细信息
	@param t_id:
	@return:
	"""
	try:
		return TemplateMessageDetails.objects.get(template_id=template_id)
	except Exception, e:
		print e
		return None

def _get_mpuser_access_token(user):
	mp_user = get_binding_weixin_mpuser(user)
	if mp_user:
		mpuser_access_token = get_mpuser_accesstoken(mp_user)
	else:
		return False

	if mpuser_access_token is None:
		return False

	if mpuser_access_token.is_active:
		return mpuser_access_token
	else:
		return None