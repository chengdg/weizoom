# -*- coding:utf-8 -*-

import time
from datetime import timedelta, datetime, date
import json
import sys
import re

from django import template
from django.core.cache import cache
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q
from workbench.models import *

from datetime import datetime
import pagestore as pagestore_manager
from mall import module_api as mall_api
from mall.models import Product
from webapp import design_api_views
from weixin.manage.customerized_menu.api_views import FakeRequest

register = template.Library()

RENDER_CONTEXT = {}


@register.filter(name='is_system_manager')
def is_system_manager(user):
	return user.username == 'manager'


@register.filter(name='parse_json_str')
def parse_json_str(json_str):
	if json_str:
		return json.loads(json_str)
	else:
		return None
	
@register.filter(name='get_design_page')
def get_design_page(request, project):
	if 'viper' == project.type:
		return '/workbench/viper_design_page/get/?project_id=%d&design_mode=1' % project.id
	elif 'jqm' == project.type:
		return '/workbench/jqm_design_page/get/?project_id=%d&design_mode=1' % project.id
	elif 'weapp' == project.type:
		return '/workbench/jqm_design_page/get/?project_id=%d&design_mode=1' % project.id
	elif 'wepage' == project.type:
		return '/termite2/webapp_design_page/?project_id=%d&design_mode=1' % project.id


@register.filter(name='get_workbench_actions')
def get_workbench_actions(request, project):
	if 'viper' == project.type:
		return ['refresh', 'preview']
	elif 'jqm' == project.type:
		return ['refresh', 'preview']
	elif 'weapp' == project.type:
		return ['refresh', 'preview', 'screenshot']
		

@register.filter(name='format_target')
def format_target(value, project_id=None):
	if not value:
		return value

	if value == '#':
		return value

	if '{' in value:
		# json字符串
		value_json = json.loads(value)
		return value_json['data']

	if project_id:
		target_page_id = value.split('-')[1]
		target_page = RENDER_CONTEXT['id2page'][target_page_id]
		if target_page['component']['model']['type'] == 'dialog_page':
			return './?is_dialog=1&project_id=%s&page_id=%s' % (project_id, value.split('-')[1])
		else:
			return './?project_id=%s&page_id=%s' % (project_id, value.split('-')[1])
	else:
		return value


@register.filter(name='get_target_resource')
def get_target_resource(value, request):
	if not value:
		return ''

	if value.startswith('page-'):
		page_id = value.split('-')[1]
	else:
		page_id = value

	if hasattr(request, 'id2page'):
		target_page = request.id2page[page_id]
		if target_page['component']['model']['type'] == 'dialog_page':
			return {
				"is_dialog": True,
				"dialog": "W.dialog.app.%s.%s" % (target_page['component']['model']['title'], target_page['component']['model']['name']),
				"resource": target_page['component']['model']['title'],
				"className": target_page['component']['model']['className']
			}
		else:
			return {
				"is_dialog": False,
				"resource": target_page['component']['model']['title'],
				"className": target_page['component']['model']['className']
			}
	else:
		return page_id


@register.filter(name='get_object_id')
def get_object_id(record):
	return str(record['_id'])


@register.filter(name='add_link_target')
def add_link_target(url, target):
	if target:
		return '%s&page_id=%s' % (url, target.split('-')[1])
	else:
		return url


@register.filter(name='append_production_parameter')
def append_production_parameter(url, datasource):
	return url
	'''
	parameter = 'datasource_page_id=%s&datasource_record_id=%s' % (datasource['datasource_page_id'], datasource['datasource_record_id'])
	if '?' in url:
		url += ('&%s' % parameter)
	else:
		url += ('?%s' % parameter)

	return url
	'''


@register.filter(name='get_grid_type')
def get_grid_type(columns):
	columns = int(columns)
	if 2 == columns:
		return 'ui-grid-a'
	elif 3 == columns:
		return 'ui-grid-b'
	elif 4 == columns:
		return 'ui-grid-c'
	elif 5 == columns:
		return 'ui-grid-d'


@register.filter(name='get_grid_block_type')
def get_grid_block_type(index, columns):
	columns = int(columns)
	type = index % columns
	if 0 == type:
		return 'ui-block-a'
	elif 1 == type:
		return 'ui-block-b'
	elif 2 == type:
		return 'ui-block-c'
	elif 3 == type:
		return 'ui-block-d'
	elif 4 == type:
		return 'ui-block-e'


hidden_cid = 0;
@register.filter(name='next_hidden_cid')
def next_hidden_cid(ignore):
	global hidden_cid
	hidden_cid -= 1
	return hidden_cid


