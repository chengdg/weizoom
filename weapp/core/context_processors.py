# -*- coding: utf-8 -*-

import os

from django.conf import settings

from weixin.user.models import WeixinMpUser
from modules.member import member_settings
from modules.member.models import NonmemberFirstVisitRecord, Member
from modules.member.util import get_request_member, member_basic_info_updater
#from webapp.models import Workspace
from help_system.models import Document
#from weixin.user.models import get_system_user_binded_mpuser
from utils import resource_util

from account.models import OperationSettings
#from market_tools.models import MarketToolAuthority
from product import module_api as weapp_product_api

from account.url_util import is_request_for_webapp

#from weixin import cache_util as weixin_cache_util
#from cache import webapp_cache
#from cache import webapp_owner_cache
#import cache

from weixin2 import export as weixin_export

def first_navs(request):
	"""
	根据request.path_info获取对应的first navs
	"""
	result = {}
	if '/new_weixin/' in request.path_info:
		if '/unbind_account/' in request.path_info:
			result['first_navs'] = weixin_export.UNBIND_ACCOUNT_FIRST_NAVS
		else:
			result['first_navs'] = weixin_export.FIRST_NAVS

	return result

def cdn_host(request):
	return {'cdn_host': settings.CDN_HOST}

#added by chuter
def page_title(request):
	if (not is_request_for_webapp(request)) or (hasattr(request, 'user_profile') and request.user_profile is None):
		return {}

	if (hasattr(request, 'context_dict') and request.context_dict is not None) and (request.context_dict.get('page_title', None)):
		return {}

	if (not hasattr(request, 'user_profile')) or (request.user_profile is None):
		return {'page_title' : ''}

	if hasattr(request, 'webapp_owner_info') and request.webapp_owner_info and request.webapp_owner_info.mpuser_preview_info.name:
		mpuser_name = request.webapp_owner_info.mpuser_preview_info.name
		return {'page_title' : mpuser_name}
	else:
		return {'page_title' : ''}


def share_page_title(request):
	if (hasattr(request, 'is_access_webapp') and not request.is_access_webapp) and (hasattr(request, 'user_profile') and request.user_profile is None):
		return {}

	if (hasattr(request, 'context_dict') and request.context_dict is not None) and (request.context_dict.get('share_page_title', None)):
		return {}

	if hasattr(request, 'webapp_owner_info') and request.webapp_owner_info and request.webapp_owner_info.mpuser_preview_info.name:
		mpuser_name = request.webapp_owner_info.mpuser_preview_info.name
		if not str.isdigit(mpuser_name.encode('utf-8')):
			return {'share_page_title' : mpuser_name}
		else:
			return {}

	return {}


def cur_webapp_owner_operation_settings(request):
	if hasattr(request, 'operation_settings') and request.operation_settings:
		return {'operation_settings' : request.operation_settings }

	if not hasattr(request, 'user_profile') or request.user_profile is None:
		return {'operation_settings' : None}
	elif hasattr(request, 'webapp_owner_info') and hasattr(request.webapp_owner_info, 'operation_settings'):
		return {'operation_settings' : request.webapp_owner_info.operation_settings}
	else:
		settings = OperationSettings.get_settings_for_user(request.user_profile.user_id)
		return {'operation_settings' : settings}

#added by chuter
def cur_request_webapp_id(request):
	if hasattr(request, 'user_profile') and request.user_profile:
		return {'webapp_id' : request.user_profile.webapp_id}
	elif hasattr(request, 'app') and request.app:
		return {'webapp_id' : request.app.appid}
	else:
		return {'webapp_id' : ''}

def member_token(request):
	member = get_request_member(request)
	if member:
		return {member_settings.FOLLOWED_MEMBER_TOKEN_SESSION_KEY : member.token}
	else:
		return {}

def get_cur_request_member(request):
	cur_request_member = get_request_member(request)
	#add is_subscribed at 21.0
	if cur_request_member and cur_request_member.is_subscribed:
		if 'shake' in request.path_info:
			member_basic_info_updater(request.user_profile, cur_request_member)
			cur_request_member = Member.objects.get(id=cur_request_member.id)
		return {'cur_request_member': cur_request_member}
	else:
		return {'cur_request_member': None}

def get_cur_request_webapp_user(request):
	if hasattr(request, 'webapp_user'):
		return {'cur_webapp_user': request.webapp_user}
	else:
		return {'cur_webapp_user': None}

