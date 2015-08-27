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


class PageStore(object):
	def __init__(self):
		self.connection = None
		self.db = None
		self.connect()

	def connect(self):
		self.connection = Connection(settings.PAGE_STORE_SERVER_HOST, settings.PAGE_STORE_SERVER_PORT)
		self.db = self.connection[settings.PAGE_STORE_DB]

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
	# save_page: 保存page
	#######################################################################
	def save_page(self, project_id, page_id, page_component):
		now = self.get_now()
		is_new_created_page = page_component.get('is_new_created', False)
		if not is_new_created_page:
			pp_id = '%s_%s' % (project_id, page_id)
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
			self.db.page.insert(page, safe=True)

		return now


	#######################################################################
	# remove_page: 删除page
	#######################################################################
	def remove_page(self, project_id, page_id):
		pp_id = '%s_%s' % (project_id, page_id)
		self.db.page.remove({'pp_id': pp_id}, safe=True)


	#######################################################################
	# update_page_display_index: 改变page的display index
	#######################################################################
	def update_page_display_index(self, project_id, page_id, index):
		pp_id = '%s_%s' % (project_id, page_id)
		self.db.page.update({'pp_id': pp_id}, {'$set':{'display_index':index}})


	#######################################################################
	# get_page_components: 获得project_id对应的所有page集合
	#######################################################################
	def get_page_components(self, project_id):
		pages = list(self.db.page.find({'project_id': project_id}))
		pages.sort(lambda x,y: cmp(x['display_index'], y['display_index']))
		page_components = []
		for page in pages:
			page_components.append(page['component'])
		return page_components


	#######################################################################
	# get_pages: 获得project_id对应的所有page集合
	#######################################################################
	def get_pages(self, project_id):
		return self.db.page.find({'project_id': project_id}, sort=[('display_index', pymongo.ASCENDING)])


	#######################################################################
	# get_page: 获得(project_id, page_id)指定的page
	#######################################################################
	def get_page(self, project_id, page_id=None):
		if not page_id:
			return self.get_first_page(project_id)
		else:
			pp_id = '%s_%s' % (project_id, page_id)
			return self.db.page.find_one({'pp_id': pp_id})


	#######################################################################
	# get_first_page: 获得project_id项目中的第一个page
	#######################################################################
	def get_first_page(self, project_id):
		return self.db.page.find_one({'project_id': project_id}, sort=[('display_index', pymongo.ASCENDING)], limit=1)


	#######################################################################
	# save_record: 保存record
	#######################################################################
	def save_record(self, project_id, page_id, content, order_by_asc):
		now = self.get_now()

		index = self.db.record.find({'page_id':page_id}).count() + 1
		if not order_by_asc:
			index = 0 - index

		#创建page
		pp_id = '%s_%s' % (project_id, page_id)
		record = {
			'project_id': project_id,
			'page_id': page_id,
			'pp_id': pp_id,
			'display_index': index,
			'created_at': now,
			'updated_at': now,
			'model': content
		}
		self.db.record.insert(record, safe=True)


	#######################################################################
	# update_record: 更新record_id指定的record
	#######################################################################
	def update_record(self, record_id, content):
		now = self.get_now()
		_id = ObjectId(record_id)
		self.db.record.update({'_id': _id}, {'$set': {'model': content, 'updated_at': now}}, safe=True)


	#######################################################################
	# update_record_display_index: 更新record_id指定的record的display index
	#######################################################################
	def update_record_display_index(self, record_id, index):
		_id = ObjectId(record_id)
		self.db.record.update({'_id': _id}, {'$set': {'display_index': index}}, safe=True)


	#######################################################################
	# remove_record: 删除record_id指定的record
	#######################################################################
	def remove_record(self, record_id):
		_id = ObjectId(record_id)
		self.db.record.remove({'_id': _id}, safe=True)


	#######################################################################
	# get_records: 获得page_id对应的record集合
	#######################################################################
	def get_records(self, project_id, page_id):
		pp_id = '%s_%s' % (project_id, page_id)
		records = []
		for record in self.db.record.find({'pp_id': pp_id}, sort=[('display_index', pymongo.ASCENDING)]):
			record['id'] = str(record['_id'])
			records.append(record)

		return records


	#######################################################################
	# get_record: 获得record_id指定的record
	#######################################################################
	def get_record(self, record_id):
		_id = ObjectId(record_id)
		record = self.db.record.find_one({'_id':_id})
		record['id'] = str(record['_id'])
		return record


pagestore = PageStore()