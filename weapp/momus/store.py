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

MOMUS_MONGO = {
    "HOST": 'mongo.weapp.com',
    "PORT": 27017,
    "DB": 'momus'
}


class Store(object):
	def __init__(self):
		self.connection = None
		self.db = None
		self.connect()

	def connect(self):
		self.connection = Connection(MOMUS_MONGO["HOST"], MOMUS_MONGO["PORT"])
		self.db = self.connection[MOMUS_MONGO["DB"]]

	def get_now(self):
		return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

	#######################################################################
	# save_record: 保存record
	#######################################################################
	def save_record(self, collection, owner_id, content, order_by_asc=None):
		#创建page
		now = self.get_now()
		record = {
			'created_at': now,
			'updated_at': now,
			'owner_id': owner_id,
			'data': content
		}

		#存储
		self.db[collection].insert(record, safe=True)


	#######################################################################
	# update_record: 更新record_id指定的record
	#######################################################################
	def update_record(self, collection, record_id, content):
		now = self.get_now()
		_id = ObjectId(record_id)

		self.db[collection].update({'_id': _id}, {'$set': {'data': content, 'updated_at': now}}, safe=True)


	#######################################################################
	# remove_record: 删除record_id指定的record
	#######################################################################
	def remove_record(self, collection, record_id):
		_id = ObjectId(record_id)
		self.db[collection].remove({'_id': _id}, safe=True)


	#######################################################################
	# get_records: 获得page_id对应的record集合
	#######################################################################
	def get_records(self, collection, owner_id, options={}):
		query = {'owner_id': owner_id}
		if 'filter' in options:
			for key, value in options['filter'].items():
				if key == '_id':
					try:
						value = ObjectId(options['filter'][key])
					except:
						try:
							if int(options['filter'][key]):
								#如果是int，则是default中指定的id
								return 0, []
						except:
							raise
					options['filter'][key] = value
			query.update(options['filter'])
		if 'search' in options:
			query.update(options['search'])

		if 'sort' in options:
			sort_option = options['sort']
		else:
			sort_option = [('_id', pymongo.ASCENDING)]

		if 'pagination' in options:
			raise RuntimeError('can not reach here')
			'''
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
			'''
		else:
			print 'query: ', query
			datas = list(self.db[collection].find(query, sort=sort_option))
			total_count = len(datas)
		
		records = []
		for record in datas:
			record["data"]['id'] = str(record['_id'])
			records.append(record["data"])

		return total_count, records


	#######################################################################
	# get_record: 获得record_id指定的record
	#######################################################################
	def get_record(self, record_id):
		_id = ObjectId(record_id)
		record = self.db[collection].find_one({'_id':_id})
		record['id'] = str(record['_id'])
		return record


store = Store()