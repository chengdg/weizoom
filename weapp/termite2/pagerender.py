# -*- coding: utf-8 -*-
import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import subprocess
import shutil
import sys

from django.template.loader import get_template
from django.template import Context, RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
from django.template import Template
from termite.core import stripper
from watchdog.utils import watchdog_info
from webapp import views as webapp_views 
from models import *
from mall import models as mall_models
from cache import webapp_cache
from mall import module_api as mall_api
from weixin.user import module_api as weixin_api
from weixin.user.models import set_share_img
from eaglet.core import watchdog

from account.models import UserProfile

type2template = {}


#################################################################################
# __extract_component_type: 从f中抽取component type
#################################################################################
def __extract_component_type(file_path):
	#print 'extract component type from ', file_path
	component_type = None
	src_file = open(file_path, 'rb')
	should_capture_type = False
	for line in src_file:
		line = line.strip()
		if 'W.component.Component.extend' in line:
			should_capture_type = True
		if should_capture_type and line.startswith('type:'):
			beg = line.find("'")
			if beg != -1:
				end = line.find("'", beg+1)
			else:
				beg = line.find('"')
				if beg == -1:
					print '[ERROR]: no W.component.register in ', file_path
				else:
					end = line.find('"', beg+1)

			component_type = line[beg+1:end]
			#only process first type line
			break
	src_file.close()

	return component_type


#################################################################################
# __load_template: 加载component dir下的template
#################################################################################
def __load_template(component_dir, component_category):
	component_name = os.path.basename(component_dir)
	template_path = os.path.join(component_dir, '%s.html' % component_name)
	if os.path.isfile(template_path):
		template_path = template_path.split('/app/')[-1]
		if settings.DEBUG:
			#print 'load... ', template_path
			pass
		template = get_template(template_path)
	else:
		print '[WARN]: no template file - ', os.path.join(component_dir, '%s.html' % component_name)
		template = None

	for file_name in os.listdir(component_dir):
		if file_name.endswith('.js'):
			file_path = os.path.join(component_dir, file_name)
			component_type = __extract_component_type(file_path)
			if component_type:
				type = '%s.%s' % (component_category, component_type)
				type2template[type] = template
	


#################################################################################
# __load_templates: 加载components的template
#################################################################################
def __load_templates():
	type2template.clear()
	components_home_dir = settings.COMPONENTS_DIR
	print 'components_home_dir: ', components_home_dir
	for components_dir in os.listdir(components_home_dir):
		component_category = components_dir
		components_dir = os.path.join(components_home_dir, components_dir)
		if not os.path.isdir(components_dir):
			continue
		for file_name in os.listdir(components_dir):
			component_dir = os.path.join(components_dir, file_name)
			if not os.path.isdir(component_dir):
				continue
		
			__load_template(component_dir, component_category)

	type2template['unknown'] = get_template('component/common/common.html')


#################################################################################
# __get_template: 获得component对应的template
#################################################################################
def __get_template(component_category, component):
	component_type = '%s.%s' % (component_category, component['type'])
	template = type2template.get(component_type, None)
	if not template:
		template = type2template['unknown']

	#if 'common.html' in template.name:
	#	print 'use template(%s) for component(%s) [!]' % (template.name, component_type)
	#else:
	#	print 'use template(%s) for component(%s)' % (template.name, component_type)
	return template


# #===============================================================================
# # __get_datas_from_datasource : 在product mode下，从page._data中获得component需要的数据
# #===============================================================================
# def __get_datas_from_datasource(request, page, component, project):
# 	page_data = page.get('_data', None)
# 	if page_data:
# 		component_name = component['model'].get('name', None)
# 		if component_name:
# 			return page_data.get(component_name, None)
# 		else:
# 			return {}

# 	return {}


# #===============================================================================
# # __get_page_data_from_datasource : 在product mode下，调用webapp的api，获得page对应的数据
# #===============================================================================
# def __get_page_data_from_datasource(request, page, component):
# 	if component['type'].endswith('.page') and (not hasattr(page, '_data')):
# 		datasource = component['model']['datasource']
# 		if not datasource:
# 			return {}