#===============================================================================
# mp_user ： 获取当前mp_user
#===============================================================================
def mp_user(request):
	try:
		mp_user = request.webapp_owner_info.mpuser
		if not mp_user:
			user = request.user
			mp_user = WeixinMpUser.objects.get(owner=user)
	except:
		mp_user = {}
	return {'mp_user': mp_user}

#===============================================================================
# system_name ： 获取显示的系统名称
#===============================================================================
def system_name(request):
	try:
		user_profile = request.user_profile
		show_system_name = user_profile.system_name
	except:
		show_system_name = u'微信营销管理系统'

	if show_system_name is None or len(show_system_name) == 0:
		show_system_name = u'微信营销管理系统'
				
	return {'system_name': show_system_name}

#===============================================================================
# debug_merged_js ： 判断当前是否处于调试合并后的all.js模式
#===============================================================================
def debug_merged_js(request):
	result = {}
	if settings.MODE == 'develop' or settings.MODE == 'test':
		result['is_use_dev_js'] = True
	else:
		result['is_use_dev_js'] = False

	if os.path.exists('./static/js/base_all.js'):
		if settings.DEBUG_MERGED_JS:
			result['debug_merged_js'] = True
		else:
			result['debug_merged_js'] = False
	else:
		result['debug_merged_js'] = False

	return result
	

#===============================================================================
# debug_merged_css ： 判断当前是否处于调试合并后的all.css模式
#===============================================================================
def debug_merged_css(request):
	if os.path.exists('./static/resources/css/content_base_all.css'):
		return {'debug_merged_css': True}
	else:
		return {'debug_merged_css': False}


#===============================================================================
# is_use_dev_resource ： 判断当前是否处于使用dev资源
#===============================================================================
def is_use_dev_resource(request):
	return {'is_use_dev_resource': settings.USE_DEV_RESOURCE}


#===============================================================================
# develop ： 判断当前是否处于develop模式
#===============================================================================
def develop_mode(request):
	if settings.MODE == 'develop':
		return {'under_develop': True}
	else:
		return {'under_develop': False}


#===============================================================================
# webapp_template ： 获得webapp模板
#===============================================================================
def webapp_template(request):
	pass
	'''
	if request.user.is_superuser:
		return {'webapp_template': 'unknown', 'webapp_editor_nav': {}}
	if request.user.is_authenticated():
		profile = request.user.get_profile()
		webapp_template_info_module = '%s.webapp_template_info' % profile.webapp_template
	
		try:
			module = __import__(webapp_template_info_module, {}, {}, ['*',])
			return {'webapp_template': profile.webapp_template, 'webapp_editor_nav': module.NAV}
		except:
			return {'webapp_template': 'unknown', 'webapp_editor_nav': {}}
	else:
		profile = request.user_profile
		if profile:
			return {'webapp_template': profile.webapp_template, 'webapp_editor_nav': {}}	
		return {'webapp_template': 'unknown', 'webapp_editor_nav': {}}
	'''


#===============================================================================
# css_name ： 获取当前使用的css文件
#===============================================================================
def css_name(request):
	pass
	'''
	css_name = None
	if request.user.is_superuser:
		return {'css_name': css_name}
	try:
		request.user.is_from_weixin
	except:
		request.user.is_from_weixin = ''
	if not request.user.is_superuser and request.user.is_from_weixin:
		profile = request.user_profile
		if profile and profile.is_customed:
			css_name ='%s_%s_customed.css' % (str(profile.user.id),profile.webapp_template)
		else:
			css_name = '%s_default.css' % profile.webapp_template
	else:
		if request.user.is_authenticated() and not request.user.is_superuser:
			user = request.user
			user_profile = user.get_profile()
			if user_profile.is_under_previewed:
				css_name = '%s_%s_preview.css' % (str(user.id),user_profile.webapp_template)
			else:
				if user_profile.is_customed:
					css_name ='%s_%s_customed.css' % (str(user.id),user_profile.webapp_template)
				else:
					css_name = '%s_default.css' % user_profile.webapp_template
		else:
			if request.user_profile:
				user_profile = request.user_profile
				if user_profile.is_customed:
						css_name ='%s_%s_customed.css' % (str(user_profile.user.id),user_profile.webapp_template)
				else:
					css_name = '%s_default.css' % user_profile.webapp_template
	return {'css_name': css_name}
	'''


#==================================================================================
#is_operator: 判断是否是运维人员
#==================================================================================d
def is_operator(request):
	if not hasattr(request, 'user') or request.user is None:
		return {'is_operator' : False}

	if request.user.is_authenticated:
		if request.user.username == 'operator':
			return {'is_operator' : True}
		else:
			return {'is_operator' : False}
	else:
		return {'is_operator' : False}


