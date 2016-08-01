# -*- coding: utf-8 -*-
import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import subprocess
import shutil

from django.conf import settings

from pymongo import Connection
import pymongo
from bson.objectid import ObjectId
from mall.models import ProductCategory


class PageStore(object):
	def __init__(self):
		self.connection = None
		self.db = None
		self.connect()

	def connect(self):
		self.connection = Connection(settings.PAGE_STORE_SERVER_HOST, settings.PAGE_STORE_SERVER_PORT)
		self.db = self.connection[settings.PAGE_STORE_DB]

	#######################################################################
	# check_whether_query_from_app: 解析page_id内容，检查查询是否从app发起
	#######################################################################
	def check_whether_query_from_app(self, page_id):
		if not page_id:
			info = {
				"mongo_collection": self.db.record
			}
			return False, info

		if page_id.startswith('apps:'):
			_, app_name, page_module, page_name = page_id.split(':')
			collection_name = '{}:{}'.format(app_name, page_name)
			#mongo_collection = self.connection[app_name][page_name]
			mongo_collection = self.connection['app_data'][collection_name]
			info = {
				"app_name": app_name,
				"page_module": page_module,
				"page_name": page_name,
				"mongo_collection": mongo_collection
			}

			return True, info
		else:
			info = {
				"mongo_collection": self.db.record
			}
			return False, info

	def get_now(self):
		return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

	#######################################################################
	# copy_project_pages: 将src_project的所有page拷贝到dst_project中
	#######################################################################
	def copy_project_pages(self, src_project_id, dst_project_id):
		for page in self.get_pages(src_project_id):
			project_id = dst_project_id
			page_id = page['page_id']
			page_component = page['component']
			page_component['is_new_created'] = True
			self.save_page(project_id, page_id, page_component)


	#######################################################################
	# save_preview_page: 保存page
	#######################################################################
	def save_preview_page(self, project_id, page_id, page_component):
		now = self.get_now()
		page = self.db.preview_page.find_one({'project_id':project_id, 'page_id':page_id}, limit=1)
		if page:
			pp_id = '%s_%s' % (project_id, page_id)
			self.db.preview_page.update({'pp_id': pp_id}, {'$set': {'component': page_component}})
		else:
			#创建page
			page = {
				'project_id': project_id,
				'page_id': page_id,
				'display_index': page_id,
				'pp_id': '%s_%s' % (project_id, page_id),
				'created_at': now,
				'updated_at': now,
				'component': page_component
			}
			self.db.preview_page.insert(page, safe=True)

		return now

	#######################################################################
	# save_page: 保存page
	#######################################################################
	def save_page(self, project_id, page_id, page_component):
		if page_id == "preview":
			return self.save_preview_page(project_id, page_id, page_component)

		now = self.get_now()
		pp_id = '%s_%s' % (project_id, page_id)
		page = self.db.page.find_one({'pp_id':pp_id}, limit=1)
		is_new_created_page = page_component.get('is_new_created', False)
		#if not is_new_created_page:
		if page or (not is_new_created_page):
			pp_id = '%s_%s' % (project_id, page_id)
			# print '-$-'*20
			# print 'update page'
			# print pp_id
			# print json.dumps(page_component)
			self.db.page.update({'pp_id': pp_id}, {'$set': {'component': page_component}})
		else:
			#创建page
			page = {
				'project_id': project_id,
				'page_id': page_id,
				'display_index': page_id,
				'pp_id': '%s_%s' % (project_id, page_id),
				'created_at': now,
				'updated_at': now,
				'component': page_component
			}
			# print '-$-'*20
			# print 'create page'
			# print json.dumps(page_component)
			self.db.page.insert(page, safe=True)

		return now


	#######################################################################
	# remove_page: 删除page
	#######################################################################
	def remove_page(self, project_id, page_id):
		pp_id = '%s_%s' % (project_id, page_id)
		self.db.page.remove({'pp_id': pp_id}, safe=True)


	#######################################################################
	# remove_project_pages: 删除project的所有page
	#######################################################################
	def remove_project_pages(self, project_id):
		self.db.page.remove({'project_id': project_id}, safe=True)

	#######################################################################
	# remove_all: 删除全部page
	#######################################################################
	def remove_all(self):
		self.db.page.remove()


	#######################################################################
	# update_page_display_index: 改变page的display index
	#######################################################################
	def update_page_display_index(self, project_id, page_id, index):
		pp_id = '%s_%s' % (project_id, page_id)
		self.db.page.update({'pp_id': pp_id}, {'$set':{'display_index':index}})


	#######################################################################
	# update_page_project_id: 鏀瑰彉page鐨刾roject id
	#######################################################################
	def update_page_project_id(self, project_id, page_id, new_project_id):
		pp_id = '%s_%s' % (project_id, page_id)
		new_pp_id = '%s_%s' % (new_project_id, page_id)
		self.db.page.update({'pp_id': pp_id}, {'$set':{'project_id':new_project_id, 'pp_id':new_pp_id}})


	#######################################################################
	# get_page_components: 获得project_id对应的所有page集合
	#######################################################################
	def get_page_components(self, project_id):
		pages = list(self.db.page.find({'project_id': project_id}))
		pages.sort(lambda x,y: cmp(x['display_index'], y['display_index']))
		page_components = []
		for page in pages:
			page_components.append(page['component'])

		page_components = self.__filter_replace(page_components)
		return page_components


	#######################################################################
	# get_pages: 获得project_id对应的所有page集合
	#######################################################################
	def get_pages(self, project_id):
		return list(self.db.page.find({'project_id': project_id}, sort=[('display_index', pymongo.ASCENDING)]))


	#######################################################################
	# get_page: 获得(project_id, page_id)指定的page
	#######################################################################
	def get_page(self, project_id, page_id=None):
		if not page_id:
			return self.get_first_page(project_id)
		else:
			pp_id = '%s_%s' % (project_id, page_id)
			if page_id == 'preview':
				result = self.db.preview_page.find_one({'pp_id': pp_id})
			else:
				result = self.db.page.find_one({'pp_id': pp_id})
			return result


	#######################################################################
	# get_first_page: 获得project_id项目中的第一个page
	#######################################################################
	def get_first_page(self, project_id):
		return self.db.page.find_one({'project_id': project_id}, sort=[('display_index', pymongo.ASCENDING)], limit=1)


	#######################################################################
	# find_page_by_datasource_page_id: 根据datasource page id寻找page
	#######################################################################
	def find_page_by_datasource_page_id(self, project_id, datasource_page_id):
		for page in self.get_pages(project_id):
			if page['component']['model']['datasource_page_id'] == datasource_page_id:
				return page


	#######################################################################
	# save_record: 保存record
	#######################################################################
	def save_record(self, owner_id, project_id, page_id, content, order_by_asc=None):
		#确定请求是否来自app
		is_query_from_app, app_info = self.check_whether_query_from_app(page_id)
		if is_query_from_app:
			page_id = app_info['page_name']
			project_id = app_info['app_name']
			connector = '-'
		else:
			connector = '_'

		#TODO: 另存一张表，维护某个collection的record总数，提升性能
		index = app_info['mongo_collection'].find({'page_id':page_id}).count() + 1

		#创建page
		now = self.get_now()
		pp_id = '%s%s%s%s%s' % (project_id, connector, page_id, connector, owner_id)
		record = {
			'project_id': project_id,
			'page_id': page_id,
			'pp_id': pp_id,
			'display_index': index,
			'created_at': now,
			'updated_at': now,
			'model': content
		}

		#存储
		app_info['mongo_collection'].insert(record, safe=True)


	#######################################################################
	# update_record: 更新record_id指定的record
	#######################################################################
	def update_record(self, record_id, content, page_id=None):
		now = self.get_now()
		_id = ObjectId(record_id)

		#确定请求是否来自app
		is_query_from_app, app_info = self.check_whether_query_from_app(page_id)
		app_info['mongo_collection'].update({'_id': _id}, {'$set': {'model': content, 'updated_at': now}}, safe=True)


	#######################################################################
	# update_record_display_index: 更新record_id指定的record的display index
	#######################################################################
	def update_record_display_index(self, record_id, index, page_id=None):
		_id = ObjectId(record_id)
		is_query_from_app, app_info = self.check_whether_query_from_app(page_id)
		app_info['mongo_collection'].update({'_id': _id}, {'$set': {'display_index': index}}, safe=True)


	#######################################################################
	# set_record_to_top: 将record置顶
	#######################################################################
	def set_record_to_top(self, record_id, order, page_id=None):
		_id = ObjectId(record_id)
		is_query_from_app, app_info = self.check_whether_query_from_app(page_id)
		collection = app_info['mongo_collection']
		records = list(collection.find(sort=[('display_index', pymongo.ASCENDING if order == 'asc' else pymongo.DESCENDING)]).limit(2))
		if len(records) < 2:
			#do nothing
			return

		first_index = records[0]['display_index']
		second_index = records[1]['display_index']
		if first_index < second_index:
			#顺序排列
			new_index = first_index - 1
		else:
			#倒序排列
			new_index = first_index + 1
		collection.update({'_id': _id}, {'$set': {'display_index': new_index}}, safe=True)


	#######################################################################
	# remove_record: 删除record_id指定的record
	#######################################################################
	def remove_record(self, record_id, page_id=None):
		_id = ObjectId(record_id)
		is_query_from_app, app_info = self.check_whether_query_from_app(page_id)
		app_info['mongo_collection'].remove({'_id': _id}, safe=True)


	#######################################################################
	# get_records: 获得page_id对应的record集合
	#######################################################################
	def get_records(self, owner_id, project_id, page_id, options={}):
		#确定请求是否来自app
		is_query_from_app, app_info = self.check_whether_query_from_app(page_id)
		if is_query_from_app:
			page_id = app_info['page_name']
			project_id = app_info['app_name']
			connector = '-'
		else:
			connector = '_'

		pp_id = '%s%s%s%s%s' % (project_id, connector, page_id, connector, owner_id)
		query = {'pp_id': pp_id}
		if 'filter' in options:
			query.update(options['filter'])
		if 'search' in options:
			query.update(options['search'])

		if 'sort' in options:
			sort_option = options['sort']
		else:
			sort_option = [('display_index', pymongo.ASCENDING)]

		if 'pagination' in options:
			pagination = options['pagination']
			skip_count = pagination['cur_page']*pagination['count_per_page']
			fetch_count = pagination['count_per_page']
			datas = list(app_info['mongo_collection'].find(query, sort=sort_option).skip(skip_count).limit(fetch_count))
			if len(datas) == 0:
				if 'search' in options:
					#没有搜索结果，转化为部分匹配
					old_search = options['search'].items()[0]
					options['search'] = {old_search[0]: {'$regex': old_search[1]}}
					query.update(options['search'])
					datas = list(app_info['mongo_collection'].find(query, sort=sort_option).skip(skip_count).limit(fetch_count))
			total_count = app_info['mongo_collection'].find(query).count()
		else:
			datas = list(app_info['mongo_collection'].find(query, sort=sort_option))
			if len(datas) == 0:
				if 'search' in options:
					#没有搜索结果，转化为部分匹配
					old_search = options['search'].items()[0]
					options['search'] = {old_search[0]: {'$regex': old_search[1]}}
					query.update(options['search'])
					datas = list(app_info['mongo_collection'].find(query, sort=sort_option))
			total_count = len(datas)

		records = []
		for record in datas:
			record['id'] = str(record['_id'])
			record['model']['created_at'] = record['created_at']
			records.append(record)

		return total_count, records


	#######################################################################
	# get_record: 获得record_id指定的record
	#######################################################################
	def get_record(self, record_id, page_id=None):
		#确定请求是否来自app
		is_query_from_app, app_info = self.check_whether_query_from_app(page_id)
		_id = ObjectId(record_id)
		record = app_info['mongo_collection'].find_one({'_id':_id})
		record['id'] = str(record['_id'])
		return record


	#######################################################################
	# __filter_replace: 过滤替换component
	#######################################################################
	def __filter_replace(self, pages):
		for i in range(0, len(pages)):
			delete_ids = []
			components = pages[i]["components"]
			for j in range(0, len(components)):
				component = components[j]
				if component["type"] == 'wepage.item_list':
					component = self.__update_category(component)
					if component:
						pages[i]["components"][j] = self.__update_category(component)
					else:
						# 组件中删除该分组信息，但保留控件 by liupeiyu
						pages[i]["components"][j]["model"]["category"] = ""
						# delete_ids.append(j)
				elif component["type"] == 'appkit.item_list':
					component = self.__update_category(component)
					if component:
						pages[i]["components"][j] = self.__update_category(component)
					else:
						# 组件中删除该分组信息，但保留控件 by liupeiyu
						pages[i]["components"][j]["model"]["category"] = ""
						# delete_ids.append(j)

			for id in delete_ids:
				del pages[i]["components"][id]

		return pages


	#######################################################################
	# __update_category: 更新分组信息
	#######################################################################
	def __update_category(self, component):
		category = component["model"].get("category")
		if category:
			category = json.loads(category)
			if len(category) > 0:
				cateoryId = category[0]["id"]
				categories = ProductCategory.objects.filter(id=cateoryId)
				if categories.count() == 0:
					component = None
				else:
					category[0]["title"] = categories[0].name
					component["model"]["category"] = json.dumps(category)

		return component

pagestore = PageStore()