# 		api_name = datasource['api_name']
# 		if api_name:
# 			request.t__api_name = api_name
# 			request.t__return_json = True
# 			page['_data'] = webapp_views.call_api(request)


def process_item_group_data(request, component):
	if hasattr(request, 'manager'):
		woid = request.manager.id
		user_profile = request.manager.get_profile()
	else:
		woid = request.user.id
		user_profile = request.user_profile

	if user_profile.manager_id != woid and user_profile.manager_id > 2:
		user_profile = UserProfile.objects.filter(user_id=user_profile.manager_id).first()

	#woid = request.user_profile.user_id
	if len(component['components']) == 0 and request.in_design_mode:
		#空商品，需要显示占位结果
		component['_has_data'] = True
		return

	product_ids = set()
	for sub_component in component['components']:
		sub_component['runtime_data'] = {}
		target = sub_component['model']['target']
		if target:
			try:
				data = json.loads(target)
				product_id = int(data['meta']['id'])
				product_ids.add(product_id)
				sub_component['__is_valid'] = True
				sub_component['runtime_data']['product_id'] = product_id
			except:
				#TODO: 记录watchdog
				sub_component['__is_valid'] = False
		else:
			sub_component['__is_valid'] = False

	#products = [product for product in mall_models.Product.objects.filter(id__in=product_ids) if product.shelve_type == mall_models.PRODUCT_SHELVE_TYPE_ON]
	valid_product_count = 0
	if len(product_ids) == 0:
		component['_has_data'] = False
	else:
		component['_has_data'] = True
		products = []
		category, cached_products = webapp_cache.get_webapp_products_new(user_profile, False, 0)
		try:
			if woid ==1120:
				watchdog_info({
					'msg_id':'wtf1120',
					'location':1,
					'length':len(cached_products)
				})
		except:
			from core.exceptionutil import unicode_full_stack
			watchdog_info({
				'msg_id': 'wtf1120',
				'location': 1,
				'traceback':unicode_full_stack()
			})

		for product in cached_products:
			if product.id in product_ids:
				products.append(product) 
		id2product = dict([(product.id, product) for product in products])
		
		for sub_component in component['components']:
			if not sub_component['__is_valid']:
				continue

			runtime_data = sub_component['runtime_data']
			product_id = runtime_data['product_id']
			product = id2product.get(product_id, None)
			if not product:
				sub_component['__is_valid'] = False
				continue

			valid_product_count = valid_product_count + 1
			runtime_data['product'] = {
				"id": product.id,
				"name": product.name,
				"thumbnails_url": product.thumbnails_url,
				"display_price": product.display_price,
				"is_member_product": product.is_member_product,
				"promotion_js": json.dumps(product.promotion) if product.promotion else ""
			}
	
	if valid_product_count == 0 and request.in_design_mode:
		valid_product_count = -1
	component['valid_product_count'] = valid_product_count

	try:
		if woid == 1120:
			watchdog_info({
				'msg_id': 'wtf1120',
				'location': 2,
				'component': str(component)
			})
	except:
		from core.exceptionutil import unicode_full_stack
		watchdog_info({
			'msg_id': 'wtf1120',
			'location': 2,
			'traceback': unicode_full_stack()
		})


def _set_empty_product_list(request, component):
	if request.in_design_mode:
		#分类信息为空，构造占位数据
		count = 4
		product_datas = []
		for i in range(count):
			product_datas.append({
				"id": -1,
				"name": "",
			})
		component['runtime_data'] = {
			"products": product_datas
		}
	else:
		component['_has_data'] = False

# 根据type，修改商品的显示数量
def _update_product_display_count_by_type(request, products, component):
	# 编辑模式下处理
	if not request.in_design_mode:
		return products

	component_count = int(component['model']['count'])
	component_type = int(component['model']['type'])
	default_display_count = [3, 4, 3, 3]
	if component_count == -1:
		count = default_display_count[component_type]
		count = count if len(products) > count else len(products)
		products = products[:count]

	return products