#===============================================================================
# weapp_dialogs ： 获取weapp项目的dialog集合
#===============================================================================
def weapp_dialogs_old(request):
	1/0
	dialogs_dir_path = os.path.join(settings.STATICFILES_DIRS[0], 'js/dialog')

	if not os.path.exists(dialogs_dir_path):
		return EMPTY_LIST

	dialogs = []
	for dialog_dir in os.listdir(dialogs_dir_path):
		if not os.path.isdir(os.path.join(dialogs_dir_path, dialog_dir)):
			continue

		if dialog_dir[0] == '.':
			continue
			
		template_path = os.path.join(dialogs_dir_path, dialog_dir, 'dialog.html')
		src_file = open(template_path, 'rb')
		template_source = src_file.read()
		src_file.close()

		js_name = '/static/js/dialog/%s/dialog.js' % dialog_dir
		dialogs.append({
			'template': template_source,
			'js': js_name
		})

	return {'weapp_dialogs': dialogs}


#===============================================================================
# weapp_dialogs : 获取weapp项目的dialog集合
#===============================================================================
def weapp_dialogs(request):
	items = []
	if ('/mall/' in request.path) or ('/mall_promotion/' in request.path) or ('/member/' in request.path) or ('auth' in request.path) or ('new_weixin' in request.path) or ('/card/' in request.path):
		version = '2'
	else:
		version = '1'
	for dialog in resource_util.get_web_dialogs(version):
		items.append(dialog['template_source'])
		items.append('<script type="text/javascript" src="%s"></script>' % dialog['js_url_path'])
		items.append('\n')

	return {'weapp_dialogs': '\n'.join(items)}


#===============================================================================
# weapp_views ： 获取weapp项目的view集合
#===============================================================================
def weapp_views(request):
	items = []
	print request.path
	if ('/mall/' in request.path) or ('/mall_promotion/' in request.path) or ('/member/' in request.path) or ('auth' in request.path) or ('new_weixin' in request.path) or ('/card/' in request.path):
		version = '2'
	else:
		version = '1'
	for view in resource_util.get_web_views(version):
		items.append(view['template_source'])
		items.append('<script type="text/javascript" src="%s"></script>' % view['js_url_path'])
		items.append('\n')

	return {'weapp_views': '\n'.join(items)}


#===============================================================================
# weapp_models ： 获取weapp项目的model集合
#===============================================================================
def weapp_models(request):
	items = []
	if ('/mall/' in request.path) or ('/mall_promotion/' in request.path) or ('/member/' in request.path) or ('auth' in request.path) or ('new_weixin' in request.path) or ('/card/' in request.path):
		version = '2'
	else:
		version = '1'
	for model in resource_util.get_web_models(version):
		items.append('<script type="text/javascript" src="%s"></script>' % model['js_url_path'])
		items.append('\n')

	return {'weapp_models': '\n'.join(items)}


#===============================================================================
# webapp_index_page ： 获取webapp首页链接
#===============================================================================
# def webapp_index_page(request):
# 	if request.project:
# 		for workspace in Workspace.objects.filter(owner=request.project.owner):
# 			if workspace.inner_name == 'cms':
# 				return {'webapp_index_page': './?workspace_id=%d&project_id=%d' % (workspace.id, workspace.template_project_id)}

# 	return {}


#===============================================================================
# homepage_workspace_info ： 获取cms的workspace信息
#===============================================================================
def homepage_workspace_info(request):
	if not hasattr(request, 'project') or not hasattr(request, 'user_profile'):
		return {}

	if not request.user_profile:
		return {}
		
	return {'homepage_workspace_info': 'workspace_id=%s&project_id=0' % request.user_profile.homepage_workspace_id}
		
#===============================================================================
# page_help_document ： 获取页面帮助文档
#  TODO: 加入缓存
#===============================================================================
def page_help_document(request):
	context = {'need_show_page_help_action': True}
	if '/help/' in request.path:
		context['need_show_page_help_action'] = False

	if hasattr(request, 'page_id') and request.page_id:
		if Document.objects.filter(page_id=request.page_id).count() > 0:
			context['has_page_help_document'] = True
		else:
			context['has_page_help_document'] = False

	return context


#===============================================================================
# page_features ： 获取页面的Feature信息
#  TODO: 加入缓存
#===============================================================================
def page_features(request):
	if not hasattr(request, 'user') or request.user is None:
		return {
			'need_show_feature': False,
			'features': "",
			'feature_count': 0
		}

	if request.user.is_authenticated() and request.user.is_manager:
		from help_system import module_api as help_system_api
		features = help_system_api.get_features_for_page(request.page_id)
		return {
			'need_show_feature': True,
			'features': features,
			'feature_count': len(features)
		}
	else:
		return {
			'need_show_feature': False,
			'features': "",
			'feature_count': 0
		}