@register.filter(name='join_sub_components_html')
def join_sub_components_html(component):
	return '\n'.join([c['html'] for c in component.get('components', [])])


@register.filter(name='item_count')
def item_count(collection):
	return len(collection)


@register.filter(name='px2int')
def px2int(px_str):
	if px_str.endswith('px'):
		return px_str[:-2].strip()
	else:
		return px_str.strip()


@register.filter(name='to_swipe_images_json')
def to_swipe_images_json(component, request=None):
	items = []
	for sub_component in component['components']:
		model = sub_component['model']
		url = model['image']
		link_url = extract_target_data(model['target'], request)
		title = model['title']
		items.append({'url':url, 'link_url':link_url, 'title':title})

	return json.dumps(items)

RICHTEXT2COUNT = {}
@register.filter(name='get_images_max_ratio')
def get_images_max_ratio(component):
	current_ratio = 0
	current_width = 0
	current_height = 0
	print str(len(component['components'])) +'-----'
	for sub_component in component['components']:
		size = sub_component['model']['size']
		if size == 'null':
			continue
		width, height = size.split(':')
		if int(width) == 0:
			continue
		ratio = int(height)/int(width)+0.0
		if ratio > current_ratio:
			current_ratio = ratio
			current_width = width
			current_height = height

	return {"width":width, "height":height}


@register.filter(name='get_component_name')
def get_component_name(component):
	try:
		name = ''
		if component['model']['name']:
			name = component['model']['name']
		else:
			name = 'component_%d' % component['cid']
		# if component['type'] == 'viper.richtext_editor':
		# 	print '.....................richtext editor'
		# 	if name in RICHTEXT2COUNT:
		# 		count = RICHTEXT2COUNT[name]
		# 	else:
		# 		count = 1
		# 	name = '%s%d' % (name, count)
		# 	print name
		# 	RICHTEXT2COUNT[name] = count+1

		return name
	except:
		return 'component_%d' % component['cid']


@register.filter(name='get_record_value')
def get_record_value(record, property):
	if settings.IS_UNDER_CODE_GENERATION:
		return '{{ record.%s }}' % property
	else:
		if record:
			return record['model'].get(property, '')
		else:
			return ''


@register.filter(name="get_plugin_datas")
def get_plugin_datas(page):
	record = page.get('record', None)
	if not record:
		return []
	else:
		plugin_datas = []
		model = record['model']
		for key, datas in model.items():
			if key.startswith('plugin:'):
				for data_name, data_value in datas.items():
					data_name = '%s/%s' % (key, data_name)
					plugin_datas.append({
						'name': data_name,
						'value': data_value
					})
		return plugin_datas


@register.filter(name='get_record_values')
def get_record_values(record, property):
	prefix = '%s/' % property
	items = []
	for key, value in record['model'].items():
		if key.startswith(prefix):
			item = {
				'name': key,
				'record_id': record['id'],
				'text': value
			}
			items.append(item)

	return items


@register.filter(name='get_record_list_value')
def get_record_list_value(record, property):
	if record:
		return record.model.get(property, [])
	else:
		return []


@register.filter(name='should_select_option')
def should_select_option(record, option_component):
	select_name = get_component_name(option_component['parent_component'])
	select_value = get_record_value(record, select_name)
	#select component存储的数据为
	#json:{"type":"select","text":"刮刮卡","value":"guaguaka"}这样的格式
	#需要解析出其中的value
	if 'json:' in select_value:
		select_value = json.loads(select_value.split('json:')[1])['value']
	return (option_component['model']['value'] == select_value)


@register.filter(name='get_related_checkbox_items')
def get_related_checkbox_items(component, request):
	pagestore = pagestore_manager.get_pagestore(request)
	page_id = component['model']['datasource_page'].split('-')[1]
	field_name = component['model']['datasource_field']

	items = []
	for record in pagestore.get_records(request.user.id, request.project.id, page_id):
		record_model = record['model']
		model = {}
		model['name'] = '%s/%s_%s' % (component['model']['name'], page_id, record['id'])
		model['text'] = record_model[field_name]
		item = {'model':model, 'parent_component':component}
		items.append(item)
	return items


@register.filter(name='is_box_checked')
def is_box_checked(record, checkbox_component):
	checkbox_name = get_component_name(checkbox_component)
	value = get_record_value(record, checkbox_name)
	if value:
		return True
	else:
		return False


@register.filter(name='get_related_radio_items')
def get_related_radio_items(component, request):
	pagestore = pagestore_manager.get_pagestore(request)
	page_id = component['model']['datasource_page'].split('-')[1]
	field_name = component['model']['datasource_field']

	items = []
	for record in pagestore.get_records(request.user.id, request.project.id, page_id):
		record_model = record['model']
		model = {}
		model['name'] = component['model']['name']
		model['text'] = record_model[field_name]
		model['value'] = model['text']
		item = {'model':model, 'parent_component':component}
		items.append(item)
	return items
	