def process_item_list_data(request, component):
	if hasattr(request, 'manager'):
		woid = request.manager.id
		user_profile = request.manager.get_profile()
	else:
		woid = request.user.id
		user_profile = request.user_profile

	component['_has_data'] = True
	count = int(component['model']['count'])

	category = component["model"].get("category", '')
	if len(category) == 0:
		_set_empty_product_list(request, component)
		return
	
	category = json.loads(category)
	if len(category) == 0:
		_set_empty_product_list(request, component)
		return

	category_id = category[0]["id"]
	categories = mall_models.ProductCategory.objects.filter(id=category_id)
	if categories.count() == 0:
		#分类已被删除，直接返回
		_set_empty_product_list(request, component)
		return

	if user_profile.manager_id != woid and user_profile.manager_id > 2:
		user_profile = UserProfile.objects.filter(user_id=user_profile.manager_id).first()

	category, products = webapp_cache.get_webapp_products_new(user_profile, False, int(category_id))
	# product_ids = set([r.product_id for r in mall_models.CategoryHasProduct.objects.filter(category_id=category_id)])
	# product_ids.sort()
	# products = [product for product in mall_models.Product.objects.filter(id__in=product_ids) if product.shelve_type == mall_models.PRODUCT_SHELVE_TYPE_ON]
	
	# 当count == -1时显示全部，大于-1时，取相应的product 
	if count > -1:
		products = products[:count]

	if len(products) == 0:
		_set_empty_product_list(request, component)

	else:
		#webapp_owner_id = products[0].owner_id
		#mall_models.Product.fill_details(webapp_owner_id, products, {'with_product_model':True})
		# products = _update_product_display_count_by_type(request, products, component)
		product_datas = []
		for product in products:
			product_datas.append({
				"id": product.id,
				"name": product.name,
				"thumbnails_url": product.thumbnails_url,
				"display_price": product.display_price,
				"url": './?module=mall&model=product&action=get&rid=%d&webapp_owner_id=%d&workspace_id=mall' % (product.id, user_profile.user_id),
				"is_member_product": product.is_member_product,
				"promotion_js": json.dumps(product.promotion) if product.promotion else ""
			})

		component['runtime_data'] = {
			"products": product_datas
		}


#===============================================================================
# create_mobile_page : 创建移动页面
#===============================================================================
def __render_component(request, page, component, project):
	start_date = datetime.now()

	# 检查是否需要在server端处理component的数据
	if component.get('need_server_process_component_data', 'no') == 'yes':
		if component['type'] == 'wepage.item_group':
			process_item_group_data(request, component)
		elif component['type'] == 'wepage.item_list':
			process_item_list_data(request, component)
		elif component['type'] == 'appkit.item_group':
			process_item_group_data(request, component)
		elif component['type'] == 'appkit.item_list':
			process_item_list_data(request, component)

		if not component['_has_data']:
			return ''
	component['app_name'] = request.GET.get('app_name', '')
	# if request.in_production_mode:
	# 	#获得数据
	# 	__get_page_data_from_datasource(request, page, component)
	# 	component['datasources'] = __get_datas_from_datasource(request, page, component, project)
	# 	print component['type']
	# 	print page.get('_data')

	#获取所有sub component的html片段
	sub_components = component.get('components', [])
	component['sub_component_count'] = len(sub_components)
	sub_components.sort(lambda x,y: cmp(x['model']['index'], y['model']['index']))
	for sub_component in sub_components:
		if not sub_component.get('__is_valid', True):
			sub_component['html'] = ''
			continue

		sub_component['parent_component'] = component
		sub_component['html'] = __render_component(request, page, sub_component, project)
		#将sub_component的信息放入component中
		sub_component_type = sub_component['type'].replace('.', '')

		# 替换 链接地址
		sub_component['html'] = sub_component['html'].replace('./?', '/workbench/jqm/preview/?')
		if not sub_component_type in component:
			component[sub_component_type] = sub_component

	
	# if hasattr(request, 'shopping_cart_product_count'):
	# 	shopping_cart_product_count = request.shopping_cart_product_count
	# else:
	# 	shopping_cart_product_count = _get_shopping_cart_product_nums(request)
	
	# 二维码
	current_auth_qrcode_img = None
	if hasattr(request, "webapp_owner_info") and request.webapp_owner_info and hasattr(request.webapp_owner_info, "qrcode_img") :
		current_auth_qrcode_img = request.webapp_owner_info.qrcode_img
	else:
		current_auth_qrcode_img = weixin_api.get_mp_qrcode_img(request.webapp_owner_id)

	if current_auth_qrcode_img is None:
		current_auth_qrcode_img = '/static/img/user-1.jpg'

	#设置分享图片为默认头像
	set_share_img(request)

	#渲染component自身
	context = Context({
		'request': request,
		'page': page,
		'component': component,
		'project': project,
		'project_id': project.id,
		'in_design_mode': request.in_design_mode,
		'in_preview_mode': request.in_preview_mode,
		'in_production_mode': request.in_production_mode,
		# 'shopping_cart_product_count': shopping_cart_product_count,
		'current_auth_qrcode_img': current_auth_qrcode_img
	})
	if hasattr(request, 'extra_page_context'):
		context.update(request.extra_page_context)
	component_category = project.type
	template = __get_template(component_category, component)
	content = stripper.strip_lines(template.render(context))
	# print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
	# types = list(type2template.keys())
	# types.sort()
	# print types
	# print component_category
	# print component
	# print content
	# print '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'

	## start watchdog.info
	if component['type'] not in ['wepage.item', 'wepage.textnav', 'wepage.imagedisplay_image', 'wepage.imagegroup_image', 'wepage.image_nav']:
		end_date = datetime.now()
		url = '{}{}'.format(request.get_host(), request.get_full_path())
		timestamp = end_date - start_date
		message_info = {
			'message_service': 'WEPAGE',
			'message_type': component['type'],
			'url': url,
			'timestamp': str(timestamp),
			'user_id': request.user_profile.user_id
		}
		watchdog.info(message_info)
	## end watchdog.info
	return content