#===============================================================================
# detect_member_operate_capability ：获取用户是否可操作
#===============================================================================
def detect_member_operate_capability(request):
	a = request.context_dict
	if (request.context_dict is not None) and (request.context_dict.get('hide_non_member_cover', None) is not None):
		return {}
		
	# 针对gaoge1账号，webapp_owner_id为16的账号，首页可以点击
	if hasattr(request, 'webapp_owner_id') and request.webapp_owner_id is 16:
		return {'hide_non_member_cover': True}

	if request.GET.get('module', None) == 'mall':
		return {'hide_non_member_cover': True}
	else:
		return {'hide_non_member_cover': False}


#===============================================================================
# detect_footer_visibility ：获取是否显示footer
#===============================================================================
def detect_footer_visibility(request):
	if not 'jqm/preview' in request.path:
		return {'should_hide_footer': True}

	if hasattr(request, 'member') and not request.member:
		return {'should_hide_footer': True}
	elif hasattr(request, 'should_hide_footer'):
		return {'should_hide_footer': request.should_hide_footer}
	else:
		return {'should_hide_footer': False}


#===============================================================================
# check_market_tool_authority ：检查market tool权限
#===============================================================================
# def check_market_tool_authority(request):
# 	try:
# 		authority = MarketToolAuthority.objects.get(owner=request.user)
# 		return {'is_enable_market_tool': authority.is_enable_market_tool}
# 	except:
# 		return {'is_enable_market_tool': False}


#===============================================================================
# get_market_tools：获取用户拥有权限的market_tool
#===============================================================================
# def get_market_tools(request):
# 	#weapp_product_api
# 	return {'is_enable_market_tool': True}


def get_user_product(request):
	"""
	获取用户的product
	"""
	if not hasattr(request, 'user') or request.user is None:
		return {
			'user_product': None,
			'name': u'',
		}
	else:
		#TODO: 换成user.product
		return {
		# 	'user_product': weapp_product_api.get_product_for_user(request.user),
		# 	'name': u'',
		}


#===============================================================================
# visit_histroy ：历史访问记录
#===============================================================================
from modules.member import member_settings
def visit_histroy(request):
	first_url = ''
	title = ''
	uuid = request.COOKIES.get(member_settings.NON_MEMBER_UUID_SESSION_KEY, None)
	if uuid is None:
		return {'visit_histroy_url': first_url, 'visit_histroy_url_title': title}	

	if hasattr(request, 'member') and request.member and hasattr(request,'app') and request.app :
		first_visit_record = NonmemberFirstVisitRecord.objects.filter(appid=request.app.appid, uuid=uuid)[0] if NonmemberFirstVisitRecord.objects.filter(uuid=uuid, appid=request.app.appid).count() > 0 else None
		if first_visit_record:
			first_url = first_visit_record.url
			title = first_visit_record.title
			NonmemberFirstVisitRecord.objects.filter(id=first_visit_record.id).delete()

	if hasattr(request, 'uuid') and request.uuid and hasattr(request,'app') and request.app and ((hasattr(request,'member') is None) or ((hasattr(request,'member') and (request.member is None))))  and hasattr(request, 'app') and  request.app:
		first_visit_record = NonmemberFirstVisitRecord.objects.filter(appid=request.app.appid, uuid=request.uuid)[0] if NonmemberFirstVisitRecord.objects.filter(uuid=request.uuid, appid=request.app.appid).count() > 0 else None
		if first_visit_record is None:
			NonmemberFirstVisitRecord.objects.create(
				uuid=request.uuid, 
				appid=request.app.appid, 
				url=request.get_full_path(),
				title = request.context_dict.get('page_title', '')
				)
	return {'visit_histroy_url': first_url, 'visit_histroy_url_title': title}	

def user_token(request):
	if not hasattr(request, 'user') or request.user is None:
		return {'token' : ''}

	from account import account_util
	user_token = account_util.get_token_for_logined_user(request.user)
	return {'token' : user_token}

def request_host(request):
	return {'request_host' : request.get_host()}

from mall.models import WeizoomMall
def is_weizoom_mall(request):
	if hasattr(request, 'user_profile') and request.user_profile:
		return {'is_weizoom_mall' : request.is_access_weizoom_mall}
	else:
		return {'is_weizoom_mall' : False}