@register.filter(name='is_radio_checked')
def is_radio_checked(record, radio_component):
	if not record:
		return radio_component['model'].get('is_checked', 'no') == 'yes'
	else:
		radio_group_name = get_component_name(radio_component['parent_component'])
		value = get_record_value(record, radio_group_name)
		#radio component存储的数据为
		#json:{"type":"radio","text":"刮刮卡","value":"guaguaka"}这样的格式
		#需要解析出其中的value
		if 'json:' in value:
			value = json.loads(value.split('json:')[1])['value']
		if not value:
			return radio_component['model'].get('is_checked', 'no') == 'yes'
		else:
			if value == radio_component['model']['value']:
				return True
			else:
				return False


@register.filter(name='format_input_in_radio_text')
def format_input_in_radio_text(text, component):
	if '${' in text:
		items = re.split(r'(\$\{[^\}]+\})', text)
		for i in range(len(items)):
			item = items[i]
			if len(item) > 2 and item[0] == '$' and item[1] == '{':
				item = item[2:-1]
				sub_items = item.split(':')
				if len(sub_items) == 1:
					input_name = sub_items[0]
					new_item = u'<input name="{}" type="text" class="xui-numberInput xui-inner-input" />'.format(input_name)
				else:
					input_name = sub_items[0]
					input_validation = sub_items[1]
					new_item = u'<input name="{}" type="text" data-validate="{}" class="xui-numberInput xui-inner-input" />'.format(input_name, input_validation)

				items[i] = new_item
			else:
				pass
	
		return ''.join(items)
	else:
		return text


@register.filter(name='format_input_from_text')
def format_input_from_text(text, component):
	items = re.split(r'(\$\{[^\}]+\})', text)
	for i in range(len(items)):
		item = items[i]
		if len(item) > 2 and item[0] == '$' and item[1] == '{':
			item = item[2:-1]
			sub_items = item.split(':')
			if len(sub_items) == 1:
				input_name = sub_items[0]
				new_item = u'<input name="{}" type="text" />'.format(input_name)
			else:
				input_name = sub_items[0]
				input_validation = sub_items[1]
				new_item = u'<input name="{}" type="text" data-validate="{}" />'.format(input_name, input_validation)

			items[i] = new_item
		else:
			pass
	
	return ''.join(items)


@register.filter(name='render_html1')
def render_html1(html, context):
	if '{{' in html or '{%' in html:
		tmpl = template.Template(html)
		return tmpl.render(template.Context(context))
	else:
		if context:
			return context['html']
		else:
			return html

@register.filter(name='render_html')
def render_html(component, request):
	print '>>>>>>>>>>>>>>>>>>>>>'
	print request.in_design_mode
	html = component['model']['html']
	data = component.get('datasources', {})
	
	if '{{' in html or '{%' in html:
		context = {
			'in_design_mode': request.in_design_mode,
		}
		context.update(data)
		print '<<<<<<<<<<<<<'
		print context
		tmpl = template.Template(html)
		return tmpl.render(template.Context(context))
	else:
		# if (component['model']['is_content_from_data'] == 'yes') and ('html' in data):
		# 	return data['html']
		# else:
		# 	return html
		return html


@register.filter(name='contains_django_template')
def contains_django_template(html):
	if '{%' in html:
		return True
	if '{{' in html:
		return True
	return False

def __get_static_nav(request, nav_name):
	if nav_name == 'user_center':
		url = '/workbench/jqm/preview/?module=user_center&model=user_info&action=get&workspace_id=user_center&webapp_owner_id=%(webapp_owner_id)d&project_id=0'
	elif nav_name == 'shopping_cart':
		url = '/workbench/jqm/preview/?module=mall&model=shopping_cart&action=show&workspace_id=mall&project_id=0&webapp_owner_id=%(webapp_owner_id)d'
	elif nav_name == 'order_list':
		url = '/workbench/jqm/preview/?module=mall&model=order_list&action=get&workspace_id=mall&project_id=0&webapp_owner_id=%(webapp_owner_id)d&type=0'
	elif nav_name == 'product_list':
		url = '/workbench/jqm/preview/?module=mall&model=products&action=list&workspace_id=mall&project_id=0&webapp_owner_id=%(webapp_owner_id)d'
	elif nav_name == 'article_list':
		url = '/workbench/jqm/preview/?module=cms&model=category&action=get&workspace_id=cms&project_id=0&webapp_owner_id=%(webapp_owner_id)d'
	elif nav_name == 'homepage':
		webapp_owner_id = request.webapp_owner_id
		if request.webapp_owner_id:
			workspace = Workspace.objects.get(owner_id=webapp_owner_id, inner_name='home_page')
			project = Project.objects.get(owner_id=webapp_owner_id, workspace=workspace, inner_name=workspace.template_name)
			url = '/workbench/jqm/preview/?project_id=%d' % project.id
		else:
			url = '/workbench/jqm/preview/?project_id=0'

	context = {
		'webapp_owner_id': request.webapp_owner_id
	}
	return url % context