#######################################################################
# __update_category: 更新分组信息
#######################################################################
# def __update_category(component):
# 	category = component["model"].get("category")
# 	if category:
# 		category = json.loads(category)
# 		if len(category) > 0:
# 			cateoryId = category[0]["id"]
# 			categories = mall_models.ProductCategory.objects.filter(id=cateoryId)
# 			if categories.count() == 0:
# 				component = None
# 			else:
# 				category[0]["title"] = categories[0].name
# 				component["model"]["category"] = json.dumps(category)

# 	return component


#设置别名，方便别的文件调用
_render_component = __render_component


#===============================================================================
# __render_component_global_content : 渲染global content
#===============================================================================
# def __render_component_global_content(request, page, components, project):
# 	project_id = project.id
# 	component_category = project.type
# 	components.sort(lambda x,y: cmp(x['model']['index'], y['model']['index']))

# 	htmls = []
# 	for component in components:
# 		#正常渲染sub component
# 		sub_components = component.get('components', [])
# 		sub_components.sort(lambda x,y: cmp(x['model']['index'], y['model']['index']))
# 		for sub_component in sub_components:
# 			sub_component['parent_component'] = component
# 			sub_component['html'] = __render_component(request, page, sub_component, project)

# 		template = __get_template(component_category, component)
# 		old_type = component['type']
# 		component['type'] = '%s:global_content' % old_type
# 		context = RequestContext(request, {
# 			'page': page,
# 			'component': component,
# 			'project_id': project_id
# 		})

# 		content = stripper.strip_lines(template.render(context))
# 		component['type'] = old_type

# 		htmls.append(content)
# 	#print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
# 	#print component
# 	#print content
# 	#print '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
# 	return '\n'.join(htmls)


def create_mobile_page_html_content(request, page, page_component, project=None):
	if settings.DEBUG:
		__load_templates()
	else:
		if len(type2template) == 0:
			__load_templates()

	# 购物车数量
	# shopping_cart_product_count = _get_shopping_cart_product_nums(request)
	# request.shopping_cart_product_count = shopping_cart_product_count
	htmls = []
	htmls.append(__render_component(request, page, page_component, project))

	return '\n'.join(htmls)


# def _get_shopping_cart_product_nums(request):
# 	shopping_cart_product_count = 0
# 	if hasattr(request, 'member') and request.member:
# 		shopping_cart_product_count = mall_api.get_shopping_cart_product_nums(request.webapp_user)

# 	return shopping_cart_product_count

	