@register.filter(name='extract_target_data')
def extract_target_data(target, request=None):
	if '{' in target:
		target_json = json.loads(target)
		data = target_json['data']
		if data.startswith('static_nav:'):
			nav_name = data.split(':')[1]
			return __get_static_nav(request, nav_name)
		else:
			return data
	elif len(target) == 0:
		return 'javascript:W.alertEditTemplateLinkTarget();'
	else:
		return target


@register.filter(name='target_child_links')
def target_child_links(target, count=5, default_name=''):
	links = []
	index = 0
	if '{' in target:
		target_json = json.loads(target)
		target_id = target_json['meta']['id']
		default_name = target_json['data_path']
		request = FakeRequest(None, None)
		request.response_ajax = False
		request.GET = {
			"id": target_id,
			"count": count
		}
		if target_json['meta']['type'] == 'product_category':
			links = design_api_views.get_products_by_category_id(request)
		elif target_json['meta']['type'] == 'article_category':
			links = design_api_views.get_articles_by_category_id(request)
	while len(links) < count:
		index = index + 1
		links.append({
			"name": default_name,
		})
	return links

@register.filter(name='category_child_links')
def category_child_links(category, count=5, default_name=''):
	links = []
	index = 0
	if '{' in category:
		target_json = json.loads(category)
		category_id = target_json[0]['id']
		request = FakeRequest(None, None)
		request.response_ajax = False
		request.GET = {
			"id": category_id,
			"count": count
		}
		links = design_api_views.get_products_by_category_id(request)

	while len(category) == 0 and len(links) < count:
		index = index + 1
		links.append({
			"name": default_name,
		})

	return links

@register.filter(name='default')
def default(value, default):
	return value if value else default


@register.filter(name='find_index_in_parent')
def find_index_in_parent(component):
	index = 1
	for sub_component in component['parent_component']['components']:
		if id(sub_component) == id(component):
			sub_component['index'] = index
			return index
		index += 1


@register.filter(name='get_specific_products_by_ids')
def get_specific_products_by_ids(component):
	ids = []
	for sub_component in component['components']:
		target = sub_component['model']['target']
		if not target:
			continue
		data = json.loads(target)
		product_id = data['meta']['id']
		sub_component['product_id'] = product_id
		ids.append(product_id)
	
	id2product = dict([(p.id, p) for p in mall_api.get_products_by_ids(ids)])
	return id2product
	

@register.filter(name='get_component_product')
def get_component_product(component, owner_id):
	target = component['model']['target']
	if not target:
		product_id = None
		product = Product()
		product.name = u'第%d个商品' % component['index']
	else:
		data = json.loads(target)
		product_id = data['meta']['id']
		component['product_id'] = product_id

	# product = mall_api.get_product_by_id(product_id)
	
		product = mall_api.get_product_detail(owner_id, product_id)
		Product.fill_display_price([product])

	return product


@register.filter(name='load_weapp_ui_role_views')
def load_weapp_ui_role_views(ingore):
	from utils import resource_util as weapp_resource_util
	views = weapp_resource_util.get_web_views()

	contents = []
	for view in views:
		contents.append(view['template_source'])

		src_file = open(view['js_file_path'], 'rb')
		contents.append('<script type="text/javascript">')
		contents.append(src_file.read())
		contents.append('</script>')
		src_file.close()

	return '\n'.join(contents)


@register.filter(name='get_table_columns')
def get_table_columns(table_component):
	items = []
	for sub_component in table_component['components']:
		items.append(sub_component['model']['field_target'])

	return ','.join(items)


@register.filter(name='dict2items')
def dict2items(dict_obj):
	return dict_obj.items()
	

@register.filter(name='format_user_input_controls_data')
def format_user_input_controls_data(component):
	if 'viper.user_input' != component['type']:
		return ''

	data = []
	for control in component['components']:
		model = control['model']
		data.append({
			"type": model['type'],
			"title": model['text'],
			"is_mandatory": (model['is_mandatory'] == 'yes')
		})

	return json.dumps(data)

@register.filter(name='str_split')
def str_split(str, arg='|'):
	if str:
		return str.split(arg)
	return []